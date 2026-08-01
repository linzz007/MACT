# P4b Paired New-Seed Gate-50 Summary

Run dir: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305`

| Dataset | MyAgent | MACT | Delta | Token Ratio | Failed MyAgent / MACT | Missing MyAgent / MACT |
|---|---:|---:|---:|---:|---:|---:|
| wtq | 37/50 | 43/50 | -6 | 0.5980 | 0/0 | 0/0 |
| tabfact | 45/50 | 44/50 | +1 | 0.2156 | 0/0 | 0/0 |
| crt | 30/50 | 24/50 | +6 | 0.7740 | 0/0 | 0/0 |

Overall: MyAgent `112/150` vs MACT `111/150`, token ratio `0.5444`.
Datasets MyAgent >= MACT: `2/3`.
Accepted by existing paired criteria: `True`.
