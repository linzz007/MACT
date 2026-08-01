#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "usage: $0 <seed_c|seed_d>" >&2
  exit 2
fi

SEED_LABEL="$1"
case "$SEED_LABEL" in
  seed_c|seed_d) ;;
  *)
    echo "seed label must be seed_c or seed_d" >&2
    exit 2
    ;;
esac

RUN_DIR=/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_multiseed_gate50_20260801_2231
MYAGENT_ROOT=/home/ubuntu/lzz/MyAgent
source "$RUN_DIR/vllm.env"
cd "$MYAGENT_ROOT"
source /home/ubuntu/miniconda3/etc/profile.d/conda.sh
conda activate lzz-agent
mkdir -p "$RUN_DIR/myagent_current/$SEED_LABEL" "$RUN_DIR/logs/$SEED_LABEL"

python scripts/server/run_sharded_tqa.py \
  --repo-root . \
  --tasks wtq \
  --wtq-dataset "$RUN_DIR/input/$SEED_LABEL/wtq_${SEED_LABEL}_gate50.jsonl" \
  --endpoints "$VLLM_ENDPOINTS" \
  --model "$SERVED_MODEL_NAME" \
  --api-key-env LOCAL_VLLM_API_KEY \
  --output-root "$RUN_DIR/myagent_current/$SEED_LABEL" \
  --mact-avg-tokens 10508.03 \
  --max-replan 3 \
  --resume

python scripts/server/run_sharded_tqa.py \
  --repo-root . \
  --tasks tabfact \
  --tabfact-dataset "$RUN_DIR/input/$SEED_LABEL/tabfact_${SEED_LABEL}_gate50.jsonl" \
  --endpoints "$VLLM_ENDPOINTS" \
  --model "$SERVED_MODEL_NAME" \
  --api-key-env LOCAL_VLLM_API_KEY \
  --output-root "$RUN_DIR/myagent_current/$SEED_LABEL" \
  --mact-avg-tokens 10830.825 \
  --max-replan 3 \
  --resume

python scripts/server/run_sharded_tqa.py \
  --repo-root . \
  --tasks crt \
  --crt-dataset "$RUN_DIR/input/$SEED_LABEL/crt_${SEED_LABEL}_gate50.jsonl" \
  --endpoints "$VLLM_ENDPOINTS" \
  --model "$SERVED_MODEL_NAME" \
  --api-key-env LOCAL_VLLM_API_KEY \
  --output-root "$RUN_DIR/myagent_current/$SEED_LABEL" \
  --mact-avg-tokens 12809.985 \
  --max-replan 3 \
  --resume

python "$RUN_DIR/summarize_seed_myagent.py" "$SEED_LABEL"
