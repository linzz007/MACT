# WTQ Compressor Hypothesis Diagnostics

Generated: 2026-07-30 17:23:00 CST

Purpose: test code-level hypotheses against WTQ discordant row/column loss signals.

## Hypothesis Signals

| signal | count |
|---|---:|
| count_reasoning_or_boundary_error | 9 |
| computed_answer_requires_operation_trace | 9 |
| temporal_order_or_boundary_error | 7 |
| row_needs_semantic_or_aggregate_selection | 7 |
| answer_selection_error_with_evidence_present | 6 |
| row_matcher_or_llm_selected_rows_missed_despite_first3_signal | 4 |
| implicit_answer_column_dropped | 3 |
| row_match_first3_blindspot | 2 |

## Interpretation

- `implicit_answer_column_dropped` maps to `TableCompressor._match_cols`: the row is kept but the answer column is pruned, common for questions such as `who drove...` where the answer column name is not literal in the question.
- `row_match_first3_blindspot` maps to `TableCompressor._match_rows`: fallback row matching only scans the first three cells, so filter evidence in later columns can fail to select the row.
- `count_reasoning_or_boundary_error` and `temporal_order_or_boundary_error` mean compression preserved the literal evidence; these need planner/operation or normalization debugging, not more row/column context alone.

## Examples

### answer_selection_error_with_evidence_present
- `nu-1434` bucket=`mact_only` loss=`gold_cell_selected` ratio=`1.0` used_cols=['Year', 'Song', 'Album', 'Position', 'Chart'] my=`\I Like It\""` mact=`3` q=what is the highest chart position ever achieved by one of dino's singles?
- `nu-2611` bucket=`mact_only` loss=`gold_cell_selected` ratio=`0.375` used_cols=['No.', 'Date/time', 'Aircraft'] my=`sopwith triplane s/n n5460` mact=`Nieuport serial number 3958` q=which was earlier, sopwith triplane s/n n5460 or nieuport serial number 3958?
- `nu-1951` bucket=`mact_only` loss=`gold_cell_selected` ratio=`0.19047619047619047` used_cols=['Outcome', 'Surface'] my=`No unique hard surface event found` mact=`Runner-up` q=what was the outcome the only time a hard surface was used?
- `nu-1093` bucket=`mact_only` loss=`gold_cell_selected` ratio=`0.5` used_cols=['Week', 'Date', 'Result'] my=`42` mact=`45` q=what are the most points won during the 1998 arizona cardinals season?
- `nu-2183` bucket=`mact_only` loss=`gold_cell_selected` ratio=`0.4` used_cols=['Player', 'Total'] my=`Total` mact=`Spas Delev` q=who scored the most goals?
- `nu-4162` bucket=`neither` loss=`gold_cell_selected` ratio=`0.5` used_cols=['Season', 'Home', 'Away'] my=`1987–88` mact=`1987–88` q=which season did flamurtari vlorë win more home games than away?

### implicit_answer_column_dropped
- `nu-2873` bucket=`mact_only` loss=`gold_row_kept_col_dropped` ratio=`0.2` used_cols=['Position', 'Car'] my=`7.0` mact=`Mike Imrie` q=who drove the only saab car?
- `nu-1913` bucket=`neither` loss=`gold_row_kept_col_dropped` ratio=`0.5714285714285714` used_cols=['#', 'Date', 'Result', 'Competition'] my=`the team` mact=`Spain.` q=which team competed for the euro 2000 qualifying the most consecutive years?
- `nu-2396` bucket=`neither` loss=`gold_row_kept_col_dropped` ratio=`0.6` used_cols=['Year', 'Premiers', 'Runners Up'] my=`5` mact=`5` q=what is the total number of years for port douglas crocs?

### row_match_first3_blindspot
- `nu-2453` bucket=`mact_only` loss=`gold_col_kept_row_dropped` ratio=`0.10714285714285714` used_cols=['Year', 'Film', 'Notes'] my=`Not found` mact=`Mahler` q=for which film did georgina hale receive her bafta award?
- `nu-2178` bucket=`neither` loss=`gold_col_kept_row_dropped` ratio=`0.05714285714285714` used_cols=['Representative', 'Title', 'Appointed by'] my=`Frank V. Ortiz, Jr.` mact=`Jeanette W. Hyde` q=who was the first us ambassador to grenada appointed by bill clinton?

