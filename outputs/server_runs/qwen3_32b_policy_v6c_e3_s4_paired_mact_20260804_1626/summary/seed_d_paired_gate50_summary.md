# E3 S4 Paired MACT Summary: seed_d

Run dir: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6c_e3_s4_paired_mact_20260804_1626`

| Dataset | MyAgent | MACT | Delta | Token Ratio | Failed MyAgent / MACT | Missing MyAgent / MACT | Paired myOnly / mactOnly |
|---|---:|---:|---:|---:|---:|---:|---:|
| wtq | 36/50 | 34/50 | +2 | 0.5424 | 0/1 | 0/1 | 7/5 |
| tabfact | 45/50 | 41/50 | +4 | 0.2341 | 0/0 | 0/0 | 4/0 |
| crt | 30/50 | 30/50 | +0 | 0.7324 | 0/0 | 0/0 | 6/6 |

Overall: MyAgent `111/150` vs MACT `105/150`, token ratio `0.5195`.
Datasets MyAgent > MACT: `2/3`.
Datasets MyAgent >= MACT: `3/3`.
Accepted by existing paired criteria: `True`.
Strict all-dataset superiority goal met: `False`.
