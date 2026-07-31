# P4a New-Seed Error Inspection

Run dir: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305`

| Dataset | Correct | Wrong | Wrong Risk Dist | Wrong Shortcut Reasons |
|---|---:|---:|---|---|
| wtq | 37/50 | 13 | `{'high': 13}` | `{'WTQ row-major listed-after value selected deterministically.': 1, 'unknown': 12}` |
| tabfact | 42/50 | 8 | `{'high': 4, 'medium': 4}` | `{'TabFact entity attribute row checked deterministically.': 2, 'unknown': 6}` |
| crt | 21/50 | 29 | `{'high': 14, 'medium': 15}` | `{'unknown': 29}` |

## Incorrect Examples

### wtq
- `nu-3537` pred=`2` gold=`['1']` risk=`high` shortcut=`` question=how many years did the true american club make the playoff?
- `nu-2572` pred=`1` gold=`['17']` risk=`high` shortcut=`` question=how many cars had a maximum velocity of at least 100 km/h?
- `nu-1108` pred=`MG William A. Mann` gold=`['William A. Mann']` risk=`high` shortcut=`` question=who came first john f. williams or william a. mann?
- `nu-1104` pred=`1` gold=`['2']` risk=`high` shortcut=`` question=how many robots are from the united states?
- `nu-2825` pred=`7` gold=`['8']` risk=`high` shortcut=`` question=what is the number of winners in the community division?
- `nu-3905` pred=`Ludwig Wolf Germany (GER)` gold=`['Ludwig Wolf']` risk=`high` shortcut=`` question=who is the last person listed under slalom?
- `nu-3317` pred=`21` gold=`['13']` risk=`high` shortcut=`` question=total number of sponsors?
- `nu-3990` pred=`Pop` gold=`['009']` risk=`high` shortcut=`` question=which experiment number came directly before felix?
- `nu-1478` pred=`0` gold=`['2']` risk=`high` shortcut=`` question=what is the number of times a game went into overtime between the eagles and giants?
- `nu-66` pred=`September 6, 2010` gold=`['December 6, 2010']` risk=`high` shortcut=`` question=what date is next listed after june 14, 2010.
- `nu-3320` pred=`Esther Shahamorov` gold=`['Yossef Romano']` risk=`high` shortcut=`` question=which person retired injured after three attempts in their event?
- `nu-1825` pred=`48712.0` gold=`['Stade Félix Bollaert']` risk=`high` shortcut=`WTQ row-major listed-after value selected deterministically.` question=what is the next stadium listed after parc des princes?

### tabfact
- `tabfact-test-7551` pred=`false` gold=`['true']` risk=`high` shortcut=`` question=the only player who be not from the united state be from scotland
- `tabfact-test-7952` pred=`false` gold=`['true']` risk=`high` shortcut=`TabFact entity attribute row checked deterministically.` question=chelsea be the home team when crystal palace be the away team and norwich city be the home team when bradford city be the away team
- `tabfact-test-11953` pred=`false` gold=`['true']` risk=`high` shortcut=`` question=the santa mesa district have a population of 99993 in 2010
- `tabfact-test-5024` pred=`false` gold=`['true']` risk=`medium` shortcut=`` question=the constructor be lotus - climax for 11 of the 20 one race
- `tabfact-test-3629` pred=`false` gold=`['true']` risk=`medium` shortcut=`` question=giorgio zampori finish 3rd 3 time
- `tabfact-test-5316` pred=`false` gold=`['true']` risk=`medium` shortcut=`` question=8 team score zero point
- `tabfact-test-11907` pred=`false` gold=`['true']` risk=`medium` shortcut=`TabFact entity attribute row checked deterministically.` question=two shortswords be the external weapon with a falcon shield animal
- `tabfact-test-5704` pred=`false` gold=`['true']` risk=`high` shortcut=`` question=the lowest average be 0.33 lower than the highest average

### crt
- `crt-188` pred=`19.0` gold=`['21']` risk=`medium` shortcut=`` question=What is the average gap in days between the original air date of episodes?
- `crt-287` pred=`No` gold=`['Yes']` risk=`high` shortcut=`` question=Did any teams in the 2008 - 09 UEFA Cup have an aggregate score of 4 - 3 with a penalty shootout?  Answer with only 'Yes' or 'No' that is most accurate and nothing else.
- `crt-415` pred=`Yes` gold=`['No']` risk=`high` shortcut=`` question=Did Peter Whitehead's performance fluctuate in any particular year? Answer with only 'Yes' or 'No' that is most accurate and nothing else.
- `crt-463` pred=`20.0` gold=`['0.25']` risk=`medium` shortcut=`` question=What is the percentage of trains within this table that are currently operated by Nemisis Rail?
- `crt-298` pred=`1.5` gold=`['3:2']` risk=`medium` shortcut=`` question=What is the ratio of gold medals earned by the United States to the total medals earned by UK?
- `crt-242` pred=`1.013586956521739` gold=`['1.01']` risk=`medium` shortcut=`` question=What is the ratio of total points earned in the 2008 A season to total points earned in the 2009 C season for teams in the Mexican Primera División season?
- `crt-704` pred=`6.43` gold=`['6.4']` risk=`high` shortcut=`` question=What is the average order of world number one golfers who have spent more than 40 weeks at the top?
- `crt-158` pred=`0` gold=`['3']` risk=`medium` shortcut=`` question=How many races has Christian Pescatori competed in throughout his career, based on the given data?
- `crt-359` pred=`0.6300530880244544` gold=`['Negative']` risk=`high` shortcut=`` question=What is the correlation between a team's number of conceded goals and their final position in the league in 2001?
- `crt-232` pred=`218.6869909253863` gold=`['434']` risk=`medium` shortcut=`` question=How much variation is there in the year established among the members of the Matariki Network of Universities?
- `crt-306` pred=`361` gold=`['185 / 56\t-  546 / 166']` risk=`medium` shortcut=`` question=What is the range in height of the tallest buildings in Portland, Oregon?
- `crt-68` pred=`Yes` gold=`['No']` risk=`high` shortcut=`` question=Have any members of the band played both the alto 1 and mellophone? Answer with only 'Yes' or 'No' that is most accurate and nothing else.

Interpretation: P4a current-only new-seed validation did not meet the predeclared accuracy gate because TabFact and CRT were below threshold. This file is for inspection; it is not a paired MACT comparison.
