#!/usr/bin/env bash
set -euo pipefail
shopt -s nullglob

RUN_DIR=/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6c_e3_s4_paired_mact_20260804_1626
cd /home/ubuntu/lzz/MACT

git add -f \
  "$RUN_DIR/README.md" \
  "$RUN_DIR/vllm.env" \
  "$RUN_DIR/run_mact_dataset.sh" \
  "$RUN_DIR/summarize_s4_paired.py" \
  "$RUN_DIR/checkpoint_to_git.sh" \
  "$RUN_DIR"/progress_snapshot_*.md

if [[ -d "$RUN_DIR/mact" ]]; then
  git add -f "$RUN_DIR/mact"
fi
if [[ -d "$RUN_DIR/logs" ]]; then
  git add -f "$RUN_DIR/logs"
fi
if [[ -d "$RUN_DIR/eval" ]]; then
  git add -f "$RUN_DIR/eval"
fi
if [[ -d "$RUN_DIR/summary" ]]; then
  git add -f "$RUN_DIR/summary"
fi

if [[ "${1:-}" == "--commit" ]]; then
  if [[ $# -lt 2 ]]; then
    echo "usage: $0 [--commit MESSAGE] [--push]" >&2
    exit 2
  fi
  COMMIT_MESSAGE="$2"
  git commit -m "$COMMIT_MESSAGE"
  shift 2
fi

if [[ "${1:-}" == "--push" ]]; then
  git push origin main
fi
