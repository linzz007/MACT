#!/usr/bin/env bash
set -euo pipefail

PATENT_RUN_DIR=/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155
P4B_RUN_DIR=/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305
E3_RUN_DIR=/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_multiseed_gate50_20260801_2231

PHASE="all"
SKIP_HEALTHCHECK="0"
CHECKPOINT="0"

usage() {
  cat <<'EOF'
usage: run_remaining_qwen3_patent_queue.sh [--phase all|wtq|e3|seed_c|seed_d] [--skip-healthcheck] [--checkpoint]

Runs the remaining Qwen3-32B patent-evidence queue with stop rules:
  wtq    Run WTQ targeted fresh, then P4b WTQ after-fix full50 only if fresh passes.
  seed_c Run Seed-C MyAgent Gate-50, then paired MACT only if current-only passes.
  seed_d Run Seed-D MyAgent Gate-50, then paired MACT only if current-only passes.
  e3     Run seed_c and seed_d.
  all    Run wtq, then e3.

Environment:
  VLLM_ENDPOINTS          Comma-separated OpenAI-compatible endpoints.
                          Default: http://127.0.0.1:8000/v1
  LOCAL_VLLM_API_KEY      Default: local-vllm-key-change-me
  SERVED_MODEL_NAME       Default: qwen3-32b-local

Use --checkpoint to commit and push MACT run-directory artifacts after each
completed phase. The MyAgent PRD still needs to be updated manually after fresh
numeric results are produced.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --phase)
      shift
      if [[ $# -eq 0 ]]; then
        echo "missing value after --phase" >&2
        exit 2
      fi
      PHASE="$1"
      shift
      ;;
    --skip-healthcheck)
      SKIP_HEALTHCHECK="1"
      shift
      ;;
    --checkpoint)
      CHECKPOINT="1"
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    all|wtq|e3|seed_c|seed_d)
      PHASE="$1"
      shift
      ;;
    *)
      echo "unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

case "$PHASE" in
  all|wtq|e3|seed_c|seed_d) ;;
  *)
    echo "phase must be all, wtq, e3, seed_c, or seed_d" >&2
    exit 2
    ;;
esac

