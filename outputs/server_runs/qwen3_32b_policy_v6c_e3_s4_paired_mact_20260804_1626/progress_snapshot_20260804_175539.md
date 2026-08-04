# S4 Paired MACT Progress Snapshot

Timestamp: `2026-08-04 17:55:39 CST`

Run directory:

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6c_e3_s4_paired_mact_20260804_1626/
```

Current output rows:

| seed | dataset | output | rows | exec_error rows | status |
|---|---|---|---:|---:|---|
| seed_c | WTQ | `mact/seed_c/wtq_mact_seed_c_gate50.jsonl` | 50/50 | 3 | completed |
| seed_c | TabFact | `mact/seed_c/tabfact_mact_seed_c_gate50.jsonl` | 50/50 | 0 | completed |
| seed_c | CRT | `mact/seed_c/crt_mact_seed_c_gate50.jsonl` | 4/50 | 0 | running on `http://127.0.0.1:8001/v1` |
| seed_d | WTQ | `mact/seed_d/wtq_mact_seed_d_gate50.jsonl` | 1/50 | 0 | running on `http://127.0.0.1:8000/v1` |
| seed_d | TabFact | `mact/seed_d/tabfact_mact_seed_d_gate50.jsonl` | 0/50 | 0 | pending |
| seed_d | CRT | `mact/seed_d/crt_mact_seed_d_gate50.jsonl` | 0/50 | 0 | pending |

Notes:

- Seed-C WTQ follows the old MACT `--max-tokens 2048` baseline口径 used by full200/P4b. Three rows currently contain `exec_error` / `mact_error`; these will be counted transparently by the S4 evaluation.
- The seed_c/WTQ shell session ended with a post-run `line 62: 3: command not found` message after all 50 rows were already written. `run_mact_dataset.sh` currently passes `bash -n`; remaining datasets should be resumed by row count if a shell session exits nonzero.

Resume:

```bash
cd /home/ubuntu/lzz/MACT
for p in outputs/server_runs/qwen3_32b_policy_v6c_e3_s4_paired_mact_20260804_1626/mact/*/*.jsonl; do
  [ -f "$p" ] && printf '%s %s\n' "$(wc -l < "$p")" "$p"
done
```
