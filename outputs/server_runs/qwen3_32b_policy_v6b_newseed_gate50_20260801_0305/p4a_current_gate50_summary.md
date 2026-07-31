# P4a Current New-Seed Gate-50 Summary

Run dir: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305`

| Dataset | Rows input/merged/eval | Correct | Accuracy | Token Ratio vs MACT full200 | Avg Tokens | Avg Elapsed s | Failed | Missing | Gate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| wtq | 50/50/50 | 37/50 | 0.7400 | 0.6436 | 6763.0 | 17.28 | 0 | 0 | pass |
| tabfact | 50/50/50 | 42/50 | 0.8400 | 0.2387 | 2585.0 | 11.51 | 0 | 0 | inspect |
| crt | 50/50/50 | 21/50 | 0.4200 | 0.8002 | 10250.4 | 24.18 | 0 | 0 | inspect |

Decision: `stop_or_inspect`

P4a is a current-only stability gate. It does not prove new-seed superiority over MACT until P4b paired MACT is run on the same IDs.
