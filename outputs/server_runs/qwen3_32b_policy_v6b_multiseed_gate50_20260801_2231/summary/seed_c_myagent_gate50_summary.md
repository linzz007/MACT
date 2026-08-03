# E3 MyAgent Gate-50 Summary: seed_c

Run dir: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_multiseed_gate50_20260801_2231`

| Dataset | Rows input/merged/eval | Correct | Accuracy | Token Ratio vs MACT full200 | Avg Tokens | Avg Elapsed s | Failed | Missing | Gate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| wtq | 50/50/50 | 40/50 | 0.8000 | 0.6013 | 6318.6 | 15.25 | 0 | 0 | pass |
| tabfact | 50/50/50 | 44/50 | 0.8800 | 0.2604 | 2820.0 | 10.65 | 0 | 0 | inspect |
| crt | 50/50/50 | 30/50 | 0.6000 | 0.9118 | 11679.9 | 25.33 | 0 | 0 | pass |

Overall: MyAgent `114/150`, token ratio vs MACT full200 `0.6096`.
Decision: `stop_or_inspect`.
