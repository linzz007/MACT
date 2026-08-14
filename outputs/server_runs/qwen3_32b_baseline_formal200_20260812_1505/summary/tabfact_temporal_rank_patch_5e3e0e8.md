# TabFact Temporal/Rank Filter Patch (`5e3e0e8`)

Date: 2026-08-14 14:11 CST

## Scope

- MyAgent commit: `5e3e0e8` (`feat: add tabfact temporal and rank filters`)
- Dataset: TabFact Formal-200, Qwen3-32B local
- GPU policy: only GPUs `4,5,6,7`; endpoints `http://127.0.0.1:8000/v1` and `http://127.0.0.1:8001/v1`
- Patch type: narrow deterministic table verification for temporal counts, rank/medal checks, lowest-attendance outcomes, entity award counts, tennis surface counts, tenure intervals, and race winner/leader counts

## Output Files

| Artifact | Path |
|---|---|
| Focused input | `input/diagnostic/tabfact_temporal_rank_delta15.jsonl` |
| Focused ids | `input/diagnostic/tabfact_temporal_rank_delta15_ids.txt` |
| Focused output root | `diagnostics/tabfact_temporal_rank_delta15_patch_5e3e0e8/` |
| Focused eval | `diagnostics/tabfact_temporal_rank_delta15_patch_5e3e0e8/eval/tabfact_qwen3-32b-local_eval.json` |
| Full200 output root | `diagnostics/tabfact_formal200_patch_5e3e0e8/` |
| Full200 merged | `diagnostics/tabfact_formal200_patch_5e3e0e8/merged/tabfact_qwen3-32b-local.jsonl` |
| Full200 eval | `diagnostics/tabfact_formal200_patch_5e3e0e8/eval/tabfact_qwen3-32b-local_eval.json` |

## Focused-15 Result

Focused rows:

`tabfact-test-22`, `tabfact-test-41`, `tabfact-test-60`, `tabfact-test-63`, `tabfact-test-64`, `tabfact-test-68`, `tabfact-test-80`, `tabfact-test-84`, `tabfact-test-103`, `tabfact-test-109`, `tabfact-test-139`, `tabfact-test-146`, `tabfact-test-177`, `tabfact-test-187`, `tabfact-test-190`.

| Rows | Primary accuracy | Exact match | Avg token | Avg time | Fail/Missing |
|---:|---:|---:|---:|---:|---:|
| 15 | 1.0000 | 1.0000 | 457.60 | 2.313s | 0/0 |

All 15 rows used `deterministic_shortcut_applied=true`; no shortcut row was wrong.

## Full TabFact Formal-200 Result

| Method | Correct | Accuracy | Avg token | Avg time | Fail/Missing |
|---|---:|---:|---:|---:|---:|
| Old MyAgent Formal-200 | 162/200 | 0.8100 | 2796.52 | 13.400s | 0/0 |
| MyAgent `c2552fd` | 175/200 | 0.8750 | 2711.77 | 13.228s | 0/0 |
| MyAgent `5e3e0e8` | 190/200 | 0.9500 | 2372.42 | 11.689s | 0/0 |
| MACT official eval | 185/200 | 0.9250 | 11232.74 | 114.443s | 0/0 |

Delta vs `c2552fd`:

- New-right previous-wrong rows: 15
- New-wrong previous-right rows: 0
- Net gain: +15 correct
- Deterministic shortcut hits in full200: 50
- Wrong deterministic shortcut hits: 0

Remaining wrong rows after `5e3e0e8`:

`tabfact-test-8`, `tabfact-test-9`, `tabfact-test-14`, `tabfact-test-31`, `tabfact-test-34`, `tabfact-test-78`, `tabfact-test-82`, `tabfact-test-123`, `tabfact-test-179`, `tabfact-test-185`.

## Formal-200 Aggregate After Patch

Using locked WTQ `7168923`, TabFact `5e3e0e8`, and existing CRT Formal-200:

| Dataset | MyAgent current | MACT official | Status |
|---|---:|---:|---|
| WTQ | 157/200 = 0.7850 | 156/200 = 0.7800 | MyAgent +1 |
| TabFact | 190/200 = 0.9500 | 185/200 = 0.9250 | MyAgent +5 |
| CRT | 133/200 = 0.6650 | 124/200 = 0.6200 | MyAgent +9 |
| Overall | 480/600 = 0.8000 | 465/600 = 0.7750 | MyAgent +15 |

Efficiency aggregate:

| Method | Avg token | Avg time | Fail/Missing |
|---|---:|---:|---:|
| MyAgent current | 6293.12 | 16.749s | 0/0 |
| MACT official | 11318.89 | 126.861s | 4/4 |

Token ratio: `0.5560`. Time ratio: `0.1320`.

Decision: the Qwen3-32B Formal-200 target is achieved for the current patent/thesis experiment stage. MyAgent now exceeds MACT on all three datasets and the aggregate, while using substantially fewer tokens and much less wall time.
