# WTQ Compression Bucket Diagnostics

Generated: 2026-07-30 17:12:48 CST

Purpose: compare WTQ compression and prediction signals by paired-disagreement bucket.

| bucket | count | median compression ratio | median compressed rows | not-found-like | header prediction | numeric scalar | top strategy |
|---|---:|---:|---:|---:|---:|---:|---|
| mact_only | 40 | 0.25 | 8.0 | 7 | 3 | 14 | expanded_context_block |
| myagent_only | 23 | 0.4 | 10.0 | 0 | 0 | 6 | expanded_context_block |
| neither | 29 | 0.4 | 12.0 | 2 | 0 | 7 | expanded_context_block |
| both_correct | 108 | 0.375 | 8.0 | 0 | 0 | 52 | expanded_context_block |

## Interpretation

- WTQ mact_only is not caused by service failures; rows are valid paired rows.
- mact_only has lower median compression ratio than both_correct, and contains not-found/header-like predictions, suggesting retrieval or table-context targeting misses in addition to reasoning errors.
- The dominant semantic categories remain temporal/count/superlative/negation, so fixes should target generic table selection and boundary handling before rerunning large samples.

## Signal Samples

### mact_only
- `nu-2873` signals=['numeric_scalar_prediction'] gold=`['Mike Imrie']` my=`7.0` mact=`Mike Imrie` ratio=`0.2` rows=`24` q=who drove the only saab car?
- `nu-2453` signals=['not_found_like_prediction'] gold=`['Mahler']` my=`Not found` mact=`Mahler` ratio=`0.10714285714285714` rows=`3` q=for which film did georgina hale receive her bafta award?
- `nu-709` signals=['numeric_scalar_prediction'] gold=`['11']` my=`12` mact=`11` ratio=`0.25` rows=`12` q=what is the number of tablets?
- `nu-3934` signals=['numeric_scalar_prediction'] gold=`['1987']` my=`1986.0` mact=`1987` ratio=`0.5` rows=`8` q=in what year did salvatore bettiol run in the most marathons?
- `nu-1505` signals=['numeric_scalar_prediction'] gold=`['74']` my=`34` mact=`74.` ratio=`0.15841584158415842` rows=`40` q=how many books did "harper & brothers" publish?
- `nu-2213` signals=['numeric_scalar_prediction'] gold=`['4']` my=`8.0` mact=`4` ratio=`0.4` rows=`11` q=what is the total number of goals?
- `nu-1826` signals=['numeric_scalar_prediction'] gold=`['7']` my=`4` mact=`7` ratio=`0.8` rows=`17` q=how many of the educational websites have used at least limited advertising?
- `nu-3535` signals=['not_found_like_prediction'] gold=`['1985']` my=`One or both bands not found in the table` mact=`1985` ratio=`0.13636363636363635` rows=`3` q=u2 and redbox both had releases in what year?

