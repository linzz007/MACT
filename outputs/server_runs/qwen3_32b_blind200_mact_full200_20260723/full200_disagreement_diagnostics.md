# Qwen3-32B Full200 Disagreement Diagnostics

Generated: 2026-07-30 17:09:20 CST

Purpose: diagnose full200 paired disagreement patterns without rerunning models.

## Overall

| bucket | count |
|---|---:|
| both_correct | 387 |
| myagent_only | 66 |
| mact_only | 63 |
| neither | 84 |

Net myAgent-only minus MACT-only: `3`.

## Dataset Summary

| dataset | both_correct | myagent_only | mact_only | neither | net | MACT exec errors |
|---|---:|---:|---:|---:|---:|---:|
| wtq | 108 | 23 | 40 | 29 | -17 | 5 |
| tabfact | 178 | 7 | 11 | 4 | -4 | 0 |
| crt | 101 | 36 | 12 | 51 | 24 | 0 |

## Main Findings

- WTQ is the main negative contributor: `myagent_only=23`, `mact_only=40`, net `-17`; MACT also has 5 context-overflow failures that are already preserved as failed rows.
- TabFact is a small negative contributor: `myagent_only=7`, `mact_only=11`, net `-4`; no MACT execution failures.
- CRT is the positive contributor: `myagent_only=36`, `mact_only=12`, net `+24`; no MACT execution failures.
- Full200 overall net is `+3` (`66` myAgent-only vs `63` MACT-only), so the overall lead is real under this evaluator but too narrow to claim broad dataset-level dominance.

## WTQ

| bucket | count | top categories | top tags | shortcut true/false | strong true/false |
|---|---:|---|---|---|---|
| mact_only | 40 | temporal:18, count:16, superlative:11, arithmetic:7, plain_lookup:6, comparison:2 | negation_logic:16, count:16, superlative_order:15, temporal:14, arithmetic:5, list_entity:2 | {'false': 40} | {'true': 39, 'false': 1} |
| myagent_only | 23 | temporal:11, plain_lookup:5, count:5, comparison:4, arithmetic:4, closed_choice:3 | temporal:10, negation_logic:8, count:5, comparison:4, list_entity:4, superlative_order:3 | {'true': 1, 'false': 22} | {'true': 21, 'false': 2} |
| neither | 29 | count:10, superlative:9, temporal:8, arithmetic:6, closed_choice:6, plain_lookup:4 | negation_logic:12, superlative_order:11, count:10, temporal:7, arithmetic:6, comparison:3 | {'false': 29} | {'true': 27, 'false': 2} |
| both_correct | 108 | temporal:47, count:40, superlative:36, arithmetic:18, comparison:17, closed_choice:12 | count:40, temporal:40, superlative_order:40, negation_logic:34, arithmetic:14, comparison:13 | {'false': 94, 'true': 14} | {'true': 100, 'false': 8} |

### WTQ mact_only Samples

- `nu-1434` gold=`['3']` my=`\I Like It\""` mact=`3` tags=`['superlative_order']` shortcut=`False` q=what is the highest chart position ever achieved by one of dino's singles?
- `nu-2873` gold=`['Mike Imrie']` my=`7.0` mact=`Mike Imrie` tags=`['negation_logic']` shortcut=`False` q=who drove the only saab car?
- `nu-2453` gold=`['Mahler']` my=`Not found` mact=`Mahler` tags=`[]` shortcut=`False` q=for which film did georgina hale receive her bafta award?
- `nu-709` gold=`['11']` my=`12` mact=`11` tags=`['count']` shortcut=`False` q=what is the number of tablets?
- `nu-3934` gold=`['1987']` my=`1986.0` mact=`1987` tags=`['superlative_order', 'temporal']` shortcut=`False` q=in what year did salvatore bettiol run in the most marathons?

### WTQ myagent_only Samples

- `nu-58` gold=`['Esther Shahamorov']` my=`Esther Shahamorov` mact=`esther shahamorov with 5th place` tags=`['superlative_order']` shortcut=`True` q=who was the top placing competitor?
- `nu-3422` gold=`['more']` my=`more` mact=`more than 15` tags=`['comparison', 'negation_logic']` shortcut=`False` q=is cassiopeia 1's magnitude more or less than 15?
- `nu-3438` gold=`['Mr B.Melman', 'Mr P.Venter', 'Mrs E.Myer']` my=`['Mr B.Melman', 'Mr P.Venter', 'Mrs E.Myer']` mact=`Mr Sakkie` tags=`['comparison', 'list_entity']` shortcut=`False` q=which mayors had more than 2 consecutive terms?
- `nu-3140` gold=`['Accepts applications prior to the start of each school year']` my=`Accepts applications prior to the start of each school year` mact=`prior to the start of each school year` tags=`[]` shortcut=`False` q=when does agape christian academy accept applications?
- `nu-1786` gold=`['1990-1991 Season']` my=`1990-1991 Season` mact=`1990-1991 Season, 12, Chivas vs América, 1-1, December 9, 1990` tags=`['temporal']` shortcut=`False` q=what was the next tie listed after the 1989-1990 season?

