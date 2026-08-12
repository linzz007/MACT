#!/usr/bin/env bash
set -euo pipefail
MYAGENT_ROOT=/home/ubuntu/lzz/MyAgent
RUN_DIR=/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_baseline_formal200_20260812_1505
cd "$MYAGENT_ROOT"
source /home/ubuntu/miniconda3/etc/profile.d/conda.sh
conda activate lzz-agent
source "$RUN_DIR/env.sh"

IFS="," read -r -a ENDPOINT_ARRAY <<< "$BASELINE_ENDPOINTS"
for API_BASE in "${ENDPOINT_ARRAY[@]}"; do
  echo "[healthcheck] $API_BASE"
  curl -sS -H "Authorization: Bearer ${!API_KEY_ENV}" "$API_BASE/models" >/dev/null
done
