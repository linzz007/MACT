# Seed-D WTQ/TabFact Boundary Shortcut Projection

Generated: `2026-08-04 15:48:51 CST`

Scope: Offline no-model projection of current deterministic shortcuts on completed Seed-D S3 WTQ/TabFact rows.

## Decision

`run_seed_d_wtq_tabfact_fresh_rerun`

## Aggregate

| rows | old correct | projected correct | delta | threshold | recovered | harmed | projected gate |
|---:|---:|---:|---:|---:|---:|---:|---|
| 100 | 67 | 81 | 14 | 80 | 14 | 0 | `True` |

## Dataset Projection

| dataset | rows | old | projected | delta | threshold | triggered | recovered | harmed | gate |
|---|---|---|---|---|---|---|---|---|---|
| wtq | 50 | 28 | 36 | 8 | 35 | 11 | 8 | 0 | `True` |
| tabfact | 50 | 39 | 45 | 6 | 45 | 11 | 6 | 0 | `True` |

## Projected Changed/Wrong Trigger Rows

| dataset | id | old ok | projected ok | reason | projected | gold |
|---|---|---|---|---|---|---|
| wtq | nu-3512 | False | True | WTQ rank gap computed as an absolute position difference. | 2 | ['2'] |
| wtq | nu-4157 | False | False | WTQ last requested table-column value selected deterministically. | 1979-80 | ['8'] |
| wtq | nu-762 | False | True | WTQ explicit metric-value entity list returned deterministically. | ['Keflavík', 'Leiftur'] | ['Keflavík', 'Leiftur'] |
| wtq | nu-240 | False | False | WTQ last requested table-column value selected deterministically. | Train Station Bus Terminal | ['Bus Terminal'] |
| wtq | nu-1283 | False | True | WTQ column-header number selected from the column containing the requested year. | 118 | ['118'] |
| wtq | nu-3127 | False | True | WTQ blank rank prefixes inferred from row order. | Erben Wennemars | ['Erben Wennemars'] |
| wtq | nu-1566 | False | True | WTQ consecutive month run counted deterministically. | 4 | ['4'] |
| wtq | nu-2972 | False | True | WTQ named year-span duration computed deterministically. | 1 year | ['1 year'] |
| wtq | nu-1816 | False | True | WTQ absent explicit option selected from table coverage. | canada | ['Canada'] |
| wtq | nu-2188 | False | True | WTQ threshold-qualified rows counted deterministically. | 1 | ['1'] |
| tabfact | tabfact-test-10076 | False | True | TabFact aircraft and call-sign identity checked with strict same-row matching. | false | ['false'] |
| tabfact | tabfact-test-6363 | False | True | TabFact lowest-attendance week set checked deterministically. | false | ['false'] |
| tabfact | tabfact-test-1327 | False | True | TabFact entity score-sum comparison checked deterministically. | false | ['false'] |
| tabfact | tabfact-test-1868 | False | True | TabFact replay count in requested month checked deterministically. | true | ['true'] |
| tabfact | tabfact-test-11960 | False | True | TabFact same-row metric value under a condition checked deterministically. | true | ['true'] |
| tabfact | tabfact-test-4106 | False | False | TabFact replay home-team win relation checked deterministically. | false | ['true'] |
| tabfact | tabfact-test-140 | False | True | TabFact entity tenure containment checked deterministically. | true | ['true'] |

## Interpretation

- This projection uses gold labels only after deterministic answers are computed, for evaluator recomputation; gold is not part of any shortcut input.
- The result is not a fresh model run and must not be cited as final Seed-D accuracy.
- Because both WTQ and TabFact pass projected gates with zero projected harm, the next step is a bounded fresh rerun on the same Seed-D WTQ/TabFact full50 inputs.
