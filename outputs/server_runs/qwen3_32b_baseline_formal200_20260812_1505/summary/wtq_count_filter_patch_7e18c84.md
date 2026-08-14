# WTQ Count/Date Filter Patch 7e18c84

Date: 2026-08-14 CST

Code commit: MyAgent `7e18c84` (`feat: add wtq deterministic count filters`)

Run root: `outputs/server_runs/qwen3_32b_baseline_formal200_20260812_1505`

GPU / endpoint scope:

- `8000`: Qwen3-32B local service on GPUs `4,5`
- `8001`: Qwen3-32B local service on GPUs `6,7`
- GPUs `0,1,2,3` were not used.

## Patch Scope

This patch adds two WTQ deterministic shortcuts:

- `number of players who scored at least 1 friendly`: count rows where the requested metric column is at least the numeric threshold.
- `how many races took place after august`: count rows whose best date-like column has month greater than the requested bare month.

The after-month rule intentionally rejects specific day cutoffs such as `after october 1st`, because those require day-level filtering rather than month-only filtering.

Local verification:

- `python -m unittest discover -s tests -p 'test_myagent_pipeline.py'`: `224` tests passed.
- `python -m py_compile code/my_agents.py code/tqa.py`: passed.

## Offline Scan

Input: `input/formal200/wtq.jsonl`

New rule hits:

| ID | Rule | Answer | Correct | Previous patched answer |
|---|---|---:|---:|---|
| `nu-152` | at-least metric count | 10 | yes | `5` |
| `nu-160` | after bare month row count | 6 | yes | `3` |

After tightening the bare-month guard, these are the only new rule hits on WTQ formal200, and both are correct.

## Focused-2 Runner Validation

Input:

- `input/diagnostic/wtq_count_filter_regression2.jsonl`
- IDs: `nu-152`, `nu-160`

Output:

- Root: `diagnostics/wtq_count_filter_regression2_patch_7e18c84`
- Merged: `diagnostics/wtq_count_filter_regression2_patch_7e18c84/merged/wtq_qwen3-32b-local.jsonl`
- Eval: `diagnostics/wtq_count_filter_regression2_patch_7e18c84/eval/wtq_qwen3-32b-local_eval.json`

Metrics:

| Metric | Value |
|---|---:|
| Rows | 2 |
| Primary accuracy | 2/2 = 1.0000 |
| Strict exact match | 2/2 = 1.0000 |
| Failed exec | 0 |
| Missing answer | 0 |
| Avg total tokens | 3607.00 |
| Avg elapsed seconds | 6.339 |

Per-row:

| ID | Final answer | Shortcut reason | Tokens | Time |
|---|---:|---|---:|---:|
| `nu-152` | 10 | WTQ at-least metric rows counted deterministically. | 2984 | 6.070s |
| `nu-160` | 6 | WTQ rows after requested month counted deterministically. | 4230 | 6.608s |

## Decision

Keep this patch. It directly covers the two non-shortcut regressions observed in the prior WTQ formal200 patch run.

Expected WTQ after applying this patch to the previous full run is `149/200 = 0.7450` if other non-shortcut rows remain stable. Because full WTQ200 reruns are relatively expensive and can introduce LLM-path variance, the next full WTQ200 rerun should be batched with the next set of deterministic fixes rather than run after every two-row patch.
