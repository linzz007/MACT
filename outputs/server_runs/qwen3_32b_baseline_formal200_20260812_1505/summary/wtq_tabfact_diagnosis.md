# Formal-200 WTQ/TabFact Error Diagnosis

Updated: 2026-08-14 10:39 CST

Scope: compare MyAgent and MACT on the same Formal-200 IDs for WTQ and TabFact. Correctness uses `evaluate_results.dataset_accuracy`, the same primary-accuracy evaluator used by the formal summary.

## Summary

| Dataset | MyAgent correct | MACT correct | Both correct | MyAgent-only | MACT-only | Both wrong | Net gap |
|---|---:|---:|---:|---:|---:|---:|---:|
| WTQ | 141/200 | 156/200 | 125 | 16 | 31 | 28 | 15 |
| TABFACT | 162/200 | 185/200 | 154 | 8 | 31 | 7 | 23 |

## WTQ

Paired gap: MACT-only `31` vs MyAgent-only `16`, net gap `15` rows.

### MACT-only rows

- Risk: high=27, light=2, medium=2
- Route: COMPLEX=29, SIMPLE=2
- Strong verification applied: true=27, false=4
- Deterministic shortcut applied: false=29, true=2
- Top problem tags: count=14, temporal=13, negation_logic=10, superlative_order=6, arithmetic=6, comparison=1
- Compression: expanded_context_block_global_rows=12, expanded_context_block=10, strict_cell_block_global_rows=5, strict_cell_block=3, full_table_for_high_coverage=1

### MyAgent-only rows

- Risk: high=15, medium=1
- Route: COMPLEX=15, SIMPLE=1
- Strong verification applied: true=15, false=1
- Deterministic shortcut applied: false=16
- Top problem tags: count=7, superlative_order=6, negation_logic=5, temporal=4, arithmetic=3, trend_correlation=1, comparison=1
- Compression: expanded_context_block_global_rows=6, expanded_context_block=5, strict_cell_block_global_rows=2, full_table_for_high_coverage=1, expanded_context_block_global_columns=1, strict_cell_block=1

### Both-wrong rows

- Risk: high=22, medium=3, light=2, fallback=1
- Route: COMPLEX=26, SIMPLE=2
- Strong verification applied: true=23, false=5
- Deterministic shortcut applied: false=26, true=2
- Top problem tags: count=11, superlative_order=9, arithmetic=7, negation_logic=5, temporal=3, comparison=1
- Compression: expanded_context_block_global_rows=10, expanded_context_block=9, strict_cell_block_global_rows=5, expanded_context_block_global_rows_global_columns=2, strict_cell_block=2

Representative MACT-only examples are stored in the JSON report under `mact_only_examples`.

## TABFACT

Paired gap: MACT-only `31` vs MyAgent-only `8`, net gap `23` rows.

### MACT-only rows

- Risk: high=29, medium=2
- Route: COMPLEX=31
- Strong verification applied: false=31
- Deterministic shortcut applied: false=31
- Top problem tags: closed_choice=31, temporal=16, negation_logic=14, superlative_order=12, comparison=5, arithmetic=3, count=1
- Compression: expanded_context_block_global_rows=24, expanded_context_block_global_rows_global_columns=6, strict_cell_block_global_rows=1

### MyAgent-only rows

- Risk: high=4, medium=4
- Route: COMPLEX=8
- Strong verification applied: false=8
- Deterministic shortcut applied: false=7, true=1
- Top problem tags: closed_choice=8, superlative_order=2, negation_logic=2, temporal=2
- Compression: expanded_context_block_global_rows=8

### Both-wrong rows

- Risk: high=6, medium=1
- Route: COMPLEX=6, SIMPLE=1
- Strong verification applied: false=7
- Deterministic shortcut applied: false=7
- Top problem tags: closed_choice=7, negation_logic=5, comparison=3, superlative_order=2, temporal=2, count=1
- Compression: expanded_context_block_global_rows=4, expanded_context_block_global_rows_global_columns=2, strict_cell_block_global_rows=1

Representative MACT-only examples are stored in the JSON report under `mact_only_examples`.

## Diagnostic Conclusion

- WTQ gap is broad rather than a missing-answer/failure problem: MyAgent has zero failures, but loses 31 MACT-only rows while gaining 16 MyAgent-only rows. The error set should be inspected for entity canonicalization, tied answers, and evidence-column selection because many rows are high-risk and complex.
- TabFact gap is more severe: MACT-only rows outnumber MyAgent-only rows 31 to 8. The likely next optimization target is selective verification for high-risk binary claims, especially compound/closed-choice statements where deterministic shortcuts helped in the ablation but strong verification did not activate often enough on Gate-50.
- The current formal200 package still supports the efficiency claim, but not the overall-accuracy-over-MACT claim. The next experiment should be a focused WTQ/TabFact patch, validated first on MACT-only diagnostic rows before any new full200 run.
