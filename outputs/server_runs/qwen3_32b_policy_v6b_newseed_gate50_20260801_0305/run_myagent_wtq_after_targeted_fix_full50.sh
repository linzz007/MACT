#!/usr/bin/env bash
set -euo pipefail

RUN_DIR=/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305
MYAGENT_ROOT=/home/ubuntu/lzz/MyAgent
FRESH_SUMMARY="$RUN_DIR/p4b_wtq_targeted_fresh_summary.json"

source "$RUN_DIR/vllm.env"
cd "$MYAGENT_ROOT"
source /home/ubuntu/miniconda3/etc/profile.d/conda.sh
conda activate lzz-agent

python - "$FRESH_SUMMARY" <<'PY'
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
if not path.exists():
    raise SystemExit(
        f"Missing targeted fresh summary: {path}. "
        "Run run_myagent_wtq_targeted_fix_slice.sh first."
    )
summary = json.loads(path.read_text(encoding="utf-8"))
if summary.get("decision") != "pass":
    raise SystemExit(
        f"Targeted fresh summary decision is {summary.get('decision')!r}, not 'pass'. "
        "Inspect fresh wrong IDs before running WTQ full50."
    )
fresh = summary.get("fresh") or {}
if int(fresh.get("num_failed_exec") or 0) or int(fresh.get("num_missing_answer") or 0):
    raise SystemExit("Targeted fresh summary contains failed/missing rows.")
print(
    "targeted fresh gate passed:",
    f"{fresh.get('correct')}/{fresh.get('rows')}",
)
PY

mkdir -p "$RUN_DIR/myagent_current_after_wtq_targeted_fix" "$RUN_DIR/logs"

python scripts/server/run_sharded_tqa.py \
  --repo-root . \
  --tasks wtq \
  --wtq-dataset "$RUN_DIR/input/wtq_newseed_gate50.jsonl" \
  --endpoints "$VLLM_ENDPOINTS" \
  --model "$SERVED_MODEL_NAME" \
  --api-key-env LOCAL_VLLM_API_KEY \
  --output-root "$RUN_DIR/myagent_current_after_wtq_targeted_fix" \
  --mact-avg-tokens 10508.03 \
  --max-replan 3 \
  --resume

bash "$RUN_DIR/run_p4b_after_wtq_targeted_eval_compare.sh"
