#!/usr/bin/env bash
set -euo pipefail

export LOCAL_VLLM_API_KEY="${LOCAL_VLLM_API_KEY:-local-vllm-key-change-me}"
export SERVED_MODEL_NAME="${SERVED_MODEL_NAME:-qwen3-32b-local}"
export API_KEY_ENV="${API_KEY_ENV:-LOCAL_VLLM_API_KEY}"

# Current user constraint: run experiments only through the Qwen services on GPUs 4,5 and 6,7.
export VLLM_ENDPOINTS="${VLLM_ENDPOINTS:-http://127.0.0.1:8000/v1,http://127.0.0.1:8001/v1}"
