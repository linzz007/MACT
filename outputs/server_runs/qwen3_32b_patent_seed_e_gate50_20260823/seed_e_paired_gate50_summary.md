# Seed-E Paired Gate-50 Summary

Run dir: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_seed_e_gate50_20260823`

| Dataset | MyAgent | MACT | Delta | Token Ratio | Failed MyAgent / MACT | Missing MyAgent / MACT |
|---|---:|---:|---:|---:|---:|---:|
| wtq | 31/50 | 37/50 | -6 | 0.6456 | 0/3 | 0/3 |
| tabfact | 40/50 | 42/50 | -2 | 0.2408 | 0/0 | 0/0 |
| crt | 24/50 | 26/50 | -2 | 0.8757 | 0/0 | 0/0 |

Overall: MyAgent `95/150` vs MACT `105/150`, token ratio `0.6019`.
Datasets MyAgent > MACT: `0/3`.
Datasets MyAgent >= MACT: `0/3`.
Accepted by existing paired criteria: `False`.
Strict all-dataset superiority goal met: `False`.
