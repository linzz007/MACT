#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 || $# -gt 3 ]]; then
  echo "usage: $0 <seed_c|seed_d> <wtq|tabfact|crt> [api_base_url]" >&2
  exit 2
fi

SEED_LABEL="$1"
DATASET="$2"
case "$SEED_LABEL" in
  seed_c|seed_d) ;;
  *)
    echo "seed label must be seed_c or seed_d" >&2
    exit 2
    ;;
esac
case "$DATASET" in
  wtq|tabfact|crt) ;;
  *)
    echo "dataset must be wtq, tabfact, or crt" >&2
    exit 2
    ;;
esac

RUN_DIR=/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_multiseed_gate50_20260801_2231
MYAGENT_ROOT=/home/ubuntu/lzz/MyAgent
MACT_ROOT=/home/ubuntu/lzz/MACT
source "$RUN_DIR/vllm.env"
API_BASE="${3:-$API_BASE_URL}"

cd "$MYAGENT_ROOT"
source /home/ubuntu/miniconda3/etc/profile.d/conda.sh
conda activate lzz-agent
mkdir -p "$RUN_DIR/mact/$SEED_LABEL" "$RUN_DIR/logs/$SEED_LABEL" "$RUN_DIR/tmp/$SEED_LABEL"

python scripts/server/run_mact_one_by_one.py \
  --mact-root "$MACT_ROOT" \
  --dataset-path "$RUN_DIR/input/$SEED_LABEL/${DATASET}_${SEED_LABEL}_gate50.jsonl" \
  --output-path "$RUN_DIR/mact/$SEED_LABEL/${DATASET}_mact_${SEED_LABEL}_gate50.jsonl" \
  --log-path "$RUN_DIR/logs/$SEED_LABEL/mact_${DATASET}_${SEED_LABEL}_gate50.log" \
  --task "$DATASET" \
  --plan-model-name "$SERVED_MODEL_NAME" \
  --code-model-name "$SERVED_MODEL_NAME" \
  --model-provider openai_compatible \
  --api-base "$API_BASE" \
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
  --temp-dir "$RUN_DIR/tmp/$SEED_LABEL" \
  --limit 50 \
  --resume
