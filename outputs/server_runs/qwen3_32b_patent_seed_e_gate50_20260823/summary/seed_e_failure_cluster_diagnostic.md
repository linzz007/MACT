# Seed-E Failure Cluster Diagnostic

Run dir: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_seed_e_gate50_20260823`

This diagnostic compares row-level correctness using the same evaluator logic as `code/evaluate_results.py`. It is intended as a mechanism-design input, not as a new acceptance result.

| Dataset | Both Correct | MyAgent Only | MACT Only | Both Wrong | Main Signal |
|---|---:|---:|---:|---:|---|
| wtq | 28 | 3 | 9 | 10 | 9 MACT-only rows; 10 both-wrong rows; largest accuracy gap |
| tabfact | 38 | 2 | 4 | 6 | 4 MACT-only rows; 6 both-wrong rows; small gap but strong token advantage |
| crt | 19 | 5 | 7 | 19 | 7 MACT-only rows; 19 both-wrong rows; token ratio weakest |

## Optimization Reading

- Seed-E does not invalidate the locked Qwen3 full200 win, but it shows the method is not yet multi-seed robust.
- The next patent-aligned work should target MACT-only rows first, because they represent recoverable accuracy without blindly expanding rules.
- CRT needs cost-specific work too: its accuracy gap is small, but MyAgent token ratio is `0.8757`, above the desired low-token boundary.
- Both-wrong rows should be treated as hard-set boundary evidence unless a narrow, table-grounded mechanism can solve a cluster cleanly.

## Candidate Mechanism Clusters

- WTQ: count/aggregate repair for road-loss counts, average-over-listed-entities, above-threshold episode counts, election-result state counts, disposed-status counts, and abbreviation-preserving country answers.
- TabFact: deterministic verification candidates for highest-crowd home/away checks, max regular-season games by player, month-filtered lowest attendance, and greatest margin of victory.
- CRT: answer-contract repair for exact numeric averages, fractions/proportions, percent-style outputs, and yes/no questions where the reasoning text drifts away from the required label.
- Cross-dataset: add a final answer-normalization contract before scoring-facing output, especially where MyAgent computes the right value but emits a format outside the evaluator target (`13.64` vs `13.635`, `0.1666` vs `1/6`, `China` vs `CHN`).

## WTQ

Counts: both_correct `28`, myagent_only `3`, mact_only `9`, both_wrong `10`.

### mact_only

- `nu-379`: what was the number of losses on the road?
  Gold: `['6']`; MyAgent: `12` (risk `high`, route `COMPLEX`, tokens `6181`); MACT: `6` (tokens `8754`).
- `nu-1287`: what is the average amount of gold medals earned by the 15 countries?
  Gold: `['3']`; MyAgent: `5.62` (risk `medium`, route `COMPLEX`, tokens `3784`); MACT: `3` (tokens `9158`).
- `nu-1783`: how many episodes had viewings above 8.00 m?
  Gold: `['11']`; MyAgent: `10` (risk `high`, route `COMPLEX`, tokens `8282`); MACT: `11` (tokens `17625`).
- `nu-1161`: how many total states have election results from 2000?
  Gold: `['6']`; MyAgent: `5` (risk `high`, route `COMPLEX`, tokens `10058`); MACT: `6.` (tokens `33277`).
- `nu-1423`: which country received the most box office revenue from national films in 2013?
  Gold: `['China']`; MyAgent: `Japan` (risk `high`, route `COMPLEX`, tokens `8972`); MACT: `China` (tokens `15573`).
- `nu-2513`: which district would be last on a list arranged by size with the largest district first?
  Gold: `['Half Tree Hollow']`; MyAgent: `Jamestown Harbour` (risk `high`, route `COMPLEX`, tokens `4598`); MACT: `Half Tree Hollow` (tokens `8513`).
- `nu-387`: how many episodes were in the last season on this chart?
  Gold: `['22']`; MyAgent: `13.0` (risk `high`, route `COMPLEX`, tokens `4791`); MACT: `22` (tokens `9305`).
- `nu-2957`: what is the total number of ships listed as "disposed of"?
  Gold: `['2']`; MyAgent: `56` (risk `high`, route `COMPLEX`, tokens `7379`); MACT: `2` (tokens `16055`).
- `nu-3415`: what country had the most amount of people in the top 10? (use abbreviation)
  Gold: `['CHN']`; MyAgent: `China` (risk `high`, route `COMPLEX`, tokens `11185`); MACT: `CHN` (tokens `18791`).

### myagent_only

- `nu-3017`: which distribution had the most columns with "discontinued listed?
  Gold: `['Debian']`; MyAgent: `Debian` (risk `high`, route `COMPLEX`, tokens `11135`); MACT: `Discontinued` (tokens `19673`).
- `nu-4343`: how many more awards did she win in 2009 than in 2007?
  Gold: `['6']`; MyAgent: `6` (risk `high`, route `COMPLEX`, tokens `7005`); MACT: `5` (tokens `15925`).
- `nu-1286`: of all the games won, which game had a score gap less than the february 28th game?
  Gold: `['February 16']`; MyAgent: `February 16` (risk `medium`, route `COMPLEX`, tokens `2352`); MACT: `February 16 against Alaska` (tokens `10389`).

### both_wrong

- `nu-4195`: which interjet airline has the highest number of passenders?
  Gold: `['Aeroméxico Connect, Interjet, Volaris']`; MyAgent: `Quintana Roo, Cancún` (risk `high`, route `COMPLEX`, tokens `6405`); MACT: `Quintana Roo, Cancún` (tokens `7119`).
- `nu-627`: are there more male or female senators?
  Gold: `['male']`; MyAgent: `Unknown` (risk `high`, route `COMPLEX`, tokens `5421`); MACT: `**more male senators**.` (tokens `22966`).
- `nu-553`: name all models with the same mpg as fiat 500 1.4 pop.
  Gold: `['Fiat 500 1.4 LOUNGE 3D', 'Fiat 500 1.4 SPORT', 'Citroen C4 2.0 SX 5DR 6SP A D'...`; MyAgent: `Fiat 500 1.4 LOUNGE 3D` (risk `light`, route `COMPLEX`, tokens `7371`); MACT: `` (tokens `0`).
- `nu-439`: which poll did anastasiades win by a larger margin, feb 1 2013 or dec 3 2012?
  Gold: `['1 February 2013']`; MyAgent: `Dec 3 2012` (risk `high`, route `COMPLEX`, tokens `12914`); MACT: `Feb 1 2013` (tokens `9258`).
- `nu-3444`: which tie game had the bigger score?
  Gold: `['38']`; MyAgent: `No tie games found` (risk `light`, route `COMPLEX`, tokens `3957`); MACT: `November 11, 1972` (tokens `14098`).
- `nu-1109`: who coached longer, john sauer or charlie taaffe?
  Gold: `['Charlie Taaffe']`; MyAgent: `Neither John Sauer nor Charlie Taaffe are listed in the table.` (risk `high`, route `COMPLEX`, tokens `12131`); MACT: `` (tokens `0`).
- `nu-1995`: which is the only community station?
  Gold: `['7THE']`; MyAgent: `7CAE` (risk `high`, route `COMPLEX`, tokens `5429`); MACT: `7CAE` (tokens `6529`).
- `nu-1730`: what number of ambassadors was selected by ronald reagan?
  Gold: `['5']`; MyAgent: `6` (risk `high`, route `COMPLEX`, tokens `7176`); MACT: `6` (tokens `14866`).
- ... 2 more rows in JSON.

## TABFACT

Counts: both_correct `38`, myagent_only `2`, mact_only `4`, both_wrong `6`.

### mact_only

- `tabfact-test-8244`: the highest crowd be 27100 at punt road oval on 22 august 1964 when st kilda be the home team and geelong the away team
  Gold: `['false']`; MyAgent: `true` (risk `high`, route `COMPLEX`, tokens `400`); MACT: `False` (tokens `10054`).
- `tabfact-test-1541`: brent sopel play more regular season game than any other player on the chart
  Gold: `['true']`; MyAgent: `false` (risk `high`, route `COMPLEX`, tokens `2735`); MACT: `True` (tokens `8345`).
- `tabfact-test-403`: the game with the lowest attendance in may of the 1991 toronto blue jays season be play against the athletics
  Gold: `['false']`; MyAgent: `true` (risk `high`, route `COMPLEX`, tokens `4314`); MACT: `False` (tokens `19695`).
- `tabfact-test-7344`: the cowboys' greatest margin of victory be 30 point in week 6 against the oiler
  Gold: `['true']`; MyAgent: `false` (risk `high`, route `COMPLEX`, tokens `6777`); MACT: `true` (tokens `22329`).

### myagent_only

- `tabfact-test-2129`: united kingdom be the nation with the least silver
  Gold: `['true']`; MyAgent: `true` (risk `high`, route `COMPLEX`, tokens `2332`); MACT: `False` (tokens `9914`).
- `tabfact-test-5595`: ensign racing field an f1 car from 1973 to 1982 , but not in 1975
  Gold: `['false']`; MyAgent: `false` (risk `high`, route `COMPLEX`, tokens `2567`); MACT: `True` (tokens `8449`).

### both_wrong

- `tabfact-test-3418`: the puebla team score about 3 less point on than the chiapas team in the 08 c pt categorization
  Gold: `['true']`; MyAgent: `false` (risk `high`, route `COMPLEX`, tokens `2908`); MACT: `False` (tokens `11774`).
- `tabfact-test-3278`: all of the minister serve 5 year term list of ministers for the police force of luxembourg
  Gold: `['true']`; MyAgent: `false` (risk `high`, route `COMPLEX`, tokens `2927`); MACT: `False` (tokens `15606`).
- `tabfact-test-2758`: during the 1974 season , the 1974 green bay packers season lose by 15 point or more 2 time , against the minnestota viking and the buffalo bill
  Gold: `['true']`; MyAgent: `false` (risk `high`, route `COMPLEX`, tokens `3704`); MACT: `False` (tokens `19696`).
- `tabfact-test-2449`: only 2 time have vladimira progress past the group stage
  Gold: `['true']`; MyAgent: `false` (risk `high`, route `COMPLEX`, tokens `3223`); MACT: `false` (tokens `15514`).
- `tabfact-test-3094`: during the 2007 - 08 minnesota wild season , minnesota play home 2 time less than they play away
  Gold: `['false']`; MyAgent: `true` (risk `high`, route `COMPLEX`, tokens `5479`); MACT: `True` (tokens `11026`).
- `tabfact-test-992`: librado andrade never win the fight against paul jones
  Gold: `['true']`; MyAgent: `false` (risk `medium`, route `COMPLEX`, tokens `774`); MACT: `False` (tokens `10853`).

## CRT

Counts: both_correct `19`, myagent_only `5`, mact_only `7`, both_wrong `19`.

### mact_only

- `crt-250`: Does being in the bundesliga increase the mitteldeutscher bc's chances of competing in european competitions? Answer with only 'Yes' or 'No' that is most accurate and nothing else.
  Gold: `['Yes']`; MyAgent: `No` (risk `high`, route `COMPLEX`, tokens `15219`); MACT: `yes.` (tokens `14286`).
- `crt-603`: Was "Maria Full of Grace" the only movie for which Catalina Sandino Moreno was nominated for an award in 2004? Answer with only 'Yes' or 'No' that is most accurate and nothing else...
  Gold: `['Yes']`; MyAgent: `No` (risk `high`, route `COMPLEX`, tokens `20626`); MACT: `Yes.` (tokens `9106`).
- `crt-380`: What is the average number of US viewers for episodes directed by Félix Alcalá in season 2 of The Good Wife?
  Gold: `['12.565']`; MyAgent: `nan` (risk `medium`, route `COMPLEX`, tokens `2878`); MACT: `12.565` (tokens `17227`).
- `crt-711`: Does Andrea Petkovic have a higher winning percentage in finals matches held in Europe or outside of Europe? Answer with only 'Yes' or 'No' that is most accurate and nothing else.
  Gold: `['Yes']`; MyAgent: `No` (risk `high`, route `COMPLEX`, tokens `17551`); MACT: `yes.` (tokens `12940`).
- `crt-502`: What was the average viewership for episodes that aired in March 2006?
  Gold: `['13.635']`; MyAgent: `13.64` (risk `medium`, route `COMPLEX`, tokens `2643`); MACT: `13.635` (tokens `15142`).
- `crt-280`: What proportion of the Malaysia Airlines group companies are involved in the airline industry?
  Gold: `['1/6']`; MyAgent: `0.16666666666666666` (risk `medium`, route `COMPLEX`, tokens `2442`); MACT: `1/6` (tokens `7874`).
- `crt-290`: What is the average number of losses for teams in the top half of the table?
  Gold: `['8.875']`; MyAgent: `9.0` (risk `high`, route `COMPLEX`, tokens `17410`); MACT: `8.875` (tokens `17429`).

### myagent_only

- `crt-450`: Can the current status of each locomotive be predicted based on the year it was built and the type of locomotive? Answer with only 'Yes' or 'No' that is most accurate and nothing e...
  Gold: `['No']`; MyAgent: `No` (risk `high`, route `COMPLEX`, tokens `15174`); MACT: `Simplex (diesel?), no, wait, Simplex is diesel. The petrol ones are Scooter (194...` (tokens `11124`).
- `crt-394`: Were there any notable differences in performance for the Tampa Bay Buccaneers during the month of September, compared to other months in the 1983 season?
  Gold: `['No']`; MyAgent: `No` (risk `high`, route `COMPLEX`, tokens `24059`); MACT: `Yes.` (tokens `12235`).
- `crt-446`: Was the 25th anniversary loonie a special edition, with a higher mintage or issue price compared to other years? Answer with only 'Yes' or 'No' that is most accurate and nothing el...
  Gold: `['No']`; MyAgent: `No` (risk `high`, route `COMPLEX`, tokens `15028`); MACT: `Yes.` (tokens `10772`).
- `crt-326`: Was there a significant correlation between the date of polling and support for the Progressive Conservatives in polls conducted by Corporate Research Associates during the 2011 Ne...
  Gold: `['No']`; MyAgent: `No` (risk `high`, route `COMPLEX`, tokens `28384`); MACT: `Yes.` (tokens `19830`).
- `crt-584`: Is there a relationship between a school's authority (state vs state integrated) and its decile rating? Answer with only 'Yes' or 'No' that is most accurate and nothing else.
  Gold: `['No']`; MyAgent: `No` (risk `high`, route `COMPLEX`, tokens `19304`); MACT: `Start with 9 (Cambridge East) +9 = 18 +8 = 26 +8 = 34 +9 =43 +10=53 +10=63 +9=72...` (tokens `13942`).

### both_wrong

- `crt-693`: Is there a difference in viewership between episodes written by a single writer and those written by multiple writers?Answer with only 'Yes' or 'No' that is most accurate and nothi...
  Gold: `['No']`; MyAgent: `Yes` (risk `high`, route `COMPLEX`, tokens `16062`); MACT: `10.6 /2=5.3. So 5.247 vs 5.3. The difference is 0.053 million, which is 53,000 v...` (tokens `18520`).
- `crt-594`: Did the attendance increase or decrease at the games held in Los Angeles compared to Philadelphia? Answer with only 'Increase' or 'Decrease' that is most accurate and nothing else.
  Gold: `['Yes']`; MyAgent: `Increase` (risk `high`, route `COMPLEX`, tokens `15739`); MACT: `Increase.` (tokens `8838`).
- `crt-390`: What was the average time difference between the episode air date and the audition date during season 5 of ídolos brazil?
  Gold: `['69.428']`; MyAgent: `69.86` (risk `high`, route `COMPLEX`, tokens `13532`); MACT: `69.86. </think> Let's think step by step. For each row, calculate the time diffe...` (tokens `15479`).
- `crt-241`: For teams in the Mexican Primera División season, what is the median difference between 2009 A season points and 2010 C season points?
  Gold: `['2']`; MyAgent: `3` (risk `high`, route `COMPLEX`, tokens `19518`); MACT: `3` (tokens `20939`).
- `crt-708`: What is the average total sumo records for holders who had their last match in the 2000s?
  Gold: `['27']`; MyAgent: `27.71` (risk `high`, route `COMPLEX`, tokens `15319`); MACT: `27.71` (tokens `18246`).
- `crt-619`: If the average attendance of all teams combined is used to predict the attendance of each team, what is the sum of the absolute differences between the predicted attendance and the...
  Gold: `['28066.933']`; MyAgent: `28066.93` (risk `medium`, route `COMPLEX`, tokens `2463`); MACT: `27899` (tokens `11553`).
- `crt-277`: What is the median win/loss percentage of the Greenville Braves across all years?ning record?
  Gold: `['0.489%']`; MyAgent: `49.275362318840585` (risk `medium`, route `COMPLEX`, tokens `2381`); MACT: `1. 1963 2. 1964 3. 1984 4. 1985 5. 1986 6. 1987 7. 1988 8. 1989 9. 1990 10. 1991...` (tokens `17355`).
- `crt-226`: What is the ratio of silver medals to the sum of gold and bronze medals for countries with a rank of 10 or lower?
  Gold: `['3:7']`; MyAgent: `0.475` (risk `medium`, route `COMPLEX`, tokens `2551`); MACT: `0.4286` (tokens `13991`).
- ... 11 more rows in JSON.
