# Qwen3-32B Blind200 MACT Core100 Live Ledger

Last updated: 2026-07-23 01:22:10 CST

## Goal

Expand the completed blind50 paired core run to blind100, using the same Qwen3-32B service, same blind200 split, same evaluator, and same-ID pairing against already-completed myAgent blind200 outputs.

Current stage: `S4 paired expansion`, blind200 first 100 samples per dataset, MACT side only, paired against existing myAgent blind200 outputs.

## Repositories

| repo | path | branch | current baseline |
|---|---|---|---|
| MyAgent | `/home/ubuntu/lzz/MyAgent` | `codex/selective-risk-collaboration` | `adf915f Record Qwen3 blind core50 paired results` |
| MACT | `/home/ubuntu/lzz/MACT` | `main` | `32873a6 Checkpoint Qwen3 blind core100 WTQ row91` |

## Canonical Run Directory

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_blind200_mact_core100_20260722
```

All MACT test results for this run must remain under this directory. The directory is ignored by MACT's default `.gitignore`, so result files are synced with explicit `git add -f`.

## Inputs

| dataset | MACT input | limit | resume start |
|---|---|---:|---:|
| WTQ | `/home/ubuntu/lzz/MyAgent/datasets_ready/blind_holdout_200_v1_2026-06-27/wtq.jsonl` | 100 | row 51 |
| TabFact | `/home/ubuntu/lzz/MyAgent/datasets_ready/blind_holdout_200_v1_2026-06-27/tabfact.jsonl` | 100 | row 51 |
| CRT | `/home/ubuntu/lzz/MyAgent/datasets_ready/blind_holdout_200_v1_2026-06-27/crt.jsonl` | 100 | row 51 |

## Paired myAgent Outputs

| dataset | myAgent output |
|---|---|
| WTQ | `/home/ubuntu/lzz/MyAgent/outputs/server_runs/qwen3_32b_current_blind200_wtq200_shortcutfix2_20260721/merged/wtq_qwen3-32b-local.jsonl` |
| TabFact | `/home/ubuntu/lzz/MyAgent/outputs/server_runs/qwen3_32b_current_blind200_20260721/merged/tabfact_qwen3-32b-local.jsonl` |
| CRT | `/home/ubuntu/lzz/MyAgent/outputs/server_runs/qwen3_32b_current_blind200_20260721/merged/crt_qwen3-32b-local.jsonl` |

The myAgent outputs cover all first 100 IDs for WTQ, TabFact, and CRT.

## Model Service

| item | value |
|---|---|
| model | `/home/ubuntu/models/Qwen3-32B` |
| served name | `qwen3-32b-local` |
| endpoint | `http://127.0.0.1:8000/v1` |
| GPUs | `5,6` |
| max model length | `8192` |
| healthcheck before run | `ok` |

## Seed From Core50

The first 50 rows per dataset were copied from:

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_blind200_mact_core50_20260722
```

The copied IDs exactly match the first 50 IDs in each blind200 input. `--resume --limit 100` continues from row 51, so the first 50 rows are not recomputed.

Core50 baseline:

| dataset | myAgent | MACT | token ratio |
|---|---:|---:|---:|
| WTQ | 34/50 | 41/50 | 0.546 |
| TabFact | 48/50 | 49/50 | 0.234 |
| CRT | 42/50 | 29/50 | 1.019 |
| Overall | 124/150 | 119/150 | 0.626 |

## Run Command Pattern

Each dataset is run with:

```text
python scripts/server/run_mact_one_by_one.py
  --mact-root /home/ubuntu/lzz/MACT
  --dataset-path datasets_ready/blind_holdout_200_v1_2026-06-27/<dataset>.jsonl
  --output-path "$RUN_ROOT/<dataset>_mact_core100.jsonl"
  --log-path "$RUN_ROOT/logs/<dataset>_mact_core100.log"
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
  --limit 100
  --resume
```

## Live Progress

| time CST | WTQ rows | TabFact rows | CRT rows | note |
|---|---:|---:|---:|---|
| 2026-07-22 14:48:55 | 50 | 50 | 50 | core100 seed created from core50; ready to resume |
| 2026-07-22 19:32:47 | 54 | 50 | 50 | runner session was no longer active; no MACT runner process found; checkpointing before staged resume |
| 2026-07-22 21:21:35 | 54 | 50 | 50 | first detached WTQ resume script exited before running because `/usr/bin/time` is unavailable; script patched to use bash `SECONDS` |
| 2026-07-23 00:08:45 | 61 | 50 | 50 | detached WTQ resume active at pid `318083`; checkpointing row 61 before continuing |
| 2026-07-23 00:24:15 | 70 | 50 | 50 | detached WTQ resume still active at pid `318083`; checkpointing row 70 before continuing |
| 2026-07-23 00:44:32 | 81 | 50 | 50 | detached WTQ resume still active at pid `318083`; checkpointing row 81 before continuing |
| 2026-07-23 01:02:33 | 91 | 50 | 50 | detached WTQ resume still active at pid `318083`; checkpointing row 91 before continuing |
| 2026-07-23 01:22:10 | 100 | 50 | 50 | WTQ reached 100/100; detached runner exited status 0 after 5,243s |

## Current Checks

| check | current status |
|---|---|
| row completeness | partial run: WTQ 100/100, TabFact 50/100, CRT 50/100 |
| wrapper failures | WTQ 2 rows: inherited `nu-4299`, new `nu-2633` |
| critical log scan | WTQ context length BadRequest only: `nu-4299` and `nu-2633`; no connection/API transport errors |
| known diagnostic | internal `Halted: 1`: WTQ 8, TabFact 4, CRT 19 |
| launcher diagnostic | `run_wtq_resume.sh` first launch exited with status 127 before new rows; fixed by removing `/usr/bin/time` dependency |

## Sync Policy

Because the server environment may lose data, sync at these checkpoints:

1. Immediately after creating this ledger.
2. Around every 10 new rows per dataset.
3. After each dataset reaches 100 rows.
4. After final evaluator and paired comparison are written.

Files to sync from MACT with `git add -f`:

```text
outputs/server_runs/qwen3_32b_blind200_mact_core100_20260722/LIVE_LEDGER.md
outputs/server_runs/qwen3_32b_blind200_mact_core100_20260722/*_mact_core100.jsonl
outputs/server_runs/qwen3_32b_blind200_mact_core100_20260722/*_mact_core100_eval.json
outputs/server_runs/qwen3_32b_blind200_mact_core100_20260722/*_mact_core100_errors.jsonl
outputs/server_runs/qwen3_32b_blind200_mact_core100_20260722/*_mact_core100_paired.json
outputs/server_runs/qwen3_32b_blind200_mact_core100_20260722/overall_mact_core100_summary.json
outputs/server_runs/qwen3_32b_blind200_mact_core100_20260722/logs/*_mact_core100.log
```

Do not sync `tmp/`.

## Next Steps

1. Push this 54/50/50 interruption checkpoint to MACT GitHub.
2. Resume WTQ only to 100 rows with `--limit 100 --resume`.
3. Update and push this ledger after WTQ reaches 100 rows.
4. Run TabFact to 100, checkpoint and push.
5. Run CRT to 100, checkpoint and push.
6. Generate per-dataset eval, paired JSON, and overall summary.
7. Update the MyAgent server report with the blind100 paired result.
