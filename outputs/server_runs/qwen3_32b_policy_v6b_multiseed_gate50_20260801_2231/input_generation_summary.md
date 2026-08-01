# E3 Multi-Seed Gate-50 Input Generation

Run dir: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_multiseed_gate50_20260801_2231`

Purpose: prepare two additional non-overlapping Gate-50 seeds for Qwen3-32B MyAgent vs MACT stability validation.

| Seed | Dataset | Source Rows | Base Excluded IDs | Prior Seed Excluded IDs | Candidate Rows | Selected Rows | Input |
|---|---|---:|---:|---:|---:|---:|---|
| seed_c | wtq | 4344 | 250 | 0 | 4094 | 50 | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_multiseed_gate50_20260801_2231/input/seed_c/wtq_seed_c_gate50.jsonl` |
| seed_c | tabfact | 12779 | 250 | 0 | 12529 | 50 | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_multiseed_gate50_20260801_2231/input/seed_c/tabfact_seed_c_gate50.jsonl` |
| seed_c | crt | 728 | 250 | 0 | 478 | 50 | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_multiseed_gate50_20260801_2231/input/seed_c/crt_seed_c_gate50.jsonl` |
| seed_d | wtq | 4344 | 250 | 50 | 4044 | 50 | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_multiseed_gate50_20260801_2231/input/seed_d/wtq_seed_d_gate50.jsonl` |
| seed_d | tabfact | 12779 | 250 | 50 | 12479 | 50 | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_multiseed_gate50_20260801_2231/input/seed_d/tabfact_seed_d_gate50.jsonl` |
| seed_d | crt | 728 | 250 | 50 | 428 | 50 | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_multiseed_gate50_20260801_2231/input/seed_d/crt_seed_d_gate50.jsonl` |

Sampling rule: deterministic shuffle over the full dataset with fixed seed, after excluding frozen full200, coarse diagnostic Gate-50, P4b new-seed Gate-50, targeted affected slices, and prior seeds in this package.

Execution is pending because the local Qwen3-32B endpoints were unavailable when this package was created.
