# P4b Environment Blocker - 2026-08-01 14:15 CST

## Scope

P4b was intended to run same-ID MACT Gate-50 for WTQ / TabFact / CRT, then compare against the P4a after-fix MyAgent outputs.

This run did not produce valid MACT P4b evaluation outputs. The blocker was the server GPU runtime state, not a model accuracy result.

## Valid Existing Evidence Before P4b

- P4a after-fix MyAgent summary: `p4a_after_fix_gate50_summary.json`
- P4a after-fix MyAgent markdown: `p4a_after_fix_gate50_summary.md`
- P4a after-fix decision: `p4a_after_fix_pass`
- P4a after-fix results: WTQ `37/50`, TabFact `45/50`, CRT `30/50`, overall `112/150`, weighted token ratio `0.5533`, failed/missing `0/0`

## Failed Environment Attempts

1. Existing `8000` / `8001` endpoints returned connection refused.
2. GPU `4,5,6,7` showed about `42GB` memory used per card, but `nvidia-smi`, `pmon`, and compute-app queries showed no visible compute PID.
3. `nvidia-smi --gpu-reset -i 4,5,6,7` failed for insufficient permissions; `sudo -n nvidia-smi --gpu-reset -i 4,5,6,7` failed because the driver reported the devices were in use by another client.
4. Temporary fallback to GPU `0,1` and `2,3` with `gpu-memory-utilization=0.88` failed because available memory was below the requested vLLM reservation.
5. GPU `0,1` with `gpu-memory-utilization=0.68` loaded weights but failed because KV cache was slightly below the requirement for `max_model_len=8192`.
6. GPU `0,1` with `gpu-memory-utilization=0.70` passed KV sizing but failed during CUDA graph capture with CUDA OOM.

## Invalid Outputs

The following P4b WTQ files are environment-failure backups only and must not be used for evaluation:

- `p4b_mact_shards/output/wtq/wtq_mact_shard00.jsonl.sandbox_network_failed_20260801_0500`
- `p4b_mact_shards/output/wtq/wtq_mact_shard01.jsonl.sandbox_network_failed_20260801_0500`
- `p4b_mact_shards/output/wtq/wtq_mact_shard00.jsonl.connection_refused_failed_20260801_0506`
- `p4b_mact_shards/output/wtq/wtq_mact_shard01.jsonl.connection_refused_failed_20260801_0506`

There are no valid active P4b MACT `.jsonl` outputs.

## Verification Completed Before Stop

- `MyAgent/tests/test_myagent_pipeline.py`: `184` tests passed.
- Full `MyAgent/tests`: `330` tests passed when rerun outside the network sandbox. The sandbox-only run produced `3` errors because local HTTPServer binding to `127.0.0.1` was denied.
- Final process check: no healthy vLLM endpoint; no visible `vllm`, `run_mact_one_by_one`, `tqa.py`, or `run_sharded_tqa` process.

## Next Resume Step

After the server is expanded or reset to a clean GPU runtime:

1. Start two healthy Qwen3-32B vLLM endpoints with `max_model_len=8192`.
2. Confirm both `/v1/models` endpoints return `qwen3-32b-local`.
3. Re-run P4b from the shard inputs under `p4b_mact_shards/input/`.
4. Merge MACT shards, run `run_p4b_eval_compare.sh`, and create `p4b_paired_summary.json/md`.

