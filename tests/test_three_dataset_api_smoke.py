import json
import argparse
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MYAGENT_ROOT = Path(r"D:\AAAcode\code-code\agent+\myAgent-main")
sys.path.insert(0, str(PROJECT_ROOT / "code"))

from agents import ReactAgent  # noqa: E402
from tqa import main  # noqa: E402
from utils import table2df  # noqa: E402


class FinishBackend:
    def __init__(self, answer):
        self.answer = answer
        self.calls = []

    def generate(self, prompt, model_name, count=1):
        self.calls.append((prompt, model_name, count))
        output = f"Thought 1: answer found in table\nAction 1: Finish[{self.answer}]"
        return [output] * count


def first_record(file_name):
    path = MYAGENT_ROOT / "datasets_ready" / file_name
    with path.open(encoding="utf-8") as handle:
        return json.loads(next(handle))


class ThreeDatasetAPISmokeTests(unittest.TestCase):
    def test_mact_main_reads_and_runs_each_prepared_dataset(self):
        cases = (
            ("wtq", "wtq_unseen_sample5.jsonl"),
            ("scitab", "tabfact_test_sample5.jsonl"),
            ("crt", "crt_sample5.jsonl"),
        )
        for task, file_name in cases:
            with self.subTest(task=task):
                backend = FinishBackend("smoke-answer")
                runtime = {
                    "api_backend": backend,
                    "model": None,
                    "tokenizer": None,
                    "codeagent_endpoint": None,
                }
                args = argparse.Namespace(
                    dataset_path=str(MYAGENT_ROOT / "datasets_ready" / file_name),
                    table_dir="",
                    task=task,
                    max_step=2,
                    max_actual_step=2,
                    plan_model_name="deepseek-v4-flash",
                    code_model_name="deepseek-v4-flash",
                    as_reward="consistency",
                    plan_sample=1,
                    code_sample=1,
                    use_pre_answer=False,
                    answer_aggregate=1.0,
                    direct_reasoning=False,
                    long_table_op="ignore",
                    debugging=True,
                    code_as_observation=False,
                    without_tool=True,
                )
                with patch("tqa.build_runtime", return_value=runtime):
                    main(args)

                self.assertEqual(len(backend.calls), 1)

    def test_real_prepared_records_complete_the_mact_react_loop(self):
        cases = (
            ("wtq", "wtq_unseen_sample5.jsonl"),
            ("scitab", "tabfact_test_sample5.jsonl"),
            ("crt", "crt_sample5.jsonl"),
        )
        for task, file_name in cases:
            with self.subTest(task=task):
                row = first_record(file_name)
                gold = row.get("answer", "smoke-answer")
                if isinstance(gold, list):
                    gold = gold[0] if gold else "smoke-answer"
                backend = FinishBackend(str(gold))
                agent = ReactAgent(
                    question=row.get("question") or row.get("statement", ""),
                    table=row["table_text"],
                    table_df=table2df(row["table_text"]),
                    df_path=None,
                    context=row.get("text", ""),
                    key=row.get("answer", ""),
                    plan_model_name="deepseek-v4-flash",
                    code_model_name="deepseek-v4-flash",
                    model=None,
                    tokenizer=None,
                    max_steps=2,
                    max_actual_steps=2,
                    task=task,
                    plan_sample=1,
                    code_sample=1,
                    as_reward="consistency",
                    use_pre_answer=False,
                    without_tool=True,
                    api_backend=backend,
                )

                agent.run()

                self.assertTrue(agent.is_finished())
                self.assertFalse(agent.is_halted())
                self.assertTrue(str(agent.answer).strip())
                self.assertEqual(backend.calls[0][1], "deepseek-v4-flash")


if __name__ == "__main__":
    unittest.main()
