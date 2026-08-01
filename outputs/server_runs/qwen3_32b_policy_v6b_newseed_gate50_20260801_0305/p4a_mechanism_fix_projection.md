# P4a Mechanism Fix Offline Projection

Run dir: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305`

Scope: replay saved P4a merged rows through the updated deterministic TabFact/CRT shortcut chain plus CRT scalar canonicalization. No Qwen3/vLLM calls were made. Rows without a new shortcut/canonicalization keep their current prediction.

| Dataset | Current | Projected | Net Gain | Shortcut Rows | Canonicalized Rows | Wrong -> Correct | Correct -> Wrong | Gate Note |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| tabfact | 42/50 | 45/50 | +3 | 10 | 0 | 3 | 0 | pass projected threshold |
| crt | 21/50 | 30/50 | +9 | 9 | 1 | 9 | 0 | pass projected threshold |

## Wrong -> Correct Rows

### tabfact
- `tabfact-test-7551` pred `false` -> `true`; gold `['true']`; reason `TabFact only-not-country claim checked deterministically.`; question: the only player who be not from the united state be from scotland
- `tabfact-test-7952` pred `false` -> `true`; gold `['true']`; reason `TabFact same-row cell mentions checked deterministically.`; question: chelsea be the home team when crystal palace be the away team and norwich city be the home team when bradford city be the away team
- `tabfact-test-11907` pred `false` -> `true`; gold `['true']`; reason `TabFact same-row cell mentions checked deterministically.`; question: two shortswords be the external weapon with a falcon shield animal

### crt
- `crt-287` pred `No` -> `Yes`; gold `['Yes']`; reason `CRT penalty score relation checked deterministically.`; question: Did any teams in the 2008 - 09 UEFA Cup have an aggregate score of 4 - 3 with a penalty shootout?  Answer with only 'Yes' or 'No' that is most accurate and nothing else.
- `crt-298` pred `1.5` -> `3:2`; gold `['3:2']`; reason `CRT medal ratio computed deterministically.`; question: What is the ratio of gold medals earned by the United States to the total medals earned by UK?
- `crt-242` pred `1.013586956521739` -> `1.01`; gold `['1.01']`; reason `CRT total-points season ratio rounded deterministically.`; question: What is the ratio of total points earned in the 2008 A season to total points earned in the 2009 C season for teams in the Mexican Primera División season?
- `crt-704` pred `6.43` -> `6.4`; gold `['6.4']`; reason `CRT threshold-filtered average rounded deterministically.`; question: What is the average order of world number one golfers who have spent more than 40 weeks at the top?
- `crt-232` pred `218.6869909253863` -> `434`; gold `['434']`; reason `CRT year-established variation computed as range.`; question: How much variation is there in the year established among the members of the Matariki Network of Universities?
- `crt-299` pred `0.2222222222222222` -> `12.5%`; gold `['12.5%']`; reason `CRT medal probability computed deterministically.`; question: What is the probability that a nation will earn at least two gold medals in the 2012 Summer Olympics?
- `crt-105` pred `netherlands (ned)` -> `netherlands`; gold `['netherlands']`; reason `CRT scalar entity suffix canonicalized.`; question: If a nation's score was equal to the sum of the number of gold and silver medals it won, which nation had the highest score?
- `crt-308` pred `0.75` -> `6:8`; gold `['6:8']`; reason `CRT partner win-loss ratio formatted deterministically.`; question: What is the win-loss ratio when Patricio Cornejo plays with Jaime Fillol?
- `crt-286` pred `['manchester city', 'aalborg bk']` -> `['manchester city and aalborg bk']`; gold `['manchester city and aalborg bk']`; reason `CRT penalty score relation checked deterministically.`; question: What teams played in a match with a score of 4 - 3 and went to penalties in the 2008 - 09 UEFA Cup?

## Correct -> Wrong Rows

### tabfact
- none

### crt
- none

## Interpretation

This is an offline mechanism projection, not a fresh model run and not a paired MACT comparison. It is used to decide whether the code change is worth a targeted Qwen3 gate.
