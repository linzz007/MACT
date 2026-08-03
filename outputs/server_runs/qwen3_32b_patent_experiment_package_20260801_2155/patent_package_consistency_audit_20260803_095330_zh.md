# Patent Package Consistency Audit

Generated: `2026-08-03 09:53:30 CST`

| item | value |
|---|---|
| overall status | `pass` |
| errors | `0` |
| warnings | `0` |
| MyAgent HEAD | `85bae0f` |
| MACT HEAD | `89f5358` |

## Errors

- none

## Warnings

- none

## Key Checks

| check | pass | actual | expected |
|---|---:|---|---|
| ledger completed rows | `True` | `13` | `>=13` |
| ledger pending rows | `True` | `5` | `<=5` |
| ledger overall status | `True` | `active_not_complete` | `active_not_complete` |
| stale completed evidence pending rows | `True` | `[]` | `[]` |
| full200 aggregate row count | `True` | `1` | `1` |
| full200 myagent correct | `True` | `489` | `489` |
| full200 mact correct | `True` | `450` | `450` |
| full200 failures | `True` | `0` | `0` |
| full200 missing | `True` | `0` | `0` |
| P4b WTQ risk row count | `True` | `1` | `1` |
| P4b WTQ MyAgent correct | `True` | `37` | `37` |
| P4b WTQ MACT correct | `True` | `43` | `43` |
| P4b WTQ decision | `True` | `complete_dataset_risk` | `complete_dataset_risk` |
| WTQ targeted fresh row count | `True` | `1` | `1` |
| WTQ targeted fresh MyAgent correct | `True` | `9` | `9` |
| WTQ targeted fresh failures | `True` | `0` | `0` |
| WTQ targeted fresh missing | `True` | `0` | `0` |
| WTQ targeted fresh decision | `True` | `pass` | `pass` |
| P4b after-targeted aggregate row count | `True` | `1` | `1` |
| P4b after-targeted MyAgent correct | `True` | `121` | `121` |
| P4b after-targeted MACT correct | `True` | `111` | `111` |
| P4b after-targeted failures | `True` | `0` | `0` |
| P4b after-targeted missing | `True` | `0` | `0` |
| P4b after-targeted decision | `True` | `accepted_after_targeted_all_dataset_superiority` | `accepted_after_targeted_all_dataset_superiority` |
| E3 pending row count | `True` | `4` | `4` |
| preflight status matches ledger | `True` | `ready_existing_endpoint` | `ready_existing_endpoint` |
| preflight generated_at matches ledger | `True` | `2026-08-03 09:32:03 CST` | `2026-08-03 09:32:03 CST` |
| manifest latest ledger path | `True` | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/latest_formal_result_ledger_current.json` | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/latest_formal_result_ledger_current.json` |
| manifest latest preflight path | `True` | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/latest_qwen3_runtime_preflight.json` | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/latest_qwen3_runtime_preflight.json` |
| manifest online status | `True` | `ready_existing_endpoint` | `ready_existing_endpoint` |
| PRD queue script | `True` | `run_remaining_qwen3_patent_queue.sh` | `` |
| PRD runtime preflight | `True` | `latest_qwen3_runtime_preflight_zh.md` | `` |
| PRD formal ledger | `True` | `latest_formal_result_ledger_current_zh.md` | `` |
| PRD active status | `True` | `active_not_complete` | `` |
