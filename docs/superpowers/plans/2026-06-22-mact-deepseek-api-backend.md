# MACT DeepSeek API Backend Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Run MACT's WTQ, TabFact, and CRT paths through a parameter-selectable official DeepSeek/OpenAI-compatible API backend without loading local inference packages in API mode.

**Architecture:** A focused `ChatCompletionsBackend` owns API requests and multi-candidate sampling. `ReactAgent` receives that backend explicitly and uses it for every generation path; `tqa.py` selects API or local runtime with lazy imports.

**Tech Stack:** Python 3, argparse, OpenAI Python SDK, unittest, MACT ReactAgent

---

### Task 1: Chat completion backend

**Files:**
- Create: `code/model_backends.py`
- Create: `tests/test_model_backends.py`

- [x] **Step 1: Write the failing API contract tests**

Create fake `client.chat.completions.create` objects and tests that call:

```python
backend = build_api_backend(args, openai_client_factory=factory)
outputs = backend.generate("prompt", model_name="deepseek-v4-flash", count=3)
```

Assert three independent requests, no `n` argument, `extra_body={"thinking": {"type": "disabled"}}`, selected model, endpoint, environment key, response texts, request count, and summed token usage. Add missing-key and empty-response tests.

- [x] **Step 2: Run tests and confirm RED**

Run: `python -m unittest discover -s tests -p "test_model_backends.py" -v`

Expected: import failure for missing `model_backends`.

- [x] **Step 3: Implement the backend**

Implement these public interfaces:

```python
DEEPSEEK_API_BASE = "https://api.deepseek.com"

def add_model_backend_args(parser): ...
def resolve_model_provider(args) -> str: ...
def build_api_backend(args, openai_client_factory=None): ...

class ChatCompletionsBackend:
    def generate(self, prompt: str, model_name: str, count: int = 1) -> list[str]: ...
    def snapshot(self) -> dict[str, int]: ...
```

For DeepSeek, loop `count` times and place `thinking` under `extra_body`; for generic OpenAI-compatible providers omit that provider-specific field.

- [x] **Step 4: Run backend tests and confirm GREEN**

Run: `python -m unittest discover -s tests -p "test_model_backends.py" -v`

Expected: all backend tests pass without network access.

### Task 2: Inject the backend into ReactAgent

**Files:**
- Modify: `code/agents.py`
- Create: `tests/test_react_agent_api.py`

- [x] **Step 1: Write failing import and agent-path tests**

Use a scripted backend:

```python
class ScriptedBackend:
    def generate(self, prompt, model_name, count=1):
        return ["Thought 1: done\nAction 1: Finish[answer]"] * count
```

Assert `agents` imports when Azure/langchain/sglang/transformers/vLLM are absent, `ReactAgent(..., api_backend=backend)` constructs without a local model, `prompt_agent`, code generation, quick answer, direct reasoning, and global planning all call the backend with the correct plan/code model.

- [x] **Step 2: Run tests and confirm RED**

Run: `python -m unittest discover -s tests -p "test_react_agent_api.py" -v`

Expected: current top-level optional dependency imports fail and `api_backend` is not accepted.

- [x] **Step 3: Decouple optional imports and route generations**

Make Azure, OpenSourceLLM, langchain, tot, and sglang imports lazy or optional. Add `api_backend=None` to `ReactAgent.__init__`, instantiate `OpenSourceLLM` only when it is absent, and centralize API generation:

```python
def _generate(self, prompt, model_name, count):
    if self.api_backend is not None:
        return self.api_backend.generate(prompt, model_name=model_name, count=count)
    return self.llm(prompt, num_return_sequences=count, return_prob=False)
```

Use this boundary in planner, retriever, calculator, quick-answer, direct-reasoning, and global-plan paths. Use the API backend directly for `as_reward=llm`; reject API `logp` and `combined` before execution.

- [x] **Step 4: Run agent tests and confirm GREEN**

Run: `python -m unittest discover -s tests -p "test_react_agent_api.py" -v`

Expected: all API agent paths pass without optional local packages.

### Task 3: Parameterized MACT entry point

**Files:**
- Modify: `code/tqa.py`
- Create: `tests/test_tqa_api_entry.py`

- [x] **Step 1: Write failing entry tests**

Run `python code/tqa.py --help` in a subprocess and assert exit 0 plus `--model_provider`, `--api_base`, `--api_key_env`, and `--thinking`. Test a `build_runtime(args, factory)` helper returns an API backend without importing local inference packages and rejects `logp/combined` in API mode.

- [x] **Step 2: Run tests and confirm RED**

Run: `python -m unittest discover -s tests -p "test_tqa_api_entry.py" -v`

Expected: current eager `sglang` import fails.

- [x] **Step 3: Implement lazy runtime selection**

Move sglang/transformers/vLLM imports inside the local branch, add shared backend arguments, build one API backend per run, and pass it into every agent. Keep the existing dataset record contract and output naming.

- [x] **Step 4: Run entry tests and confirm GREEN**

Run: `python -m unittest discover -s tests -p "test_tqa_api_entry.py" -v`

Expected: API help/runtime tests pass on the lightweight local environment.

### Task 4: Three-dataset smoke verification and runbook

**Files:**
- Create: `tests/test_three_dataset_api_smoke.py`
- Modify: `D:/AAAcode/code-code/agent+/myAgent-main/EXPERIMENT_READINESS.md`

- [x] **Step 1: Write smoke tests using the real prepared records**

Load the first record from each of:

```text
D:/AAAcode/code-code/agent+/myAgent-main/datasets_ready/wtq_unseen_sample5.jsonl
D:/AAAcode/code-code/agent+/myAgent-main/datasets_ready/tabfact_test_sample5.jsonl
D:/AAAcode/code-code/agent+/myAgent-main/datasets_ready/crt_sample5.jsonl
```

Construct MACT `ReactAgent` instances with a scripted Finish response, run each agent, and assert the predicted answer is non-empty for tasks `wtq`, `scitab`, and `crt`.

- [x] **Step 2: Run the smoke tests**

Run: `python -m unittest discover -s tests -p "test_three_dataset_api_smoke.py" -v`

Expected: all three task paths pass with no real API spend.

- [x] **Step 3: Document fair DeepSeek smoke commands**

Document both projects with `deepseek-v4-flash`, thinking disabled, temperature 0, `plan_sample=1`, `code_sample=1`, matching dataset files, and task mapping `TabFact -> scitab`.

- [x] **Step 4: Run the full verification gate**

Run:

```powershell
python -m unittest discover -s tests -v
python -m py_compile code/model_backends.py code/agents.py code/tqa.py
python code/tqa.py --help
```

Expected: all tests pass, compilation exits 0, and CLI help starts without local inference packages. A real DeepSeek request remains a separate gate requiring `DEEPSEEK_API_KEY` in the process environment.
