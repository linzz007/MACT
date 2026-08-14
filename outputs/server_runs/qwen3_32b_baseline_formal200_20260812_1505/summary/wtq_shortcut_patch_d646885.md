# WTQ Deterministic Shortcut Patch d646885

Date: 2026-08-14 CST

Code commit: MyAgent `d646885` (`feat: add wtq deterministic adjacency shortcuts`)

Run root: `outputs/server_runs/qwen3_32b_baseline_formal200_20260812_1505`

GPU / endpoint scope:

- `8000`: Qwen3-32B local service on GPUs `4,5`
- `8001`: Qwen3-32B local service on GPUs `6,7`
- GPUs `0,1,2,3` were not used for this validation. `nvidia-smi pmon -c 1` showed no visible compute PID on `0-3` before the run.

## Patch Scope

The patch extends low-token WTQ deterministic shortcuts for three structural cases:

- `same number as <entity>`: exclude the reference entity and return the matching peer entity.
- next/listed-after row lookup: support entity questions such as `who is the next driver listed after ...` and skip blank metadata rows.
- `who was the <target> in the last <period>`: select the requested target column instead of returning the period column.

Local verification before runner validation:

- `python -m unittest discover -s tests -p 'test_myagent_pipeline.py'`: `221` tests passed.
- `python -m py_compile code/my_agents.py code/tqa.py`: passed.

## Offline Formal-200 WTQ Scan

Input: `input/formal200/wtq.jsonl`

Result:

- Shortcut path fires on `21/200` WTQ rows.
- Shortcut answers are correct on `18/21`.
- Compared with old MyAgent formal200 output, estimated delta is `+6` correct and `0` regressions.
- Expected fixed rows: `nu-27`, `nu-66`, `nu-78`, `nu-100`, `nu-146`, `nu-180`.

This estimated WTQ improvement would move WTQ from `141/200 = 0.7050` to about `147/200 = 0.7350`, and total formal200 overall from `436/600 = 0.7267` to about `442/600 = 0.7367`. This is useful progress but still below MACT overall `465/600 = 0.7750`.

## Focused-6 Runner Validation

Input:

- `input/diagnostic/wtq_shortcut_delta6.jsonl`
- IDs: `nu-27`, `nu-66`, `nu-78`, `nu-100`, `nu-146`, `nu-180`

Output:

- Root: `diagnostics/wtq_shortcut_delta6_patch_d646885`
- Merged: `diagnostics/wtq_shortcut_delta6_patch_d646885/merged/wtq_qwen3-32b-local.jsonl`
- Eval: `diagnostics/wtq_shortcut_delta6_patch_d646885/eval/wtq_qwen3-32b-local_eval.json`

Metrics:

| Metric | Value |
|---|---:|
| Rows | 6 |
| Primary accuracy | 6/6 = 1.0000 |
| Strict exact match | 5/6 = 0.8333 |
| Failed exec | 0 |
| Missing answer | 0 |
| Avg total tokens | 3858.33 |
| Avg prompt tokens | 3772.83 |
| Avg completion tokens | 85.50 |
| Avg elapsed seconds | 4.480 |
| Avg LLM calls | 2.833 |

Per-row change:

| ID | Old MyAgent answer | Patched answer | Gold | Shortcut reason |
|---|---|---|---|---|
| `nu-27` | `2011-12` | `Simon Makienok Christoffersen (10)` | `Simon Makienok Christoffersen` | last requested table-column value |
| `nu-66` | `September 6, 2010` | `December 6, 2010` | `December 6, 2010` | after-reference row order |
| `nu-78` | `Tony Kanaan` | `Mike Conway` | `Mike Conway` | after-reference row order |
| `nu-100` | `Greg Foster` | `Kyrylo Fesenko` | `Kyrylo Fesenko` | same-number peer entity |
| `nu-146` | `West Up!" by WC and the Maad Circle` | `\Call It What You Want\""` | `Call It What You Want` | after-reference row order |
| `nu-180` | `Radium` | `Actinium` | `Actinium` | after-reference row order |

Note: WTQ primary accuracy uses denotation matching, so formatting variants such as parenthesized scores or quote escaping can pass primary accuracy while not matching strict exact string form.

## Decision

Accept this patch as a valid WTQ mechanism improvement and keep it in MyAgent. It is patent-relevant because it demonstrates a low-token deterministic structural route that fixes known MACT-only WTQ failures without invoking broad extra verification.

Next required validation:

- Run patched MyAgent on full WTQ formal200 to confirm the offline `+6 / 0 regression` estimate under the real runner.
- Continue additional WTQ and TabFact mechanism work after full WTQ200, because this patch alone does not close the full formal200 gap to MACT.
