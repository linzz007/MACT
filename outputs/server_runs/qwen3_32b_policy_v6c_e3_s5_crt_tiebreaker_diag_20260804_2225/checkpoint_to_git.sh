#!/usr/bin/env bash
set -euo pipefail

RUN_DIR=/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6c_e3_s5_crt_tiebreaker_diag_20260804_2225

cd /home/ubuntu/lzz/MACT
git add -f "$RUN_DIR"

if [[ "${1:-}" == "--commit" ]]; then
  if [[ $# -lt 2 ]]; then
    echo "usage: $0 --commit <message> [--push]" >&2
    exit 2
  fi
  message="$2"
  git commit -m "$message"
  if [[ "${3:-}" == "--push" ]]; then
    git push
  fi
elif [[ $# -gt 0 ]]; then
  echo "usage: $0 [--commit <message> [--push]]" >&2
  exit 2
fi
