# Latest Recovery Readiness Audit

Generated: 2026-07-30 20:13:09 CST

This audit checks whether the current staged evidence can be recovered from GitHub after the server is cleared.

## Git State Checked

The commits below are the minimum pushed checkpoints needed for this recovery set. Later metadata-only commits may supersede them without changing the underlying recoverable evidence.

| repo | branch | minimum evidence commit |
|---|---|---|
| MyAgent | `codex/selective-risk-collaboration` | `b5c7b44 Record canonical myAgent artifact recovery path` |
| MACT | `main` | `aebf366 Mirror canonical myAgent full200 artifacts` |

Both repositories were clean before this audit metadata correction.

## Recoverable Evidence

| evidence | path | tracked status |
|---|---|---|
| Unique Chinese PRD | `/home/ubuntu/lzz/MyAgent/docs/server/server_codex_reports/current-qwen3-mact-experiment-prd.md` | tracked |
| Canonical full200 MACT summary | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_blind200_mact_full200_20260723/overall_mact_full200_summary.json` | tracked |
| Latest experiment readiness audit | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_blind200_mact_full200_20260723/latest_experiment_readiness_audit.json` | tracked |
| Latest expert evidence summary | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_blind200_mact_full200_20260723/latest_expert_evidence_summary.md` | tracked |
| Current CRT full200 comparison | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_crt_full200_current_20260730_1822/crt_full200_current_comparison.json` | tracked |
| WTQ representative100 comparison | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_wtq_extreme_fix_representative100_20260730_1805/wtq_representative100_extreme_fix_comparison.json` | tracked |
| Multi-model Gate-50 summaries | `/home/ubuntu/lzz/MACT/outputs/server_runs/multimodel_gate50_summaries_20260730_1948/` | tracked |
| Multi-model Gate-50 raw artifacts | `/home/ubuntu/lzz/MACT/outputs/server_runs/multimodel_gate50_raw_artifacts_20260730_2002/` | tracked |
| Canonical myAgent full200 raw artifacts | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_canonical_myagent_full200_raw_artifacts_20260730_2008/` | tracked |

## Dataset Row Checks

| artifact | rows |
|---|---:|
| MACT WTQ full200 raw | 200 |
| MACT TabFact full200 raw | 200 |
| MACT CRT full200 raw | 200 |
| Canonical myAgent WTQ merged | 200 |
| Canonical myAgent TabFact merged | 200 |
| Canonical myAgent CRT merged | 200 |
| Each non-main model Gate-50 merged total | 150 |

## Metric Checks

Canonical full200:

| side | correct | rows | avg tokens |
|---|---:|---:|---:|
| myAgent | 453 | 600 | 6497.355 |
| MACT | 450 | 600 | 11382.9467 |

Current CRT staged composite:

| side | correct | rows | token ratio |
|---|---:|---:|---:|
| myAgent staged composite | 456 | 600 | 0.5708 |
| MACT | 450 | 600 | 1.0000 |

## Local-Only Files

The canonical full200 MACT directory still has local untracked files, but they are not required recovery evidence:

| local-only type | count | decision |
|---|---:|---|
| `tmp/mact_one_by_one_crt_*/sample_*.jsonl` and `*_out.jsonl` | 42 | temporary one-by-one MACT runner files; final raw/eval/paired outputs are tracked |
| `*.pid` | 2 | stale local process bookkeeping; not evidence |

## Decision

Recovery readiness is acceptable for the current staged evidence. The canonical myAgent full200 raw artifact directory has been committed and pushed to MACT. Do not restart old no-go models; the next experiment should start only after a new local model is mounted or a usable external API key is provided.