### WTQ neither Samples

- `nu-2178` gold=`['Ollie P. Anderson, Jr.']` my=`Frank V. Ortiz, Jr.` mact=`Jeanette W. Hyde` tags=`['superlative_order']` shortcut=`False` q=who was the first us ambassador to grenada appointed by bill clinton?
- `nu-965` gold=`['5']` my=`16` mact=`15.` tags=`['count']` shortcut=`False` q=how many times was a nomination awarded?
- `nu-4062` gold=`['18']` my=`18.94` mact=`18.9375` tags=`['superlative_order', 'arithmetic']` shortcut=`False` q=in cycle 4 of austria's next top model, what is the average of all the contestants' ages?
- `nu-4299` gold=`['Puff Daddy']` my=`Not found` mact=`` tags=`['superlative_order', 'temporal']` shortcut=`False` q=which artist did jaycen joshua work with before his first job with rick ross?
- `nu-1177` gold=`['Seven']` my=`Lady In The Jaguar` mact=`"The Harvest"` tags=`['superlative_order']` shortcut=`False` q=on which song did the axe murder boyz first collaborate with boondox regarding lyrics?

## TABFACT

| bucket | count | top categories | top tags | shortcut true/false | strong true/false |
|---|---:|---|---|---|---|
| mact_only | 11 | binary_fact:11, closed_choice:11, temporal:9, superlative:2, comparison:1, arithmetic:1 | closed_choice:11, temporal:7, negation_logic:4, superlative_order:3, comparison:1 | {'false': 11} | {'false': 11} |
| myagent_only | 7 | binary_fact:7, closed_choice:7, temporal:3, arithmetic:2, superlative:1, negation:1 | closed_choice:7, temporal:3, negation_logic:3, superlative_order:1 | {'true': 2, 'false': 5} | {'false': 7} |
| neither | 4 | binary_fact:4, closed_choice:4, arithmetic:3, temporal:3, count:1, superlative:1 | closed_choice:4, superlative_order:2, temporal:2, negation_logic:2, count:1 | {'false': 4} | {'false': 4} |
| both_correct | 178 | binary_fact:178, closed_choice:178, temporal:73, arithmetic:41, superlative:32, comparison:31 | closed_choice:178, temporal:68, negation_logic:54, superlative_order:35, comparison:26, arithmetic:13 | {'false': 147, 'true': 31} | {'false': 178} |

### TABFACT mact_only Samples

- `tabfact-test-4211` gold=`['false']` my=`true` mact=`false` tags=`['temporal', 'comparison', 'closed_choice']` shortcut=`False` q=there be less than 17 player who untimely retire during the 1984 european grand prix
- `tabfact-test-5090` gold=`['false']` my=`true` mact=`False` tags=`['closed_choice']` shortcut=`False` q=jesper parnevik be from sweden , while justin leonard be from argentina
- `tabfact-test-6964` gold=`['true']` my=`false` mact=`True` tags=`['closed_choice']` shortcut=`False` q=there be 6 nation that didn't have any gold medal
- `tabfact-test-8573` gold=`['false']` my=`true` mact=`False.**` tags=`['negation_logic', 'closed_choice']` shortcut=`False` q=motherwell be 1 of 4 team against whom llanelli a.f.c afc have only 1 victory
- `tabfact-test-3580` gold=`['true']` my=`false` mact=`True` tags=`['superlative_order', 'temporal', 'negation_logic', 'closed_choice']` shortcut=`False` q=over 3 century pass between southwark have the tallest building or structure

### TABFACT myagent_only Samples

