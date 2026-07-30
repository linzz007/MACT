# Qwen3-32B Canonical MyAgent Full200 Raw Artifacts

Generated: 2026-07-30 20:08:45 CST

This directory mirrors the canonical myAgent raw artifacts used by the MACT paired full200 evidence. It exists so the full200 myAgent side can be recovered from the MACT repository after a server wipe.

No model service was started and no dataset row was rerun for this checkpoint.

## Canonical Source Mapping

| dataset | copied MyAgent source | merged rows | correct | avg tokens | failed | missing |
|---|---|---:|---:|---:|---:|---:|
| WTQ | `/home/ubuntu/lzz/MyAgent/outputs/server_runs/qwen3_32b_current_blind200_wtq200_shortcutfix2_20260721/` | 200 | 131 | 6226.925 | 0 | 0 |
| TabFact | `/home/ubuntu/lzz/MyAgent/outputs/server_runs/qwen3_32b_current_blind200_20260721/` | 200 | 185 | 2426.89 | 0 | 0 |
| CRT | `/home/ubuntu/lzz/MyAgent/outputs/server_runs/qwen3_32b_current_blind200_20260721/` | 200 | 137 | 10838.25 | 0 | 0 |

These values match the myAgent side of:

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_blind200_mact_full200_20260723/overall_mact_full200_summary.json
```

## Contents

| subdir | content |
|---|---|
| `wtq_shortcutfix2/` | WTQ canonical shortcutfix2 raw, merged, eval, shard, and log files |
| `tabfact_crt_current_blind200/` | TabFact and CRT canonical current-blind200 raw, merged, eval, shard, and log files |

## Verification Notes

- Copied source files before this README: 15.
- Total copied size before Git compression: about 29 MB.
- Merged row counts are 200 rows for WTQ, 200 for TabFact, and 200 for CRT.
- JSON and JSONL files parsed successfully.
- A narrow secret scan for Authorization/Bearer/API-key style values had no matches.

## Recovery Use

For canonical full200 paired evidence, use these files as the recoverable myAgent raw side and the MACT full200 directory as the recoverable MACT raw/eval/paired/summary side. Do not mix these canonical artifacts with later staged CRT reruns unless the report explicitly says it is using the staged composite口径.
