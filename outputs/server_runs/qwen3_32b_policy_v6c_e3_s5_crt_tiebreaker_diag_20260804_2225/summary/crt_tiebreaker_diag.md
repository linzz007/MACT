# Qwen3-32B CRT Tie-breaker Diagnosis

Run dir: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6c_e3_s5_crt_tiebreaker_diag_20260804_2225`

## Paired Counts

| Seed | Rows | MyAgent Correct | MACT Correct | both_correct | myagent_only | mact_only | both_wrong | MyAgent Avg Tokens | MACT Avg Tokens |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| seed_c | 50 | 32 | 32 | 26 | 6 | 6 | 12 | 11785.16 | 13347.08 |
| seed_d | 50 | 30 | 30 | 24 | 6 | 6 | 14 | 9751.56 | 13313.70 |

## Combined

- Rows: `100`
- MyAgent correct: `62`
- MACT correct: `62`
- Paired counts: `both_correct=50`, `myagent_only=12`, `mact_only=12`, `both_wrong=26`
- Token ratio MyAgent/MACT: `0.8078`

## Files

- `cases/{seed}_crt_mact_only.jsonl`: MACT correct, MyAgent wrong, highest-value tie-breaker targets.
- `cases/{seed}_crt_myagent_only.jsonl`: MyAgent correct, MACT wrong, no-harm guard targets.
- `cases/{seed}_crt_both_wrong.jsonl`: shared failure modes for later improvement.
- `summary/crt_tiebreaker_diag.json`: machine-readable summary.

## Immediate Reading

Current CRT is an exact tie across the two seeds. A strict all-dataset win needs at least one gold-free CRT improvement with no loss on the paired MyAgent-only cases.
