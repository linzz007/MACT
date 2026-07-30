# Qwen3-32B CRT Full200 Current myAgent Run Ledger

## Purpose

Rerun current `myAgent` on the same blind-holdout CRT 200-row slice used by the MACT full200 comparison, after the July 30 runtime and WTQ compression fixes. This run is stored under MACT because server storage is unstable and experiment artifacts must be synced from one place.

## Run Scope

| item | value |
|---|---|
| started | 2026-07-30 18:22 CST |
| repo | `/home/ubuntu/lzz/MyAgent` |
| branch | `codex/selective-risk-collaboration` |
| task | CRT |
| dataset copy | `input/crt_blind200.jsonl` |
| rows | 200 |
| first id | `crt-601` |
| last id | `crt-686` |
| output root | `myagent_crt200` |
| model | `qwen3-32b-local` |
| endpoints | `http://127.0.0.1:8000/v1`, `http://127.0.0.1:8001/v1` |
| GPU groups | `4,5;6,7` |
| max replan | 2 |
| MACT avg-token reference | 12809.985 |

## Baseline

Current paired MACT full200 CRT baseline:

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_blind200_mact_full200_20260723/crt_mact_full200_eval.json
MACT: 113/200, primary_accuracy 0.565, avg_total_tokens 12809.985, failed 0, missing 0

/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_blind200_mact_full200_20260723/crt_mact_full200_paired.json
older myAgent matched baseline: 137/200, primary_accuracy 0.685, avg_total_tokens 10838.25, failed 0, missing 0
```

## Live Status

```text
2026-07-30 18:22 CST: input/env copied; two vLLM endpoints healthchecked; runner ready to start.
2026-07-30 18:34 CST: raw progress 50/200; shard00 22/100, shard01 28/100; no error keywords in logs.
2026-07-30 18:45 CST: raw progress 103/200; shard00 45/100, shard01 58/100; no error keywords in logs.
2026-07-30 18:54 CST: raw progress 150/200; shard00 68/100, shard01 82/100; vLLM endpoints healthy, no error keywords in logs.
2026-07-30 19:12 CST: vLLM and runner processes stopped after validation; GPU 4-7 memory released.
```

## Output Files

Expected after completion:

```text
myagent_crt200/raw/crt/crt_shard00_out.jsonl
myagent_crt200/raw/crt/crt_shard01_out.jsonl
myagent_crt200/merged/crt_qwen3-32b-local.jsonl
myagent_crt200/eval/crt_qwen3-32b-local_eval.json
crt_full200_current_comparison.json
crt_full200_current_comparison.md
```

## Final Result

```text
2026-07-30 19:08 CST: raw 200/200, merged/eval complete.
new myAgent: 140/200, primary_accuracy 0.7000, avg_total_tokens 10839.17, avg_elapsed_seconds 24.46, failed 0, missing 0
old myAgent: 137/200, primary_accuracy 0.6850, avg_total_tokens 10838.25
MACT: 113/200, primary_accuracy 0.5650, avg_total_tokens 12809.99, failed 0, missing 0
new/MACT token ratio 0.8461; new/old token ratio 1.0001
new vs MACT paired: both_correct 100, myAgent_only 40, MACT_only 13, neither 47
overall context replacing CRT only: myAgent 456/600 (0.7600) vs MACT 450/600 (0.7500), token ratio 0.5708
Conclusion: Current CRT full200 remains above MACT and at or above the previous myAgent CRT baseline, while preserving a clear token advantage over MACT.
```
