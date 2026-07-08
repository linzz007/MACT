# MACT DeepSeek API Backend Design

## Goal

Make MACT run WTQ, TabFact (`scitab` prompt family), and CRT through the official DeepSeek OpenAI-compatible API without requiring local CUDA, vLLM, transformers, sglang, Azure, or langchain packages at API startup.

## Chosen Architecture

Add `code/model_backends.py` with a small injected chat backend. The backend owns provider resolution, API client construction, request parameters, response validation, and token counters. `code/tqa.py` owns CLI parsing and runtime selection. `ReactAgent` receives either an API backend or the existing local model objects and never infers the runtime from a model-name substring.

The rejected minimal alternative would route DeepSeek through MACT's existing GPT branches. That path references an uninitialized global client, hard-codes the Azure deployment name, and sends the unsupported `n` request parameter. Replacing MACT with myAgent's single-call abstraction was also rejected because MACT's multi-candidate voting is part of the baseline behavior.

## CLI Contract

- `--model_provider`: `auto`, `deepseek`, `openai_compatible`, `azure`, or `local`.
- `--plan_model_name` and `--code_model_name`: preserve MACT's two model-name fields.
- `--api_base`: defaults to `https://api.deepseek.com`.
- `--api_key_env`: defaults to `DEEPSEEK_API_KEY`; no plaintext key argument exists.
- `--thinking`: `disabled` or `enabled`.
- `--temperature`, `--max_tokens`, and `--api_timeout`: common request controls.

`auto` maps DeepSeek names to `deepseek`, GPT names to `azure`, and all other names to `local`. `openai_compatible` permits future providers by changing parameters only.

## API Data Flow

`tqa.py` creates one API backend per run and injects it into every `ReactAgent`. Planner sampling, code generation, direct reasoning, quick-answer fallback, and global planning call the same backend with the appropriate model name.

DeepSeek's current official Chat Completion schema does not expose an `n` parameter. To preserve MACT's `plan_sample` and `code_sample` semantics, `generate(..., count=N)` performs N independent non-streaming requests and returns N texts. A smoke run uses one candidate to control cost; full experiments can restore the paper setting.

## Compatibility Boundaries

- API mode supports `consistency`, `rollout`, and API-based `llm` selection.
- `logp` and `combined` remain local-only because MACT expects sequence-level local generation scores with a different shape from chat token logprobs.
- Wikipedia search is optional. If langchain is absent, the agent continues without the search tool; table retrieval and calculation remain available.
- Local mode preserves the existing vLLM and optional sglang code-server paths through lazy imports.
- Azure uses the same injected backend interface but retains the existing credential loader.

## Errors and Observability

Missing keys, empty responses, unsupported reward modes, or missing local dependencies fail with explicit messages before processing the dataset. API exceptions are not converted to empty candidates. The backend records request count plus prompt/completion token usage when the provider returns usage data.

## Verification

Unit tests inject a fake OpenAI client and verify endpoint, environment key, model selection, thinking parameters, independent multi-sampling, response validation, and token accounting. Agent tests inject a fake backend and verify Planner, code, quick-answer, and direct paths do not touch local model dependencies. Entry-point tests run `tqa.py --help` on the current lightweight Python environment. Three one-record dry runs use deterministic fake API responses and the prepared WTQ, TabFact, and CRT JSONL records.
