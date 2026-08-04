# E3 S4 Paired MACT Summary: seed_c

Run dir: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6c_e3_s4_paired_mact_20260804_1626`

| Dataset | MyAgent | MACT | Delta | Token Ratio | Failed MyAgent / MACT | Missing MyAgent / MACT | Paired myOnly / mactOnly |
|---|---:|---:|---:|---:|---:|---:|---:|
| wtq | 40/50 | 40/50 | +0 | 0.6168 | 0/3 | 0/3 | 4/4 |
| tabfact | 46/50 | 46/50 | +0 | 0.2827 | 0/0 | 0/0 | 4/4 |
| crt | 32/50 | 32/50 | +0 | 0.8830 | 0/0 | 0/0 | 6/6 |

Overall: MyAgent `118/150` vs MACT `118/150`, token ratio `0.6253`.
Datasets MyAgent > MACT: `0/3`.
Datasets MyAgent >= MACT: `3/3`.
Accepted by existing paired criteria: `True`.
Strict all-dataset superiority goal met: `False`.
