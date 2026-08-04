# E3 Semantic Boundary Repair Plan

Generated: `2026-08-04 11:12:23 CST`

## Scope

Planning artifact only. It uses completed E3 Seed-C/D diagnosis and max_replan=5 probe; it does not run models or change benchmark results.

Current decision: `do_not_rerun_full200_or_paired_mact_until_targeted_guards_pass`.

## Evidence Snapshot

| item | value |
|---|---:|
| E3 rows | 300 |
| E3 correct/wrong | 212/88 |
| E3 weighted token ratio | 0.5916 |
| E3 failed/missing | 0/0 |
| budget probe rows | 12 |
| budget probe recovered | 4 |

Budget probe decision: `mixed_budget_sensitivity_not_enough_for_e3_stability`.

Zero-recovery probe categories:

- `crt_multi_step_numeric_composition_boundary`
- `wtq_entity_lookup_or_row_selection_boundary`
- `crt_span_or_universal_quantifier_boundary`
- `tabfact_false_negative_entailment_boundary`

Budget-sensitive categories:

- `wtq_temporal_or_age_lookup_boundary`
- `tabfact_temporal_order_boundary`
- `tabfact_numeric_count_or_comparison_boundary`

## Seed Gate Gap

| seed | dataset | current | threshold | needed | pass |
|---|---|---:|---:|---:|---|
| seed_c | wtq | 40/50 | 35/50 | 0 | `True` |
| seed_c | tabfact | 44/50 | 45/50 | 1 | `False` |
| seed_c | crt | 30/50 | 30/50 | 0 | `True` |
| seed_d | wtq | 30/50 | 35/50 | 5 | `False` |
| seed_d | tabfact | 38/50 | 45/50 | 7 | `False` |
| seed_d | crt | 30/50 | 30/50 | 0 | `True` |

## Category Plan

| priority | dataset | category | E3 wrong | probe recovered/rows | track | claim families |
|---|---|---|---:|---:|---|---|
| P0 | crt | `crt_multi_step_numeric_composition_boundary` | 15 | 0/2 | `semantic_guard_required_after_budget_failed` | C3, C5 |
| P0 | wtq | `wtq_entity_lookup_or_row_selection_boundary` | 11 | 0/2 | `semantic_guard_required_after_budget_failed` | C1, C2, C4, C5 |
| P0 | crt | `crt_span_or_universal_quantifier_boundary` | 9 | 0/2 | `semantic_guard_required_after_budget_failed` | C3, C5 |
| P0 | tabfact | `tabfact_false_negative_entailment_boundary` | 4 | 0/1 | `semantic_guard_required_after_budget_failed` | C3, C5 |
| P1 | crt | `crt_table_reasoning_or_entity_boundary` | 9 | n/a | `unprobed_semantic_guard_candidate` | C2, C3, C5 |
| P1 | wtq | `wtq_numeric_aggregation_or_difference_boundary` | 9 | n/a | `unprobed_semantic_guard_candidate` | C3, C5 |
| P1 | crt | `crt_percentage_complement_or_aggregation_boundary` | 7 | n/a | `unprobed_semantic_guard_candidate` | C3, C5 |
| P1 | wtq | `wtq_temporal_or_age_lookup_boundary` | 5 | 1/2 | `mixed_budget_and_semantic_guard` | C1, C4, C5, C6 |
| P2 | tabfact | `tabfact_temporal_order_boundary` | 9 | 2/2 | `adaptive_budget_candidate` | C3, C4, C6 |
| P2 | wtq | `wtq_rank_direction_or_ordinal_boundary` | 5 | n/a | `unprobed_followup` | C3, C5 |
| P2 | tabfact | `tabfact_false_positive_or_negation_boundary` | 3 | n/a | `unprobed_followup` | C3, C5 |
| P2 | tabfact | `tabfact_numeric_count_or_comparison_boundary` | 2 | 1/1 | `adaptive_budget_candidate` | C3, C4, C6 |

## High Priority Work Items

### P0 `crt_multi_step_numeric_composition_boundary`

- E3 wrong rows: `15`; budget probe: `0/2`.
- Mechanism: CRT multi-step numeric composition guard that validates intermediate quantities, units, averages, and yes/no answer form.
- Code hook: CRT numeric program audit and answer-shape validator before final response selection.
- Validation gate: Recover at least one of two probe rows while keeping CRT current seed gate at >=30/50 and token ratio <1.0.
- Probe IDs: seed_c/crt/crt-325, seed_d/crt/crt-121
- Patent note: Zero recovery and high token cost under extra budget; do not blanket-increase max_replan for CRT.

### P0 `wtq_entity_lookup_or_row_selection_boundary`

- E3 wrong rows: `11`; budget probe: `0/2`.
- Mechanism: Entity lookup / row-selection guard that validates the selected row against numeric predicates and returns null only after evidence exhaustion.
- Code hook: Table compression row recall, simple lookup fallback, and final answer contract.
- Validation gate: Recover at least one probe row and preserve no-harm rows where entity lookup already agrees with gold-free verifier evidence.
- Probe IDs: seed_c/wtq/nu-2577, seed_d/wtq/nu-3380
- Patent note: Zero recovery under extra budget; treat as semantic guard backlog rather than a replan-budget problem.

### P0 `crt_span_or_universal_quantifier_boundary`

