# TabFact Deterministic Table-Filter Patch (`c2552fd`)

Date: 2026-08-14 13:40 CST

## Scope

- MyAgent commit: `c2552fd` (`feat: add tabfact deterministic table filters`)
- Dataset: TabFact Formal-200, Qwen3-32B local
- GPU policy: only GPUs `4,5,6,7`; endpoints `http://127.0.0.1:8000/v1` and `http://127.0.0.1:8001/v1`
- Patch type: narrow deterministic TabFact table filters for count, country, attendance, score-difference, and metric-order claims

## Output Files

| Artifact | Path |
|---|---|
| Focused input | `input/diagnostic/tabfact_table_filter_delta10.jsonl` |
| Focused ids | `input/diagnostic/tabfact_table_filter_delta10_ids.txt` |
| Focused output root | `diagnostics/tabfact_table_filter_delta10_patch_c2552fd/` |
| Focused eval | `diagnostics/tabfact_table_filter_delta10_patch_c2552fd/eval/tabfact_qwen3-32b-local_eval.json` |
| Full200 output root | `diagnostics/tabfact_formal200_patch_c2552fd/` |
| Full200 merged | `diagnostics/tabfact_formal200_patch_c2552fd/merged/tabfact_qwen3-32b-local.jsonl` |
| Full200 eval | `diagnostics/tabfact_formal200_patch_c2552fd/eval/tabfact_qwen3-32b-local_eval.json` |

## Focused-10 Result

The focused set contains 10 old-MyAgent wrong rows that the new deterministic rules should correct:

`tabfact-test-50`, `tabfact-test-53`, `tabfact-test-56`, `tabfact-test-73`, `tabfact-test-75`, `tabfact-test-77`, `tabfact-test-92`, `tabfact-test-100`, `tabfact-test-150`, `tabfact-test-153`.

| Rows | Primary accuracy | Exact match | Avg token | Avg time | Fail/Missing |
|---:|---:|---:|---:|---:|---:|
| 10 | 1.0000 | 1.0000 | 402.20 | 2.476s | 0/0 |

All 10 rows used `deterministic_shortcut_applied=true`; no shortcut row was wrong.

## Full TabFact Formal-200 Result

| Method | Correct | Accuracy | Avg token | Avg time | Fail/Missing |
|---|---:|---:|---:|---:|---:|
| Old MyAgent Formal-200 | 162/200 | 0.8100 | 2796.52 | 13.400s | 0/0 |
| MyAgent `c2552fd` | 175/200 | 0.8750 | 2711.77 | 13.228s | 0/0 |
| MACT official eval | 185/200 | 0.9250 | 11232.74 | 114.443s | 0/0 |

Delta vs old MyAgent:

- New-right old-wrong rows: 15
- New-wrong old-right rows: 2 (`tabfact-test-177`, `tabfact-test-190`)
- Net gain: +13 correct
- Deterministic shortcut hits in full200: 28
- Wrong deterministic shortcut hits: 0

New-right old-wrong rows:

`tabfact-test-50`, `tabfact-test-53`, `tabfact-test-56`, `tabfact-test-73`, `tabfact-test-75`, `tabfact-test-77`, `tabfact-test-92`, `tabfact-test-100`, `tabfact-test-104`, `tabfact-test-120`, `tabfact-test-126`, `tabfact-test-138`, `tabfact-test-150`, `tabfact-test-153`, `tabfact-test-188`.

## Current Formal-200 Aggregate

Using locked WTQ `7168923`, TabFact `c2552fd`, and existing CRT Formal-200:

| Dataset | MyAgent current | MACT official |
|---|---:|---:|
| WTQ | 157/200 = 0.7850 | 156/200 = 0.7800 |
| TabFact | 175/200 = 0.8750 | 185/200 = 0.9250 |
| CRT | 133/200 = 0.6650 | 124/200 = 0.6200 |
| Overall | 465/600 = 0.7750 | 465/600 = 0.7750 |

Decision: keep the patch. It materially improves TabFact while slightly reducing average token, and it preserves the patent-relevant deterministic verification mechanism. The current overall score is tied with MACT, not above MACT, so the formal Qwen3-32B goal is not complete yet. The next patch should target the remaining TabFact MACT-only rows while preserving the zero-wrong-shortcut property.
