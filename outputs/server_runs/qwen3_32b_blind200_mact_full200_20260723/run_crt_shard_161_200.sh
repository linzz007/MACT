#!/usr/bin/env bash
set -euo pipefail

cd /home/ubuntu/lzz/MyAgent
source /home/ubuntu/miniconda3/etc/profile.d/conda.sh
conda activate lzz-agent
source /home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_blind200_mact_full200_20260723/qwen3_32b_4gpu_2svc.env

RUN_ROOT=/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_blind200_mact_full200_20260723
mkdir -p "${RUN_ROOT}/logs" "${RUN_ROOT}/tmp_shard_161_200"
exec >> "${RUN_ROOT}/logs/crt_shard_161_200_stdout.log" 2>&1

date "+START_CRT_SHARD_161_200 %F %T %Z"
python scripts/server/run_mact_one_by_one.py \
  --mact-root /home/ubuntu/lzz/MACT \
  --dataset-path "${RUN_ROOT}/shards/crt_161_200.jsonl" \
  --output-path "${RUN_ROOT}/crt_mact_full200_shard_161_200.jsonl" \
  --log-path "${RUN_ROOT}/logs/crt_mact_full200_shard_161_200.log" \
  --task crt \
  --plan-model-name "${SERVED_MODEL_NAME}" \
  --code-model-name "${SERVED_MODEL_NAME}" \
  --model-provider openai_compatible \
  --api-base http://127.0.0.1:8001/v1 \
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
  --temp-dir "${RUN_ROOT}/tmp_shard_161_200" \
  --limit 40 \
  --resume
date "+END_CRT_SHARD_161_200 %F %T %Z"
