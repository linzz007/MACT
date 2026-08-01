# Patent Package Consistency Audit

Generated: `2026-08-01 23:22:19 CST`

| item | value |
|---|---|
| overall status | `pass` |
| errors | `0` |
| warnings | `1` |
| MyAgent HEAD | `6f7bd9c` |
| MACT HEAD | `3f8574b` |

## Errors

- none

## Warnings

- online experiments remain gated by runtime status: blocked_gpu_runtime_residual

## Key Checks

| check | pass | actual | expected |
|---|---:|---|---|
| ledger completed rows | `True` | `8` | `8` |
| ledger pending rows | `True` | `7` | `7` |
| ledger overall status | `True` | `active_not_complete` | `active_not_complete` |
| full200 aggregate row count | `True` | `1` | `1` |
| full200 myagent correct | `True` | `489` | `489` |
| full200 mact correct | `True` | `450` | `450` |
| full200 failures | `True` | `0` | `0` |
| full200 missing | `True` | `0` | `0` |
| P4b WTQ risk row count | `True` | `1` | `1` |
| P4b WTQ MyAgent correct | `True` | `37` | `37` |
| P4b WTQ MACT correct | `True` | `43` | `43` |
| P4b WTQ decision | `True` | `complete_dataset_risk` | `complete_dataset_risk` |
| E3 pending row count | `True` | `4` | `4` |
| preflight status matches ledger | `True` | `blocked_gpu_runtime_residual` | `blocked_gpu_runtime_residual` |
| preflight generated_at matches ledger | `True` | `2026-08-01 23:19:45 CST` | `2026-08-01 23:19:45 CST` |
| manifest latest ledger path | `True` | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/latest_formal_result_ledger_current.json` | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/latest_formal_result_ledger_current.json` |
| manifest latest preflight path | `True` | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/latest_qwen3_runtime_preflight.json` | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/latest_qwen3_runtime_preflight.json` |
| manifest online status | `True` | `blocked_gpu_runtime_residual` | `blocked_gpu_runtime_residual` |
| PRD queue script | `True` | `run_remaining_qwen3_patent_queue.sh` | `` |
| PRD runtime preflight | `True` | `latest_qwen3_runtime_preflight_zh.md` | `` |
| PRD formal ledger | `True` | `latest_formal_result_ledger_current_zh.md` | `` |
| PRD active status | `True` | `active_not_complete` | `` |