- `tabfact-test-2658` gold=`['true']` my=`true` mact=`False` tags=`['superlative_order', 'closed_choice']` shortcut=`True` q=ask riga be the last place in the competition in the basketball
- `tabfact-test-33` gold=`['false']` my=`false` mact=`True` tags=`['closed_choice']` shortcut=`False` q=guillaume gillet score 3 time as much as each of the other 2 player in the uefa champion league tournament
- `tabfact-test-8673` gold=`['false']` my=`false` mact=`Let's check the dates numerically. The screening that ended on 30 June 2006 started on 18 May 2006. The screening that ended on 10 October 2006 started on 7 September 2006. The difference between 18 May 2006 and 7 September 2006 is about 3 months and 19 days. That's not 5 months. 

Therefore, the claim that the screening starting on 18 May 2006 (which ended on 30 June 2006) is 5 months after the screening that ended on 10 October 2006 (which started on 7 September 2006) is false. 

But wait, the user's original question says "the screening complete on 30 june 2006 be start 5 month after the screening that be complete on 4 october 2006". So the start date of the 30 June 2006 screening is supposed to be 5 months after the start date of the screening that ended on 4 October 2006. However, since there's no screening that ended on 4 October 2006, perhaps the user made a mistake. If we assume that the intended date is 10 October 2006, then the start date of that screening is 7 September 2006. Adding 5 months to 7 September 2006 would be February 7, 2007. The start date of the 30 June 2006 screening is 18 May 2006, which is earlier than February 2007. Therefore, the claim is false. 

Alternatively, if the user meant that the screening that ended on 30 June 2006 started 5 months after the screening that ended on 4 October 2006, but since the 30 June screening started in May and the 4 October screening started in September, the May start is` tags=`['temporal', 'closed_choice']` shortcut=`False` q=the screening complete on 30 june 2006 be start 5 month after the screening that be complete on 4 october 2006
- `tabfact-test-12022` gold=`['true']` my=`true` mact=`False` tags=`['negation_logic', 'closed_choice']` shortcut=`False` q=model 26.260e and 31.260e have a gcm (kg) technical capacity of 42000
- `tabfact-test-6673` gold=`['false']` my=`false` mact=`True` tags=`['temporal', 'negation_logic', 'closed_choice']` shortcut=`False` q=binibining pilipinas - tourism do not start not until the year 1989

### TABFACT neither Samples

- `tabfact-test-6430` gold=`['false']` my=`true` mact=`True` tags=`['superlative_order', 'temporal', 'closed_choice']` shortcut=`False` q=on april 2 2008 , the 2007 - 08 los angeles clippers season be the visitor compete against the supersonics with 10392 in attendance , while 1 day later in april 3 , 2008 the clipper be 1 time again the visitor against the king with attendan
- `tabfact-test-5425` gold=`['true']` my=`false` mact=`False` tags=`['count', 'superlative_order', 'negation_logic', 'closed_choice']` shortcut=`False` q=the team play at least 1 game per day , every day , up until september 14th
- `tabfact-test-4166` gold=`['true']` my=`false` mact=`False` tags=`['temporal', 'negation_logic', 'closed_choice']` shortcut=`False` q=the test matches (1991 - 2000) in november and december take place at 2 different venue
- `tabfact-test-7026` gold=`['true']` my=`false` mact=`False` tags=`['closed_choice']` shortcut=`False` q=dana quigley have 45 win

## CRT

| bucket | count | top categories | top tags | shortcut true/false | strong true/false |
|---|---:|---|---|---|---|
| mact_only | 12 | crt_comparison:12, temporal:11, superlative:9, arithmetic:8, closed_choice:7, negation:7 | superlative_order:9, negation_logic:9, temporal:7, closed_choice:7, arithmetic:6, comparison:3 | {'false': 12} | {'true': 9, 'false': 3} |
| myagent_only | 36 | crt_comparison:36, superlative:29, closed_choice:26, temporal:25, negation:21, arithmetic:17 | superlative_order:31, negation_logic:30, closed_choice:26, temporal:15, arithmetic:12, comparison:11 | {'false': 28, 'true': 8} | {'true': 31, 'false': 5} |
| neither | 51 | crt_comparison:51, temporal:35, arithmetic:28, superlative:19, comparison:17, closed_choice:16 | temporal:29, negation_logic:27, superlative_order:25, arithmetic:23, comparison:16, closed_choice:11 | {'false': 51} | {'false': 31, 'true': 20} |
| both_correct | 101 | crt_comparison:101, superlative:78, closed_choice:74, temporal:67, negation:55, comparison:48 | superlative_order:80, negation_logic:73, closed_choice:72, comparison:41, temporal:36, arithmetic:28 | {'false': 91, 'true': 10} | {'true': 79, 'false': 22} |

### CRT mact_only Samples

- `crt-240` gold=`['15']` my=`13` mact=`15.0` tags=`['superlative_order', 'temporal', 'comparison', 'arithmetic', 'negation_logic']` shortcut=`False` q=What is the maximum points difference between the 2008 A season and the 2009 C season for the teams in the Mexican Primera División season?
- `crt-234` gold=`['Yes']` my=`No` mact=`yes.` tags=`['superlative_order', 'comparison', 'arithmetic', 'negation_logic', 'closed_choice']` shortcut=`False` q=Are there any countries in the Matariki Network of Universities that have a higher average World Rank by the WUR, ARWU or QS than the members from the USA? Answer with only 'Yes' or 'No' that is most accurate and nothing else.
- `crt-265` gold=`['uruguay']` my=`['uruguay', 'chile', 'peru']` mact=`Uruguay.` tags=`['temporal', 'arithmetic', 'list_entity']` shortcut=`False` q=What countries experienced the greatest percentage increase in international tourist arrivals from 2010 to 2011?What countries experienced the greatest percentage increase in international tourist arrivals from 2010 to 2011?
- `crt-254` gold=`['yes']` my=`No` mact=`Yes.` tags=`['superlative_order', 'temporal', 'arithmetic', 'negation_logic', 'closed_choice']` shortcut=`False` q=Is there any evidence of an increase/decrease in Krung Thai Bank's performance from 2004-2005 and from 2008-2009? Answer with only 'Yes' or 'No' that is most accurate and nothing else.
- `crt-180` gold=`['16:117']` my=`0.13675213675213677` mact=`16:117` tags=`['arithmetic']` shortcut=`False` q=What is the ratio of stumpings to catches for West Indies test wicket-keepers?

