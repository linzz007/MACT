# E3 Guard Validation After-Guard Summary

Generated: `2026-08-04 12:17:47 CST`

Decision: `after_guard_passes_s2_gate`

Fresh after-guard run on the 30-row E3 S2 guard-validation input package. This run evaluates gold-free semantic guards for WTQ multi-condition lookup, TabFact numbered same-team relation, CRT numeric outlier detection, CRT top-k years-played averages, and CRT constructor retirement-reason percentage.

## Aggregate

| metric | value |
| --- | ---: |
| rows | 30/30 |
| representative recovered | 8/12 |
| no-harm correct | 18/18 |
| failed/missing | 0/0 |
| avg total tokens | 7028.87 |
| weighted token ratio vs MACT full200 | 0.6104 |
| avg elapsed seconds | 16.14 |

## Dataset Results

| dataset | rows | representative recovered | no-harm correct | failed/missing | token ratio | avg tokens | avg seconds |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| wtq | 10/10/10 | 2/4 | 6/6 | 0/0 | 0.6832 | 7179.00 | 18.88 |
| tabfact | 8/8/8 | 4/4 | 4/4 | 0/0 | 0.2720 | 2946.50 | 12.42 |
| crt | 12/12/12 | 2/4 | 8/8 | 0/0 | 0.7514 | 9625.33 | 16.34 |

## Category Results

| category | rows | correct | representative recovered | no-harm retained |
| --- | ---: | ---: | ---: | ---: |
| crt_multi_step_numeric_composition_boundary | 4 | 3 | 1 | 2 |
| crt_percentage_complement_or_aggregation_boundary | 2 | 2 | 0 | 2 |
| crt_span_or_universal_quantifier_boundary | 4 | 3 | 1 | 2 |
| crt_table_reasoning_or_entity_boundary | 2 | 2 | 0 | 2 |
| tabfact_binary_entailment_boundary | 2 | 2 | 0 | 2 |
| tabfact_false_negative_entailment_boundary | 1 | 1 | 1 | 0 |
| tabfact_numeric_count_or_comparison_boundary | 2 | 2 | 1 | 1 |
| tabfact_temporal_order_boundary | 3 | 3 | 2 | 1 |
| wtq_entity_lookup_or_row_selection_boundary | 4 | 2 | 0 | 2 |
| wtq_numeric_aggregation_or_difference_boundary | 2 | 2 | 0 | 2 |
| wtq_temporal_or_age_lookup_boundary | 4 | 4 | 2 | 2 |

## Wrong Or Harm Rows

| source_key | role | category | prediction | gold |
| --- | --- | --- | --- | --- |
| seed_c/wtq/nu-2577 | representative_wrong | wtq_entity_lookup_or_row_selection_boundary | `Banyan` | `['Simul']` |
| seed_d/wtq/nu-3380 | representative_wrong | wtq_entity_lookup_or_row_selection_boundary | `{"answer": null}` | `['Tony Drago']` |
| seed_c/crt/crt-325 | representative_wrong | crt_multi_step_numeric_composition_boundary | `No` | `['Yes']` |
| seed_d/crt/crt-303 | representative_wrong | crt_span_or_universal_quantifier_boundary | `0.71` | `['0']` |
