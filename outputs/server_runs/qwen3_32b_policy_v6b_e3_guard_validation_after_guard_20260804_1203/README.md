# Qwen3-32B E3 S2 Guard Validation After-Guard Rerun

This run reruns the 30-row E3 S2 guard-validation input package after the
gold-free semantic guard changes in MyAgent.

- Input package: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_e3_guard_validation_inputs_20260804_1128`
- Output root: `myagent_after_guard`
- Model endpoints: `http://127.0.0.1:8000/v1`, `http://127.0.0.1:8001/v1`
- Model: `qwen3-32b-local`
- Decoding: temperature `0`, max tokens `2048`
- MyAgent mode: selective, max_replan `3`

The summary keeps the same fields as the current-policy baseline:
eval rows, merged rows, recovery, no-harm, failed/missing, token and elapsed
metrics.
