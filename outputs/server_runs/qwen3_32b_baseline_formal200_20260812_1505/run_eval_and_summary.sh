#!/usr/bin/env bash
set -euo pipefail
MYAGENT_ROOT=/home/ubuntu/lzz/MyAgent
RUN_DIR=/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_baseline_formal200_20260812_1505
cd "$MYAGENT_ROOT"
source /home/ubuntu/miniconda3/etc/profile.d/conda.sh
conda activate lzz-agent
source "$RUN_DIR/env.sh"

mkdir -p "$RUN_DIR/eval" "$RUN_DIR/summary"
for DATASET in wtq tabfact crt; do
  if [ -f "$RUN_DIR/mact/${DATASET}_mact_formal200.jsonl" ]; then
    python code/evaluate_results.py \
      "$RUN_DIR/mact/${DATASET}_mact_formal200.jsonl" \
      --error_output "$RUN_DIR/eval/${DATASET}_mact_formal200_errors.jsonl" \
      > "$RUN_DIR/eval/${DATASET}_mact_formal200_eval.json"
  fi
done
python scripts/server/summarize_baseline_experiment.py \
  --run-dir "$RUN_DIR"