### CRT myagent_only Samples

- `crt-601` gold=`['less']` my=`less` mact=`"4 + 24 / 24" – maybe 4 fatalities (crew?) and 24 total (passengers?), but the total is 24` tags=`['count', 'superlative_order', 'temporal', 'comparison', 'negation_logic', 'closed_choice']` shortcut=`False` q=How does the number of fatalities compare between accidents that occurred during training flights versus those that occurred during take-offs or landings? Answer with only 'more', 'less' or 'equal' that is most accurate and nothing else.
- `crt-419` gold=`['No']` my=`No` mact=`Yes.` tags=`['superlative_order', 'negation_logic', 'closed_choice']` shortcut=`False` q=Is religious or spiritual content a popular format among radio stations in Fargo-Moorhead? Answer with only 'Yes' or 'No' that is most accurate and nothing else.
- `crt-541` gold=`['No']` my=`No` mact=`People Are Bunny (MM)

Looking through all these dates, none of them repeat. Each date is unique. Therefore, there are no films released on the same date with different series. The answer should be No.
</think>

No` tags=`['superlative_order', 'temporal', 'negation_logic', 'closed_choice']` shortcut=`False` q=Are there any films that were released on the same date but belong to different series? Answer with only 'Yes' or 'No' that is most accurate and nothing else.
- `crt-613` gold=`['Increase']` my=`Increase` mact=`Remain stable` tags=`['count', 'superlative_order', 'arithmetic', 'negation_logic', 'closed_choice']` shortcut=`False` q=How did the number of points scored by Derek Daly vary according to the different teams? Answer with only 'Increase', 'Decrease' or 'Remain stable' that is most accurate and nothing else.
- `crt-313` gold=`['worse']` my=`worse` mact=`better` tags=`['superlative_order', 'temporal', 'comparison', 'negation_logic', 'closed_choice']` shortcut=`False` q=How does the Miami Dolphins' record in the first half of the season compare to their record in the second half? Answer with only 'better', 'worse' or 'equal' that is most accurate and nothing else.

### CRT neither Samples

- `crt-391` gold=`['28']` my=`19 days` mact=`June 10, 2010, to June 29, 2010.` tags=`['temporal', 'arithmetic']` shortcut=`False` q=What was the total time frame for filming for all episodes during season 5 of ídolos brazil?
- `crt-505` gold=`['4']` my=`3` mact=`2.` tags=`['count', 'superlative_order', 'comparison']` shortcut=`False` q=How many buildings in the European Union have held the title of tallest building for more than 10 years?
- `crt-381` gold=`['dean parisot, ted humphrey']` my=`robert king & michelle king` mact=`Dean Parisot and Ted Humphrey.` tags=`['count', 'superlative_order', 'temporal', 'arithmetic', 'negation_logic']` shortcut=`False` q=Which combination of writer and director in season 2 of The Good Wife had the highest average number of US viewers?
- `crt-606` gold=`['11:5']` my=`0.0` mact=`11:6` tags=`['temporal', 'arithmetic']` shortcut=`False` q=What was the ratio of awards won to nominations received by Catalina Sandino Moreno in 2004?
- `crt-204` gold=`['6.44%']` my=`0.32% per year` mact=`0.322` tags=`['temporal', 'arithmetic', 'negation_logic']` shortcut=`False` q=What is the rate of change in the percentage of popular vote for the Green Party between 1988 and 2008?

## Next Debugging Direction

1. Do not optimize TabFact first: its full200 deficit is only 4 rows.
2. Focus WTQ disagreement rows, especially MACT-only cases with comparison/negation/count/temporal tags.
3. For WTQ fixes, use a small discordant subset first and require red/green evidence before rerunning blind200.
4. Keep MACT context-overflow rows as failures unless a separate repaired baseline is explicitly created and labeled.
5. See `wtq_discordant_debug_subset_50.*` and `wtq_compression_bucket_diagnostics.*` for the next WTQ-focused debugging inputs.
