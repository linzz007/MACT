# E3 Seed-C/D Boundary Error Diagnosis

Generated: `2026-08-03 11:24:36 CST`

Scope: Offline evaluator-based diagnosis of completed Seed-C/Seed-D MyAgent current-only Gate-50 outputs. No model was run.

## Decision

Seed-C and Seed-D remain `stop_or_inspect`. This diagnosis supports not running paired MACT for those seeds yet: there are no execution or missing-answer failures, tokens remain lower than the MACT full200 reference, and the remaining issue is semantic accuracy stability.

## Aggregate

| rows | correct | wrong | accuracy | weighted token ratio vs MACT full200 | failed | missing | verification |
|---:|---:|---:|---:|---:|---:|---:|---|
| 300 | 212 | 88 | 0.7067 | 0.5916 | 0 | 0 | `pass` |

## Coverage Check

| seed | dataset | input/merged/eval | recomputed correct | summary correct | summary wrong | mismatch |
|---|---|---|---|---|---|---|
| seed_c | wtq | 50/50/50 | 40/50 | 40 | 10 | `no` |
| seed_c | tabfact | 50/50/50 | 44/50 | 44 | 6 | `no` |
| seed_c | crt | 50/50/50 | 30/50 | 30 | 20 | `no` |
| seed_d | wtq | 50/50/50 | 30/50 | 30 | 20 | `no` |
| seed_d | tabfact | 50/50/50 | 38/50 | 38 | 12 | `no` |
| seed_d | crt | 50/50/50 | 30/50 | 30 | 20 | `no` |

## Wrong-Row Profile

| seed | dataset | wrong | high-risk ratio | complex-route ratio | deterministic shortcut ratio | strong verifier ratio | wrong avg tokens | right avg tokens |
|---|---|---|---|---|---|---|---|---|
| seed_c | wtq | 10 | 0.70 | 0.00 | 0.00 | 0.70 | 7069.0 | 6130.9 |
| seed_c | tabfact | 6 | 1.00 | 0.00 | 0.17 | 0.00 | 2990.7 | 2796.8 |
| seed_c | crt | 20 | 0.55 | 0.00 | 0.05 | 0.55 | 9617.0 | 13055.2 |
| seed_d | wtq | 20 | 0.95 | 0.00 | 0.10 | 0.95 | 6771.7 | 6568.9 |
| seed_d | tabfact | 12 | 0.83 | 0.00 | 0.00 | 0.00 | 3444.2 | 2734.9 |
| seed_d | crt | 20 | 0.35 | 0.00 | 0.00 | 0.40 | 8645.0 | 10951.0 |

## Heuristic Boundary Categories

| seed | dataset | category | wrong rows |
|---|---|---|---|
| seed_c | wtq | wtq_entity_lookup_or_row_selection_boundary | 5 |
| seed_c | wtq | wtq_numeric_aggregation_or_difference_boundary | 4 |
| seed_c | wtq | wtq_temporal_or_age_lookup_boundary | 1 |
| seed_c | tabfact | tabfact_temporal_order_boundary | 3 |
| seed_c | tabfact | tabfact_false_negative_entailment_boundary | 2 |
| seed_c | tabfact | tabfact_numeric_count_or_comparison_boundary | 1 |
| seed_c | crt | crt_multi_step_numeric_composition_boundary | 8 |
| seed_c | crt | crt_span_or_universal_quantifier_boundary | 6 |
| seed_c | crt | crt_table_reasoning_or_entity_boundary | 3 |
| seed_c | crt | crt_percentage_complement_or_aggregation_boundary | 3 |
| seed_d | wtq | wtq_entity_lookup_or_row_selection_boundary | 6 |
| seed_d | wtq | wtq_rank_direction_or_ordinal_boundary | 5 |
| seed_d | wtq | wtq_numeric_aggregation_or_difference_boundary | 5 |
| seed_d | wtq | wtq_temporal_or_age_lookup_boundary | 4 |
| seed_d | tabfact | tabfact_temporal_order_boundary | 6 |
| seed_d | tabfact | tabfact_false_positive_or_negation_boundary | 3 |
| seed_d | tabfact | tabfact_false_negative_entailment_boundary | 2 |
| seed_d | tabfact | tabfact_numeric_count_or_comparison_boundary | 1 |
| seed_d | crt | crt_multi_step_numeric_composition_boundary | 7 |
| seed_d | crt | crt_table_reasoning_or_entity_boundary | 6 |
| seed_d | crt | crt_percentage_complement_or_aggregation_boundary | 4 |
| seed_d | crt | crt_span_or_universal_quantifier_boundary | 3 |

