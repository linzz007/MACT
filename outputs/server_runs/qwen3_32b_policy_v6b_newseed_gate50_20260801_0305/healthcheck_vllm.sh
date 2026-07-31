#!/usr/bin/env bash
set -euo pipefail
RUN_DIR=/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305
source "$RUN_DIR/vllm.env"
curl -fsS \
  -H "Authorization: Bearer $LOCAL_VLLM_API_KEY" \
  "$API_BASE_URL/models" | tee "$RUN_DIR/healthcheck_vllm_models.json"
