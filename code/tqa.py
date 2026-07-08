""" 与 MACT（NAACL 2025）相关的工具类与函数。

版权 (c) 2025 Robert Bosch GmbH

本程序是自由软件：你可以按照自由软件基金会发布的 GNU Affero 通用公共许可证第 3 版或（你可以选择的）更高版本的条款重新发布和/或修改。

本程序的发布目的是希望它有用，但不提供任何保证；甚至不包含适销性或特定用途适用性的默示保证。详情参见 GNU Affero 通用公共许可证。

你应该已经收到一份 GNU Affero 通用公共许可证副本；如果没有，请访问 <https://www.gnu.org/licenses/>。
"""


import traceback
import json
import argparse
import os
import time

from agents import ReactAgent
from model_backends import (
    add_model_backend_args,
    build_api_backend,
    resolve_model_provider,
)
from utils import summarize_react_trial, table2df
from utils import get_databench_table


def write_to_file(path, agent, idx, new_table_dataset, given_plan):
    # 输入：path(str)输出文件路径；agent(ReactAgent 实例)代理对象；idx(int)样本索引；new_table_dataset(list)数据集；given_plan(Optional[str])预设计划
    # 输出：ReactAgent，包含运行后的预测与中间状态
    # 作用：运行代理获取回答日志，将结果与轨迹追加写入指定文件。
    api_backend = getattr(agent, "api_backend", None)
    api_metrics_before = api_backend.snapshot() if api_backend is not None else None
    with open(path, "a", encoding="utf-8") as f:
        # 执行agent的run方法
        sample_started_at = time.perf_counter()
        agent.run(given_plan)
        elapsed_seconds_total = time.perf_counter() - sample_started_at
        pred_answer = agent.answer
        item = new_table_dataset[idx]
        item["pred_answer"] = pred_answer
        item["history"] = agent.scratchpad
        item["pred_answer_all"] = agent.pre_ans_all
        item["elapsed_seconds_total"] = elapsed_seconds_total
        if api_backend is not None:
            api_metrics_after = api_backend.snapshot()
            item["api_metrics"] = {
                key: api_metrics_after.get(key, 0) - api_metrics_before.get(key, 0)
                for key in api_metrics_after
            }
        # item["code_log"] = agent.generated_code
        # item["plan_log"] = agent.generated_plan
        f.write(json.dumps(item, ensure_ascii=False)+"\n")
    return agent

# ===================================================


def load_codellama_template(endpoint2):
    # 输入：endpoint2(RuntimeEndpoint) 代码代理的端点
    # 输出：无
    # 作用：注册并应用 CodeLlama 的聊天模板到运行时端点。
    from sglang.lang.chat_template import (
        ChatTemplate,
        get_chat_template,
        register_chat_template,
    )

    codellama_template = ChatTemplate(
        name="codellama",
        default_system_prompt=(
            "You are an intelligent programming assistant."
        ),
        role_prefix_and_suffix={
            "system": ("### System Promopt\n", "\n"),
            "user": ("### User Message\n", "\n"),
            "assistant": ("### Assistant", ""),
        }
    )
    register_chat_template(codellama_template)
    endpoint2.chat_template = get_chat_template("codellama")


def build_runtime(args, openai_client_factory=None):
    provider = resolve_model_provider(args)
    if provider in {"deepseek", "openai_compatible", "azure"}:
        if args.as_reward in {"logp", "combined"}:
            raise ValueError(
                f"as_reward={args.as_reward!r} requires a local model backend."
            )
        return {
            "api_backend": build_api_backend(
                args,
                openai_client_factory=openai_client_factory,
            ),
            "model": None,
            "tokenizer": None,
            "codeagent_endpoint": None,
        }

    if not args.model_path:
        raise RuntimeError("--model_path is required when --model_provider=local.")

    from transformers import AutoTokenizer
    from vllm import LLM

    tokenizer = AutoTokenizer.from_pretrained(args.model_path)
    model = LLM(model=args.model_path)
    codeagent_endpoint = None
    if args.code_model_name != args.plan_model_name:
        import sglang as sgl

        codeagent_endpoint = sgl.RuntimeEndpoint(
            f"http://localhost:{args.code_endpoint}"
        )
        if "codellama" in args.code_model_name.lower():
            load_codellama_template(codeagent_endpoint)
    return {
        "api_backend": None,
        "model": model,
        "tokenizer": tokenizer,
        "codeagent_endpoint": codeagent_endpoint,
    }


