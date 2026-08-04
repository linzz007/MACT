# E3 S3 Current-Only Summary: seed_d

Generated: `2026-08-04 15:13:08 CST`
Run dir: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_e3_s3_current_rerun_after_guard_20260804_1425`

| dataset | rows input/merged/eval | correct | threshold | token ratio | avg tokens | avg seconds | failed/missing | gate |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| wtq | 50/50/50 | 28/50 | 35/50 | 0.6417 | 6743.5 | 17.74 | 0/0 | inspect |
| tabfact | 50/50/50 | 39/50 | 45/50 | 0.2613 | 2829.9 | 11.32 | 0/0 | inspect |
| crt | 50/50/50 | 30/50 | 30/50 | 0.7612 | 9751.6 | 25.23 | 0/0 | pass |

Overall: `97/150`, weighted token ratio `0.5659`, failed/missing `0/0`.
Decision: `s3_seed_stop_or_inspect`.