## Representative Wrong Rows

| seed | dataset | id | category | question/statement | prediction | gold | tokens |
|---|---|---|---|---|---|---|---|
| seed_c | wtq | nu-1456 | wtq_temporal_or_age_lookup_boundary | at which age was the overall as 48 and the giant slalom 48, too? | 2010.0 | 26 | 10583 |
| seed_c | wtq | nu-2577 | wtq_entity_lookup_or_row_selection_boundary | which timber tree has below 451 kg/m3 density? | Banyan | Simul | 8975 |
| seed_c | tabfact | tabfact-test-9637 | tabfact_false_negative_entailment_boundary | telmo and paulo play on the same team as no 6 and no 9 | false | true | 7097 |
| seed_c | tabfact | tabfact-test-8555 | tabfact_temporal_order_boundary | a jacksonville state player be draft several round before a player from florida | true | false | 2795 |
| seed_c | crt | crt-325 | crt_multi_step_numeric_composition_boundary | Was there a significant difference in the level of support for the Progressive Conservatives in p... | No | Yes | 23263 |
| seed_c | crt | crt-0 | crt_span_or_universal_quantifier_boundary | Can we identify any outlier events based on the number of acts or number of stages compared to th... | more | Yes | 17834 |
| seed_d | wtq | nu-515 | wtq_temporal_or_age_lookup_boundary | one what date were the most total goals scored in a game? | September 27, 2008 | December 27, 2008 | 12844 |
| seed_d | wtq | nu-3380 | wtq_entity_lookup_or_row_selection_boundary | which player scored only one point in a tournament? | {"answer": null} | Tony Drago | 10844 |
| seed_d | tabfact | tabfact-test-12194 | tabfact_temporal_order_boundary | the record of 3 - 4 be from week 7 , sun oct 29 , after the game with the new england patriot | true | false | 6657 |
| seed_d | tabfact | tabfact-test-1383 | tabfact_numeric_count_or_comparison_boundary | frank martin be the most recent coach | false | true | 6288 |
| seed_d | crt | crt-121 | crt_multi_step_numeric_composition_boundary | What is the average number of years played by the top 10 players on this list? | 18.75 | 18 | 23256 |
| seed_d | crt | crt-303 | crt_span_or_universal_quantifier_boundary | What is the average difference in score between teams from Division 1 and teams from Division 2 i... | 0.71 | 0 | 18903 |

## Findings

- Seed-C/Seed-D had 300 merged rows and zero failed execution or missing answers; the boundary is semantic answer correctness, not runtime/tool coverage.
- Tokens remained below the frozen MACT full200 reference on every dataset and seed; the blocker is accuracy stability, not token budget.
- Seed-C is near the current gate on TabFact and exactly at the CRT gate, while Seed-D exposes broader WTQ and TabFact instability.
- Do not spend paired MACT runtime for these seeds until boundary categories are addressed or explicitly accepted as limitation evidence.
- Patent-facing claim should use E3 as applicability-boundary evidence, not as multi-seed stable superiority evidence.

## Next Actions

- If continuing Qwen3 optimization, target reusable guards for WTQ rank-direction/temporal lookup, TabFact temporal/numeric entailment, and CRT percentage/aggregation categories.
- If continuing experiment collection, keep E3 paired MACT marked not required and prioritize new-model Gate-10/Gate-50 only when a viable new model or API key exists.
- For patent drafting, cite full200 and P4b after-targeted as positive evidence; cite this E3 diagnosis as boundary and future-improvement evidence.
