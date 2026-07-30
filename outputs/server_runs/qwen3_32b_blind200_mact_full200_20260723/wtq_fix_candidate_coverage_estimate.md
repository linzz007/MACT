# WTQ Fix Candidate Coverage Estimate

Generated: 2026-07-30 17:23:06 CST

Purpose: estimate which generic WTQ fix direction is worth testing before code changes or model reruns. Counts are coverage potential, not measured accuracy gain.

## Scenario Counts

| candidate direction | rows in debug subset |
|---|---:|
| planner_or_answer_selection_fix | 22 |
| global_rows_for_wtq_extreme_or_only | 10 |
| operation_trace_or_count_fix | 9 |
| preserve_more_answer_columns_for_implicit_answer | 3 |
| row_match_all_cells_or_semantic_filter | 3 |
| other | 3 |

## Recommended Test Order

1. `global_rows_for_wtq_extreme_or_only`: likely best first test. It could recover 10 literal-gold row-loss cases in the 50-row debug subset, including 9 MACT-only rows.
2. `row_match_all_cells_or_semantic_filter`: targeted row matcher improvement for non-global questions where clue tokens occur outside the first three cells.
3. `planner_or_answer_selection_fix`: needed for 22 rows where gold survived compression; more context alone is not enough.
4. `operation_trace_or_count_fix`: needed for 9 count/arithmetic rows where gold is not a literal table cell.
5. `preserve_more_answer_columns_for_implicit_answer`: small scope; only 3 rows in this subset, so not the first fix.

## Examples

### planner_or_answer_selection_fix
- `nu-1434` bucket=`mact_only` loss=`gold_cell_selected` ratio=`1.0` used_cols=['Year', 'Song', 'Album', 'Position', 'Chart'] my=`\I Like It\""` mact=`3` q=what is the highest chart position ever achieved by one of dino's singles?
- `nu-709` bucket=`mact_only` loss=`gold_cell_selected` ratio=`0.25` used_cols=['Tablet'] my=`12` mact=`11` q=what is the number of tablets?
- `nu-3934` bucket=`mact_only` loss=`gold_cell_selected` ratio=`0.5` used_cols=['Year', 'Competition', 'Event'] my=`1986.0` mact=`1987` q=in what year did salvatore bettiol run in the most marathons?
- `nu-2213` bucket=`mact_only` loss=`gold_cell_selected` ratio=`0.4` used_cols=['Season', 'Goals'] my=`8.0` mact=`4` q=what is the total number of goals?
- `nu-2611` bucket=`mact_only` loss=`gold_cell_selected` ratio=`0.375` used_cols=['No.', 'Date/time', 'Aircraft'] my=`sopwith triplane s/n n5460` mact=`Nieuport serial number 3958` q=which was earlier, sopwith triplane s/n n5460 or nieuport serial number 3958?
- `nu-3535` bucket=`mact_only` loss=`gold_cell_selected` ratio=`0.13636363636363635` used_cols=['Band', 'Released', 'Disc Description'] my=`One or both bands not found in the table` mact=`1985` q=u2 and redbox both had releases in what year?
- `nu-2232` bucket=`mact_only` loss=`gold_cell_selected` ratio=`0.8` used_cols=['Result', 'Date', 'Category', 'Tournament', 'Surface', 'Partnering', 'Opponents', 'Score'] my=`0` mact=`4` q=how many championship tournaments did she play in after 1984?
- `nu-1951` bucket=`mact_only` loss=`gold_cell_selected` ratio=`0.19047619047619047` used_cols=['Outcome', 'Surface'] my=`No unique hard surface event found` mact=`Runner-up` q=what was the outcome the only time a hard surface was used?

### preserve_more_answer_columns_for_implicit_answer
- `nu-2873` bucket=`mact_only` loss=`gold_row_kept_col_dropped` ratio=`0.2` used_cols=['Position', 'Car'] my=`7.0` mact=`Mike Imrie` q=who drove the only saab car?
- `nu-1913` bucket=`neither` loss=`gold_row_kept_col_dropped` ratio=`0.5714285714285714` used_cols=['#', 'Date', 'Result', 'Competition'] my=`the team` mact=`Spain.` q=which team competed for the euro 2000 qualifying the most consecutive years?
- `nu-2396` bucket=`neither` loss=`gold_row_kept_col_dropped` ratio=`0.6` used_cols=['Year', 'Premiers', 'Runners Up'] my=`5` mact=`5` q=what is the total number of years for port douglas crocs?

### row_match_all_cells_or_semantic_filter
- `nu-2453` bucket=`mact_only` loss=`gold_col_kept_row_dropped` ratio=`0.10714285714285714` used_cols=['Year', 'Film', 'Notes'] my=`Not found` mact=`Mahler` q=for which film did georgina hale receive her bafta award?
- `nu-721` bucket=`mact_only` loss=`gold_col_kept_row_dropped` ratio=`0.16666666666666666` used_cols=['Episode', 'Show #', 'Iron Chef', 'Challenger', 'Challenger specialty', 'Secret ingredient(s) or theme', 'Winner', 'Final score'] my=`sugar not found in the table` mact=`carrots` q=what is the next secret ingredient after sugar?
- `nu-717` bucket=`mact_only` loss=`gold_col_kept_row_dropped` ratio=`0.08333333333333333` used_cols=['Game', 'Date', 'Team', 'Score'] my=`Game 33 not found in the table.` mact=`6` q=what was the point difference between the sacramento and detroit for game 33?

