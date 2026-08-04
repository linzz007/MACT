# Seed-D WTQ/TabFact After-Guard Boundary Diagnosis

Generated: `2026-08-04 15:33:53 CST`

Scope: Offline same-ID comparison of Seed-D WTQ/TabFact original E3 current-only outputs and S3 after-guard outputs. No model was run.

## Decision

`diagnose_then_build_small_fresh_repair_slice`: Seed-D WTQ/TabFact still cannot trigger paired MACT. Use the generated affected-slice inputs for the next bounded repair probe.

## Aggregate

| rows | old correct | after-guard correct | delta | threshold | deficit | recovered | regressed |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 100 | 68 | 67 | -1 | 80 | 13 | 4 | 5 |

## Dataset Summary

| dataset | input/merged/eval | old correct | after-guard correct | delta | threshold | deficit | token ratio | failed/missing |
|---|---|---|---|---|---|---|---|---|
| wtq | 50/50/50 | 30 | 28 | -2 | 35 | 7 | 0.6417 | 0/0 |
| tabfact | 50/50/50 | 38 | 39 | 1 | 45 | 6 | 0.2613 | 0/0 |

## Same-ID Transitions

| dataset | stable right | recovered | regressed | stable wrong |
|---|---|---|---|---|
| wtq | 27 | 1 | 3 | 19 |
| tabfact | 36 | 3 | 2 | 9 |

## Wrong Boundary Categories

| dataset | category | wrong rows |
|---|---|---|
| wtq | wtq_numeric_aggregation_or_difference_boundary | 7 |
| wtq | wtq_rank_direction_or_ordinal_boundary | 5 |
| wtq | wtq_entity_lookup_or_row_selection_boundary | 5 |
| wtq | wtq_temporal_or_age_lookup_boundary | 4 |
| wtq | wtq_rank_signed_difference_direction_boundary | 1 |
| tabfact | tabfact_temporal_order_boundary | 5 |
| tabfact | tabfact_false_positive_or_negation_boundary | 3 |
| tabfact | tabfact_false_negative_entailment_boundary | 2 |
| tabfact | tabfact_numeric_or_same_row_relation_boundary | 1 |

## Priority Probe Rows

| dataset | id | status | category | question/statement | prediction | gold | tokens |
|---|---|---|---|---|---|---|---|
| wtq | nu-298 | regressed | wtq_temporal_or_age_lookup_boundary | where does the bus stop after kingston centre on route 11? | Bath Road Gardiners Town Centre | Cataraqui Town Centre | 8954 |
| wtq | nu-2972 | regressed | wtq_rank_direction_or_ordinal_boundary | how long did derek fisher's career last? | 2006-2007 | 1 year | 8076 |
| wtq | nu-1566 | regressed | wtq_numeric_aggregation_or_difference_boundary | how many consecutive seasons premiered in october? | 3 | 4 | 5582 |
| wtq | nu-898 | stable_wrong | wtq_entity_lookup_or_row_selection_boundary | which episode has the same episode and production numbers? | 5a | Danger In The Depths | 13205 |
| wtq | nu-3380 | stable_wrong | wtq_numeric_aggregation_or_difference_boundary | which player scored only one point in a tournament? | {"answer": null} | Tony Drago | 10827 |
| wtq | nu-4301 | stable_wrong | wtq_temporal_or_age_lookup_boundary | how long did they play before they won a game? | No win recorded | 2 games | 9676 |
| wtq | nu-1899 | stable_wrong | wtq_numeric_aggregation_or_difference_boundary | total number of entries from "leroy and stitch" episode. | 87 | 89 | 9554 |
| wtq | nu-3430 | stable_wrong | wtq_numeric_aggregation_or_difference_boundary | how many candidates are over 1.8 meters tall? | 20 | 21 | 9183 |
| tabfact | tabfact-test-1327 | regressed | tabfact_numeric_or_same_row_relation_boundary | jack fleck score less point that harvie ward in the 1955 u.s. open (golf) us open | true | false | 2623 |
| tabfact | tabfact-test-11960 | regressed | tabfact_temporal_order_boundary | the total number of point in the year with 7 assist be 39 | false | true | 2537 |
| tabfact | tabfact-test-2265 | stable_wrong | tabfact_false_positive_or_negation_boundary | in 2011 the earnings be 365231 | true | false | 5748 |
| tabfact | tabfact-test-9698 | stable_wrong | tabfact_false_positive_or_negation_boundary | adelaide united play in front of 10256 crowd in hindmarsh stadium on november 18 | true | false | 3737 |
| tabfact | tabfact-test-6363 | stable_wrong | tabfact_temporal_order_boundary | during the 1982 denver broncos season , week 1 , 2 and 10 be play with the lowest attendance at t... | true | false | 3557 |
| tabfact | tabfact-test-1868 | stable_wrong | tabfact_false_negative_entailment_boundary | 3 match be replay in january 1976 | false | true | 3275 |
| tabfact | tabfact-test-3904 | stable_wrong | tabfact_temporal_order_boundary | they be in the fiba europe cup champion europ[ean competition before 2005 | true | false | 3044 |
| tabfact | tabfact-test-5513 | stable_wrong | tabfact_temporal_order_boundary | in 2003 , the 2003 washington redskins season play 9 home game | false | true | 2992 |

## Generated Repair Inputs

- wtq wrong/regressed: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_e3_s3_current_rerun_after_guard_20260804_1425/input/seed_d_wtq_tabfact_boundary_repair/wtq_seed_d_after_guard_wrong.jsonl`
- wtq no-harm correct: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_e3_s3_current_rerun_after_guard_20260804_1425/input/seed_d_wtq_tabfact_boundary_repair/wtq_seed_d_after_guard_no_harm_correct.jsonl`
- wtq priority probe: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_e3_s3_current_rerun_after_guard_20260804_1425/input/seed_d_wtq_tabfact_boundary_repair/wtq_seed_d_after_guard_priority_probe.jsonl`
- tabfact wrong/regressed: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_e3_s3_current_rerun_after_guard_20260804_1425/input/seed_d_wtq_tabfact_boundary_repair/tabfact_seed_d_after_guard_wrong.jsonl`
- tabfact no-harm correct: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_e3_s3_current_rerun_after_guard_20260804_1425/input/seed_d_wtq_tabfact_boundary_repair/tabfact_seed_d_after_guard_no_harm_correct.jsonl`
- tabfact priority probe: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_e3_s3_current_rerun_after_guard_20260804_1425/input/seed_d_wtq_tabfact_boundary_repair/tabfact_seed_d_after_guard_priority_probe.jsonl`

## Interpretation

- After-guard S3 did not fail because of missing answers or runner errors; both WTQ and TabFact have 50/50 rows with zero failures.
- The Seed-D blocker is not uniform: WTQ regressed by two correct rows versus the old current-only run, while TabFact gained one correct row but remains below its gate.
- A direct paired MACT run is still not justified for Seed-D; the next evidence step should be a bounded affected-slice/no-harm fresh probe using the generated repair inputs.
- The generated repair inputs include audit metadata, but model runners must consume only the original task fields; metadata is for traceability and must not be used as a prompt feature.

## Next Actions

- Inspect the top WTQ rank/temporal/entity rows and TabFact temporal/entity relation rows for reusable, gold-free guards.
- Implement only mechanisms that can be described as selective-risk collaboration or deterministic semantic verification, not ID-specific fixes.
- Run the priority probe first; only if it recovers enough boundary rows without no-harm regressions should Seed-D WTQ/TabFact full50 be rerun.