def main(args):
    # 输入：args(argparse.Namespace) 命令行参数集合
    # 输出：无
    # 作用：根据参数加载模型与数据集，构建代理执行任务，并记录输出结果。
    runtime = build_runtime(args)
    model = runtime["model"]
    tokenizer = runtime["tokenizer"]
    codeagent_endpoint = runtime["codeagent_endpoint"]
    api_backend = runtime["api_backend"]

    with open(args.dataset_path, "r", encoding="utf-8") as f:
        table_dataset = [json.loads(line) for line in f]

    trial = 0
    agent_cls = ReactAgent
    agents = [agent_cls(question=row["question"] if "question" in list(row.keys()) else row["statement"],
              table=get_databench_table(args.table_dir, row["dataset"])[
        0] if args.task == "databench" else row["table_text"],
        table_df=table2df(get_databench_table(args.table_dir, row["dataset"])[
            1]) if args.task == "databench" else table2df(row["table_text"]),
        df_path=get_databench_table(args.table_dir, row["dataset"])[
        2] if args.task == "databench" else None,
        context=row["text"] if "text" in list(row.keys()) else "",
        key=row["answer"] if "answer" in list(row.keys()) else "none",
        answer="",
        max_steps=args.max_step,
        max_actual_steps=args.max_actual_step,
        plan_model_name=args.plan_model_name,
        code_model_name=args.code_model_name,
        model=model,
        tokenizer=tokenizer,
        task=args.task,
        codeagent_endpoint=codeagent_endpoint,
        as_reward=args.as_reward,
        plan_sample=args.plan_sample,
        code_sample=args.code_sample,
        use_pre_answer=args.use_pre_answer,
        answer_aggrement=args.answer_aggregate,
        direct_reasoning=args.direct_reasoning,
        long_table_op=args.long_table_op,
        debugging=args.debugging,
        code_as_observation=args.code_as_observation,
        without_tool=args.without_tool,
        api_backend=api_backend) for _, row in enumerate(table_dataset)]
    if args.debugging:
        agents = agents[0:1]
        for idx, agent in enumerate([a for a in agents]):
            print(idx)
            print(agent.question)
            print(agent.table_string)
            agent.run()
            print(f'Answer: {agent.key}, Pred: {agent.answer}')
            print(agent.scratchpad)
            trial += 1
            correct, incorrect, halted = summarize_react_trial(agents)
            print(f'Finished Trial {trial}, Correct: {len(correct)}, \
                    Incorrect: {len(incorrect)}, Halted: {len(halted)}')
    else:
        finished_agents = []
        plan_model_name = args.plan_model_name.split("/")[-1].strip()
        code_model_name = args.code_model_name.split("/")[-1].strip()
        output_path = args.output_path or (
            f"{args.task}_{plan_model_name}_{code_model_name}_{args.as_reward}_"
            f"{args.plan_sample}_{args.code_sample}_direct_"
            f"{args.direct_reasoning}_{args.answer_aggregate}.jsonl"
        )
        if not args.append_output and os.path.exists(output_path):
            os.remove(output_path)
        for idx, agent in enumerate([a for a in agents]):
            try:
                finished_agent = write_to_file(
                    output_path, agent, idx, table_dataset, given_plan=None)
                finished_agents.append(finished_agent)
                trial += 1
                correct, incorrect, halted = summarize_react_trial(
                    finished_agents)
                print(
                    f'Finished Trial {trial}, Correct: {len(correct)}, Incorrect: {len(incorrect)}, Halted: {len(halted)}')
            except Exception as e:
                print(traceback.format_exc())
                break


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--plan_model_name',
                        default="", help="name of the planning model.")
    parser.add_argument('--code_model_name',
                        default="", help="name of the coding model.")
    parser.add_argument('--cache_dir', default="",
                        help="cache dir to load a model from.")
    parser.add_argument('--model_path', type=str,
                        default="", help="model path to the planning model.")
    parser.add_argument('--dataset_path', type=str,
                        default="../datasets/wtq.jsonl", help="dataset path.")
    parser.add_argument('--output_path', type=str, default="",
                        help="output JSONL path; defaults to a parameter-derived file name.")
    parser.add_argument('--append_output', action='store_true',
                        help="append to output_path instead of replacing it.")
    parser.add_argument('--table_dir', type=str,
                        default="../datasets/databench/data", help="databench table directory")
    parser.add_argument('--max_step', type=int, default=6,
                        help="maximum number for valid iterations.")
    parser.add_argument('--max_actual_step', type=int, default=6,
                        help="maximum number for all iterations.")
    parser.add_argument('--task', type=str, default="wtq",
                        choices=["wtq", "crt", "tat", "scitab", "databench"])
    parser.add_argument('--as_reward', type=str, default="consistency",
                        choices=["consistency", "llm", "logp", "rollout", "combined"])
    parser.add_argument('--long_table_op', type=str, default="ignore",
                        choices=["code-agent", "ignore", "short-table"],
                        help="methods to shorten long table. default passing the whole table.")
    parser.add_argument('--plan_sample', type=int, default=5,
                        help="number of actions sampled from a planning model.")
    parser.add_argument('--code_sample', type=int, default=5,
                        help="numbers of trails for generating codes to address an action.")
    parser.add_argument('--use_pre_answer', type=bool, default=True,
                        help="whether use answers from the first iteration as final answers.")
    parser.add_argument('--answer_aggregate', type=float, default=1.,
                        help="agreement threshold for answer selection of use_pre_answer.")
    parser.add_argument('--direct_reasoning', action='store_true',
                        help="whether to use cot and symbolic reasoning directly or not.")
    parser.add_argument('--without_tool', action='store_true')
    parser.add_argument('--code_endpoint', default="11039",
                        help="coding agent port.")
    parser.add_argument('--debugging', action='store_true')
    parser.add_argument('--code_as_observation', action='store_true',
                        help="only use code as the final observations or not.")
    add_model_backend_args(parser)
    return parser


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    main(args)
