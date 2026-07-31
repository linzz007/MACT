# Qwen3-32B Policy v6b P4 New-Seed Gate-50

Created: 2026-08-01 03:05 CST

Purpose: run a new-seed Gate-50 validation that excludes the frozen full200 inputs and the P2 diagnostic Gate-50 inputs. This directory is part of P4 in the single PRD:

```text
/home/ubuntu/lzz/MyAgent/docs/server/server_codex_reports/current-qwen3-mact-experiment-prd.md
```

## Inputs

| Dataset | Input | Source Rows | Excluded Unique IDs | Candidate Rows | Selected Rows |
|---|---|---:|---:|---:|---:|
| wtq | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/input/wtq_newseed_gate50.jsonl` | 4344 | 200 | 4144 | 50 |
| tabfact | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/input/tabfact_newseed_gate50.jsonl` | 12779 | 200 | 12579 | 50 |
| crt | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/input/crt_newseed_gate50.jsonl` | 728 | 200 | 528 | 50 |


## Execute P4a

Start Qwen3-32B on GPU 6,7 in a persistent terminal/session:

```bash
bash /home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/start_qwen3_67_service.sh
```

Then healthcheck and run current MyAgent:

```bash
bash /home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/healthcheck_vllm.sh
bash /home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/run_myagent_p4a_current.sh
cat /home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/p4a_current_gate50_summary.md
```

P4a is current-only. If `p4a_current_gate50_summary.json` has `decision=p4b_candidate`, run paired MACT on the same IDs:

```bash
bash /home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/run_mact_wtq_p4b_gate50.sh
bash /home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/run_mact_tabfact_p4b_gate50.sh
bash /home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/run_mact_crt_p4b_gate50.sh
bash /home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/run_p4b_eval_compare.sh
cat /home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/p4b_paired_gate50_summary.md
```

Checkpoint frequently:

```bash
bash /home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/checkpoint_to_git.sh --commit "checkpoint: p4 newseed gate50 inputs" --push
```
