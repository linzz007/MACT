import argparse
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "code"))

from tqa import build_runtime, create_parser, write_to_file  # noqa: E402


class RecordingClientFactory:
    def __init__(self):
        self.calls = []
        self.client = SimpleNamespace(
            chat=SimpleNamespace(completions=SimpleNamespace(create=lambda **_kwargs: None))
        )

    def __call__(self, **kwargs):
        self.calls.append(kwargs)
        return self.client


def make_args(**overrides):
    values = {
        "model_provider": "deepseek",
        "plan_model_name": "deepseek-v4-flash",
        "code_model_name": "deepseek-v4-flash",
        "model_path": "",
        "code_endpoint": "11039",
        "as_reward": "consistency",
        "api_base": "https://api.deepseek.com",
        "api_key_env": "DEEPSEEK_API_KEY",
        "thinking": "disabled",
        "temperature": 0.0,
        "max_tokens": 2048,
        "api_timeout": 120.0,
    }
    values.update(overrides)
    return argparse.Namespace(**values)


class TQAAPIEntryTests(unittest.TestCase):
    def test_output_records_per_sample_api_usage_delta(self):
        class CountingBackend:
            def __init__(self):
                self.metrics = {
                    "request_count": 4,
                    "prompt_tokens": 40,
                    "completion_tokens": 8,
                }

            def snapshot(self):
                return dict(self.metrics)

        class FakeAgent:
            def __init__(self):
                self.api_backend = CountingBackend()
                self.answer = ""
                self.scratchpad = ""
                self.pre_ans_all = []

            def run(self, _given_plan):
                self.answer = "42"
                self.scratchpad = "trace"
                self.api_backend.metrics["request_count"] += 2
                self.api_backend.metrics["prompt_tokens"] += 30
                self.api_backend.metrics["completion_tokens"] += 6

        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "result.jsonl"
            write_to_file(
                output_path,
                FakeAgent(),
                0,
                [{"question": "q", "answer": "42"}],
                given_plan=None,
            )
            record = json.loads(output_path.read_text(encoding="utf-8"))

        self.assertEqual(
            record["api_metrics"],
            {"request_count": 2, "prompt_tokens": 30, "completion_tokens": 6},
        )
        self.assertIn("elapsed_seconds_total", record)
        self.assertGreaterEqual(record["elapsed_seconds_total"], 0.0)

    def test_help_starts_without_local_inference_dependencies(self):
        result = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "code" / "tqa.py"), "--help"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            timeout=30,
            check=False,
        )
        stdout = result.stdout.decode("ascii", errors="ignore")
        stderr = result.stderr.decode("ascii", errors="ignore")
        self.assertEqual(result.returncode, 0, msg=stderr)
        for flag in ("--model_provider", "--api_base", "--api_key_env", "--thinking"):
            self.assertIn(flag, stdout)

    def test_build_runtime_constructs_api_backend_without_local_models(self):
        factory = RecordingClientFactory()
        with patch.dict(os.environ, {"DEEPSEEK_API_KEY": "test-key"}, clear=False):
            runtime = build_runtime(make_args(), openai_client_factory=factory)

        self.assertIsNotNone(runtime["api_backend"])
        self.assertIsNone(runtime["model"])
        self.assertIsNone(runtime["tokenizer"])
        self.assertIsNone(runtime["codeagent_endpoint"])
        self.assertEqual(factory.calls[0]["base_url"], "https://api.deepseek.com")

    def test_api_runtime_rejects_local_logprob_reward_modes(self):
        for reward_mode in ("logp", "combined"):
            with self.subTest(reward_mode=reward_mode):
                with self.assertRaisesRegex(ValueError, "local model"):
                    build_runtime(make_args(as_reward=reward_mode))

    def test_parser_preserves_mact_flags_and_adds_backend_flags(self):
        args = create_parser().parse_args(
            [
                "--model_provider",
                "deepseek",
                "--plan_model_name",
                "deepseek-v4-flash",
                "--code_model_name",
                "deepseek-v4-flash",
            ]
        )
        self.assertEqual(args.model_provider, "deepseek")
        self.assertEqual(args.plan_sample, 5)
        self.assertEqual(args.code_sample, 5)
        self.assertEqual(args.output_path, "")
        self.assertFalse(args.append_output)


if __name__ == "__main__":
    unittest.main()
