# S5 CRT Affected-slice Real Rerun

Run dir: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6c_e3_s5_crt_tiebreaker_diag_20260804_2225`

| System | Correct | Accuracy | Avg Tokens | Failed | Missing |
|---|---:|---:|---:|---:|---:|
| old_myagent | 12/25 | 0.4800 | 11852.76 | 0 | 0 |
| new_myagent_s5 | 16/25 | 0.6400 | 11653.80 | 0 | 0 |
| mact | 12/25 | 0.4800 | 14180.20 | 0 | 0 |

## New MyAgent vs MACT

- both_correct: `4`
- myagent_only: `12`
- mact_only: `8`
- both_wrong: `1`
- delta_correct: `+4`

## Changed Correctness vs Old MyAgent

- `seed_d crt-136`: old `False` -> new `False`, MACT `False`, old `ita`, new `Italy`, gold `['Finland and italy.']`.
- `seed_d crt-139`: old `False` -> new `True`, MACT `True`, old `chn`, new `China`, gold `['china']`.
- `seed_d crt-373`: old `False` -> new `True`, MACT `True`, old `-1.0`, new `1.0`, gold `['1']`.
- `seed_c crt-458`: old `False` -> new `True`, MACT `True`, old `Yes`, new `No`, gold `['No']`.
- `seed_d crt-624`: old `False` -> new `True`, MACT `True`, old `No`, new `Yes`, gold `['Yes']`.
