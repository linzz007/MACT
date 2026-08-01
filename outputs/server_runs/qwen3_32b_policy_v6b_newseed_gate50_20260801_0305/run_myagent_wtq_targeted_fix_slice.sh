#!/usr/bin/env bash
set -euo pipefail

RUN_DIR=/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305
MYAGENT_ROOT=/home/ubuntu/lzz/MyAgent

source "$RUN_DIR/vllm.env"
cd "$MYAGENT_ROOT"
source /home/ubuntu/miniconda3/etc/profile.d/conda.sh
conda activate lzz-agent

mkdir -p "$RUN_DIR/myagent_wtq_targeted_fix" "$RUN_DIR/logs"

python scripts/server/run_sharded_tqa.py \
  --repo-root . \
  --tasks wtq \
  --wtq-dataset "$RUN_DIR/input/wtq_p4b_targeted_fix_affected_slice.jsonl" \
  --endpoints "$VLLM_ENDPOINTS" \
  --model "$SERVED_MODEL_NAME" \
  --api-key-env LOCAL_VLLM_API_KEY \
  --output-root "$RUN_DIR/myagent_wtq_targeted_fix" \
  --mact-avg-tokens 10508.03 \
  --max-replan 3 \
  --resume
