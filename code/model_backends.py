"""Parameter-selectable chat backends for MACT."""

from __future__ import annotations

import os
from argparse import ArgumentParser, Namespace
from typing import Any, Callable, Optional


DEEPSEEK_API_BASE = "https://api.deepseek.com"
MODEL_PROVIDERS = ("auto", "deepseek", "openai_compatible", "azure", "local")


def estimate_text_tokens(text: Any) -> int:
    if text is None:
        return 0
    value = str(text)
    if not value:
        return 0
    try:
        import tiktoken

        encoding = tiktoken.get_encoding("cl100k_base")
        return len(encoding.encode(value))
    except Exception:
        return max(1, len(value) // 2)


def add_model_backend_args(parser: ArgumentParser) -> None:
    parser.add_argument(
        "--model_provider",
        choices=MODEL_PROVIDERS,
        default="auto",
        help="Model backend. 'auto' infers DeepSeek/Azure/local from the planning model name.",
    )
    parser.add_argument(
        "--api_base",
        default=DEEPSEEK_API_BASE,
        help="Base URL for DeepSeek or another OpenAI-compatible API.",
    )
    parser.add_argument(
        "--api_key_env",
        default="DEEPSEEK_API_KEY",
        help="Environment variable containing the API key.",
    )
    parser.add_argument(
        "--thinking",
        choices=("disabled", "enabled"),
        default="disabled",
        help="DeepSeek thinking mode.",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.0,
        help="Sampling temperature used by API backends.",
    )
    parser.add_argument(
        "--max_tokens",
        type=int,
        default=2048,
        help="Maximum generated tokens for each API request.",
    )
    parser.add_argument(
        "--api_timeout",
        type=float,
        default=120.0,
        help="API request timeout in seconds.",
    )
    parser.add_argument(
        "--api_max_retries",
        type=int,
        default=5,
        help="Maximum automatic retries for transient API failures.",
    )


def resolve_model_provider(args: Namespace) -> str:
    provider = getattr(args, "model_provider", "auto") or "auto"
    if provider != "auto":
        return provider

    model_name = (getattr(args, "plan_model_name", "") or "").lower()
    if "deepseek" in model_name:
        return "deepseek"
    if "gpt" in model_name:
        return "azure"
    return "local"


class ChatCompletionsBackend:
    """Generate MACT candidates through a chat-completions client."""

    def __init__(
        self,
        client: Any,
        provider: str,
        thinking: str = "disabled",
        temperature: float = 0.0,
        max_tokens: int = 2048,
    ) -> None:
        self.client = client
        self.provider = provider
        self.thinking = thinking
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.request_count = 0
        self.prompt_tokens = 0
        self.completion_tokens = 0
        self.prompt_tokens_est = 0
        self.completion_tokens_est = 0

    def _record_usage(self, response: Any) -> None:
        usage = getattr(response, "usage", None)
        self.prompt_tokens += int(getattr(usage, "prompt_tokens", 0) or 0)
        self.completion_tokens += int(getattr(usage, "completion_tokens", 0) or 0)

    @staticmethod
    def _response_text(response: Any) -> str:
        try:
            content = response.choices[0].message.content
        except (AttributeError, IndexError, TypeError) as exc:
            raise RuntimeError("The model API returned an invalid chat completion response.") from exc
        if not content or not str(content).strip():
            raise RuntimeError("The model API returned an empty response.")
        return str(content)

    def generate(self, prompt: str, model_name: str, count: int = 1) -> list[str]:
        if not model_name:
            raise RuntimeError("A model name is required for API generation.")
        if count < 1:
            raise ValueError("count must be at least 1.")

        outputs = []
        for _ in range(count):
            request = {
                "model": model_name,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": self.temperature,
                "max_tokens": self.max_tokens,
                "stream": False,
            }
            if self.provider == "deepseek":
                request["extra_body"] = {"thinking": {"type": self.thinking}}
            response = self.client.chat.completions.create(**request)
            self.request_count += 1
            self._record_usage(response)
            output = self._response_text(response)
            self.prompt_tokens_est += estimate_text_tokens(prompt)
            self.completion_tokens_est += estimate_text_tokens(output)
            outputs.append(output)
        return outputs

    def snapshot(self) -> dict[str, int]:
        return {
            "request_count": self.request_count,
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "total_tokens": self.prompt_tokens + self.completion_tokens,
            "prompt_tokens_est": self.prompt_tokens_est,
            "completion_tokens_est": self.completion_tokens_est,
            "total_tokens_est": self.prompt_tokens_est + self.completion_tokens_est,
        }


def build_api_backend(
    args: Namespace,
    openai_client_factory: Optional[Callable[..., Any]] = None,
) -> ChatCompletionsBackend:
    provider = resolve_model_provider(args)
    if provider not in {"deepseek", "openai_compatible", "azure"}:
        raise ValueError(f"Provider {provider!r} is not an API backend.")

    if provider == "azure":
        from agents import load_gpt_azure

        client = load_gpt_azure()
    else:
        api_key_env = getattr(args, "api_key_env", "DEEPSEEK_API_KEY")
        api_key = os.getenv(api_key_env)
        if not api_key:
            raise RuntimeError(
                f"Environment variable {api_key_env} is not set. "
                "Set it before starting the experiment."
            )
        if openai_client_factory is None:
            from openai import OpenAI

            openai_client_factory = OpenAI
        base_url = getattr(args, "api_base", DEEPSEEK_API_BASE) or DEEPSEEK_API_BASE
        timeout = float(getattr(args, "api_timeout", 120.0))
        max_retries = int(getattr(args, "api_max_retries", 5))
        client = openai_client_factory(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
        )

    return ChatCompletionsBackend(
        client=client,
        provider=provider,
        thinking=getattr(args, "thinking", "disabled"),
        temperature=float(getattr(args, "temperature", 0.0)),
        max_tokens=int(getattr(args, "max_tokens", 2048)),
    )
