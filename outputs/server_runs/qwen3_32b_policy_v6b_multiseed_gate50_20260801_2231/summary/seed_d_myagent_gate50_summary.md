# E3 MyAgent Gate-50 Summary: seed_d

Run dir: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_multiseed_gate50_20260801_2231`

| Dataset | Rows input/merged/eval | Correct | Accuracy | Token Ratio vs MACT full200 | Avg Tokens | Avg Elapsed s | Failed | Missing | Gate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| wtq | 50/50/50 | 30/50 | 0.6000 | 0.6329 | 6650.0 | 17.54 | 0 | 0 | inspect |
| tabfact | 50/50/50 | 38/50 | 0.7600 | 0.2682 | 2905.2 | 11.68 | 0 | 0 | inspect |
| crt | 50/50/50 | 30/50 | 0.6000 | 0.7829 | 10028.6 | 27.39 | 0 | 0 | pass |

Overall: MyAgent `98/150`, token ratio vs MACT full200 `0.5735`.
Decision: `stop_or_inspect`.
