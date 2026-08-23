# Qwen3-32B Patent Seed-E Gate-50 Package

Created: 2026-08-23 CST

Purpose: prepare one additional paired Gate-50 seed for MyAgent vs MACT stability evidence. This package is prepared but not executed.

GPU policy:

- Use only existing Qwen3-32B services on GPUs `4,5` and `6,7`.
- Default endpoints are `http://127.0.0.1:8000/v1,http://127.0.0.1:8001/v1`.
- Do not use GPUs `0,1,2,3` unless the user explicitly changes the constraint.

Prepared inputs:

```text
input/wtq_seed_e_gate50.jsonl
input/tabfact_seed_e_gate50.jsonl
input/crt_seed_e_gate50.jsonl
```

Run order after Qwen3 services are healthy:

```bash
cd /home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_seed_e_gate50_20260823
export LOCAL_VLLM_API_KEY=local-vllm-key-change-me
bash run_myagent_seed_e_gate50.sh
bash run_mact_seed_e_gate50_sharded.sh wtq
bash run_mact_seed_e_gate50_sharded.sh tabfact
bash run_mact_seed_e_gate50_sharded.sh crt
bash run_eval_seed_e_gate50.sh
```

Expected final files after execution:

```text
myagent_seed_e/merged/*_qwen3-32b-local.jsonl
mact/*_mact_seed_e_gate50.jsonl
eval/*_mact_seed_e_gate50_eval.json
seed_e_paired_gate50_summary.json
seed_e_paired_gate50_summary.md
```

This is a stability-strengthening experiment. It should not replace the Formal-200 result package.
