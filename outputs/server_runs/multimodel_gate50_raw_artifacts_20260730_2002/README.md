# Multi-Model Gate-50 Raw Artifacts

Generated: 2026-07-30 20:02:09 CST

This directory mirrors the historical MyAgent Gate-50 raw artifacts into the MACT repository so the evidence survives a server wipe. No model service was started and no dataset row was rerun for this checkpoint.

The compact decision summaries remain in:

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/multimodel_gate50_summaries_20260730_1948/
```

## Contents

| model | copied source | files | merged rows | decision |
|---|---|---:|---:|---|
| Qwen3-14B-AWQ | `/home/ubuntu/lzz/MyAgent/outputs/server_runs/qwen3_14b_awq_gate50_20260721/` | 22 | 150 | no-go |
| Qwen2.5-14B-AWQ | `/home/ubuntu/lzz/MyAgent/outputs/server_runs/qwen25_14b_awq_gate50_20260721/` | 22 | 150 | no-go |
| Qwen2.5-3B-Instruct | `/home/ubuntu/lzz/MyAgent/outputs/server_runs/qwen25_3b_current_frozen_gate50_20260720/` | 15 | 150 | no-go |

Each copied run keeps its available `raw/`, `merged/`, `eval/`, `compare/`, `shards/`, and `logs/` files. Qwen2.5-3B did not have historical `compare/` files in the MyAgent source directory; its unified no-go decision is captured in the summary directory above.

## Verification Notes

- Total copied files before this README: 59.
- Total copied size before Git compression: about 20 MB.
- Merged row counts are 50 rows each for WTQ, TabFact, and CRT per model.
- JSON eval and compare files parsed successfully before copy.
- A narrow secret scan for Authorization/Bearer/API-key style values had no matches; the placeholder/local metrics fields in raw JSON are not credentials.

## Recovery Use

Use these raw artifacts only for audit, reproduction of summaries, or error analysis. Do not expand these models to Gate-150 or paired-200 unless a future code/model change creates a new run with a new run directory and a new summary.
