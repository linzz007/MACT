# TabFact Compound Verification Patch

Updated: 2026-08-14 12:05 CST

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

## Trigger-71 Validation

Input:

```text
outputs/server_runs/qwen3_32b_baseline_formal200_20260812_1505/input/diagnostic/tabfact_compound_trigger71.jsonl
```

Output:

```text
outputs/server_runs/qwen3_32b_baseline_formal200_20260812_1505/diagnostics/tabfact_compound71_patch_ed6ceca/
```

This input contains all 71 Formal-200 TabFact rows that match the new trigger predicate.

| Rows | Old MyAgent correct | Patched MyAgent correct | MACT correct | Old-wrong to new-right | Old-right to new-wrong | Avg token | Avg time | Fail/Missing |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 71 | 50/71 = 0.7042 | 51/71 = 0.7183 | 65/71 = 0.9155 | 8 | 7 | 16961.89 | 33.425s | 0/0 |

Cost comparison on the same 71 rows:

| Metric | Old MyAgent | Patched MyAgent | Delta |
|---|---:|---:|---:|
| Accuracy | 0.7042 | 0.7183 | +0.0141 |
| Avg token | 3427.48 | 16961.89 | +13534.41 |
| Avg time | 17.547s | 33.425s | +15.878s |

Trigger-71 interpretation:

- The trigger gives only a small net gain on the full triggered slice: +1 correct row.
- It recovers 8 previously wrong rows but regresses 7 previously correct rows.
- The token cost is too high for direct Formal-200 expansion unless an acceptance gate reduces wrong overrides.
- Because the rerun can also change the base code candidate, the next required control is the same 71-row run with `--disable-strong-verification`.

## Trigger-71 No-Strong Control

Output:

```text
outputs/server_runs/qwen3_32b_baseline_formal200_20260812_1505/diagnostics/tabfact_compound71_no_strong_control_ed6ceca/
```

| Rows | No-strong correct | Strong-trigger correct | Strong recovers vs no-strong | Strong regresses vs no-strong | No-strong avg token | Strong avg token | No-strong avg time | Strong avg time |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 71 | 51/71 = 0.7183 | 51/71 = 0.7183 | 7 | 7 | 3482.51 | 16961.89 | 18.128s | 33.425s |

Final control interpretation:

- The high-risk TabFact strong-verification trigger has no net accuracy gain over the same 71-row no-strong rerun.
- It adds about `13479` tokens per triggered row and roughly doubles latency.
- The code trigger should not be kept as a production/formal200 optimization.
- The useful evidence is diagnostic: strong verification can recover some rows, but needs a better acceptance gate before it is patent-grade.
