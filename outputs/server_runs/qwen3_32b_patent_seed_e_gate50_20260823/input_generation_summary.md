# Seed-E Gate-50 Input Generation

Run dir: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_seed_e_gate50_20260823`

Purpose: prepare a non-overlapping paired Gate-50 seed for Qwen3-32B MyAgent vs MACT stability validation.

| Dataset | Source Rows | Excluded IDs | Candidate Rows | Selected Rows | Input |
|---|---:|---:|---:|---:|---|
| wtq | 4344 | 533 | 3811 | 50 | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_seed_e_gate50_20260823/input/wtq_seed_e_gate50.jsonl` |
| tabfact | 12779 | 543 | 12236 | 50 | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_seed_e_gate50_20260823/input/tabfact_seed_e_gate50.jsonl` |
| crt | 728 | 459 | 269 | 50 | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_seed_e_gate50_20260823/input/crt_seed_e_gate50.jsonl` |

Sampling rule: deterministic shuffle over full dataset rows using seed `20260823`, after excluding Formal-200, ablation50, prior new-seed, targeted slices, and Seed-C/D inputs.

Execution status: prepared only. No model was called while generating this package.
