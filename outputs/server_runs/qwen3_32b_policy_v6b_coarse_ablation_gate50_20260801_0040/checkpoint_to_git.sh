#!/usr/bin/env bash
set -euo pipefail
cd /home/ubuntu/lzz/MACT
git add -f outputs/server_runs/qwen3_32b_policy_v6b_coarse_ablation_gate50_20260801_0040
if [[ "${1:-}" == "--commit" ]]; then
  msg="${2:-checkpoint: qwen3 coarse ablation gate50}"
  git commit -m "$msg"
  git push
fi
