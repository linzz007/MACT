#!/usr/bin/env bash
set -euo pipefail
MYAGENT_ROOT=/home/ubuntu/lzz/MyAgent
RUN_DIR=/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_baseline_formal200_20260812_1505
cd "$MYAGENT_ROOT"
source /home/ubuntu/miniconda3/etc/profile.d/conda.sh
conda activate lzz-agent
source "$RUN_DIR/env.sh"

mkdir -p "$RUN_DIR/mact" "$RUN_DIR/logs" "$RUN_DIR/tmp" "$RUN_DIR/mact_shards"
python scripts/server/run_mact_sharded_one_by_one.py \
  --mact-root /home/ubuntu/lzz/MACT \
  --dataset-path "$RUN_DIR/input/formal200/wtq.jsonl" \
  --output-path "$RUN_DIR/mact/wtq_mact_formal200.jsonl" \
  --log-dir "$RUN_DIR/logs/mact_wtq_sharded" \
  --shard-dir "$RUN_DIR/mact_shards" \
  --task wtq \
  --plan-model-name "$SERVED_MODEL_NAME" \
  --code-model-name "$SERVED_MODEL_NAME" \
  --model-provider openai_compatible \
  --endpoints "$BASELINE_ENDPOINTS" \
  --api-key-env "$API_KEY_ENV" \
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
  --limit 200 \
  --resume
