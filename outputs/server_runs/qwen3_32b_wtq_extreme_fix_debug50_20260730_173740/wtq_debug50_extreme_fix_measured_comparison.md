# WTQ Debug50 Extreme Fix Measured Comparison

Generated at: 2026-07-30 17:59:05 CST

This is a targeted WTQ debug50 subset made of old myAgent wrong rows: 40 mact_only + 10 neither. It is not representative accuracy and should not be compared as a random sample.

## Summary

| metric | value |
|---|---:|
| rows | 50 |
| old_myagent_correct | 0 |
| new_myagent_correct | 14 |
| mact_correct | 40 |
| new_eval_num_em_mismatch | 36 |
| new_exec_failures | 0 |
| new_eval_num_missing_answer | 0 |
| old_myagent_avg_total_tokens | 6714.6400 |
| new_myagent_avg_total_tokens | 6857.7200 |
| mact_avg_total_tokens | 11412.1020 |
| token_ratio_new_myagent_to_mact | 0.6009 |
| token_ratio_new_to_old_myagent | 1.0213 |
| old_avg_compression_ratio | 0.3363 |
| new_avg_compression_ratio | 0.4781 |
| new_avg_elapsed_seconds | 16.8523 |
| new_vs_mact_net_on_debug50 | -26 |

Transition counts:

```json
{
  "recovered": 14,
  "still_wrong": 36
}
```

## Targeted Buckets

| bucket | rows | old myAgent | new myAgent | MACT | new avg tokens | new avg compression |
|---|---:|---:|---:|---:|---:|---:|
| newly_global_triggered | 18 | 0 | 10 | 15 | 6768.22 | 0.6055 |
| strict_recoverable_offline | 10 | 0 | 7 | 9 | 6327.00 | 0.6342 |
| mact_only | 40 | 0 | 14 | 40 | 6698.20 | 0.4703 |
| neither | 10 | 0 | 0 | 0 | 7495.80 | 0.5092 |

## Recovered Rows

| id | bucket | targeted | strict row-loss | gold | old myAgent | new myAgent | MACT | question |
|---|---|---|---|---|---|---|---|---|
| nu-1434 | mact_only | False | False | ['3'] | \I Like It\"" | 3 | 3 | what is the highest chart position ever achieved by one of dino's singles? |
| nu-709 | mact_only | False | False | ['11'] | 12 | 11 | 11 | what is the number of tablets? |
| nu-2223 | mact_only | True | True | ['Kazuki Yoshino'] | Rizawan Abdullah | Kazuki Yoshino | Kazuki Yoshino | name the only player transferred from albirex niigata. |
| nu-1951 | mact_only | True | False | ['Runner-up'] | No unique hard surface event found | Runner-up | Runner-up | what was the outcome the only time a hard surface was used? |
| nu-2850 | mact_only | True | True | ['Ironic'] | ['You Oughta Know" A', 'Hand in My Pocket'] | ['Ironic'] | "Ironic" | which singles charted in the top five of canada and also australia? |
| nu-2109 | mact_only | False | False | ['5'] | 3 | 5 | 5 | how many tournaments did stephen hendry win? |
| nu-2139 | mact_only | True | True | ['Thin Line'] | No data available for 1984 in the table. | \Thin Line\"" | \Thin Line\" | what is sinnamon's only hit of 1984? |
| nu-3375 | mact_only | True | True | ['Commonwealth Games'] | No unique race in Malaysia found. | Commonwealth Games | Commonwealth Games | what was the competition in his only race in malaysia? |
| nu-1870 | mact_only | True | True | ['Five'] | ['Four'] | ['Five'] | Five | in the beginning of the show thee were only 3 judges, but what series did the show change to 4 judges? |
| nu-3279 | mact_only | False | False | ['3'] | 5 | 3 | 3 | how many consecutive days did south korea play? |
| nu-4291 | mact_only | True | True | ['Center'] | Right Wing | Center | Center | name the position with only two players in such a position. |
| nu-1424 | mact_only | True | False | ['September 23, 2001'] | September 9, 2001 | September 23, 2001 | September 23, 2001 | what was the first date they played the 49ers? |
| nu-1845 | mact_only | True | False | ['Re-establishment of Krooni currency'] | Barcelona Olympics | Re-establishment of Krooni currency | Re-establishment of Krooni currency | which is the first model listed with 10 krooni as the denomination? |
| nu-53 | mact_only | True | True | ['1935'] | 1988 | 1935 | 1935 | what is the earliest date kodak made 16mm film? |

## Interpretation

- The patch improves a targeted adversarial subset from old myAgent 0/50 to new myAgent 14/50, with no execution failures in the final merged output.
- On the 18 rows newly triggering global rows, measured accuracy is shown separately above; the offline row-recall gain only partially converts to answer accuracy.
- MACT remains higher on this debug subset because it was selected to contain 40 old MACT-only rows; this is a root-cause regression check, not the formal benchmark.