### operation_trace_or_count_fix
- `nu-1505` bucket=`mact_only` loss=`gold_not_literal_or_computed` ratio=`0.15841584158415842` used_cols=['Year', 'Publisher'] my=`34` mact=`74.` q=how many books did "harper & brothers" publish?
- `nu-1826` bucket=`mact_only` loss=`gold_not_literal_or_computed` ratio=`0.8` used_cols=['Name', 'Topic', 'Target age', 'Advertising'] my=`4` mact=`7` q=how many of the educational websites have used at least limited advertising?
- `nu-216` bucket=`mact_only` loss=`gold_not_literal_or_computed` ratio=`0.5` used_cols=['Contestant', 'Original Tribe', 'First Switch', 'Second Switch'] my=`12` mact=`11` q=how many contestants were on the original manobo tribe?
- `nu-2663` bucket=`mact_only` loss=`gold_not_literal_or_computed` ratio=`0.05217391304347826` used_cols=['Single / EP', 'Tracks', 'Label'] my=`2` mact=`5` q=how many total labels did this singer release single on?
- `nu-2919` bucket=`mact_only` loss=`gold_not_literal_or_computed` ratio=`0.019704433497536946` used_cols=['County', 'Brown', 'Votes', 'Nixon'] my=`0.0` mact=`1773` q=in plumas, what was the difference between brown and nixon's votes?
- `nu-1424` bucket=`mact_only` loss=`gold_not_literal_or_computed` ratio=`0.025210084033613446` used_cols=['Week', 'Date', 'Opponent'] my=`September 9, 2001` mact=`September 23, 2001` q=what was the first date they played the 49ers?
- `nu-1591` bucket=`neither` loss=`gold_not_literal_or_computed` ratio=`0.875` used_cols=['Season', 'Episodes', 'Original airing Season premiere', 'Original airing Season finale', 'Original airing TV season', 'Rank', 'Viewers (in millions)'] my=`24.86` mact=`24.86` q=how many viewers tuned in for the 6th season?
- `nu-983` bucket=`neither` loss=`gold_not_literal_or_computed` ratio=`0.028125` used_cols=['Year', 'Winner', 'Time'] my=`0:2.04` mact=`2.04 seconds` q=what is the time difference between take charge indy and vicar?

### global_rows_for_wtq_extreme_or_only
- `nu-3949` bucket=`mact_only` loss=`gold_col_kept_row_dropped` ratio=`0.11688311688311688` used_cols=['Callsign', 'Area served', 'Frequency'] my=`Derby` mact=`Ulverstone` q=derby and which other station are the only ones to not have a frequency?
- `nu-2223` bucket=`mact_only` loss=`gold_col_kept_row_dropped` ratio=`0.125` used_cols=['Position', 'Player', 'Transferred From'] my=`Rizawan Abdullah` mact=`Kazuki Yoshino` q=name the only player transferred from albirex niigata.
- `nu-4328` bucket=`mact_only` loss=`gold_col_kept_row_dropped` ratio=`0.05` used_cols=['Rank', 'Nation', 'Silver'] my=`Total` mact=`Spain` q=which country has the top number of silver medals won?
- `nu-2850` bucket=`mact_only` loss=`gold_col_kept_row_dropped` ratio=`0.12121212121212122` used_cols=['Year', 'Title', 'Chart positions AU', 'Chart positions CA'] my=`['You Oughta Know" A', 'Hand in My Pocket']` mact=`"Ironic"` q=which singles charted in the top five of canada and also australia?
- `nu-2139` bucket=`mact_only` loss=`gold_col_kept_row_dropped` ratio=`0.11428571428571428` used_cols=['Year', 'Name'] my=`No data available for 1984 in the table.` mact=`\Thin Line\"` q=what is sinnamon's only hit of 1984?
- `nu-3375` bucket=`mact_only` loss=`gold_col_kept_row_dropped` ratio=`0.3` used_cols=['Year', 'Competition', 'Venue', 'Event'] my=`No unique race in Malaysia found.` mact=`Commonwealth Games` q=what was the competition in his only race in malaysia?
- `nu-1870` bucket=`mact_only` loss=`gold_col_kept_row_dropped` ratio=`0.2222222222222222` used_cols=['Series', 'Premiere', 'Finale', 'Winner', 'Runner-up', 'Third place', 'Host(s)', 'Judging panel', 'Guest judge(s)'] my=`['Four']` mact=`Five` q=in the beginning of the show thee were only 3 judges, but what series did the show change to 4 judges?
- `nu-4291` bucket=`mact_only` loss=`gold_col_kept_row_dropped` ratio=`0.07142857142857142` used_cols=['Pick #', 'Player', 'Position'] my=`Right Wing` mact=`Center` q=name the position with only two players in such a position.

### other
- `nu-3279` bucket=`mact_only` loss=`gold_row_kept_col_dropped` ratio=`0.25` used_cols=['Date', 'column_3', 'column_5'] my=`5` mact=`3` q=how many consecutive days did south korea play?
- `nu-3767` bucket=`mact_only` loss=`gold_row_kept_col_dropped` ratio=`0.02857142857142857` used_cols=['Club performance Season Norway', 'Club performance Club Norway', 'Total Goals Total'] my=`Total` mact=`0` q=how many goals did manchester have in 1997-1998?
- `nu-976` bucket=`mact_only` loss=`gold_row_kept_col_dropped` ratio=`0.42857142857142855` used_cols=['Season', 'League Competition', 'League Top scorer'] my=`0` mact=`4` q=how many seasons was morten rasmussen the top scorer?
