# P4b WTQ Discordant Diagnosis

Run dir: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305`

This report diagnoses the WTQ new-seed Gate-50 paired comparison where MyAgent scored `37/50` and MACT scored `43/50`.
It is generated from frozen P4b artifacts without starting a model.

## Method

- MyAgent rows: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/myagent_current/merged/wtq_qwen3-32b-local.jsonl`
- MACT rows: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/mact/wtq_mact_newseed_gate50.jsonl`
- Evaluation module: `/home/ubuntu/lzz/MyAgent/code/evaluate_results.py`
- Correctness: recomputed with the same WTQ denotation metric used by `evaluate_results.py`.

## Pair Confusion

| bucket | count |
|---|---:|
| both_correct | 34 |
| myagent_only | 3 |
| mact_only | 9 |
| both_wrong | 4 |

## Root-Cause Buckets

| category | count |
|---|---:|
| answer_target_column | 1 |
| both_wrong_location_alias | 1 |
| both_wrong_multi_answer_contract | 1 |
| both_wrong_numeric_range_parsing | 1 |
| both_wrong_same_row_next_field | 1 |
| conflict_gate_and_cell_semantics | 1 |
| count_semantics | 2 |
| domain_marker_parsing | 1 |
| entity_surface_contract | 2 |
| listed_after_shortcut_targeting | 1 |
| myagent_strength_answer_contract | 1 |
| myagent_strength_semantic_disambiguation | 1 |
| myagent_strength_temporal_neighbor | 1 |
| ordinal_phrase_matching | 1 |

## Diagnosis

WTQ P4b loss is mainly semantic/answer-contract risk, not execution failure. All 9 MACT-only rows used high-risk MyAgent routing with strong verification, but several wrong answers came from target-column selection, surface normalization, count semantics, or conflict-gate rejection of a better candidate.

For the 9 MACT-only rows, average MyAgent compression ratio was `0.6364` and `2/9` rows used effectively full-row context. This means the main WTQ gap is not a simple case of missing table rows.

The most actionable MACT-only causes are answer target/surface contract errors, deterministic row-neighbor shortcut targeting, explicit marker parsing, count semantics, and conflict-gate behavior when a verifier candidate is better than the code candidate.

## Discordant Rows

| group | id | category | question | gold | MyAgent | MACT | cause | next action |
|---|---|---|---|---|---|---|---|---|
| mact_only | nu-1108 | entity_surface_contract | who came first john f. williams or william a. mann? | ['William A. Mann'] | MG William A. Mann | William A. Mann | MyAgent selected the right person but returned the table cell with military title prefix `MG`; WTQ gold expects the mentioned person surface `William A. Mann`. | Add requested-entity surface canonicalization for rank/title prefixes when the question names the candidate entity without the prefix. |
| mact_only | nu-1478 | domain_marker_parsing | what is the number of times a game went into overtime between the eagles and giants? | ['2'] | 0 | 2 | MyAgent treated overtime as tied final scores and returned 0. The table explicitly marks overtime with `(OT)` in the Result column. | Add a generic sports-score marker audit for overtime/extra-time tokens such as `(OT)` before score-equality heuristics. |
| mact_only | nu-1825 | listed_after_shortcut_targeting | what is the next stadium listed after parc des princes? | ['Stade Félix Bollaert'] | 48712.0 | Stade Félix Bollaert | The row-major listed-after shortcut returned the current row Capacity value `48712` instead of the next row Stadium value. | Fix listed-after shortcut column targeting: when the question asks for a column/entity after a named item, return the same requested column from the next row. |
| mact_only | nu-2825 | count_semantics | what is the number of winners in the community division? | ['8'] | 7 | 8 | Question asks the number of winners in a division. MyAgent interpreted this as distinct/non-empty winners and returned 7, while gold counts the 8 non-empty Community Division en... | Add a count-intent audit that separates row/cell occurrence count from distinct-value count for `number of winners in <column>` questions. |
| mact_only | nu-3317 | count_semantics | total number of sponsors? | ['13'] | 21 | 13. | MyAgent summed filled cells across sponsor columns and returned 21. Gold expects the main sponsor occurrence count used by WTQ for this table, 13. | Add sponsor-count disambiguation: for open `total number of sponsors` questions prefer the primary sponsor column/row occurrence unless the question names multiple sponsor columns. |
| mact_only | nu-3320 | ordinal_phrase_matching | which person retired injured after three attempts in their event? | ['Yossef Romano'] | Esther Shahamorov | Yossef Romano | MyAgent looked for literal `3 attempts` and missed `third attempt`; it then chose a different athlete. | Normalize ordinal phrases (`third attempt`, `3rd attempt`, `three attempts`) in WTQ event/performance matching. |
| mact_only | nu-3537 | conflict_gate_and_cell_semantics | how many years did the true american club make the playoff? | ['1'] | 2 | 1 | Code counted `Champion (no playoff)` as a playoff row. The thinking verifier found the correct count, but the conflict gate did not let that candidate take over. | Add a generic WTQ playoff/no-playoff cell audit and allow high-confidence verifier override when a parenthetical negator contradicts the code path. |
| mact_only | nu-3905 | entity_surface_contract | who is the last person listed under slalom? | ['Ludwig Wolf'] | Ludwig Wolf Germany (GER) | Ludwig Wolf | MyAgent identified the correct row but returned `Ludwig Wolf Germany (GER)` instead of the requested person name only. | Add medal/person column answer cleanup that strips adjacent country suffixes when the question asks `who/person` rather than full medal cell text. |
| mact_only | nu-3990 | answer_target_column | which experiment number came directly before felix? | ['009'] | Pop | 009 | MyAgent found the previous row before Felix but returned the previous row nickname `Pop`; the question asks for the experiment number, `009`. | Strengthen answer-contract target-column detection for `which <column> number` questions before accepting row-neighbor shortcuts. |
| myagent_only | nu-2441 | myagent_strength_answer_contract | was there only one time when their wins and losses are the same? | ['no'] | No | No, there were two instances (2009 and 2010) when wins and losses were the same. | MyAgent returned the compact WTQ denotation `No`; MACT returned a full explanatory sentence that is semantically right but fails strict WTQ denotation matching. | Use this as patent evidence for answer-shape checking and concise denotation enforcement. |
| myagent_only | nu-3246 | myagent_strength_temporal_neighbor | what building was designed after hvittrask studio and home? | ['Swedish Theatre'] | Swedish Theatre | Kleinhans Music Hall | MyAgent selected the immediately next designed building after Hvittrask Studio and Home; MACT selected a later building. | Use this as evidence for row-neighbor temporal evidence retention under compressed routing. |
| myagent_only | nu-4296 | myagent_strength_semantic_disambiguation | what was the date of the first vessel that was acquired? | ['2001'] | 2001 | 1998 | MyAgent used Notes semantics to distinguish acquired/ordered vessels and returned 2001; MACT took the minimum Date value, 1998, from a row that is not an acquisition answer unde... | Preserve this behavior as evidence that verifier/thinking fallback can correct naive min-date execution. |
| both_wrong | nu-1104 | both_wrong_location_alias | how many robots are from the united states? | ['2'] | 1 | 3 | Both systems disagreed with gold on United States location matching; table contains United States plus city/state aliases such as Michigan and New Jersey. | Treat country aliases and US state/city cells explicitly before country-count audits. |
| both_wrong | nu-1775 | both_wrong_multi_answer_contract | which competitions did she compete in before the 2001 world championships? | ['World Youth Championships', 'World Junior Championships', 'European Junior Championships'] | ['World Youth Championships', 'World Junior Championships'] | World Youth Championships, World Junior Championships, European Junior Championships | MyAgent omitted one competition and MACT emitted a comma-delimited sentence rather than a structured WTQ answer list. | Strengthen list-answer arity enforcement and pre-event filtering for multi-answer temporal questions. |
| both_wrong | nu-2572 | both_wrong_numeric_range_parsing | how many cars had a maximum velocity of at least 100 km/h? | ['17'] | 1 | 19. | Both systems mishandled speed thresholds/ranges such as `85 km/h-105 km/h`; MyAgent undercounted and MACT overcounted. | Add range-aware numeric parsing for threshold count questions if WTQ stability remains a priority. |
| both_wrong | nu-66 | both_wrong_same_row_next_field | what date is next listed after june 14, 2010. | ['December 6, 2010'] | September 6, 2010 | September 6, 2010 | Both systems returned the next row premiere date. Gold expects the next listed date after June 14, 2010 in row-major order, the same row's following finale date December 6, 2010. | Clarify `next listed after` semantics: scan row-major cells after the matched cell, not only the next row. |

## Patent Implication

This supports the patent framing that selective risk collaboration needs a bounded repel/override layer plus deterministic semantic audits. The next evidence should be targeted WTQ diagnostics and fine-grained ablation, not blind Gate-100/full200 expansion.

## Next Priority

Run or implement targeted WTQ checks for listed-after target columns, experiment-number target selection, overtime marker parsing, entity surface cleanup, and verifier override on parenthetical negators.
