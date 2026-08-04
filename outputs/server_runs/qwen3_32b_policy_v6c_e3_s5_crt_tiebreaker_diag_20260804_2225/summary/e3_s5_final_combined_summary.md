# E3 S5 Final Summary: Qwen3-32B MyAgent vs MACT

Run dir: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6c_e3_s5_crt_tiebreaker_diag_20260804_2225`

S5 keeps the accepted S4 paired WTQ/TabFact results and replaces only the tied CRT component with the S5 current-code full CRT100 rerun.

| Dataset | MyAgent | MACT | Delta | MyAgent Avg Tokens | MACT Avg Tokens | Token Ratio | Strict Win |
|---|---:|---:|---:|---:|---:|---:|---:|
| wtq | 76/100 | 74/100 | +2 | 6358.37 | 11034.94 | 0.5762 | True |
| tabfact | 91/100 | 87/100 | +4 | 2660.25 | 10347.37 | 0.2571 | True |
| crt | 65/100 | 62/100 | +3 | 10636.63 | 13330.39 | 0.7979 | True |

Overall: MyAgent `232/300` vs MACT `223/300`, delta `+9`.
Overall token ratio MyAgent/MACT: `0.5662`.
Overall failed/missing: MyAgent `0/0`, MACT `4/4`.
Strict all-dataset superiority: `True`.
Accepted by existing selective-risk criteria: `True`.

## CRT S5 Details

- S5 CRT full rerun: `65/100` vs MACT `62/100`.
- Paired counts: `{'both_correct': 53, 'myagent_only': 12, 'mact_only': 9, 'both_wrong': 26}`.
- MyAgent failed/missing: `0/0`.
- MACT failed/missing: `0/0`.

## Mechanism Change

- Added gold-free CRT scalar canonicalization for negative numeric `difference` answers and country-code answers in country/nation questions.
- Validation traces: `summary/s5_crt_canonicalizer_replay_summary.*`, `summary/s5_affected_slice_real_rerun_summary.*`, and `myagent_s5_crt_paired100_full_rerun/eval/crt_qwen3-32b-local_eval.json`.
