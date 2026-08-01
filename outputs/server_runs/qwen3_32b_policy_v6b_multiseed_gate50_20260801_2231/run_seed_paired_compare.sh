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
mkdir -p "$RUN_DIR/eval/$SEED_LABEL" "$RUN_DIR/summary"

python code/evaluate_results.py "$RUN_DIR/mact/$SEED_LABEL/wtq_mact_${SEED_LABEL}_gate50.jsonl" \
  --error_output "$RUN_DIR/eval/$SEED_LABEL/wtq_mact_${SEED_LABEL}_gate50_errors.jsonl" \
  > "$RUN_DIR/eval/$SEED_LABEL/wtq_mact_${SEED_LABEL}_gate50_eval.json"
python code/evaluate_results.py "$RUN_DIR/mact/$SEED_LABEL/tabfact_mact_${SEED_LABEL}_gate50.jsonl" \
  --error_output "$RUN_DIR/eval/$SEED_LABEL/tabfact_mact_${SEED_LABEL}_gate50_errors.jsonl" \
  > "$RUN_DIR/eval/$SEED_LABEL/tabfact_mact_${SEED_LABEL}_gate50_eval.json"
python code/evaluate_results.py "$RUN_DIR/mact/$SEED_LABEL/crt_mact_${SEED_LABEL}_gate50.jsonl" \
  --error_output "$RUN_DIR/eval/$SEED_LABEL/crt_mact_${SEED_LABEL}_gate50_errors.jsonl" \
  > "$RUN_DIR/eval/$SEED_LABEL/crt_mact_${SEED_LABEL}_gate50_eval.json"

python code/compare_blind_results.py \
  --myagent_wtq "$RUN_DIR/myagent_current/$SEED_LABEL/merged/wtq_qwen3-32b-local.jsonl" \
  --myagent_tabfact "$RUN_DIR/myagent_current/$SEED_LABEL/merged/tabfact_qwen3-32b-local.jsonl" \
  --myagent_crt "$RUN_DIR/myagent_current/$SEED_LABEL/merged/crt_qwen3-32b-local.jsonl" \
  --mact_wtq "$RUN_DIR/mact/$SEED_LABEL/wtq_mact_${SEED_LABEL}_gate50.jsonl" \
  --mact_tabfact "$RUN_DIR/mact/$SEED_LABEL/tabfact_mact_${SEED_LABEL}_gate50.jsonl" \
  --mact_crt "$RUN_DIR/mact/$SEED_LABEL/crt_mact_${SEED_LABEL}_gate50.jsonl" \
  --output "$RUN_DIR/summary/${SEED_LABEL}_paired_gate50_summary.json"

python "$RUN_DIR/render_seed_paired_summary.py" "$SEED_LABEL"
