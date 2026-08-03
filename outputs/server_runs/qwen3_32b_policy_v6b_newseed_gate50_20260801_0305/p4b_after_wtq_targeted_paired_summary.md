# P4b Paired New-Seed Gate-50 Summary After WTQ Targeted Fix

Run dir: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305`

| Dataset | MyAgent | MACT | Delta | Token Ratio | Failed MyAgent / MACT | Missing MyAgent / MACT |
|---|---:|---:|---:|---:|---:|---:|
| wtq | 46/50 | 43/50 | +3 | 0.5571 | 0/0 | 0/0 |
| tabfact | 45/50 | 44/50 | +1 | 0.2156 | 0/0 | 0/0 |
| crt | 30/50 | 24/50 | +6 | 0.7740 | 0/0 | 0/0 |

Overall: MyAgent `121/150` vs MACT `111/150`, token ratio `0.5310`.
Datasets MyAgent > MACT: `3/3`.
Strict all-dataset new-seed goal met: `True`.
Accepted by existing paired criteria: `True`.
