#!/usr/bin/env bash
set -euo pipefail
RUN_DIR=/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305
MYAGENT_ROOT=/home/ubuntu/lzz/MyAgent
MACT_ROOT=/home/ubuntu/lzz/MACT
source "$RUN_DIR/vllm.env"
cd "$MYAGENT_ROOT"
source /home/ubuntu/miniconda3/etc/profile.d/conda.sh
conda activate lzz-agent
mkdir -p "$RUN_DIR/mact" "$RUN_DIR/logs" "$RUN_DIR/tmp"
python scripts/server/run_mact_one_by_one.py \
  --mact-root "$MACT_ROOT" \
  --dataset-path "$RUN_DIR/input/crt_newseed_gate50.jsonl" \
  --output-path "$RUN_DIR/mact/crt_mact_newseed_gate50.jsonl" \
  --log-path "$RUN_DIR/logs/mact_crt_newseed_gate50.log" \
  --task crt \
  --plan-model-name "$SERVED_MODEL_NAME" \
  --code-model-name "$SERVED_MODEL_NAME" \
  --model-provider openai_compatible \
  --api-base "$API_BASE_URL" \
  --api-key-env LOCAL_VLLM_API_KEY \
  --thinking disabled \
  --temperature 0 \
  --max-tokens 2048 \
  --api-timeout 180 \
  --api-max-retries 5 \
  --plan-sample 1 \
  --code-sample 1 \
  --max-step 3 \
  --max-actual-step 3 \
  --temp-dir "$RUN_DIR/tmp" \
  --limit 50 \
  --resume