- E3 wrong rows: `9`; budget probe: `0/2`.
- Mechanism: Span / universal-quantifier guard that enforces yes/no or scalar answer contracts instead of comparative-span leakage.
- Code hook: CRT answer-contract enforcement and quantifier parser.
- Validation gate: Recover answer-shape failures such as comparative words returned for yes/no questions; no missing-answer regressions.
- Probe IDs: seed_c/crt/crt-0, seed_d/crt/crt-303
- Patent note: Zero recovery under budget probe; evidence points to answer-contract semantics, not runtime budget.

### P0 `tabfact_false_negative_entailment_boundary`

- E3 wrong rows: `4`; budget probe: `0/1`.
- Mechanism: Multi-entity equality / same-team entailment audit to prevent false negatives when multiple entities share a table relation.
- Code hook: TabFact entity-attribute and same-row/multi-entity deterministic audit.
- Validation gate: Recover the same-team representative row without flipping existing false-positive/negation rows.
- Probe IDs: seed_c/tabfact/tabfact-test-9637
- Patent note: Zero recovery under extra budget; requires semantic entailment audit rather than more replan attempts.

### P1 `crt_table_reasoning_or_entity_boundary`

- E3 wrong rows: `9`; budget probe: `0/0`.
- Mechanism: CRT table entity grounding guard for matching row groups before doing numeric or logical composition.
- Code hook: CRT row/column grounding and evidence-retention audit.
- Validation gate: Run affected-slice plus no-harm rows where entity grounding is already correct.
- Probe IDs: no representative probe row
- Patent note: High-volume unprobed category; prioritize after the two zero-recovery CRT probe categories.

### P1 `wtq_numeric_aggregation_or_difference_boundary`

- E3 wrong rows: `9`; budget probe: `0/0`.
- Mechanism: Numeric aggregation/difference contract that checks count, sum, difference, and comparison operators against parsed table columns.
- Code hook: WTQ deterministic numeric audit before accepting high-risk denotation.
- Validation gate: Use a gold-free affected slice from Seed-C/D wrong rows plus held-out correct aggregation rows; no answer-format regressions.
- Probe IDs: no representative probe row
- Patent note: High-volume unprobed category; should be evaluated before spending paired MACT runtime.

### P1 `crt_percentage_complement_or_aggregation_boundary`

- E3 wrong rows: `7`; budget probe: `0/0`.
- Mechanism: Percentage complement and aggregation guard for percent-to-count, complement, and weighted-average questions.
- Code hook: CRT percentage parser and numeric-composition validator.
- Validation gate: No harm on CRT rows already answered through deterministic shortcuts; failed/missing must stay 0.
- Probe IDs: no representative probe row
- Patent note: High-volume unprobed CRT category; belongs in semantic numeric guard work.

### P1 `wtq_temporal_or_age_lookup_boundary`

- E3 wrong rows: `5`; budget probe: `1/2`.
- Mechanism: WTQ temporal/age lookup contract plus selective max_replan=5 when the answer column is temporal or age-like.
- Code hook: WTQ high-risk denotation verifier and answer-contract layer.
- Validation gate: Recover remaining temporal representative rows without changing already-correct direct lookup rows; failed/missing must stay 0.
- Probe IDs: seed_c/wtq/nu-1456, seed_d/wtq/nu-515
- Patent note: Useful as adaptive-budget evidence, but partial recovery means it still needs a semantic answer-shape guard.

## Next Experiment Ladder

| stage | action | entry condition | exit gate |
|---|---|---|---|
| `S1_design_and_unit` | Implement or specify gold-free semantic guards for P0 categories first; keep adaptive max_replan restricted to budget-sensitive categories. | No sample ID or gold-answer logic; existing full200/P4b artifacts remain frozen. | Code/unit/offline checks pass and guard trigger evidence is logged per row. |
| `S2_affected_slice_fresh` | Run a small affected slice using current Qwen endpoints: all 12 budget-probe representative rows plus no-harm rows from each touched category. | S1 passes and services 8000/8001 are healthy. | Recover >=3 of the 7 zero-recovery probe rows, keep the 4 already-recovered budget rows correct, failed/missing 0/0, and avoid blanket CRT replan token growth. |
| `S3_e3_current_only_rerun` | Only after S2 passes, rerun E3 Seed-C/D current-only Gate-50 rather than paired MACT. | Affected-slice gate passes with no-harm evidence. | For every seed/dataset: rows 50/50/50, failed/missing 0/0, token ratio <1.0, WTQ >=35/50, TabFact >=45/50, CRT >=30/50. |
| `S4_paired_mact_or_boundary_closeout` | Run paired MACT only if both Seed-C and Seed-D pass current-only gates; otherwise update the patent package as an explicit applicability boundary. | S3 decision becomes run_paired_mact for both seeds. | Paired MACT summary is generated and committed, or the boundary is explicitly accepted in the patent package. |

## Patent Writing Boundary

Can write:

- Adaptive replan budget helps selected TabFact temporal/numeric and one WTQ temporal representative row.
- E3 remaining failures are semantic-boundary failures with failed/missing 0/0 and token still below MACT full200 reference overall.
- Future optimization should be framed as semantic audit and answer-contract expansion, not as benchmark reruns.

Cannot write:

- Blanket max_replan=5 closes E3 stability.
- CRT representative errors are budget-sensitive.
- Multi-seed stable superiority is complete.
- Multi-model validation is complete.
