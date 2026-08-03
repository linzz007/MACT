# P4b WTQ Targeted Fresh Validation

Run dir: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305`

| metric | value |
|---|---:|
| decision | `pass` |
| fresh correct | 9/9 |
| min correct | 7 |
| failed exec | 0 |
| missing answer | 0 |
| avg total tokens | 5437.33 |
| avg elapsed seconds | 8.98 |
| expected rows | 9 |
| merged rows | 9 |
| eval rows | 9 |
| projected targeted rows | 9 |

Decision reasons: `fresh_targeted_validation_passed`

Fresh wrong IDs:

- none

Input/output paths:

- `input_jsonl`: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/input/wtq_p4b_targeted_fix_affected_slice.jsonl`
- `projection_json`: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/p4b_wtq_targeted_fix_projection.json`
- `merged_jsonl`: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/myagent_wtq_targeted_fix/merged/wtq_qwen3-32b-local.jsonl`
- `eval_json`: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/myagent_wtq_targeted_fix/eval/wtq_qwen3-32b-local_eval.json`
