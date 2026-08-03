# Qwen3-32B Policy v6b E3 Multi-Seed Gate-50

Status: inputs and runners prepared on 2026-08-01 22:31 CST. Seed-C and Seed-D current-only were executed on 2026-08-03 using the healthy GPU `0,1,2,3` Qwen3 endpoints. Both stopped before paired MACT with `decision=stop_or_inspect`.

Purpose: add two additional random-seed Gate-50 validations for the patent-facing MyAgent selective risk collaboration evidence chain. This is not a new optimization pass and does not change MyAgent code.

## Sampling

Two seeds are prepared:

| Seed label | Random seed | Rows |
|---|---:|---:|
| seed_c | 20260802 | WTQ 50 + TabFact 50 + CRT 50 |
| seed_d | 20260803 | WTQ 50 + TabFact 50 + CRT 50 |

Sampling excludes frozen full200 inputs, coarse diagnostic Gate-50 inputs, P4b new-seed Gate-50 inputs, affected targeted slices, and prior seeds in this package. The selected IDs are recorded in:

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_multiseed_gate50_20260801_2231/multiseed_gate50_manifest.json
```

## Current Results

Seed-C current-only summary:

```text
summary/seed_c_myagent_gate50_summary.json
summary/seed_c_myagent_gate50_summary.md
```

Seed-C result: WTQ `40/50`, TabFact `44/50`, CRT `30/50`, overall `114/150`, token ratio vs MACT full200 reference `0.6096`, failures/missing `0/0`, decision `stop_or_inspect`. Under this gate, Seed-C paired MACT is not required; inspect MyAgent errors before spending baseline runtime.

Seed-D current-only summary:

```text
summary/seed_d_myagent_gate50_summary.json
summary/seed_d_myagent_gate50_summary.md
```

Seed-D result: WTQ `30/50`, TabFact `38/50`, CRT `30/50`, overall `98/150`, token ratio vs MACT full200 reference `0.5735`, failures/missing `0/0`, decision `stop_or_inspect`. Under this gate, Seed-D paired MACT is not required. This is boundary evidence, not a multi-seed stability pass.

## Run Order After Server Recovery

Start one or two Qwen3-32B vLLM services. Recommended if GPU `4,5,6,7` are clean; run these in separate terminal sessions because each vLLM command stays in the foreground:

```bash
cd /home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_multiseed_gate50_20260801_2231
# terminal A
bash start_qwen3_service.sh 4,5 8000
# terminal B
bash start_qwen3_service.sh 6,7 8001
```

Then verify endpoints:

```bash
bash healthcheck_vllm.sh
```

Run MyAgent current-only gate first:

```bash
bash run_seed_myagent_gate50.sh seed_c
cat summary/seed_c_myagent_gate50_summary.md
```

If the decision is `run_paired_mact`, run the MACT baseline on the same IDs:

```bash
bash run_seed_mact_gate50.sh seed_c wtq http://127.0.0.1:8000/v1
bash run_seed_mact_gate50.sh seed_c tabfact http://127.0.0.1:8001/v1
bash run_seed_mact_gate50.sh seed_c crt http://127.0.0.1:8000/v1
bash run_seed_paired_compare.sh seed_c
cat summary/seed_c_paired_gate50_summary.md
```

Repeat the same sequence for `seed_d`.

## Decision Rule

For each seed, preserve these fields in the summary before making claims:

```text
eval rows
merged rows
correct
avg_total_tokens
avg_elapsed_seconds
num_failed_exec
num_missing_answer
token_ratio_myagent_to_mact
datasets_myagent_strictly_above_mact
strict_all_dataset_superiority
```

Interpretation:

| Result | Meaning |
|---|---|
| `strict_all_dataset_superiority=true` | Strong stability evidence: MyAgent beats MACT on WTQ, TabFact, and CRT for this seed |
| existing paired criteria accepted but strict goal false | Useful but not enough for the user's patent target; inspect the losing dataset before expansion |
| current-only decision `stop_or_inspect` | Do not spend MACT runtime yet; inspect MyAgent errors first |

## Checkpoint

Before long runs and after every completed seed:

```bash
bash checkpoint_to_git.sh --commit "checkpoint: e3 multiseed gate50 <stage>" --push
```
