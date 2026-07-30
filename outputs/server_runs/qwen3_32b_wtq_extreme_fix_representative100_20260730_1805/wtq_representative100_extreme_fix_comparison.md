# WTQ Representative100 Extreme/Only Fix Comparison

## Scope

| item | value |
|---|---|
| dataset | WTQ blind200 first 100 |
| rows | 100 |
| input | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_wtq_extreme_fix_representative100_20260730_1805/input/wtq_blind200_first100.jsonl` |
| new merged | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_wtq_extreme_fix_representative100_20260730_1805/myagent_wtq100/merged/wtq_qwen3-32b-local.jsonl` |
| old myAgent merged | `/home/ubuntu/lzz/MyAgent/outputs/server_runs/qwen3_32b_current_blind200_wtq200_shortcutfix2_20260721/merged/wtq_qwen3-32b-local.jsonl` |
| MACT paired baseline | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_blind200_mact_core100_20260722/wtq_mact_core100_paired.json` |

## Metrics

| system | correct | primary_accuracy | avg_total_tokens | avg_elapsed_seconds | failed | missing |
|---|---:|---:|---:|---:|---:|---:|
| old myAgent | 69/100 | 0.6900 | 6039.68 | 15.16 | 0 | 0 |
| new myAgent | 69/100 | 0.6900 | 6094.77 | 15.00 | 0 | 0 |
| MACT | 79/100 | 0.7900 | 10527.28 | 116.23 | 2 | 2 |

## Token Ratios

| ratio | value |
|---|---:|
| new / MACT | 0.5790 |
| new / old myAgent | 1.0091 |

## Old To New Transitions

| bucket | count | ids |
|---|---:|---|
| old_wrong_new_correct | 3 | `nu-2223, nu-1951, nu-2850` |
| old_correct_new_wrong | 3 | `nu-4168, nu-484, nu-35` |
| both_correct | 66 | `nu-2923, nu-58, nu-1874, nu-4342, nu-2772, nu-3720, nu-342, nu-3442, nu-192, nu-4268, nu-1952, nu-3470, nu-195, nu-1373, nu-1836, nu-226, nu-3191, nu-2779, nu-2525, nu-1214 ...` |
| both_wrong | 28 | `nu-1434, nu-2873, nu-2178, nu-965, nu-2453, nu-709, nu-4062, nu-4299, nu-3934, nu-1505, nu-1177, nu-2213, nu-613, nu-1826, nu-1263, nu-2611, nu-3535, nu-4324, nu-3949, nu-3542 ...` |

## Trigger Term Segment

| segment | rows | old correct | new correct | MACT correct | old->new recovered | old->new regressed |
|---|---:|---:|---:|---:|---:|---:|
| trigger_terms | 23 | 13 | 16 | 18 | 3 | 0 |
| non_trigger | 77 | 56 | 53 | 61 | 0 | 3 |

## Conclusion

The extreme/only global-row trigger fixed the adversarial debug50 slice, but on the representative first100 WTQ slice it produced no net accuracy gain and a small token increase. Do not broaden this as the next primary optimization without more targeted diagnostics.
