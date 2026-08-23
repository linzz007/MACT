#!/usr/bin/env bash
set -euo pipefail

RUN_DIR=/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_seed_e_gate50_20260823
MYAGENT_ROOT=/home/ubuntu/lzz/MyAgent

cd "$MYAGENT_ROOT"
source /home/ubuntu/miniconda3/etc/profile.d/conda.sh
conda activate lzz-agent
mkdir -p "$RUN_DIR/eval"

python code/evaluate_results.py "$RUN_DIR/mact/wtq_mact_seed_e_gate50.jsonl" \
  --error_output "$RUN_DIR/eval/wtq_mact_seed_e_gate50_errors.jsonl" \
  > "$RUN_DIR/eval/wtq_mact_seed_e_gate50_eval.json"
python code/evaluate_results.py "$RUN_DIR/mact/tabfact_mact_seed_e_gate50.jsonl" \
  --error_output "$RUN_DIR/eval/tabfact_mact_seed_e_gate50_errors.jsonl" \
  > "$RUN_DIR/eval/tabfact_mact_seed_e_gate50_eval.json"
python code/evaluate_results.py "$RUN_DIR/mact/crt_mact_seed_e_gate50.jsonl" \
  --error_output "$RUN_DIR/eval/crt_mact_seed_e_gate50_errors.jsonl" \
  > "$RUN_DIR/eval/crt_mact_seed_e_gate50_eval.json"

python code/compare_blind_results.py \
  --myagent_wtq "$RUN_DIR/myagent_seed_e/merged/wtq_qwen3-32b-local.jsonl" \
  --myagent_tabfact "$RUN_DIR/myagent_seed_e/merged/tabfact_qwen3-32b-local.jsonl" \
  --myagent_crt "$RUN_DIR/myagent_seed_e/merged/crt_qwen3-32b-local.jsonl" \
  --mact_wtq "$RUN_DIR/mact/wtq_mact_seed_e_gate50.jsonl" \
  --mact_tabfact "$RUN_DIR/mact/tabfact_mact_seed_e_gate50.jsonl" \
  --mact_crt "$RUN_DIR/mact/crt_mact_seed_e_gate50.jsonl" \
  --output "$RUN_DIR/seed_e_paired_gate50_summary.json"

python "$RUN_DIR/summarize_seed_e_paired.py"
