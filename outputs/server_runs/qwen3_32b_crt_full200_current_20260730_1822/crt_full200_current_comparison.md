# CRT Full200 Current myAgent Comparison

## Scope

| item | value |
|---|---|
| dataset | CRT blind-holdout 200 |
| rows | 200 |
| input | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_crt_full200_current_20260730_1822/input/crt_blind200.jsonl` |
| new merged | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_crt_full200_current_20260730_1822/myagent_crt200/merged/crt_qwen3-32b-local.jsonl` |
| old myAgent merged | `/home/ubuntu/lzz/MyAgent/outputs/server_runs/qwen3_32b_current_blind200_20260721/merged/crt_qwen3-32b-local.jsonl` |
| MACT merged | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_blind200_mact_full200_20260723/crt_mact_full200.jsonl` |

## Metrics

| system | correct | primary_accuracy | avg_total_tokens | avg_elapsed_seconds | failed | missing |
|---|---:|---:|---:|---:|---:|---:|
| old myAgent | 137/200 | 0.6850 | 10838.25 | 24.90 | 0 | 0 |
| new myAgent | 140/200 | 0.7000 | 10839.17 | 24.46 | 0 | 0 |
| MACT | 113/200 | 0.5650 | 12809.99 | 163.68 | 0 | 0 |

## Token Ratios

| ratio | value |
|---|---:|
| new / MACT | 0.8461 |
| new / old myAgent | 1.0001 |

## New myAgent vs MACT

| bucket | count |
|---|---:|
| both_correct | 100 |
| myagent_only | 40 |
| mact_only | 13 |
| neither | 47 |

## Old To New Transitions

| bucket | count | ids |
|---|---:|---|
| a_wrong_b_correct | 6 | `crt-265, crt-82, crt-574, crt-295, crt-228, crt-682` |
| a_correct_b_wrong | 3 | `crt-243, crt-696, crt-257` |
| both_correct | 134 | `crt-601, crt-419, crt-387, crt-543, crt-634, crt-24, crt-541, crt-444, crt-414, crt-613, crt-538, crt-313, crt-59, crt-530, crt-422, crt-137, crt-519, crt-459, crt-721, crt-551, crt-95, crt-201, crt-104, crt-327 ...` |
| both_wrong | 57 | `crt-391, crt-505, crt-381, crt-240, crt-234, crt-606, crt-204, crt-685, crt-570, crt-667, crt-431, crt-494, crt-656, crt-333, crt-254, crt-212, crt-180, crt-39, crt-561, crt-351, crt-289, crt-499, crt-282, crt-54 ...` |

## Overall Context

| system | correct | accuracy | avg_total_tokens |
|---|---:|---:|---:|
| myAgent WTQ+TabFact previous + current CRT | 456/600 | 0.7600 | 6497.66 |
| MACT full200 | 450/600 | 0.7500 | 11382.95 |
| token ratio |  |  | 0.5708 |

## Conclusion

Current CRT full200 remains above MACT and at or above the previous myAgent CRT baseline, while preserving a clear token advantage over MACT.
