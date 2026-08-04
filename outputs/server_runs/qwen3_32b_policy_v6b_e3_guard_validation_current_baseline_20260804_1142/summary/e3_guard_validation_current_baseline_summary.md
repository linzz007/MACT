# E3 Guard Validation Current Baseline Summary

Generated: `2026-08-04 11:52:05 CST`

Decision: `baseline_needs_guard_implementation`

Fresh current-policy baseline on the 30-row E3 S2 guard-validation input package. No MyAgent policy changes are introduced by this artifact.

## Aggregate

| metric | value |
| --- | ---: |
| rows | 30/30 |
| representative recovered | 4/12 |
| no-harm correct | 17/18 |
| failed/missing | 0/0 |
| avg total tokens | 8032.07 |
| weighted token ratio vs MACT full200 | 0.6975 |
| avg elapsed seconds | 23.23 |

## Dataset Results

| dataset | rows | representative recovered | no-harm correct | failed/missing | token ratio | avg tokens | avg seconds |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| wtq | 10/10/10 | 1/4 | 6/6 | 0/0 | 0.7208 | 7573.70 | 20.36 |
| tabfact | 8/8/8 | 3/4 | 4/4 | 0/0 | 0.3489 | 3778.50 | 14.76 |
| crt | 12/12/12 | 0/4 | 7/8 | 0/0 | 0.8782 | 11249.75 | 31.27 |

## Category Results

| category | rows | correct | representative recovered | no-harm retained |
| --- | ---: | ---: | ---: | ---: |
| crt_multi_step_numeric_composition_boundary | 4 | 2 | 0 | 2 |
| crt_percentage_complement_or_aggregation_boundary | 2 | 1 | 0 | 1 |
| crt_span_or_universal_quantifier_boundary | 4 | 2 | 0 | 2 |
| crt_table_reasoning_or_entity_boundary | 2 | 2 | 0 | 2 |
| tabfact_binary_entailment_boundary | 2 | 2 | 0 | 2 |
| tabfact_false_negative_entailment_boundary | 1 | 0 | 0 | 0 |
| tabfact_numeric_count_or_comparison_boundary | 2 | 2 | 1 | 1 |
| tabfact_temporal_order_boundary | 3 | 3 | 2 | 1 |
| wtq_entity_lookup_or_row_selection_boundary | 4 | 2 | 0 | 2 |
| wtq_numeric_aggregation_or_difference_boundary | 2 | 2 | 0 | 2 |
| wtq_temporal_or_age_lookup_boundary | 4 | 3 | 1 | 2 |

## Wrong Or Harm Rows

| source_key | role | category | prediction | gold |
| --- | --- | --- | --- | --- |
| seed_c/wtq/nu-2577 | representative_wrong | wtq_entity_lookup_or_row_selection_boundary | `Banyan` | `['Simul']` |
| seed_d/wtq/nu-3380 | representative_wrong | wtq_entity_lookup_or_row_selection_boundary | `{"answer": null}` | `['Tony Drago']` |
| seed_c/wtq/nu-1456 | representative_wrong | wtq_temporal_or_age_lookup_boundary | `2010.0` | `['26']` |
| seed_c/tabfact/tabfact-test-9637 | representative_wrong | tabfact_false_negative_entailment_boundary | `false` | `['true']` |
| seed_c/crt/crt-325 | representative_wrong | crt_multi_step_numeric_composition_boundary | `No` | `['Yes']` |
| seed_d/crt/crt-121 | representative_wrong | crt_multi_step_numeric_composition_boundary | `24.11` | `['18']` |
| seed_c/crt/crt-0 | representative_wrong | crt_span_or_universal_quantifier_boundary | `more` | `['Yes']` |
| seed_d/crt/crt-303 | representative_wrong | crt_span_or_universal_quantifier_boundary | `0.71` | `['0']` |
| seed_c/crt/crt-107 | no_harm_correct | crt_percentage_complement_or_aggregation_boundary | `tyrrell - renault` | `['renault']` |
