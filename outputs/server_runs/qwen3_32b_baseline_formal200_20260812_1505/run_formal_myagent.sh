#!/usr/bin/env bash
set -euo pipefail
MYAGENT_ROOT=/home/ubuntu/lzz/MyAgent
RUN_DIR=/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_baseline_formal200_20260812_1505
cd "$MYAGENT_ROOT"
source /home/ubuntu/miniconda3/etc/profile.d/conda.sh
conda activate lzz-agent
source "$RUN_DIR/env.sh"

python scripts/server/run_sharded_tqa.py \
  --repo-root . \
  --tasks wtq,tabfact,crt \
  --wtq-dataset "$RUN_DIR/input/formal200/wtq.jsonl" \
  --tabfact-dataset "$RUN_DIR/input/formal200/tabfact.jsonl" \
  --crt-dataset "$RUN_DIR/input/formal200/crt.jsonl" \
  --endpoints "$BASELINE_ENDPOINTS" \
  --model "$SERVED_MODEL_NAME" \
  --api-key-env "$API_KEY_ENV" \
  --output-root "$RUN_DIR/myagent_formal200" \
  --limit-per-task 200 \
  --max-replan 3 \
  --mact-avg-tokens 47439.2633 \
  --thinking disabled \
  --temperature 0 \
  --max-tokens 2048 \
  --resume
