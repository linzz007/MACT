#!/usr/bin/env bash
set -euo pipefail
MACT_ROOT=/home/ubuntu/lzz/MACT
RUN_DIR=/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_baseline_formal200_20260812_1505
MESSAGE="${1:-results: checkpoint baseline formal200 package}"
cd "$MACT_ROOT"
RUN_REL="${RUN_DIR#$MACT_ROOT/}"
git add -f -- "$RUN_REL"
git commit -m "$MESSAGE"
git push origin HEAD
