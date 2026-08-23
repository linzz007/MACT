#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "usage: $0 <wtq|tabfact|crt>" >&2
  exit 2
fi

DATASET="$1"
case "$DATASET" in
  wtq)
    MACT_TASK=wtq
    ;;
  tabfact)
    MACT_TASK=scitab
    ;;
  crt)
    MACT_TASK=crt
    ;;
  *)
    echo "dataset must be wtq, tabfact, or crt" >&2
    exit 2
    ;;
esac

RUN_DIR=/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_seed_e_gate50_20260823
MYAGENT_ROOT=/home/ubuntu/lzz/MyAgent
MACT_ROOT=/home/ubuntu/lzz/MACT

source "$RUN_DIR/env.sh"
cd "$MYAGENT_ROOT"
source /home/ubuntu/miniconda3/etc/profile.d/conda.sh
conda activate lzz-agent

python scripts/server/run_mact_sharded_one_by_one.py \
  --myagent-root "$MYAGENT_ROOT" \
  --mact-root "$MACT_ROOT" \
  --dataset-path "$RUN_DIR/input/${DATASET}_seed_e_gate50.jsonl" \
  --output-path "$RUN_DIR/mact/${DATASET}_mact_seed_e_gate50.jsonl" \
  --log-dir "$RUN_DIR/logs/mact_${DATASET}" \
  --shard-dir "$RUN_DIR/mact_shards" \
  --task "$MACT_TASK" \
  --plan-model-name "$SERVED_MODEL_NAME" \
  --code-model-name "$SERVED_MODEL_NAME" \
  --model-provider openai_compatible \
  --endpoints "$VLLM_ENDPOINTS" \
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
  --temp-dir "$RUN_DIR/tmp/mact_${DATASET}" \
  --limit 50 \
  --resume
