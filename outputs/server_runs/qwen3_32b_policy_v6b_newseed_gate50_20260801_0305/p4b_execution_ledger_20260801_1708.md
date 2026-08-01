# P4b Qwen3-32B New-Seed MACT Gate-50 Execution Ledger

Generated: 2026-08-01 17:08 CST

Run dir:

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305
```

## Scope

P4b runs MACT on the same 50 new-seed IDs per dataset used by P4a after-fix MyAgent, then compares MyAgent vs MACT under the existing paired Gate-50 criteria.

Runtime resource actually used after recovery:

| endpoint | GPU | status |
|---|---|---|
| `http://127.0.0.1:8000/v1` | `0,1` | used for WTQ/TabFact/CRT shard00 |
| `http://127.0.0.1:8001/v1` | `2,3` | used for WTQ/TabFact/CRT shard01 |

GPU `4,5,6,7` still showed about `42GB/GPU` residual memory without visible compute PID, so this run did not use them.

## Row Counts

| dataset | shard00 | shard01 | merged |
|---|---:|---:|---:|
| WTQ | 25 | 25 | 50 |
| TabFact | 25 | 25 | 50 |
| CRT | 25 | 25 | 50 |

Merged files:

```text
mact/wtq_mact_newseed_gate50.jsonl
mact/tabfact_mact_newseed_gate50.jsonl
mact/crt_mact_newseed_gate50.jsonl
```

Merge validation: each merged file has 50 parsed JSONL rows, and merged ID order matches the corresponding `input/*_newseed_gate50.jsonl`.

Old WTQ environment-failure files with suffixes `sandbox_network_failed_20260801_0500` and `connection_refused_failed_20260801_0506` were not used.

## Eval And Comparison Artifacts

```text
eval/wtq_mact_newseed_gate50_eval.json
eval/tabfact_mact_newseed_gate50_eval.json
eval/crt_mact_newseed_gate50_eval.json
p4b_paired_gate50_summary.json
p4b_paired_gate50_summary.md
```

## Results

| dataset | MyAgent correct | MACT correct | delta | token ratio | MyAgent avg elapsed | MACT avg elapsed | MyAgent failed/missing | MACT failed/missing |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| WTQ | 37/50 | 43/50 | -6 | 0.5980 | 17.2846s | 119.7402s | 0/0 | 0/0 |
| TabFact | 45/50 | 44/50 | +1 | 0.2156 | 10.4797s | 94.8386s | 0/0 | 0/0 |
| CRT | 30/50 | 24/50 | +6 | 0.7740 | 21.9934s | 159.1165s | 0/0 | 0/0 |
| Overall | 112/150 | 111/150 | +1 | 0.5444 | 16.5859s | 124.5651s | 0/0 | 0/0 |

Existing paired Gate-50 acceptance criteria result: `accepted=true`.

Important interpretation: this P4b run passes the existing paired criteria because overall accuracy is at least MACT, at least two datasets are at least MACT, token ratio is below 0.75, and execution failure rate is 0. It does not prove that the new seed passes the stricter user goal of all three datasets individually beating MACT, because WTQ is `37/50` vs MACT `43/50`.

Next diagnostic priority if continuing optimization: inspect WTQ P4b `mact_only=9` and `myagent_only=3` cases to identify whether the new-seed WTQ gap is caused by evidence compression, answer normalization, verifier gating, or MACT-specific stronger execution on these IDs.
