# Qwen3-32B E3 Guard Validation Current Baseline

This directory runs the current MyAgent policy on the 30-row E3 S2 guard-validation input package.

It is a baseline artifact only:

- no MyAgent code changes are introduced here;
- `max_replan=3` matches the current policy seed-run budget;
- the result is used to decide which P0/P1 gold-free semantic guard to implement next.

Input package:

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_e3_guard_validation_inputs_20260804_1128/
```

Runner:

```bash
export VLLM_ENDPOINTS=http://127.0.0.1:8000/v1,http://127.0.0.1:8001/v1
bash /home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_e3_guard_validation_current_baseline_20260804_1142/run_current_baseline.sh
```

Expected summary:

```text
summary/e3_guard_validation_current_baseline_summary.json
summary/e3_guard_validation_current_baseline_summary.md
```