### count_reasoning_or_boundary_error
- `nu-709` bucket=`mact_only` loss=`gold_cell_selected` ratio=`0.25` used_cols=['Tablet'] my=`12` mact=`11` q=what is the number of tablets?
- `nu-2213` bucket=`mact_only` loss=`gold_cell_selected` ratio=`0.4` used_cols=['Season', 'Goals'] my=`8.0` mact=`4` q=what is the total number of goals?
- `nu-2232` bucket=`mact_only` loss=`gold_cell_selected` ratio=`0.8` used_cols=['Result', 'Date', 'Category', 'Tournament', 'Surface', 'Partnering', 'Opponents', 'Score'] my=`0` mact=`4` q=how many championship tournaments did she play in after 1984?
- `nu-1125` bucket=`mact_only` loss=`gold_cell_selected` ratio=`1.0` used_cols=['No. in series', 'No. in season', 'Title', 'Directed by', 'Written by', 'Original air date', 'Prod. code'] my=`0` mact=`7` q=in season 1, what number of episodes were written by morton fine and david friedkin?
- `nu-3939` bucket=`mact_only` loss=`gold_cell_selected` ratio=`0.5` used_cols=['Sl no', 'Name of the prabandham', 'Number of pasurams'] my=`Total number of pasurams` mact=`Thiruvay Mozhi` q=name the prabandham with the most number of pasurams
- `nu-2109` bucket=`mact_only` loss=`gold_cell_selected` ratio=`0.3157894736842105` used_cols=['Date', 'Tournament name', 'Winner', 'Runner-up', 'Score'] my=`3` mact=`5` q=how many tournaments did stephen hendry win?
- `nu-463` bucket=`mact_only` loss=`gold_cell_selected` ratio=`0.375` used_cols=['Year', 'Network', 'Ratings'] my=`5` mact=`3` q=list the number of times the rating was above a 4.0.
- `nu-697` bucket=`mact_only` loss=`gold_cell_selected` ratio=`0.6666666666666666` used_cols=['No. in season', 'Canadian airdate', 'US airdate', 'Production code'] my=`13` mact=`40` q=how many total episodes aired in season 13?

### temporal_order_or_boundary_error
- `nu-3934` bucket=`mact_only` loss=`gold_cell_selected` ratio=`0.5` used_cols=['Year', 'Competition', 'Event'] my=`1986.0` mact=`1987` q=in what year did salvatore bettiol run in the most marathons?
- `nu-3535` bucket=`mact_only` loss=`gold_cell_selected` ratio=`0.13636363636363635` used_cols=['Band', 'Released', 'Disc Description'] my=`One or both bands not found in the table` mact=`1985` q=u2 and redbox both had releases in what year?
- `nu-2635` bucket=`mact_only` loss=`gold_cell_selected` ratio=`0.6666666666666666` used_cols=['Name', 'From', 'To', 'Honours'] my=`Henrik Jensen` mact=`Ole Mørk` q=list the only coach that won promotion to the first tier.
- `nu-830` bucket=`mact_only` loss=`gold_cell_selected` ratio=`1.0` used_cols=['Player', 'No.', 'Nationality', 'Position', 'Years for Jazz', 'School/Club Team'] my=`Bernie Fryer` mact=`Terry Furlow` q=who was ranked last among this group?
- `nu-1845` bucket=`mact_only` loss=`gold_cell_selected` ratio=`0.45` used_cols=['Year', 'Model', 'Denomination'] my=`Barcelona Olympics` mact=`Re-establishment of Krooni currency` q=which is the first model listed with 10 krooni as the denomination?
- `nu-3088` bucket=`neither` loss=`gold_cell_selected` ratio=`0.0234375` used_cols=['Game', 'Date', 'Score'] my=`L 8–14` mact=`L 8–14` q=what was the score of the last game of the season?
- `nu-4299` bucket=`neither` loss=`gold_cell_selected` ratio=`0.08771929824561403` used_cols=['Chart Year', 'Artist', 'Album', 'Song', 'Billboard Hot 100', 'Billboard Hot R&B/Hip Hop', 'column_7'] my=`Not found` mact=`` q=which artist did jaycen joshua work with before his first job with rick ross?

