# Qwen3-32B E3 S4 Paired MACT

Created: `2026-08-04 16:26 CST`

Purpose: run same-ID MACT Gate-50 baselines for the latest E3 v6c boundary-fresh current-only candidate, then compare MyAgent vs MACT on Seed-C and Seed-D.

This run follows the candidate recorded in:

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6c_seed_d_boundary_fresh_20260804_1549/summary/e3_boundary_fresh_combined_summary.json
```

MyAgent evidence used for comparison:

- Seed-C WTQ/TabFact/CRT: inherited from S3 after-guard current-only.
- Seed-D WTQ/TabFact: fresh v6c boundary rerun.
- Seed-D CRT: inherited from S3 because v6c did not alter CRT shortcut paths and CRT already passed the current gate.

This run creates new MACT baseline outputs only. It does not rerun MyAgent.

Commands:

```bash
cd /home/ubuntu/lzz/MACT
bash outputs/server_runs/qwen3_32b_policy_v6c_e3_s4_paired_mact_20260804_1626/run_mact_dataset.sh seed_c wtq http://127.0.0.1:8000/v1
bash outputs/server_runs/qwen3_32b_policy_v6c_e3_s4_paired_mact_20260804_1626/run_mact_dataset.sh seed_c tabfact http://127.0.0.1:8001/v1

for p in outputs/server_runs/qwen3_32b_policy_v6c_e3_s4_paired_mact_20260804_1626/mact/*/*.jsonl; do
  [ -f "$p" ] && printf '%s %s\n' "$(wc -l < "$p")" "$p"
done

# After all six seed/dataset outputs reach 50 rows:
python outputs/server_runs/qwen3_32b_policy_v6c_e3_s4_paired_mact_20260804_1626/summarize_s4_paired.py
```

Checkpoint as server-loss protection:

```bash
bash outputs/server_runs/qwen3_32b_policy_v6c_e3_s4_paired_mact_20260804_1626/checkpoint_to_git.sh
bash outputs/server_runs/qwen3_32b_policy_v6c_e3_s4_paired_mact_20260804_1626/checkpoint_to_git.sh --commit "checkpoint: qwen3 v6c s4 paired mact" --push
```

Current checkpoint at `2026-08-04 16:38 CST`:

- `seed_c/wtq` is running on `http://127.0.0.1:8000/v1`, output `5/50`.
- `seed_c/tabfact` is running on `http://127.0.0.1:8001/v1`, output `4/50`.
- `seed_c/crt`, `seed_d/wtq`, `seed_d/tabfact`, and `seed_d/crt` are pending.
- TabFact is mapped to MACT internal task `scitab` by `run_mact_dataset.sh`; output filenames remain `tabfact_*`.

Checkpoint at `2026-08-04 17:55 CST`:

- `seed_c/wtq` completed `50/50`; `3` rows have MACT `exec_error`/`mact_error` under the old `--max-tokens 2048` context口径.
- `seed_c/tabfact` completed `50/50`; `0` rows have `exec_error`.
- `seed_c/crt` is running on `http://127.0.0.1:8001/v1`, output `4/50`.
- `seed_d/wtq` is running on `http://127.0.0.1:8000/v1`, output `1/50`.
- `seed_d/tabfact` and `seed_d/crt` are pending.

Checkpoint at `2026-08-04 18:52 CST`:

- `seed_c/wtq` completed `50/50`; `3` rows have MACT `exec_error`/`mact_error`.
- `seed_c/tabfact` completed `50/50`; `0` rows have `exec_error`.
- `seed_c/crt` is running on `http://127.0.0.1:8001/v1`, output `23/50`.
- `seed_d/wtq` is running on `http://127.0.0.1:8000/v1`, output `26/50`; `1` row has `exec_error`.
- `seed_d/tabfact` and `seed_d/crt` are pending. Prefer starting `seed_d/crt` first when `8000` becomes free.

Checkpoint at `2026-08-04 20:08 CST`:

- `seed_c/wtq` completed `50/50`; `3` rows have MACT `exec_error`/`mact_error`: `nu-1073`, `nu-2047`, `nu-575`.
- `seed_c/tabfact` completed `50/50`; `0` rows have `exec_error`.
- `seed_c/crt` completed `50/50`; `0` rows have `exec_error`.
- `seed_d/wtq` completed `50/50`; `1` row has MACT `exec_error`/`mact_error`: `nu-3573`.
- `seed_d/crt` is running on `http://127.0.0.1:8000/v1`, output `8/50`, `0` current rows have `exec_error`.
- `seed_d/tabfact` is running on `http://127.0.0.1:8001/v1`, output `2/50`, `0` current rows have `exec_error`.
- Continue these two sessions. After both reach `50/50`, run `python outputs/server_runs/qwen3_32b_policy_v6c_e3_s4_paired_mact_20260804_1626/summarize_s4_paired.py`.

Acceptance language:

- Strong patent-seed claim requires MyAgent strictly above MACT on WTQ, TabFact, and CRT for each paired seed, with token ratio materially below MACT and failed/missing `0/0`.
- Existing paired criterion is weaker: overall accuracy at least MACT, at least two datasets at least MACT, token ratio <= `0.75`, and execution failure rate <= `2%`.
- Until this run is complete, E3 remains `current_only_candidate_paired_pending`.
