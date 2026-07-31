#!/usr/bin/env bash
set -euo pipefail
MACT_ROOT=/home/ubuntu/lzz/MACT
RUN_DIR=/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305
COMMIT_MESSAGE=""
PUSH_AFTER_COMMIT="0"
PUSH_REMOTE="${PUSH_REMOTE:-origin}"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --commit)
      shift
      if [[ $# -eq 0 ]]; then
        echo "missing commit message after --commit" >&2
        exit 2
      fi
      COMMIT_MESSAGE="$1"
      shift
      ;;
    --push)
      PUSH_AFTER_COMMIT="1"
      shift
      ;;
    *)
      echo "unknown argument: $1" >&2
      echo "usage: $0 [--commit MESSAGE] [--push]" >&2
      exit 2
      ;;
  esac
done
cd "$MACT_ROOT"
case "$RUN_DIR" in
  "$MACT_ROOT"/*) RUN_REL=${RUN_DIR#"$MACT_ROOT"/} ;;
  *)
    echo "RUN_DIR is not under MACT_ROOT: $RUN_DIR" >&2
    exit 2
    ;;
esac
git add -f -- "$RUN_REL"
git status --short -- "$RUN_REL"
if [[ -n "$COMMIT_MESSAGE" ]]; then
  if git diff --cached --quiet -- "$RUN_REL"; then
    echo "No staged checkpoint changes under $RUN_REL"
  else
    git commit -m "$COMMIT_MESSAGE" -- "$RUN_REL"
  fi
  if [[ "$PUSH_AFTER_COMMIT" == "1" ]]; then
    BRANCH=$(git branch --show-current)
    git push "$PUSH_REMOTE" "$BRANCH"
  fi
else
  echo "Staged checkpoint for $RUN_REL"
  echo "Remote backup option: bash $RUN_DIR/checkpoint_to_git.sh --commit "checkpoint: p4 newseed stage" --push"
fi
