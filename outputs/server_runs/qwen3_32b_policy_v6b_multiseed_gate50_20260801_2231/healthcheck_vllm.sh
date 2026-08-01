#!/usr/bin/env bash
set -euo pipefail

RUN_DIR=/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_multiseed_gate50_20260801_2231
source "$RUN_DIR/vllm.env"

IFS=',' read -r -a ENDPOINTS <<< "$VLLM_ENDPOINTS"
for endpoint in "${ENDPOINTS[@]}"; do
  endpoint="${endpoint%/}"
  echo "checking ${endpoint}/models"
  curl -sS --max-time 10 \
    -H "Authorization: Bearer ${LOCAL_VLLM_API_KEY}" \
    "${endpoint}/models"
  echo
done
