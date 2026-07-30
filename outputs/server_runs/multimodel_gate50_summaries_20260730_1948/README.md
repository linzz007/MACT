# Multi-Model Gate-50 Summaries

Generated: 2026-07-30 19:45:55 CST

These files are derived from existing MyAgent Gate-50 eval JSON files. No model service was started and no dataset row was rerun for this checkpoint.

## Source Eval Roots

| model | source eval root |
|---|---|
| Qwen3-14B-AWQ | `/home/ubuntu/lzz/MyAgent/outputs/server_runs/qwen3_14b_awq_gate50_20260721` |
| Qwen2.5-14B-AWQ | `/home/ubuntu/lzz/MyAgent/outputs/server_runs/qwen25_14b_awq_gate50_20260721` |
| Qwen2.5-3B-Instruct | `/home/ubuntu/lzz/MyAgent/outputs/server_runs/qwen25_3b_current_frozen_gate50_20260720` |

## Decision Summary

Criteria: Qwen3-32B Gate-50 reference `124/150`, failure rate <= `2%`, token ratio to MACT <= `0.75`.

| model | correct | accuracy | avg tokens | token ratio | bad rows | decision |
|---|---:|---:|---:|---:|---:|---|
| Qwen3-14B-AWQ | 108/150 | 72.0% | 7344.51 | 0.6521 | 0 | no-go |
| Qwen2.5-14B-AWQ | 107/150 | 71.3% | 7308.35 | 0.6489 | 0 | no-go |
| Qwen2.5-3B-Instruct | 89/150 | 59.3% | 7298.51 | 0.6480 | 0 | no-go |

All three models are below the Qwen3-32B Gate-50 accuracy reference, so none should expand to Gate-150 or MACT paired-200.

## Files

| file | content |
|---|---|
| `qwen3_14b_awq_gate50_summary.json` | machine-readable Gate-50 summary and decision |
| `qwen3_14b_awq_gate50_summary.md` | human-readable Gate-50 summary |
| `qwen25_14b_awq_gate50_summary.json` | machine-readable Gate-50 summary and decision |
| `qwen25_14b_awq_gate50_summary.md` | human-readable Gate-50 summary |
| `qwen25_3b_gate50_summary.json` | machine-readable Gate-50 summary and decision |
| `qwen25_3b_gate50_summary.md` | human-readable Gate-50 summary |
