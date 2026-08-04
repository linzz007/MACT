# E3 Guard Validation Input Plan

- Generated: `2026-08-04 11:32:04 CST`
- Decision: `ready_for_guard_implementation_not_model_run`
- Scope: Input/package artifact only. It does not run models or change benchmark results.
- Total rows: `30`

## Dataset Counts

| dataset | rows |
| --- | ---: |
| wtq | 10 |
| tabfact | 8 |
| crt | 12 |

## Role Counts

| role | rows |
| --- | ---: |
| representative_wrong | 12 |
| no_harm_correct | 18 |

## Gate Targets

- Representative wrong recovery minimum: `7/12`.
- No-harm correct minimum: `18/18`.
- Failed/missing maximum: `0`.
- Token ratio to MACT full200 reference maximum: `< 1.0`.

## Row Index

| source_key | role | category | priority | source_correct | max_replan5_recovered | proxy_for |
| --- | --- | --- | --- | ---: | ---: | --- |
| seed_c/wtq/nu-2577 | representative_wrong | wtq_entity_lookup_or_row_selection_boundary | P0 | false | false |  |
| seed_d/wtq/nu-3380 | representative_wrong | wtq_entity_lookup_or_row_selection_boundary | P0 | false | false |  |
| seed_c/wtq/nu-1456 | representative_wrong | wtq_temporal_or_age_lookup_boundary | P1 | false | false |  |
| seed_d/wtq/nu-515 | representative_wrong | wtq_temporal_or_age_lookup_boundary | P1 | false | true |  |
| seed_c/wtq/nu-125 | no_harm_correct | wtq_entity_lookup_or_row_selection_boundary | P0 | true |  |  |
| seed_c/wtq/nu-1715 | no_harm_correct | wtq_entity_lookup_or_row_selection_boundary | P0 | true |  |  |
| seed_c/wtq/nu-1073 | no_harm_correct | wtq_numeric_aggregation_or_difference_boundary | P1 | true |  |  |
| seed_c/wtq/nu-120 | no_harm_correct | wtq_numeric_aggregation_or_difference_boundary | P1 | true |  |  |
| seed_c/wtq/nu-1239 | no_harm_correct | wtq_temporal_or_age_lookup_boundary | P1 | true |  |  |
| seed_c/wtq/nu-2307 | no_harm_correct | wtq_temporal_or_age_lookup_boundary | P1 | true |  |  |
| seed_c/tabfact/tabfact-test-9637 | representative_wrong | tabfact_false_negative_entailment_boundary | P0 | false | false |  |
| seed_d/tabfact/tabfact-test-1383 | representative_wrong | tabfact_numeric_count_or_comparison_boundary | P2 | false | true |  |
| seed_c/tabfact/tabfact-test-8555 | representative_wrong | tabfact_temporal_order_boundary | P2 | false | true |  |
| seed_d/tabfact/tabfact-test-12194 | representative_wrong | tabfact_temporal_order_boundary | P2 | false | true |  |
| seed_c/tabfact/tabfact-test-11195 | no_harm_correct | tabfact_binary_entailment_boundary | P0 | true |  | tabfact_false_negative_entailment_boundary |
| seed_c/tabfact/tabfact-test-12164 | no_harm_correct | tabfact_binary_entailment_boundary | P0 | true |  | tabfact_false_negative_entailment_boundary |
| seed_c/tabfact/tabfact-test-1701 | no_harm_correct | tabfact_numeric_count_or_comparison_boundary | P2 | true |  |  |
| seed_c/tabfact/tabfact-test-1270 | no_harm_correct | tabfact_temporal_order_boundary | P2 | true |  |  |
| seed_c/crt/crt-325 | representative_wrong | crt_multi_step_numeric_composition_boundary | P0 | false | false |  |
| seed_d/crt/crt-121 | representative_wrong | crt_multi_step_numeric_composition_boundary | P0 | false | false |  |
| seed_c/crt/crt-0 | representative_wrong | crt_span_or_universal_quantifier_boundary | P0 | false | false |  |
| seed_d/crt/crt-303 | representative_wrong | crt_span_or_universal_quantifier_boundary | P0 | false | false |  |
| seed_c/crt/crt-208 | no_harm_correct | crt_multi_step_numeric_composition_boundary | P0 | true |  |  |
| seed_c/crt/crt-324 | no_harm_correct | crt_multi_step_numeric_composition_boundary | P0 | true |  |  |
| seed_c/crt/crt-14 | no_harm_correct | crt_span_or_universal_quantifier_boundary | P0 | true |  |  |
| seed_c/crt/crt-184 | no_harm_correct | crt_span_or_universal_quantifier_boundary | P0 | true |  |  |
| seed_c/crt/crt-102 | no_harm_correct | crt_percentage_complement_or_aggregation_boundary | P1 | true |  |  |
| seed_c/crt/crt-107 | no_harm_correct | crt_percentage_complement_or_aggregation_boundary | P1 | true |  |  |
| seed_c/crt/crt-195 | no_harm_correct | crt_table_reasoning_or_entity_boundary | P1 | true |  |  |
| seed_c/crt/crt-352 | no_harm_correct | crt_table_reasoning_or_entity_boundary | P1 | true |  |  |
