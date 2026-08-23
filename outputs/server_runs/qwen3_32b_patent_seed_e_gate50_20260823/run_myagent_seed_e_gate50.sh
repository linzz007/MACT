#!/usr/bin/env bash
set -euo pipefail

RUN_DIR=/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_seed_e_gate50_20260823
MYAGENT_ROOT=/home/ubuntu/lzz/MyAgent

source "$RUN_DIR/env.sh"
cd "$MYAGENT_ROOT"
source /home/ubuntu/miniconda3/etc/profile.d/conda.sh
conda activate lzz-agent

python scripts/server/run_sharded_tqa.py \
  --repo-root . \
  --tasks wtq,tabfact,crt \
  --wtq-dataset "$RUN_DIR/input/wtq_seed_e_gate50.jsonl" \
  --tabfact-dataset "$RUN_DIR/input/tabfact_seed_e_gate50.jsonl" \
  --crt-dataset "$RUN_DIR/input/crt_seed_e_gate50.jsonl" \
  --endpoints "$VLLM_ENDPOINTS" \
  --model "$SERVED_MODEL_NAME" \
  --api-key-env "$API_KEY_ENV" \
  --output-root "$RUN_DIR/myagent_seed_e" \
  --limit-per-task 50 \
  --max-replan 3 \
  --mact-avg-tokens 11318.89 \
  --thinking disabled \
  --temperature 0 \
  --max-tokens 2048 \
  --resume
