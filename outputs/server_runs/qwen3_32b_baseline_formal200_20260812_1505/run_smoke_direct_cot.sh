#!/usr/bin/env bash
set -euo pipefail
MYAGENT_ROOT=/home/ubuntu/lzz/MyAgent
RUN_DIR=/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_baseline_formal200_20260812_1505
cd "$MYAGENT_ROOT"
source /home/ubuntu/miniconda3/etc/profile.d/conda.sh
conda activate lzz-agent
source "$RUN_DIR/env.sh"

python scripts/server/run_baseline_tqa.py \
  --repo-root . \
  --baseline direct_cot \
  --tasks wtq,tabfact,crt \
  --wtq-dataset "$RUN_DIR/input/smoke5/wtq.jsonl" \
  --tabfact-dataset "$RUN_DIR/input/smoke5/tabfact.jsonl" \
  --crt-dataset "$RUN_DIR/input/smoke5/crt.jsonl" \
  --endpoints "$BASELINE_ENDPOINTS" \
  --model "$SERVED_MODEL_NAME" \
  --api-key-env "$API_KEY_ENV" \
  --output-root "$RUN_DIR/direct_cot_smoke5" \
  --limit-per-task 5 \
  --thinking disabled \
  --temperature 0 \
  --max-tokens 1024 \
  --resume
