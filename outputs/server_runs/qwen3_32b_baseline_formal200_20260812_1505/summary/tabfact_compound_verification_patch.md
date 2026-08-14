# TabFact Compound Verification Patch

Updated: 2026-08-14 11:10 CST

Code commit under test: MyAgent `ed6ceca`.

Patch mechanism:

- Keep simple TabFact labels on the cheaper path.
- Trigger strong verification only when the row is `tabfact`, answer kind is `label`, tags include `closed_choice`, risk level is `high`, and at least two compound-risk tags are present among `temporal`, `negation_logic`, `superlative_order`, `comparison`, `arithmetic`, and `count`.

## Focused-17 Validation

Input:

```text
outputs/server_runs/qwen3_32b_baseline_formal200_20260812_1505/input/diagnostic/tabfact_mact_only_compound17.jsonl
```

Output:

```text
outputs/server_runs/qwen3_32b_baseline_formal200_20260812_1505/diagnostics/tabfact_compound17_patch_ed6ceca/
```

This input contains the 17 Formal-200 TabFact rows that were MACT-correct / old-MyAgent-wrong and matched the new trigger predicate.

| Rows | Old MyAgent correct | Patched MyAgent correct | MACT correct | Strong verification triggered | Avg token | Avg time | Fail/Missing |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 17 | 0/17 | 9/17 = 0.5294 | 17/17 | 17/17 | 18999.24 | 37.224s | 0/0 |

Interpretation:

- The patch direction is effective on the targeted old-error set: it recovers 9 of 17 rows.
- Token/time cost is much higher than the default TabFact path, so the trigger must remain selective.
- This is not enough to claim final improvement because the full trigger predicate hits 71 Formal-200 TabFact rows. The next validation must run all 71 triggered rows to measure regressions among previously correct samples.
