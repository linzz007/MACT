# E3 S4 Paired MACT Combined Summary

Run dir: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6c_e3_s4_paired_mact_20260804_1626`

| Dataset | MyAgent | MACT | Delta | Token Ratio |
|---|---:|---:|---:|---:|
| wtq | 76/100 | 74/100 | +2 | 0.5762 |
| tabfact | 91/100 | 87/100 | +4 | 0.2571 |
| crt | 62/100 | 62/100 | +0 | 0.8078 |
| aggregate | 229/300 | 223/300 | +6 | 0.5700 |

MyAgent failed/missing: `0/0`.
MACT failed/missing: `4/4`.
Accepted existing paired criteria: `True`.
Strict all-dataset superiority: `False`.
Decision: `s4_paired_pass_existing_criteria_not_strict`.
