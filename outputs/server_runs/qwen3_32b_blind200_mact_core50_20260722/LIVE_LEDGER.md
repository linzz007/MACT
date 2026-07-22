# Qwen3-32B Blind200 MACT Core50 Live Ledger

Last updated: 2026-07-22 10:33:19 CST

## Goal

Use the current Qwen3-32B myAgent outputs and same-split MACT outputs to build a staged, expert-ready paired evaluation without running every full dataset for every model.

Current stage: `S3 paired core`, blind200 first 50 samples per dataset, MACT side only, paired against already-completed myAgent blind200 outputs.

## Repositories

| repo | path | branch | remote |
|---|---|---|---|
| MyAgent | `/home/ubuntu/lzz/MyAgent` | `codex/selective-risk-collaboration` | `git@github.com:linzz007/MyAgent.git` |
| MACT | `/home/ubuntu/lzz/MACT` | `main` | `git@github.com:linzz007/MACT.git` |

## Canonical Run Directory

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_blind200_mact_core50_20260722
```

All MACT test results for this run must remain under this directory. The directory is ignored by MACT's default `.gitignore`, so result files are synced with explicit `git add -f`.

## Inputs

| dataset | MACT input | limit | task |
|---|---|---:|---|
| WTQ | `/home/ubuntu/lzz/MyAgent/datasets_ready/blind_holdout_200_v1_2026-06-27/wtq.jsonl` | 50 | `wtq` |
| TabFact | `/home/ubuntu/lzz/MyAgent/datasets_ready/blind_holdout_200_v1_2026-06-27/tabfact.jsonl` | 50 | `scitab` |
| CRT | `/home/ubuntu/lzz/MyAgent/datasets_ready/blind_holdout_200_v1_2026-06-27/crt.jsonl` | 50 | `crt` |

## Paired myAgent Outputs

| dataset | myAgent output |
|---|---|
| WTQ | `/home/ubuntu/lzz/MyAgent/outputs/server_runs/qwen3_32b_current_blind200_wtq200_shortcutfix2_20260721/merged/wtq_qwen3-32b-local.jsonl` |
| TabFact | `/home/ubuntu/lzz/MyAgent/outputs/server_runs/qwen3_32b_current_blind200_20260721/merged/tabfact_qwen3-32b-local.jsonl` |
| CRT | `/home/ubuntu/lzz/MyAgent/outputs/server_runs/qwen3_32b_current_blind200_20260721/merged/crt_qwen3-32b-local.jsonl` |

## Model Service

| item | value |
|---|---|
| model | `/home/ubuntu/models/Qwen3-32B` |
| served name | `qwen3-32b-local` |
| endpoint | `http://127.0.0.1:8000/v1` |
| GPUs | `5,6` |
| max model length | `8192` |
| healthcheck before run | `ok` |

## Run Command Pattern

Each dataset is run with:

```text
python scripts/server/run_mact_one_by_one.py
  --mact-root /home/ubuntu/lzz/MACT
  --dataset-path datasets_ready/blind_holdout_200_v1_2026-06-27/<dataset>.jsonl
  --output-path "$RUN_ROOT/<dataset>_mact_core50.jsonl"
  --log-path "$RUN_ROOT/logs/<dataset>_mact_core50.log"
  --task <wtq|scitab|crt>
  --plan-model-name "$SERVED_MODEL_NAME"
  --code-model-name "$SERVED_MODEL_NAME"
  --model-provider openai_compatible
  --api-base http://127.0.0.1:8000/v1
  --api-key-env LOCAL_VLLM_API_KEY
  --thinking disabled
  --temperature 0
  --max-tokens 2048
  --api-timeout 180
  --api-max-retries 5
  --plan-sample 1
  --code-sample 1
  --max-step 3
  --max-actual-step 3
  --temp-dir "$RUN_ROOT/tmp"
  --limit 50
  --resume
```

## Seed From Smoke5

The first 5 rows per dataset were copied from:

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_blind200_mact_smoke5_20260721
```

The copied IDs exactly match the first 5 IDs in each blind200 input. `--resume` continues from row 6, so the first 5 rows are not recomputed.

## Live Progress

| time CST | WTQ rows | TabFact rows | CRT rows | note |
|---|---:|---:|---:|---|
| 2026-07-22 09:44:09 | 5 | 5 | 5 | started core50 continuation |
| 2026-07-22 10:00:28 | 16 | 5 | 5 | WTQ running, all new rows so far `ok` |
| 2026-07-22 10:09:29 | 20 | 5 | 5 | WTQ checkpoint; critical error scan empty |
| 2026-07-22 10:13:28 | 22 | 5 | 5 | WTQ sample `nu-4299` failed with context length BadRequest |
| 2026-07-22 10:33:19 | 30 | 5 | 5 | WTQ checkpoint; failed/missing remains 1 row |

## Current Checks

| check | current status |
|---|---|
| row completeness | partial: WTQ 30/50, TabFact 5/50, CRT 5/50 |
| wrapper failures | WTQ 1 row: `nu-4299` |
| critical log scan | context length BadRequest found on WTQ `nu-4299` |
| known diagnostic | MACT internal `Halted: 1` currently appears on WTQ 3 rows and CRT 1 row; output rows are still preserved |

## Issues Found During Core50

### WTQ `nu-4299`: context length failure

Observed at 2026-07-22 10:13:28 CST.

```text
openai.BadRequestError: Error code: 400
You passed 6145 input tokens and requested 2048 output tokens.
The model's context length is only 8192 tokens, resulting in a maximum input length of 6144 tokens.
```

Wrapper behavior:

```text
[mact-one] wtq 22/50 failed
JSONL row preserved with exec_error=True and empty pred_answer
```

Current interpretation:

- This is not a vLLM outage; it is a prompt-budget boundary error under `VLLM_MAX_MODEL_LEN=8192` and MACT `--max-tokens 2048`.
- The row should be counted as MACT failed/missing in the paired table.
- If failures become frequent, rerun policy should be discussed before changing `--max-tokens`, because changing the budget mid-run would make the baseline less comparable.

## Sync Policy

Because the server environment may lose data, sync at these checkpoints:

1. Immediately after creating/updating this ledger.
2. After each dataset reaches 50 rows.
3. After final evaluator and paired comparison are written.

Files to sync from MACT with `git add -f`:

```text
outputs/server_runs/qwen3_32b_blind200_mact_core50_20260722/LIVE_LEDGER.md
outputs/server_runs/qwen3_32b_blind200_mact_core50_20260722/*_mact_core50.jsonl
outputs/server_runs/qwen3_32b_blind200_mact_core50_20260722/logs/*_mact_core50.log
```

Do not sync `tmp/`.

## Next Steps

1. Continue polling session `7668` until WTQ reaches 50 rows.
2. Push a new checkpoint after WTQ completes.
3. Continue TabFact and CRT under the same session.
4. Run `code/evaluate_results.py` on the three MACT outputs.
5. Pair by exact sample `id` against the myAgent outputs above.
6. Update this ledger and the MyAgent server report with final core50 numbers.
