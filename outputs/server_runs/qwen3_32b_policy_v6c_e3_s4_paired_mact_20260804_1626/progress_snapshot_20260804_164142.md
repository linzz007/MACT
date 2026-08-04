# S4 Paired MACT Progress Snapshot

Timestamp: `2026-08-04 16:41:42 CST`

Run directory:

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6c_e3_s4_paired_mact_20260804_1626/
```

Current output rows:

| seed | dataset | output | rows | status |
|---|---|---|---:|---|
| seed_c | WTQ | `mact/seed_c/wtq_mact_seed_c_gate50.jsonl` | 7/50 | running on `http://127.0.0.1:8000/v1` |
| seed_c | TabFact | `mact/seed_c/tabfact_mact_seed_c_gate50.jsonl` | 6/50 | running on `http://127.0.0.1:8001/v1` |
| seed_c | CRT | `mact/seed_c/crt_mact_seed_c_gate50.jsonl` | 0/50 | pending |
| seed_d | WTQ | `mact/seed_d/wtq_mact_seed_d_gate50.jsonl` | 0/50 | pending |
| seed_d | TabFact | `mact/seed_d/tabfact_mact_seed_d_gate50.jsonl` | 0/50 | pending |
| seed_d | CRT | `mact/seed_d/crt_mact_seed_d_gate50.jsonl` | 0/50 | pending |

Resume:

```bash
cd /home/ubuntu/lzz/MACT
for p in outputs/server_runs/qwen3_32b_policy_v6c_e3_s4_paired_mact_20260804_1626/mact/*/*.jsonl; do
  [ -f "$p" ] && printf '%s %s\n' "$(wc -l < "$p")" "$p"
done
```

All `run_mact_dataset.sh` invocations use `--resume`, so rerunning a seed/dataset command continues from the existing row count.
