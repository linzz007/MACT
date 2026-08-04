#!/usr/bin/env bash
set -euo pipefail

RUN_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MYAGENT_ROOT="${MYAGENT_ROOT:-/home/ubuntu/lzz/MyAgent}"

export LOCAL_VLLM_API_KEY="${LOCAL_VLLM_API_KEY:-local-vllm-key-change-me}"
export SERVED_MODEL_NAME="${SERVED_MODEL_NAME:-qwen3-32b-local}"
export VLLM_ENDPOINTS="${VLLM_ENDPOINTS:-http://127.0.0.1:8000/v1}"

if command -v conda >/dev/null 2>&1; then
  # shellcheck disable=SC1091
  source "$(conda info --base)/etc/profile.d/conda.sh"
  conda activate "${CONDA_ENV:-lzz-agent}"
fi

python "$RUN_DIR/build_probe_inputs.py"

run_task() {
  local task="$1"
  local mact_avg_tokens="$2"
  local dataset_path="$RUN_DIR/input/${task}_e3_boundary_budget_probe.jsonl"

  python "$MYAGENT_ROOT/scripts/server/run_sharded_tqa.py" \
    --repo-root "$MYAGENT_ROOT" \
    --tasks "$task" \
    --"${task}"-dataset "$dataset_path" \
    --endpoints "$VLLM_ENDPOINTS" \
    --model "$SERVED_MODEL_NAME" \
    --output-root "$RUN_DIR/myagent_max_replan5" \
    --api-key-env LOCAL_VLLM_API_KEY \
    --api-timeout 240 \
    --api-max-retries 5 \
    --temperature 0 \
    --max-tokens 2048 \
    --mact-avg-tokens "$mact_avg_tokens" \
    --max-replan 5 \
    --collaboration-mode selective \
    --resume
}

run_task wtq 10508.03
run_task tabfact 10830.825
run_task crt 12809.985

python "$RUN_DIR/summarize_probe.py"
