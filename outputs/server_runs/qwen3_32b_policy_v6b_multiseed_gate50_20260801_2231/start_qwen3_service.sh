#!/usr/bin/env bash
set -euo pipefail

GPU_SET="${1:-6,7}"
PORT="${2:-8000}"
RUN_DIR=/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_multiseed_gate50_20260801_2231
source "$RUN_DIR/vllm.env"
export CUDA_VISIBLE_DEVICES="$GPU_SET"

exec /home/ubuntu/miniconda3/envs/lzz-agent/bin/vllm serve /home/ubuntu/models/Qwen3-32B \
  --host 0.0.0.0 \
  --port "$PORT" \
  --api-key "$LOCAL_VLLM_API_KEY" \
  --served-model-name "$SERVED_MODEL_NAME" \
  --tensor-parallel-size 2 \
  --max-model-len 8192 \
  --gpu-memory-utilization 0.88 \
  --dtype auto \
  --trust-remote-code