### computed_answer_requires_operation_trace
- `nu-1505` bucket=`mact_only` loss=`gold_not_literal_or_computed` ratio=`0.15841584158415842` used_cols=['Year', 'Publisher'] my=`34` mact=`74.` q=how many books did "harper & brothers" publish?
- `nu-1826` bucket=`mact_only` loss=`gold_not_literal_or_computed` ratio=`0.8` used_cols=['Name', 'Topic', 'Target age', 'Advertising'] my=`4` mact=`7` q=how many of the educational websites have used at least limited advertising?
- `nu-216` bucket=`mact_only` loss=`gold_not_literal_or_computed` ratio=`0.5` used_cols=['Contestant', 'Original Tribe', 'First Switch', 'Second Switch'] my=`12` mact=`11` q=how many contestants were on the original manobo tribe?
- `nu-2663` bucket=`mact_only` loss=`gold_not_literal_or_computed` ratio=`0.05217391304347826` used_cols=['Single / EP', 'Tracks', 'Label'] my=`2` mact=`5` q=how many total labels did this singer release single on?
- `nu-2919` bucket=`mact_only` loss=`gold_not_literal_or_computed` ratio=`0.019704433497536946` used_cols=['County', 'Brown', 'Votes', 'Nixon'] my=`0.0` mact=`1773` q=in plumas, what was the difference between brown and nixon's votes?
- `nu-1424` bucket=`mact_only` loss=`gold_not_literal_or_computed` ratio=`0.025210084033613446` used_cols=['Week', 'Date', 'Opponent'] my=`September 9, 2001` mact=`September 23, 2001` q=what was the first date they played the 49ers?
- `nu-1591` bucket=`neither` loss=`gold_not_literal_or_computed` ratio=`0.875` used_cols=['Season', 'Episodes', 'Original airing Season premiere', 'Original airing Season finale', 'Original airing TV season', 'Rank', 'Viewers (in millions)'] my=`24.86` mact=`24.86` q=how many viewers tuned in for the 6th season?
- `nu-983` bucket=`neither` loss=`gold_not_literal_or_computed` ratio=`0.028125` used_cols=['Year', 'Winner', 'Time'] my=`0:2.04` mact=`2.04 seconds` q=what is the time difference between take charge indy and vicar?

### row_needs_semantic_or_aggregate_selection
- `nu-3949` bucket=`mact_only` loss=`gold_col_kept_row_dropped` ratio=`0.11688311688311688` used_cols=['Callsign', 'Area served', 'Frequency'] my=`Derby` mact=`Ulverstone` q=derby and which other station are the only ones to not have a frequency?
- `nu-4328` bucket=`mact_only` loss=`gold_col_kept_row_dropped` ratio=`0.05` used_cols=['Rank', 'Nation', 'Silver'] my=`Total` mact=`Spain` q=which country has the top number of silver medals won?
- `nu-2850` bucket=`mact_only` loss=`gold_col_kept_row_dropped` ratio=`0.12121212121212122` used_cols=['Year', 'Title', 'Chart positions AU', 'Chart positions CA'] my=`['You Oughta Know" A', 'Hand in My Pocket']` mact=`"Ironic"` q=which singles charted in the top five of canada and also australia?
- `nu-1870` bucket=`mact_only` loss=`gold_col_kept_row_dropped` ratio=`0.2222222222222222` used_cols=['Series', 'Premiere', 'Finale', 'Winner', 'Runner-up', 'Third place', 'Host(s)', 'Judging panel', 'Guest judge(s)'] my=`['Four']` mact=`Five` q=in the beginning of the show thee were only 3 judges, but what series did the show change to 4 judges?
- `nu-4291` bucket=`mact_only` loss=`gold_col_kept_row_dropped` ratio=`0.07142857142857142` used_cols=['Pick #', 'Player', 'Position'] my=`Right Wing` mact=`Center` q=name the position with only two players in such a position.
- `nu-721` bucket=`mact_only` loss=`gold_col_kept_row_dropped` ratio=`0.16666666666666666` used_cols=['Episode', 'Show #', 'Iron Chef', 'Challenger', 'Challenger specialty', 'Secret ingredient(s) or theme', 'Winner', 'Final score'] my=`sugar not found in the table` mact=`carrots` q=what is the next secret ingredient after sugar?
- `nu-717` bucket=`mact_only` loss=`gold_col_kept_row_dropped` ratio=`0.08333333333333333` used_cols=['Game', 'Date', 'Team', 'Score'] my=`Game 33 not found in the table.` mact=`6` q=what was the point difference between the sacramento and detroit for game 33?

### row_matcher_or_llm_selected_rows_missed_despite_first3_signal
- `nu-2223` bucket=`mact_only` loss=`gold_col_kept_row_dropped` ratio=`0.125` used_cols=['Position', 'Player', 'Transferred From'] my=`Rizawan Abdullah` mact=`Kazuki Yoshino` q=name the only player transferred from albirex niigata.
- `nu-2139` bucket=`mact_only` loss=`gold_col_kept_row_dropped` ratio=`0.11428571428571428` used_cols=['Year', 'Name'] my=`No data available for 1984 in the table.` mact=`\Thin Line\"` q=what is sinnamon's only hit of 1984?
- `nu-3375` bucket=`mact_only` loss=`gold_col_kept_row_dropped` ratio=`0.3` used_cols=['Year', 'Competition', 'Venue', 'Event'] my=`No unique race in Malaysia found.` mact=`Commonwealth Games` q=what was the competition in his only race in malaysia?
- `nu-53` bucket=`mact_only` loss=`gold_col_kept_row_dropped` ratio=`0.0625` used_cols=['Film', 'Film_2', 'Date'] my=`1988` mact=`1935` q=what is the earliest date kodak made 16mm film?