export LOCAL_VLLM_API_KEY=${LOCAL_VLLM_API_KEY:-local-vllm-key-change-me}
export SERVED_MODEL_NAME=${SERVED_MODEL_NAME:-qwen3-32b-local}
export VLLM_ENDPOINTS=${VLLM_ENDPOINTS:-http://127.0.0.1:8000/v1}
export API_BASE_URL=${API_BASE_URL:-${VLLM_ENDPOINTS%%,*}}

split_endpoints() {
  local endpoints_csv="$1"
  IFS=',' read -r -a ENDPOINT_ARRAY <<< "$endpoints_csv"
}

first_endpoint() {
  split_endpoints "$VLLM_ENDPOINTS"
  printf '%s\n' "${ENDPOINT_ARRAY[0]}"
}

second_or_first_endpoint() {
  split_endpoints "$VLLM_ENDPOINTS"
  if [[ ${#ENDPOINT_ARRAY[@]} -ge 2 ]]; then
    printf '%s\n' "${ENDPOINT_ARRAY[1]}"
  else
    printf '%s\n' "${ENDPOINT_ARRAY[0]}"
  fi
}

healthcheck_endpoints() {
  local endpoints_csv="$1"
  split_endpoints "$endpoints_csv"
  for endpoint in "${ENDPOINT_ARRAY[@]}"; do
    endpoint="${endpoint%/}"
    echo "checking ${endpoint}/models"
    curl -fsS --max-time 10 \
      -H "Authorization: Bearer ${LOCAL_VLLM_API_KEY}" \
      "${endpoint}/models" >/dev/null
  done
}

require_targeted_fresh_pass() {
  python - "$P4B_RUN_DIR/p4b_wtq_targeted_fresh_summary.json" <<'PY'
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
if not path.exists():
    raise SystemExit(f"missing targeted fresh summary: {path}")
summary = json.loads(path.read_text(encoding="utf-8"))
fresh = summary.get("fresh") or {}
coverage = summary.get("coverage") or {}
decision = summary.get("decision")
correct = int(fresh.get("correct") or 0)
rows = int(fresh.get("rows") or 0)
failed = int(fresh.get("num_failed_exec") or 0)
missing = int(fresh.get("num_missing_answer") or 0)
merged_rows = int(coverage.get("merged_rows") or 0)
eval_rows = int(coverage.get("eval_rows") or 0)
if decision != "pass" or rows != 9 or merged_rows != 9 or eval_rows != 9 or failed or missing or correct < 7:
    raise SystemExit(
        "WTQ targeted fresh did not pass: "
        f"decision={decision!r}, correct={correct}/{rows}, "
        f"merged/eval={merged_rows}/{eval_rows}, failed/missing={failed}/{missing}"
    )
print(f"WTQ targeted fresh passed: {correct}/{rows}, failed/missing={failed}/{missing}")
PY
}

require_seed_current_pass() {
  local seed_label="$1"
  python - "$E3_RUN_DIR/summary/${seed_label}_myagent_gate50_summary.json" <<'PY'
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
if not path.exists():
    raise SystemExit(f"missing seed MyAgent summary: {path}")
summary = json.loads(path.read_text(encoding="utf-8"))
decision = summary.get("decision")
overall = summary.get("overall") or {}
if decision != "run_paired_mact":
    raise SystemExit(
        "Seed current-only gate stopped before paired MACT: "
        f"{path.name} decision={decision!r}, "
        f"overall={overall.get('correct')}/{overall.get('rows')}"
    )
print(
    "Seed current-only gate passed:",
    path.name,
    f"overall={overall.get('correct')}/{overall.get('rows')}",
    f"token_ratio={overall.get('token_ratio_to_mact_full200_weighted')}",
)
PY
}

report_paired_summary() {
  local seed_label="$1"
  local summary_json="$E3_RUN_DIR/summary/${seed_label}_paired_gate50_summary.json"
  python - "$summary_json" <<'PY'
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
if not path.exists():
    raise SystemExit(f"missing paired summary: {path}")
summary = json.loads(path.read_text(encoding="utf-8"))
overall = summary.get("overall") or {}
my = overall.get("myagent") or {}
mact = overall.get("mact") or {}
rows = int(my.get("num_samples") or 0)
my_correct = int(round(float(my.get("primary_accuracy") or 0.0) * rows))
mact_correct = int(round(float(mact.get("primary_accuracy") or 0.0) * rows))
print(
    f"{path.name}: MyAgent {my_correct}/{rows} vs MACT {mact_correct}/{rows}, "
    f"accepted={summary.get('accepted')}, "
    f"token_ratio={summary.get('token_ratio_myagent_to_mact')}"
)
PY
}

checkpoint_run_dir() {
  local run_dir="$1"
  local message="$2"
  if [[ "$CHECKPOINT" != "1" ]]; then
    return 0
  fi
  bash "$run_dir/checkpoint_to_git.sh" --commit "$message" --push
}

run_wtq_phase() {
  echo "== WTQ targeted fresh + after-fix full50 =="
  if [[ "$SKIP_HEALTHCHECK" != "1" ]]; then
    healthcheck_endpoints "$VLLM_ENDPOINTS"
  fi

  bash "$P4B_RUN_DIR/run_myagent_wtq_targeted_fix_slice.sh"
  require_targeted_fresh_pass
  checkpoint_run_dir "$P4B_RUN_DIR" "checkpoint: wtq targeted fresh validation"

  bash "$P4B_RUN_DIR/run_myagent_wtq_after_targeted_fix_full50.sh"
  checkpoint_run_dir "$P4B_RUN_DIR" "checkpoint: wtq after-targeted full50 validation"

  echo "WTQ phase completed. Update the PRD and formal result table before making final claims."
}

run_seed_phase() {
  local seed_label="$1"
  echo "== E3 ${seed_label} MyAgent current-only Gate-50 =="
  if [[ "$SKIP_HEALTHCHECK" != "1" ]]; then
    healthcheck_endpoints "$VLLM_ENDPOINTS"
  fi

  bash "$E3_RUN_DIR/run_seed_myagent_gate50.sh" "$seed_label"
  require_seed_current_pass "$seed_label"
  checkpoint_run_dir "$E3_RUN_DIR" "checkpoint: e3 ${seed_label} myagent gate50"

  echo "== E3 ${seed_label} paired MACT Gate-50 =="
  local endpoint_a
  local endpoint_b
  endpoint_a="$(first_endpoint)"
  endpoint_b="$(second_or_first_endpoint)"
  bash "$E3_RUN_DIR/run_seed_mact_gate50.sh" "$seed_label" wtq "$endpoint_a"
  bash "$E3_RUN_DIR/run_seed_mact_gate50.sh" "$seed_label" tabfact "$endpoint_b"
  bash "$E3_RUN_DIR/run_seed_mact_gate50.sh" "$seed_label" crt "$endpoint_a"
  bash "$E3_RUN_DIR/run_seed_paired_compare.sh" "$seed_label"
  report_paired_summary "$seed_label"
  checkpoint_run_dir "$E3_RUN_DIR" "checkpoint: e3 ${seed_label} paired gate50"

  echo "E3 ${seed_label} completed. Update the PRD and formal result table before making final claims."
}

echo "Patent package: $PATENT_RUN_DIR"
echo "Phase: $PHASE"
echo "VLLM_ENDPOINTS: $VLLM_ENDPOINTS"
echo "Checkpoint after phases: $CHECKPOINT"

case "$PHASE" in
  wtq)
    run_wtq_phase
    ;;
  seed_c|seed_d)
    run_seed_phase "$PHASE"
    ;;
  e3)
    run_seed_phase seed_c
    run_seed_phase seed_d
    ;;
  all)
    run_wtq_phase
    run_seed_phase seed_c
    run_seed_phase seed_d
    ;;
esac

echo "Queue phase finished."
