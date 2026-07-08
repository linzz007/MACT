import io
import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "code"))

from agents import ReactAgent, _console_safe_text  # noqa: E402
from utils import table2df  # noqa: E402


TABLE = [["Year", "Value"], ["2023", "41"], ["2024", "42"]]


class ScriptedBackend:
    def __init__(self, responder=None):
        self.calls = []
        self.responder = responder or (lambda prompt, model_name, index: "Answer: 42")

    def generate(self, prompt, model_name, count=1):
        self.calls.append(
            {"prompt": prompt, "model_name": model_name, "count": count}
        )
        return [self.responder(prompt, model_name, index) for index in range(count)]


def make_agent(backend, **overrides):
    values = {
        "question": "What is the value in 2024?",
        "table": TABLE,
        "table_df": table2df(TABLE),
        "df_path": None,
        "context": "",
        "key": "42",
        "plan_model_name": "deepseek-v4-flash",
        "code_model_name": "deepseek-v4-flash",
        "model": None,
        "tokenizer": None,
        "max_steps": 2,
        "max_actual_steps": 2,
        "task": "wtq",
        "plan_sample": 1,
        "code_sample": 1,
        "as_reward": "consistency",
        "use_pre_answer": False,
        "without_tool": True,
        "api_backend": backend,
    }
    values.update(overrides)
    return ReactAgent(**values)


class ReactAgentAPITests(unittest.TestCase):
    def test_console_trace_is_safe_for_gbk_output(self):
        stream = io.TextIOWrapper(io.BytesIO(), encoding="gbk", errors="strict")

        stream.write(_console_safe_text("sør-trøndelag", encoding=stream.encoding))
        stream.flush()

    def test_planner_and_code_generation_use_the_injected_backend(self):
        backend = ScriptedBackend()
        agent = make_agent(
            backend,
            plan_model_name="plan-model",
            code_model_name="code-model",
            plan_sample=2,
            code_sample=3,
        )

        planner_outputs = agent.prompt_agent(mode="both")
        code_outputs = agent.prompt_agent_gpt_coder("code prompt")

        self.assertEqual(len(planner_outputs), 2)
        self.assertEqual(len(code_outputs), 3)
        self.assertEqual(backend.calls[0]["model_name"], "plan-model")
        self.assertEqual(backend.calls[0]["count"], 2)
        self.assertEqual(backend.calls[1], {"prompt": "code prompt", "model_name": "code-model", "count": 3})

    def test_quick_answer_and_global_plan_use_the_api_backend(self):
        backend = ScriptedBackend()
        agent = make_agent(backend)
        self.assertEqual(agent.get_quick_answer(), "42")

        databench_agent = make_agent(backend, task="databench")
        self.assertEqual(databench_agent.get_global_plan(), ["Answer: 42"])
        self.assertEqual(backend.calls[-1]["model_name"], "deepseek-v4-flash")
        self.assertEqual(backend.calls[-1]["count"], 1)

    def test_direct_reasoning_uses_api_for_text_and_code_models(self):
        def responder(prompt, model_name, _index):
            if model_name == "code-model":
                return "```python\nresult = '42'\n```"
            return "Answer: 42"

        backend = ScriptedBackend(responder)
        agent = make_agent(
            backend,
            direct_reasoning=True,
            plan_model_name="plan-model",
            code_model_name="code-model",
        )

        agent.step()

        self.assertTrue(agent.is_finished())
        self.assertEqual(agent.answer, "42")
        self.assertEqual([call["model_name"] for call in backend.calls], ["plan-model", "code-model"])

    def test_normal_react_run_finishes_from_api_planner_output(self):
        backend = ScriptedBackend(
            lambda _prompt, _model, _index: "Thought 1: table lookup complete\nAction 1: Finish[42]"
        )
        agent = make_agent(backend)

        agent.run()

        self.assertTrue(agent.is_finished())
        self.assertEqual(agent.answer, "42")
        self.assertEqual(backend.calls[0]["model_name"], "deepseek-v4-flash")

    def test_api_numerical_tool_executes_code_for_non_databench_tasks(self):
        backend = ScriptedBackend(
            lambda _prompt, _model, _index: "```python\nfinal_result = 42\n```"
        )
        agent = make_agent(backend)

        results = agent.numerical_tool(
            "calculate the requested value",
            agent.table_df,
            df_path=None,
        )

        self.assertEqual(results, ["42"])

    def test_multistep_react_run_calculates_then_finishes(self):
        scripted_outputs = iter(
            [
                "Thought 1: calculation required\nAction 1: Calculate[compute the 2024 value]",
                "```python\nfinal_result = 42\n```",
                "Thought 2: calculation complete\nAction 2: Finish[42]",
            ]
        )
        backend = ScriptedBackend(
            lambda _prompt, _model, _index: next(scripted_outputs)
        )
        agent = make_agent(
            backend,
            without_tool=False,
            max_steps=3,
            max_actual_steps=3,
        )

        agent.run()

        self.assertTrue(agent.is_finished())
        self.assertEqual(agent.answer, "42")
        self.assertIn("Observation 1: 42", agent.scratchpad)
        self.assertEqual(len(backend.calls), 3)


if __name__ == "__main__":
    unittest.main()
