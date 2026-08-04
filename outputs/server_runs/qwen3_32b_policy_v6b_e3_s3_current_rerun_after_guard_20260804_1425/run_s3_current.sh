#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "usage: $0 <seed_c|seed_d|all>" >&2
  exit 2
fi

SEED_ARG="$1"
case "$SEED_ARG" in
  seed_c|seed_d|all) ;;
  *)
    echo "seed argument must be seed_c, seed_d, or all" >&2
    exit 2
    ;;
esac

RUN_DIR=/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_e3_s3_current_rerun_after_guard_20260804_1425
SOURCE_RUN_DIR=/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_multiseed_gate50_20260801_2231
MYAGENT_ROOT=/home/ubuntu/lzz/MyAgent

export LOCAL_VLLM_API_KEY=${LOCAL_VLLM_API_KEY:-local-vllm-key-change-me}
export SERVED_MODEL_NAME=${SERVED_MODEL_NAME:-qwen3-32b-local}
export VLLM_ENDPOINTS=${VLLM_ENDPOINTS:-http://127.0.0.1:8000/v1,http://127.0.0.1:8001/v1}

cd "$MYAGENT_ROOT"
source /home/ubuntu/miniconda3/etc/profile.d/conda.sh
conda activate lzz-agent

run_seed() {
  local seed_label="$1"
  local output_root="$RUN_DIR/myagent_s3_after_guard/$seed_label"
  mkdir -p "$output_root" "$RUN_DIR/summary"

  python scripts/server/run_sharded_tqa.py \
    --repo-root . \
    --tasks wtq \
    --wtq-dataset "$SOURCE_RUN_DIR/input/$seed_label/wtq_${seed_label}_gate50.jsonl" \
    --endpoints "$VLLM_ENDPOINTS" \
    --model "$SERVED_MODEL_NAME" \
    --api-key-env LOCAL_VLLM_API_KEY \
    --output-root "$output_root" \
    --mact-avg-tokens 10508.03 \
    --max-replan 3 \
    --resume

  python scripts/server/run_sharded_tqa.py \
    --repo-root . \
    --tasks tabfact \
    --tabfact-dataset "$SOURCE_RUN_DIR/input/$seed_label/tabfact_${seed_label}_gate50.jsonl" \
    --endpoints "$VLLM_ENDPOINTS" \
    --model "$SERVED_MODEL_NAME" \
    --api-key-env LOCAL_VLLM_API_KEY \
    --output-root "$output_root" \
    --mact-avg-tokens 10830.825 \
    --max-replan 3 \
    --resume

  python scripts/server/run_sharded_tqa.py \
    --repo-root . \
    --tasks crt \
    --crt-dataset "$SOURCE_RUN_DIR/input/$seed_label/crt_${seed_label}_gate50.jsonl" \
    --endpoints "$VLLM_ENDPOINTS" \
    --model "$SERVED_MODEL_NAME" \
    --api-key-env LOCAL_VLLM_API_KEY \
    --output-root "$output_root" \
    --mact-avg-tokens 12809.985 \
    --max-replan 3 \
    --resume

  python "$RUN_DIR/summarize_s3_current.py" --seed "$seed_label"
}

if [[ "$SEED_ARG" == "all" ]]; then
  run_seed seed_c
  run_seed seed_d
  python "$RUN_DIR/summarize_s3_current.py" --combined
else
  run_seed "$SEED_ARG"
fi
