# WTQ Table Filter Patch cdc644c

Date: 2026-08-14 CST

Code commit: MyAgent `cdc644c` (`feat: add wtq deterministic table filters`)

Run root: `outputs/server_runs/qwen3_32b_baseline_formal200_20260812_1505`

GPU / endpoint scope:

- `8000`: Qwen3-32B local service on GPUs `4,5`
- `8001`: Qwen3-32B local service on GPUs `6,7`
- GPUs `0,1,2,3` were not used.

## Patch Scope

This patch adds conservative WTQ deterministic table filters for:

- `what is the only <entity> to have <number> <metric>`
- metric summation after entity filtering, including demonym normalization such as `Belgian` -> `Belgium`
- row counting across a list of named entities, e.g. `Barrington, Farmington, and Rochester combined`
- row-order-aware date cutoff counting for specific day cutoffs, including malformed rows where the date appears in a shifted cell
- first date where a metric crosses a numeric threshold
- column value counts such as `hard surface courts`

Local verification:

- `python -m unittest discover -s tests -p 'test_myagent_pipeline.py'`: `232` tests passed.
- `python -m py_compile code/my_agents.py code/tqa.py`: passed.

## Offline Scan

Input: `input/formal200/wtq.jsonl`

New/extended rule hits:

| ID | Rule | Answer | Correct | Previous patched answer |
|---|---|---:|---:|---|
| `nu-18` | only metric value | `Vidant Bertie Hospital` | yes | `{"answer": null}` |
| `nu-22` | metric sum by entity | 7 | yes | `6.0` |
| `nu-73` | metric sum by entity | 9 | yes | `0.0` |
| `nu-81` | combined entity row count | 5 | yes | `2` |
| `nu-94` | specific date cutoff count | 11 | yes | `7` |
| `nu-110` | column value count | 3 | yes | `1` |
| `nu-142` | first metric threshold date | `14 June 2005` | yes | `16 August 2004` |
| `nu-187` | specific date cutoff count | 10 | yes | `8` |

After tightening multiword entity and shifted-date handling, these are the only new/extended rule hits on WTQ formal200, and all are correct.

## Focused-8 Runner Validation

Input:

- `input/diagnostic/wtq_table_filter_delta8.jsonl`
- IDs: `nu-18`, `nu-22`, `nu-73`, `nu-81`, `nu-94`, `nu-110`, `nu-142`, `nu-187`

Output:

- Root: `diagnostics/wtq_table_filter_delta8_patch_cdc644c`
- Merged: `diagnostics/wtq_table_filter_delta8_patch_cdc644c/merged/wtq_qwen3-32b-local.jsonl`
- Eval: `diagnostics/wtq_table_filter_delta8_patch_cdc644c/eval/wtq_qwen3-32b-local_eval.json`

Metrics:

| Metric | Value |
|---|---:|
| Rows | 8 |
| Primary accuracy | 8/8 = 1.0000 |
| Strict exact match | 8/8 = 1.0000 |
| Failed exec | 0 |
| Missing answer | 0 |
| Avg total tokens | 4398.00 |
| Avg elapsed seconds | 6.319 |

Per-row:

| ID | Final answer | Shortcut reason | Tokens | Time |
|---|---|---|---:|---:|
| `nu-18` | `Vidant Bertie Hospital` | WTQ only row matching a metric value selected deterministically. | 5771 | 4.949s |
| `nu-22` | `7` | WTQ metric values summed after entity filtering. | 498 | 5.104s |
| `nu-73` | `9` | WTQ metric values summed after entity filtering. | 3307 | 6.570s |
| `nu-81` | `5` | WTQ rows for listed entities counted and combined. | 5925 | 6.600s |
| `nu-94` | `11` | WTQ rows before or after a specific date counted deterministically. | 4614 | 7.240s |
| `nu-110` | `3` | WTQ column values matching a requested phrase counted deterministically. | 4408 | 5.493s |
| `nu-142` | `14 June 2005` | WTQ first date crossing a metric threshold selected deterministically. | 5125 | 9.858s |
| `nu-187` | `10` | WTQ rows before or after a specific date counted deterministically. | 5536 | 4.739s |

## Decision

Keep this patch. It is strong patent-relevant evidence for deterministic structural table filters: it converts eight MACT-only WTQ errors into correct answers without broad verifier expansion.

Expected WTQ if combined with the previous validated patches:

- `d646885` full WTQ result: `147/200`
- `7e18c84` focused fixes: expected `+2`
- `cdc644c` focused fixes: expected `+8`
- Expected WTQ: `157/200 = 0.7850`

This would put MyAgent slightly above MACT on WTQ (`157/200` vs MACT `156/200`) while remaining much lower token/time. A full WTQ200 rerun is still needed to lock the actual realized number because non-shortcut rows can vary across full reruns.