### neither
- `nu-965` signals=['numeric_scalar_prediction'] gold=`['5']` my=`16` mact=`15.` ratio=`0.75` rows=`21` q=how many times was a nomination awarded?
- `nu-4299` signals=['not_found_like_prediction'] gold=`['Puff Daddy']` my=`Not found` mact=`` ratio=`0.08771929824561403` rows=`15` q=which artist did jaycen joshua work with before his first job with rick ross?
- `nu-1263` signals=['not_found_like_prediction'] gold=`['4']` my=`The table does not provide a consistent number of nominees per year for the NAACP Image Award.` mact=`the Supporting Actor is the winner, and the Nominees column lists all the other nominees. So for 1997, the winner is Samuel L. Jackson, and the Nominees column lists Blair Underwood, Charles S. Dutton, Delroy Lindo, Forest Whitaker. That's four other nominees, making a total of 5 nominees for that year. 

So for each year, the total number of nominees is 1 (the winner) plus the number of names listed in the Nominees column. However, in some years, the Nominees column is empty, meaning the winner was the only nominee. 

So to calculate the total number of nominees across all years, we need to go through each year, count the number of nominees (1 if Nominees is empty, else 1 + number of names in Nominees column), and sum them all. 

But the question is phrased as "how many nominees are there each year for the naacp image award?" which is a bit ambiguous. If it's asking for the number of nominees in each year, the answer would vary each year. But the answer format requires a single number. However, looking at the examples, the user might be asking for the total number of nominees across all years. 

Alternatively, maybe the question is asking for the number of nominees per year, but the answer is that it varies. However, the answer format requires a specific number. 

Wait, perhaps the user is asking for the number of nominees in each year, but the answer is that each year has a certain` ratio=`0.5` rows=`46` q=how many nominees are there each year for the naacp image award?
- `nu-2396` signals=['numeric_scalar_prediction'] gold=`['2']` my=`5` mact=`5` ratio=`0.6` rows=`11` q=what is the total number of years for port douglas crocs?
- `nu-712` signals=['numeric_scalar_prediction'] gold=`['Cahill', 'Colosimo', 'Culina', 'Elrich', 'Griffiths', 'Skoko', 'Zdrilic']` my=`7` mact=`Cahill, Colosimo, Culina, Elrich, Griffiths, Skoko, Zdrilic` ratio=`0.4` rows=`14` q=players who scored at most 1 total goal
- `nu-506` signals=['numeric_scalar_prediction'] gold=`['2']` my=`5.0` mact=`5.0` ratio=`0.6666666666666666` rows=`13` q=what is the total number of fw-190's he damaged or destroyed?
- `nu-3290` signals=['numeric_scalar_prediction'] gold=`['17']` my=`49` mact=`` ratio=`0.75` rows=`62` q=how many terminals have at least four major streets listed?
- `nu-824` signals=['numeric_scalar_prediction'] gold=`['34']` my=`9` mact=`Lev Urusov (9)

So that's 9 ambassadors in the first part (entries 1-16). Then from 23 to` ratio=`0.3333333333333333` rows=`34` q=how many total ambassadors were there?

### myagent_only
- `nu-3438` signals=['list_prediction'] gold=`['Mr B.Melman', 'Mr P.Venter', 'Mrs E.Myer']` my=`['Mr B.Melman', 'Mr P.Venter', 'Mrs E.Myer']` mact=`Mr Sakkie` ratio=`1.0` rows=`31` q=which mayors had more than 2 consecutive terms?
- `nu-3406` signals=['numeric_scalar_prediction'] gold=`['4']` my=`4` mact=`15` ratio=`0.6` rows=`29` q=how many accolades ranked the album below 100th place?
- `nu-2502` signals=['list_prediction'] gold=`['China PR', 'Guam', 'Hong Kong', 'Japan', 'Korea DPR', 'Korea Republic', 'Macau', 'Mongolia', 'Northern Mariana Islands', 'Chinese Taipei']` my=`['China PR', 'Guam', 'Hong Kong', 'Japan', 'Korea DPR', 'Korea Republic', 'Macau', 'Mongolia', 'Northern Mariana Islands', 'Chinese Taipei']` mact=`China PR, Guam, Hong Kong, Japan, Korea DPR, Korea Republic, Macau, Mongolia, Northern Mariana Islands, Chinese Taipei` ratio=`0.8` rows=`10` q=which associations have both a women's and men's team?
- `nu-3977` signals=['numeric_scalar_prediction'] gold=`['18']` my=`18` mact=`-18` ratio=`0.026785714285714284` rows=`3` q=what is the difference of the jsu and tu scores in 2001
- `nu-1329` signals=['list_prediction'] gold=`['Major General Raza Hussain', 'Major General Ahmed Bilal']` my=`['Major General Raza Hussain', 'Major General Ahmed Bilal']` mact=`Major General Raza Hussain and Major General Ahmed Bilal` ratio=`1.0` rows=`9` q=which administrators started their terms after 1998?
- `nu-2903` signals=['list_prediction'] gold=`['Narkhed-New Amravati Pass', 'Bhusaval-Narkhed Pass']` my=`['Narkhed-New Amravati Pass', 'Bhusaval-Narkhed Pass']` mact=`Narkhed-New Amravati Pass, Bhusaval-Narkhed Pass` ratio=`0.8333333333333334` rows=`35` q=which trains do not give an arrival time
- `nu-3139` signals=['numeric_scalar_prediction'] gold=`['3']` my=`3` mact=`` ratio=`0.003094777562862669` rows=`8` q=what is the number of locations named st. clair in pennsylvania?
- `nu-2032` signals=['numeric_scalar_prediction'] gold=`['11']` my=`11` mact=`82` ratio=`0.6666666666666666` rows=`11` q=how many players competed in the 1939 masters tournament?
