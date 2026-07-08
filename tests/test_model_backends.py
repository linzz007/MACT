import argparse
import os
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "code"))

from model_backends import (  # noqa: E402
    DEEPSEEK_API_BASE,
    add_model_backend_args,
    build_api_backend,
    estimate_text_tokens,
    resolve_model_provider,
)


class FakeCompletions:
    def __init__(self, content_prefix="answer"):
        self.calls = []
        self.content_prefix = content_prefix

    def create(self, **kwargs):
        self.calls.append(kwargs)
        content = f"{self.content_prefix}-{len(self.calls)}"
        usage = SimpleNamespace(prompt_tokens=10, completion_tokens=2)
        message = SimpleNamespace(content=content)
        return SimpleNamespace(
            choices=[SimpleNamespace(message=message)],
            usage=usage,
        )


class RecordingClientFactory:
    def __init__(self, content_prefix="answer"):
        self.calls = []
        self.client = SimpleNamespace(
            chat=SimpleNamespace(completions=FakeCompletions(content_prefix))
        )

    def __call__(self, **kwargs):
        self.calls.append(kwargs)
        return self.client


def make_args(**overrides):
    values = {
        "model_provider": "deepseek",
        "plan_model_name": "deepseek-v4-flash",
        "code_model_name": "deepseek-v4-flash",
        "api_base": DEEPSEEK_API_BASE,
        "api_key_env": "DEEPSEEK_API_KEY",
        "thinking": "disabled",
        "temperature": 0.0,
        "max_tokens": 2048,
        "api_timeout": 120.0,
        "api_max_retries": 5,
    }
    values.update(overrides)
    return argparse.Namespace(**values)


class ModelBackendTests(unittest.TestCase):
    def test_deepseek_multi_sampling_uses_independent_supported_requests(self):
        factory = RecordingClientFactory()
        with patch.dict(os.environ, {"DEEPSEEK_API_KEY": "test-key"}, clear=False):
            backend = build_api_backend(make_args(), openai_client_factory=factory)
            outputs = backend.generate(
                "prompt",
                model_name="deepseek-v4-flash",
                count=3,
            )

        self.assertEqual(outputs, ["answer-1", "answer-2", "answer-3"])
        self.assertEqual(
            factory.calls,
            [{
                "api_key": "test-key",
                "base_url": DEEPSEEK_API_BASE,
                "timeout": 120.0,
                "max_retries": 5,
            }],
        )
        requests = factory.client.chat.completions.calls
        self.assertEqual(len(requests), 3)
        for request in requests:
            self.assertNotIn("n", request)
            self.assertEqual(request["model"], "deepseek-v4-flash")
            self.assertEqual(request["messages"], [{"role": "user", "content": "prompt"}])
            self.assertEqual(request["extra_body"], {"thinking": {"type": "disabled"}})
            self.assertEqual(request["temperature"], 0.0)
            self.assertEqual(request["max_tokens"], 2048)
            self.assertFalse(request["stream"])

        snapshot = backend.snapshot()
        self.assertEqual(snapshot["request_count"], 3)
        self.assertEqual(snapshot["prompt_tokens"], 30)
        self.assertEqual(snapshot["completion_tokens"], 6)
        self.assertEqual(snapshot["total_tokens"], 36)
        self.assertEqual(snapshot["prompt_tokens_est"], 3 * estimate_text_tokens("prompt"))
        self.assertEqual(
            snapshot["completion_tokens_est"],
            sum(estimate_text_tokens(output) for output in outputs),
        )
        self.assertEqual(
            snapshot["total_tokens_est"],
            snapshot["prompt_tokens_est"] + snapshot["completion_tokens_est"],
        )

    def test_generic_openai_compatible_backend_uses_custom_configuration(self):
        factory = RecordingClientFactory()
        args = make_args(
            model_provider="openai_compatible",
            api_base="https://provider.example/v1",
            api_key_env="PROVIDER_API_KEY",
        )
        with patch.dict(os.environ, {"PROVIDER_API_KEY": "provider-key"}, clear=False):
            backend = build_api_backend(args, openai_client_factory=factory)
            backend.generate("prompt", model_name="other-model", count=1)

        self.assertEqual(
            factory.calls,
            [
                {
                    "api_key": "provider-key",
                    "base_url": "https://provider.example/v1",
                    "timeout": 120.0,
                    "max_retries": 5,
                }
            ],
        )
        self.assertNotIn("extra_body", factory.client.chat.completions.calls[0])

    def test_missing_key_fails_before_client_construction(self):
        factory = RecordingClientFactory()
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(RuntimeError, "DEEPSEEK_API_KEY"):
                build_api_backend(make_args(), openai_client_factory=factory)
        self.assertEqual(factory.calls, [])

    def test_empty_response_is_rejected(self):
        factory = RecordingClientFactory(content_prefix="")
        factory.client.chat.completions.content_prefix = ""
        with patch.dict(os.environ, {"DEEPSEEK_API_KEY": "test-key"}, clear=False):
            backend = build_api_backend(make_args(), openai_client_factory=factory)
            original_create = factory.client.chat.completions.create

            def empty_create(**kwargs):
                response = original_create(**kwargs)
                response.choices[0].message.content = ""
                return response

            factory.client.chat.completions.create = empty_create
            with self.assertRaisesRegex(RuntimeError, "empty"):
                backend.generate("prompt", "deepseek-v4-flash")

    def test_provider_resolution_and_argument_defaults(self):
        self.assertEqual(resolve_model_provider(make_args(model_provider="auto")), "deepseek")
        self.assertEqual(
            resolve_model_provider(make_args(model_provider="auto", plan_model_name="gpt-4o")),
            "azure",
        )
        self.assertEqual(
            resolve_model_provider(make_args(model_provider="auto", plan_model_name="Qwen2.5")),
            "local",
        )

        parser = argparse.ArgumentParser()
        add_model_backend_args(parser)
        args = parser.parse_args([])
        self.assertEqual(args.model_provider, "auto")
        self.assertEqual(args.api_base, DEEPSEEK_API_BASE)
        self.assertEqual(args.api_key_env, "DEEPSEEK_API_KEY")
        self.assertEqual(args.thinking, "disabled")
        self.assertEqual(args.temperature, 0.0)
        self.assertEqual(args.max_tokens, 2048)
        self.assertEqual(args.api_max_retries, 5)


if __name__ == "__main__":
    unittest.main()
