# Qwen3-32B Policy v6b E3 Multi-Seed Gate-50

Status: inputs and runners prepared on 2026-08-01 22:31 CST. No model run was executed in this directory at creation time because `8000/8001` were unavailable and GPU `6,7` were occupied by non-visible runtime state.

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
