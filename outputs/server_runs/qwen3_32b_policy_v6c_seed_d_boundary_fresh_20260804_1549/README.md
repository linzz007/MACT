# Qwen3-32B v6c Seed-D Boundary Fresh Rerun

Purpose: verify Seed-D WTQ/TabFact boundary fixes after the S3 after-guard run exposed WTQ/TabFact instability.

Input source:

- WTQ: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_multiseed_gate50_20260801_2231/input/seed_d/wtq_seed_d_gate50.jsonl`
- TabFact: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_multiseed_gate50_20260801_2231/input/seed_d/tabfact_seed_d_gate50.jsonl`

Fresh outputs:

- `myagent_seed_d_boundary_fresh/merged/wtq_qwen3-32b-local.jsonl`
- `myagent_seed_d_boundary_fresh/merged/tabfact_qwen3-32b-local.jsonl`
- `myagent_seed_d_boundary_fresh/eval/wtq_qwen3-32b-local_eval.json`
- `myagent_seed_d_boundary_fresh/eval/tabfact_qwen3-32b-local_eval.json`

Result:

| dataset | evidence | input/merged/eval | correct | threshold | token ratio | avg tokens | avg seconds | failed/missing | gate |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| WTQ | fresh v6c rerun | 50/50/50 | 36/50 | 35/50 | 0.6217 | 6533.18 | 15.75 | 0/0 | pass |
| TabFact | fresh v6c rerun | 50/50/50 | 45/50 | 45/50 | 0.2356 | 2552.16 | 10.25 | 0/0 | pass |
| CRT | inherited from S3 | 50/50/50 | 30/50 | 30/50 | 0.7612 | 9751.56 | 25.23 | 0/0 | pass |

Seed-D aggregate with inherited CRT: `111/150`, weighted token ratio `0.5516`, failed/missing `0/0`.

Combined with inherited Seed-C S3: `229/300`, weighted token ratio `0.5794`, failed/missing `0/0`, decision `boundary_fresh_pass_run_paired_mact_candidate`.

Important limitation: this is not yet paired MACT evidence. Seed-D WTQ/TabFact are fresh v6c reruns; Seed-D CRT and Seed-C are inherited from the prior S3 result because the v6c patch touched WTQ/TabFact deterministic shortcut paths only. The next experiment step is S4 paired MACT or an optional strict full S3 rerun before paired MACT.

Key summaries:

- `summary/seed_d_boundary_fresh_summary.json`
- `summary/seed_d_boundary_fresh_summary.md`
- `summary/e3_boundary_fresh_combined_summary.json`
- `summary/e3_boundary_fresh_combined_summary.md`
