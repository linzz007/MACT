# Qwen3-32B E3 S3 Current-Only Rerun After Guard

Created: 2026-08-04 14:25 CST

Purpose: rerun E3 Seed-C/Seed-D current-only Gate-50 with the current MyAgent
gold-free semantic guards after S2 passed. This package does not overwrite the
original E3 boundary run at:

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_multiseed_gate50_20260801_2231/
```

Input source:

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_multiseed_gate50_20260801_2231/input/seed_c/
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_multiseed_gate50_20260801_2231/input/seed_d/
```

Output root:

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_e3_s3_current_rerun_after_guard_20260804_1425/myagent_s3_after_guard/
```

Run:

```bash
export VLLM_ENDPOINTS=http://127.0.0.1:8000/v1,http://127.0.0.1:8001/v1
bash run_s3_current.sh all
```

Gate rule: each seed passes current-only only if WTQ >= 35/50, TabFact >=
45/50, CRT >= 30/50, token ratio < 1.0 for every dataset, and failed/missing
are 0/0. Paired MACT is still not run here; paired runtime is considered only
if both Seed-C and Seed-D pass this S3 current-only gate.

Final result:

```text
Seed-C: 118/150, weighted token ratio 0.6073, failed/missing 0/0,
        decision=s3_seed_pass_run_paired_mact_candidate
Seed-D:  97/150, weighted token ratio 0.5659, failed/missing 0/0,
        decision=s3_seed_stop_or_inspect
Combined: 215/300, weighted token ratio 0.5866, failed/missing 0/0,
        decision=s3_stop_or_inspect_boundary_remains
```

Interpretation: S2 guards improved Seed-C enough to pass the current-only gate,
but Seed-D remains below the WTQ and TabFact thresholds. This run is therefore
boundary evidence with clear token advantage, not multi-seed stability closure;
paired MACT is not started from this S3 result.

Summary artifacts:

```text
summary/seed_c_s3_current_summary.json
summary/seed_c_s3_current_summary.md
summary/seed_d_s3_current_summary.json
summary/seed_d_s3_current_summary.md
summary/e3_s3_current_combined_summary.json
summary/e3_s3_current_combined_summary.md
```
