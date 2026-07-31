#!/usr/bin/env bash
set -euo pipefail
export LOCAL_VLLM_API_KEY="${LOCAL_VLLM_API_KEY:-local-vllm-key-change-me}"
REPO_ROOT=/home/ubuntu/lzz/MyAgent
RUN_DIR=/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_coarse_ablation_gate50_20260801_0040
ENDPOINT=http://127.0.0.1:8000/v1
MODEL=qwen3-32b-local
VARIANT=no_strong_verification
COMMON_FLAGS=('--disable-strong-verification')
run_task() {
  local task="$1"
  local dataset="$2"
  local mact_avg="$3"
  python "$REPO_ROOT/scripts/server/run_sharded_tqa.py"     --repo-root "$REPO_ROOT"     --tasks "$task"     --${task}-dataset "$dataset"     --endpoints "$ENDPOINT"     --model "$MODEL"     --api-key-env LOCAL_VLLM_API_KEY     --output-root "$RUN_DIR/variants/$VARIANT"     --max-replan 3     --mact-avg-tokens "$mact_avg"     --resume     "${COMMON_FLAGS[@]}"
}
run_task wtq "$RUN_DIR/input/wtq_diagnostic_gate50.jsonl" 10508.03
run_task tabfact "$RUN_DIR/input/tabfact_diagnostic_gate50.jsonl" 10830.825
run_task crt "$RUN_DIR/input/crt_diagnostic_gate50.jsonl" 12809.985
