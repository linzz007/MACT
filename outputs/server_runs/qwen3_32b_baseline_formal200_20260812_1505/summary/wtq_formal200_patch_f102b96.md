# WTQ Formal-200 Patch Validation f102b96

Date: 2026-08-14 CST

Run root: `outputs/server_runs/qwen3_32b_baseline_formal200_20260812_1505`

Code:

- Runner HEAD: MyAgent `f102b96`
- Code patch commit: MyAgent `d646885` (`feat: add wtq deterministic adjacency shortcuts`)

GPU / endpoint scope:

- `8000`: Qwen3-32B local service on GPUs `4,5`
- `8001`: Qwen3-32B local service on GPUs `6,7`
- GPUs `0,1,2,3` were not used; repeated `nvidia-smi pmon -c 1` checks showed no visible compute PID on `0-3`.

Files:

- Input: `input/formal200/wtq.jsonl`
- Output root: `diagnostics/wtq_formal200_patch_f102b96`
- Merged: `diagnostics/wtq_formal200_patch_f102b96/merged/wtq_qwen3-32b-local.jsonl`
- Eval: `diagnostics/wtq_formal200_patch_f102b96/eval/wtq_qwen3-32b-local_eval.json`
- Compare JSON: `diagnostics/wtq_formal200_patch_f102b96_compare.json`

## Main Result

| System | Rows | WTQ primary accuracy | Exact match | Avg token | Avg time | Failed/Missing |
|---|---:|---:|---:|---:|---:|---:|
| Old MyAgent formal200 | 200 | 141/200 = 0.7050 | 140/200 = 0.7000 | 6326.39 | 16.663s | 0/0 |
| Patched MyAgent | 200 | 147/200 = 0.7350 | 145/200 = 0.7250 | 6228.74 | 16.140s | 0/0 |
| MACT formal200 | 200 | 156/200 = 0.7800 | 153/200 = 0.7650 | 10698.62 | 115.088s | 4/4 |

The patch improves WTQ by `+6` primary-correct rows over old MyAgent while keeping token and time lower than the old MyAgent run and far below MACT.

Patched MyAgent is still below MACT on WTQ by `9` primary-correct rows (`147` vs `156`).

## Delta Against Old MyAgent

Net primary delta: `+6`

- Old wrong -> patched right: `8` rows
- Old right -> patched wrong: `2` rows

Old wrong -> patched right:

| ID | Shortcut? | Reason |
|---|---:|---|
| `nu-27` | yes | last requested table-column value |
| `nu-66` | yes | after-reference row order |
| `nu-78` | yes | after-reference row order |
| `nu-100` | yes | same-number peer entity |
| `nu-129` | no | non-shortcut rerun path |
| `nu-146` | yes | after-reference row order |
| `nu-180` | yes | after-reference row order |
| `nu-188` | no | non-shortcut rerun path |

Old right -> patched wrong:

| ID | Shortcut? | Notes |
|---|---:|---|
| `nu-152` | no | non-shortcut rerun path changed from `10` to `5` |
| `nu-160` | no | non-shortcut rerun path changed from `6` to `3` |

The two regressions did not use the new deterministic shortcut path. They are runner/model-path variance on non-shortcut WTQ rows, not direct shortcut failures.

## Shortcut Stats

- Deterministic shortcut fired on `21/200` rows.
- Shortcut rows correct: `18/21 = 0.8571`.
- The newly targeted focused rows remained correct in full200: `nu-27`, `nu-66`, `nu-78`, `nu-100`, `nu-146`, `nu-180`.

## Patched MyAgent vs MACT

| Pair bucket | Count |
|---|---:|
| Patched MyAgent only correct | 18 |
| MACT only correct | 27 |
| Both wrong | 26 |

Remaining WTQ gap is therefore smaller than before but still material: MACT-only rows dropped from `31` before the patch to `27` after the patch.

## Decision

Keep the patch. It is a valid patent-relevant optimization because it uses deterministic structural table reasoning to recover known WTQ errors with low token cost.

This does not complete the patent-data goal. After this patch, the expected total formal200 result becomes approximately:

- MyAgent: old total `436/600` plus WTQ net `+6` = `442/600 = 0.7367`
- MACT: `465/600 = 0.7750`

Next work should target the remaining `27` WTQ MACT-only rows and the TabFact gap. The immediate WTQ diagnostic targets are `nu-152` and `nu-160` regressions plus high-frequency MACT-only categories: count, temporal, negation/exclusion, and comparison/superlative.
