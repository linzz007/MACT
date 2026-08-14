# WTQ Shortcut Generalization Diagnostic 20260814

Date: 2026-08-14 CST

Run root: `outputs/server_runs/qwen3_32b_baseline_formal200_20260812_1505`

Code context:

- MyAgent docs HEAD: `3eab6a1`
- Latest WTQ locked code included in the formal200 result path: `7168923`
- Latest Qwen3 formal target completion patch: `5e3e0e8`

GPU / endpoint scope:

- This diagnostic is offline and did not call the model.
- Active Qwen services remain on `http://127.0.0.1:8000/v1` for GPUs `4,5` and `http://127.0.0.1:8001/v1` for GPUs `6,7`.
- Recheck at 2026-08-14 14:18 CST showed visible vLLM compute workers only on GPUs `4,5,6,7`. GPUs `0,2,3` reported memory/utilization that was not exposed as a visible experiment/vLLM compute PID, so they were not killed blindly.

Files:

- Diagnostic root: `diagnostics/wtq_shortcut_generalization_20260814`
- Summary JSON: `diagnostics/wtq_shortcut_generalization_20260814/summary.json`
- Hit rows: `diagnostics/wtq_shortcut_generalization_20260814/*_hits.jsonl`
- Wrong-hit rows: `diagnostics/wtq_shortcut_generalization_20260814/*_wrong_hits.jsonl`
- Exception rows: `diagnostics/wtq_shortcut_generalization_20260814/*_exceptions.jsonl`

## Purpose

This diagnostic checks whether current WTQ deterministic shortcut rules are high precision outside the formal200 sample. It runs the same shortcut functions offline against WTQ rows, canonicalizes shortcut answers with the current WTQ scalar normalizer, and evaluates against gold answers with the project WTQ denotation matcher.

The result should be used as boundary evidence for patent/thesis writing, not as a new optimization.

## Results

| Split | Input rows | Scanned rows | Shortcut hits | Correct hits | Wrong hits | Exceptions | Accuracy on hits |
|---|---:|---:|---:|---:|---:|---:|---:|
| formal200 | 200 | 200 | 31 | 28 | 3 | 0 | 0.9032 |
| blind200_v1 | 200 | 200 | 19 | 18 | 1 | 0 | 0.9474 |
| frozen150 | 150 | 150 | 32 | 24 | 8 | 0 | 0.7500 |
| full_unseen | 4344 | 4344 | 438 | 290 | 148 | 0 | 0.6621 |
| full_unseen_minus_formal200 | 4344 | 4144 | 407 | 262 | 145 | 0 | 0.6437 |

High-frequency wrong-hit sources on `full_unseen_minus_formal200`:

| Shortcut | Hits | Correct | Wrong |
|---|---:|---:|---:|
| `after_reference` | 137 | 81 | 56 |
| `last_requested_column` | 96 | 40 | 56 |
| `superlative_owner` | 109 | 89 | 20 |
| `existing_total_metric` | 12 | 4 | 8 |
| `listed_after_cell` | 9 | 7 | 2 |
| `date_cutoff_row_count` | 4 | 3 | 1 |

Representative wrong hits:

| Split | ID | Shortcut | Prediction | Gold | Question |
|---|---|---|---|---|---|
| formal200 | `nu-72` | `superlative_owner` | `1994.0` | `2003` | `which year had the least amount of toy sales?` |
| formal200 | `nu-144` | `last_requested_column` | `December 2, 1982 (#82000626)` | `Samuel Wyatt House` | `what was the last listed historical place in strafford county, new hampshire?` |
| blind200_v1 | `nu-1786` | `after_reference` | `1989-1990 Season` | `1990-1991 Season` | `what was the next tie listed after the 1989-1990 season?` |
| frozen150 | `nu-625` | `playoff_count` | `10` | `7` | `how many years did they make the playoffs?` |
| full_unseen_minus_formal200 | `nu-228` | `after_reference` | `2003.0` | `Nightrain` | `what was released after paradise city?` |
| full_unseen_minus_formal200 | `nu-240` | `last_requested_column` | `Train Station Bus Terminal` | `Bus Terminal` | `what is the name of the last destination listed on this chart?` |

## Interpretation

The WTQ shortcut rules are useful and high precision on the locked formal200 and blind200 samples, and they contributed to the Qwen3 formal200 win over MACT. However, the same rules are not broadly safe on the full WTQ unseen pool: hit accuracy drops to `0.6437` after removing formal200 IDs.

This means the current project should not expand WTQ shortcut coverage by pattern matching alone. Future WTQ improvements need a stronger acceptance gate, for example:

- verify that the selected answer column matches the semantic answer type requested by the question,
- reject ambiguous row/column matches when multiple candidate rows satisfy the reference phrase,
- require explicit target-column evidence for "last/listed/after" questions,
- preserve LLM fallback when shortcut confidence is below a high threshold.

## Decision

For the current patent/thesis stage, keep the locked Qwen3 formal200 result as the main evidence and document this diagnostic as a generalization boundary. Do not spend more time optimizing WTQ until the formal report package, ablation evidence, and cross-model gate plan are complete.
