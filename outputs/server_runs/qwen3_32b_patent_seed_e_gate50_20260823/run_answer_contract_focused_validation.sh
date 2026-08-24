#!/usr/bin/env bash
set -euo pipefail

RUN_DIR=/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_seed_e_gate50_20260823
MYAGENT_ROOT=/home/ubuntu/lzz/MyAgent
OUTPUT_ROOT="$RUN_DIR/diagnostics/answer_contract_patch_focused_20260824"

source "$RUN_DIR/env.sh"
cd "$MYAGENT_ROOT"
source /home/ubuntu/miniconda3/etc/profile.d/conda.sh
conda activate lzz-agent

python scripts/server/run_sharded_tqa.py \
  --repo-root . \
  --tasks wtq,crt \
  --wtq-dataset "$RUN_DIR/input/diagnostic/seed_e_answer_contract_wtq.jsonl" \
  --crt-dataset "$RUN_DIR/input/diagnostic/seed_e_answer_contract_crt.jsonl" \
  --endpoints "$VLLM_ENDPOINTS" \
  --model "$SERVED_MODEL_NAME" \
  --api-key-env "$API_KEY_ENV" \
  --output-root "$OUTPUT_ROOT" \
  --max-replan 3 \
  --mact-avg-tokens 11318.89 \
  --thinking disabled \
  --temperature 0 \
  --max-tokens 2048 \
  --resume

python "$RUN_DIR/summarize_answer_contract_focused.py"
