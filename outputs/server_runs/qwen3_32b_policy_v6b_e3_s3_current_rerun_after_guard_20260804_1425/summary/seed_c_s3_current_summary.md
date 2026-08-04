# E3 S3 Current-Only Summary: seed_c

Generated: `2026-08-04 14:48:14 CST`
Run dir: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_e3_s3_current_rerun_after_guard_20260804_1425`

| dataset | rows input/merged/eval | correct | threshold | token ratio | avg tokens | avg seconds | failed/missing | gate |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| wtq | 50/50/50 | 40/50 | 35/50 | 0.5885 | 6183.6 | 14.63 | 0/0 | pass |
| tabfact | 50/50/50 | 46/50 | 45/50 | 0.2556 | 2768.3 | 10.92 | 0/0 | pass |
| crt | 50/50/50 | 32/50 | 30/50 | 0.9200 | 11785.2 | 25.72 | 0/0 | pass |

Overall: `118/150`, weighted token ratio `0.6073`, failed/missing `0/0`.
Decision: `s3_seed_pass_run_paired_mact_candidate`.
