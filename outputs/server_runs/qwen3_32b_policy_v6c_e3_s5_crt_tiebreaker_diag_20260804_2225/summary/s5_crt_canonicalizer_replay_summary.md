# S5 CRT Canonicalizer Patch Replay

Run dir: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6c_e3_s5_crt_tiebreaker_diag_20260804_2225`

This replay applies only the new CRT scalar canonicalization rules to existing MyAgent outputs.
It does not use gold answers during patching and does not rerun the model.

| Seed | MyAgent Patched | MACT | Delta | both_correct | myagent_only | mact_only | both_wrong | Token Ratio | Flips |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| seed_c | 32/50 | 32/50 | +0 | 26 | 6 | 6 | 12 | 0.8830 | 0 |
| seed_d | 32/50 | 30/50 | +2 | 26 | 6 | 4 | 14 | 0.7324 | 3 |

Combined CRT: MyAgent patched `64/100` vs MACT `62/100`, delta `+2`, token ratio `0.8078`.

## Changed Cases

- `seed_d crt-136`: `ita` -> `Italy`, MyAgent `False` -> `False`, MACT `False`.
- `seed_d crt-139`: `chn` -> `China`, MyAgent `False` -> `True`, MACT `True`.
- `seed_d crt-373`: `-1.0` -> `1`, MyAgent `False` -> `True`, MACT `True`.
