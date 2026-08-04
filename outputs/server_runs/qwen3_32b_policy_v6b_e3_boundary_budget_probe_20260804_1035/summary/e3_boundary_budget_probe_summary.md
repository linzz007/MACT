# E3 Boundary Budget Probe Summary

Generated: `2026-08-04 10:48:28 CST`

## Decision

`mixed_budget_sensitivity_not_enough_for_e3_stability`

This probe reran representative E3 Seed-C/D wrong rows with `max_replan=5`; the original E3 runs used `max_replan=3`.

## Aggregate

| rows | original correct | max_replan=5 correct | recovered | recovery rate | failed | missing | avg original tokens | avg replan5 tokens | avg replan5 seconds |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 12 | 0 | 4 | 4 | 0.3333 | 0 | 0 | 12444.9 | 13136.1 | 45.21 |

## Dataset Summary

| dataset | rows | eval rows | max_replan=5 correct | recovered | failed | missing | avg original tokens | avg replan5 tokens | token ratio vs MACT full200 | avg seconds |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| wtq | 4 | 4 | 1 | 1 | 0 | 0 | 10811.5 | 12501.0 | 1.1897 | 42.90 |
| tabfact | 4 | 4 | 3 | 3 | 0 | 0 | 5709.2 | 4626.8 | 0.4272 | 19.49 |
| crt | 4 | 4 | 0 | 0 | 0 | 0 | 20814.0 | 22280.5 | 1.7393 | 73.25 |

## Category Recovery

| category | recovered | total | rate |
|---|---:|---:|---:|
| crt_multi_step_numeric_composition_boundary | 0 | 2 | 0.0000 |
| crt_span_or_universal_quantifier_boundary | 0 | 2 | 0.0000 |
| tabfact_false_negative_entailment_boundary | 0 | 1 | 0.0000 |
| tabfact_numeric_count_or_comparison_boundary | 1 | 1 | 1.0000 |
| tabfact_temporal_order_boundary | 2 | 2 | 1.0000 |
| wtq_entity_lookup_or_row_selection_boundary | 0 | 2 | 0.0000 |
| wtq_temporal_or_age_lookup_boundary | 1 | 2 | 0.5000 |

## Row-Level Trace

| seed | dataset | id | category | original pred | replan5 pred | gold | recovered | tokens 3->5 |
|---|---|---|---|---|---|---|---|---:|
| seed_c | wtq | nu-1456 | wtq_temporal_or_age_lookup_boundary | 2010.0 | 2010.0 | ["26"] | no | 10583->13733 |
| seed_c | wtq | nu-2577 | wtq_entity_lookup_or_row_selection_boundary | Banyan | Banyan | ["Simul"] | no | 8975->13887 |
| seed_d | wtq | nu-515 | wtq_temporal_or_age_lookup_boundary | September 27, 2008 | December 27, 2008 | ["December 27, 2008"] | yes | 12844->8059 |
| seed_d | wtq | nu-3380 | wtq_entity_lookup_or_row_selection_boundary | {"answer": null} | {"answer": null} | ["Tony Drago"] | no | 10844->14325 |
| seed_c | tabfact | tabfact-test-9637 | tabfact_false_negative_entailment_boundary | false | false | ["true"] | no | 7097->7100 |
| seed_c | tabfact | tabfact-test-8555 | tabfact_temporal_order_boundary | true | false | ["false"] | yes | 2795->2954 |
| seed_d | tabfact | tabfact-test-12194 | tabfact_temporal_order_boundary | true | false | ["false"] | yes | 6657->6257 |
| seed_d | tabfact | tabfact-test-1383 | tabfact_numeric_count_or_comparison_boundary | false | true | ["true"] | yes | 6288->2196 |
| seed_c | crt | crt-325 | crt_multi_step_numeric_composition_boundary | No | No | ["Yes"] | no | 23263->23312 |
| seed_c | crt | crt-0 | crt_span_or_universal_quantifier_boundary | more | more | ["Yes"] | no | 17834->21740 |
| seed_d | crt | crt-121 | crt_multi_step_numeric_composition_boundary | 18.75 | 24.11 | ["18"] | no | 23256->26697 |
| seed_d | crt | crt-303 | crt_span_or_universal_quantifier_boundary | 0.71 | 0.71 | ["0"] | no | 18903->17373 |

## Interpretation

- Recovery below a majority should not be treated as E3 stability closure; it is mechanism evidence for adaptive budgeting plus remaining semantic boundaries.
- Categories with zero recovery should stay on the semantic guard backlog rather than receive more blanket replan budget.
