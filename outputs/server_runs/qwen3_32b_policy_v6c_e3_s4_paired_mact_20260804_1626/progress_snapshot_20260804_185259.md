# S4 Paired MACT Progress Snapshot

Timestamp: `2026-08-04 18:52:59 CST`

Run directory:

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6c_e3_s4_paired_mact_20260804_1626/
```

Current output rows:

| seed | dataset | output | rows | exec_error rows | status |
|---|---|---|---:|---:|---|
| seed_c | WTQ | `mact/seed_c/wtq_mact_seed_c_gate50.jsonl` | 50/50 | 3 | completed |
| seed_c | TabFact | `mact/seed_c/tabfact_mact_seed_c_gate50.jsonl` | 50/50 | 0 | completed |
| seed_c | CRT | `mact/seed_c/crt_mact_seed_c_gate50.jsonl` | 23/50 | 0 | running on `http://127.0.0.1:8001/v1` |
| seed_d | WTQ | `mact/seed_d/wtq_mact_seed_d_gate50.jsonl` | 26/50 | 1 | running on `http://127.0.0.1:8000/v1` |
| seed_d | TabFact | `mact/seed_d/tabfact_mact_seed_d_gate50.jsonl` | 0/50 | 0 | pending |
| seed_d | CRT | `mact/seed_d/crt_mact_seed_d_gate50.jsonl` | 0/50 | 0 | pending |

Failed row ids observed so far:

| seed | dataset | failed ids |
|---|---|---|
| seed_c | WTQ | `nu-1073`, `nu-2047`, `nu-575` |
| seed_d | WTQ | `nu-3573` |

Next scheduling preference:

1. Keep seed_c/CRT on `8001`.
2. Keep seed_d/WTQ on `8000`.
3. When seed_d/WTQ completes, start seed_d/CRT on `8000` so both CRT baselines run in parallel.
4. Run seed_d/TabFact on the first free endpoint after that.
