#!/usr/bin/env bash
set -euo pipefail

RUN_ROOT=/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_blind200_mact_core100_20260722
mkdir -p "$RUN_ROOT/logs" "$RUN_ROOT/tmp"

exec >> "$RUN_ROOT/logs/tabfact_core100_resume_stdout.log" 2>&1
echo "$$" > "$RUN_ROOT/tabfact_resume.pid"

date "+RESUME_TABFACT %F %T %Z"

source /home/ubuntu/miniconda3/etc/profile.d/conda.sh
conda activate lzz-agent
cd /home/ubuntu/lzz/MyAgent
source configs/server/qwen3_32b_2gpu_local.env

status=0
start_seconds=$SECONDS
python scripts/server/run_mact_one_by_one.py \
  --mact-root /home/ubuntu/lzz/MACT \
  --dataset-path datasets_ready/blind_holdout_200_v1_2026-06-27/tabfact.jsonl \
  --output-path "$RUN_ROOT/tabfact_mact_core100.jsonl" \
  --log-path "$RUN_ROOT/logs/tabfact_mact_core100.log" \
  --task scitab \
  --plan-model-name "$SERVED_MODEL_NAME" \
  --code-model-name "$SERVED_MODEL_NAME" \
  --model-provider openai_compatible \
  --api-base http://127.0.0.1:8000/v1 \
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
  --temp-dir "$RUN_ROOT/tmp" \
  --limit 100 \
  --resume || status=$?
elapsed_seconds=$((SECONDS - start_seconds))

echo "TABFACT_ELAPSED_SECONDS $elapsed_seconds"
date "+END_TABFACT %F %T %Z status=$status"
exit "$status"
