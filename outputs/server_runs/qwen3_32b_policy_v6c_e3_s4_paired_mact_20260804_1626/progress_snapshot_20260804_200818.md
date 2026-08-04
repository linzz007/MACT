# S4 Paired MACT Progress Snapshot

Timestamp: `2026-08-04 20:08:18 CST`

Run directory:

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6c_e3_s4_paired_mact_20260804_1626/
```

Current row counts:

| seed | dataset | output rows | exec_error rows | status |
|---|---:|---:|---:|---|
| seed_c | WTQ | 50/50 | 3 | completed; failed IDs `nu-1073`, `nu-2047`, `nu-575` |
| seed_c | TabFact | 50/50 | 0 | completed |
| seed_c | CRT | 50/50 | 0 | completed |
| seed_d | WTQ | 50/50 | 1 | completed; failed ID `nu-3573` |
| seed_d | CRT | 8/50 | 0 | running on `http://127.0.0.1:8000/v1` |
| seed_d | TabFact | 2/50 | 0 | running on `http://127.0.0.1:8001/v1` |

Do not conclude paired MACT performance yet. S4 remains `current_only_candidate_paired_pending` until all six MACT output files reach 50 rows and `summarize_s4_paired.py` generates the paired summaries.

Resume commands:

```bash
cd /home/ubuntu/lzz/MACT

for p in outputs/server_runs/qwen3_32b_policy_v6c_e3_s4_paired_mact_20260804_1626/mact/*/*.jsonl; do
  [ -f "$p" ] && printf '%s %s\n' "$(wc -l < "$p")" "$p"
done

bash outputs/server_runs/qwen3_32b_policy_v6c_e3_s4_paired_mact_20260804_1626/run_mact_dataset.sh seed_d crt http://127.0.0.1:8000/v1
bash outputs/server_runs/qwen3_32b_policy_v6c_e3_s4_paired_mact_20260804_1626/run_mact_dataset.sh seed_d tabfact http://127.0.0.1:8001/v1

python outputs/server_runs/qwen3_32b_policy_v6c_e3_s4_paired_mact_20260804_1626/summarize_s4_paired.py
```
