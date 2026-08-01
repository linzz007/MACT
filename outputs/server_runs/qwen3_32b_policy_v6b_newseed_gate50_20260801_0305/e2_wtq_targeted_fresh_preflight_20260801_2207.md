# E2 WTQ Targeted Fresh Preflight - 2026-08-01 22:07 CST

Scope: preflight for `run_myagent_wtq_targeted_fix_slice.sh`.

Fresh run executed: `false`.

Reason: Qwen3-32B vLLM endpoints were down, and the user-constrained GPU pair
`6,7` had high residual memory/use without visible compute PIDs. Starting a new
Qwen3-32B service under this state would risk another environment-failed run.

## Endpoint Checks

| endpoint | status |
|---|---|
| `http://127.0.0.1:8000/v1/models` | connection refused |
| `http://127.0.0.1:8001/v1/models` | connection refused |

## GPU Snapshot

| gpu | used / total MiB | util % |
|---:|---:|---:|
| 0 | 41710 / 49140 | 0 |
| 1 | 47018 / 49140 | 100 |
| 2 | 19983 / 49140 | 0 |
| 3 | 19981 / 49140 | 0 |
| 4 | 42031 / 49140 | 10 |
| 5 | 42031 / 49140 | 100 |
| 6 | 42031 / 49140 | 100 |
| 7 | 42027 / 49140 | 100 |

`nvidia-smi --query-compute-apps` returned no visible compute app rows. Process
scan for vLLM, API server, MACT runner, `tqa.py`, and `run_sharded_tqa.py`
returned no visible runner rows.

## Automation Added

The affected-slice runner now calls:

```bash
python /home/ubuntu/lzz/MyAgent/scripts/server/summarize_wtq_targeted_fresh.py \
  --run-dir /home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305 \
  --output-root /home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/myagent_wtq_targeted_fix \
  --min-correct 7 \
  --fail-on-inspect
```

Future successful fresh runs will write:

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/p4b_wtq_targeted_fresh_summary.json
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/p4b_wtq_targeted_fresh_summary.md
```

Next action after server cleanup: start Qwen3-32B on GPU `6,7`, run
`run_myagent_wtq_targeted_fix_slice.sh`, inspect the fresh summary, and only
rerun P4b WTQ full50 if the affected slice passes.
