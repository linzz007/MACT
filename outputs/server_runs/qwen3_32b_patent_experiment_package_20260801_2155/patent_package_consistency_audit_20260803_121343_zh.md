# Patent Package Consistency Audit

Generated: `2026-08-03 12:13:43 CST`

| item | value |
|---|---|
| overall status | `pass` |
| errors | `0` |
| warnings | `1` |
| MyAgent HEAD | `bb4e3d3` |
| MACT HEAD | `24efb3b` |

## Errors

- none

## Warnings

- online experiments remain gated by runtime status: start_service_required

## Key Checks

| check | pass | actual | expected |
|---|---:|---|---|
| ledger completed rows | `True` | `21` | `>=13` |
| ledger pending rows | `True` | `3` | `<=5` |
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
| E3 Seed-C current row count | `True` | `1` | `1` |
| E3 Seed-C current MyAgent correct | `True` | `114` | `114` |
| E3 Seed-C current failures | `True` | `0` | `0` |
| E3 Seed-C current missing | `True` | `0` | `0` |
| E3 Seed-C current decision | `True` | `stop_or_inspect` | `stop_or_inspect` |
| E3 Seed-D current row count | `True` | `1` | `1` |
| E3 Seed-D current MyAgent correct | `True` | `98` | `98` |
| E3 Seed-D current failures | `True` | `0` | `0` |
| E3 Seed-D current missing | `True` | `0` | `0` |
| E3 Seed-D current decision | `True` | `stop_or_inspect` | `stop_or_inspect` |
| E3 pending row count lower bound | `True` | `2` | `>=2` |
| E3 pending row count upper bound | `True` | `2` | `<=4` |
| preflight status matches ledger | `True` | `start_service_required` | `start_service_required` |
| preflight generated_at matches ledger | `True` | `2026-08-03 11:13:18 CST` | `2026-08-03 11:13:18 CST` |
| manifest latest ledger path | `True` | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/latest_formal_result_ledger_current.json` | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/latest_formal_result_ledger_current.json` |
| manifest latest preflight path | `True` | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/latest_qwen3_runtime_preflight.json` | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/latest_qwen3_runtime_preflight.json` |
| manifest E3 boundary json path | `True` | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_multiseed_gate50_20260801_2231/summary/seed_boundary_error_diagnosis.json` | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_multiseed_gate50_20260801_2231/summary/seed_boundary_error_diagnosis.json` |
| manifest E3 boundary md path | `True` | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_multiseed_gate50_20260801_2231/summary/seed_boundary_error_diagnosis.md` | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_multiseed_gate50_20260801_2231/summary/seed_boundary_error_diagnosis.md` |
| manifest E3 boundary status | `True` | `complete_offline_diagnosis` | `complete_offline_diagnosis` |
| manifest E3 boundary rows | `True` | `300` | `300` |
| manifest E3 boundary correct | `True` | `212` | `212` |
| manifest E3 boundary failed | `True` | `0` | `0` |
| manifest E3 boundary missing | `True` | `0` | `0` |
| manifest E3 boundary verification | `True` | `pass` | `pass` |
| manifest E4 readiness json path | `True` | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/latest_e4_multimodel_gate_readiness_audit.json` | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/latest_e4_multimodel_gate_readiness_audit.json` |
| manifest E4 readiness md path | `True` | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/latest_e4_multimodel_gate_readiness_audit_zh.md` | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/latest_e4_multimodel_gate_readiness_audit_zh.md` |
| manifest E4 readiness status | `True` | `no_candidate_wait` | `no_candidate_wait` |
| manifest E4 can start gate10 | `True` | `False` | `False` |
| manifest E4 default GPU pool availability | `True` | `False` | `False` |
| E4 readiness decision | `True` | `no_candidate_wait` | `no_candidate_wait` |
| E4 untested local model count | `True` | `0` | `0` |
| E4 API key count | `True` | `0` | `0` |
| manifest current patent section json path | `True` | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/latest_current_patent_experiment_section.json` | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/latest_current_patent_experiment_section.json` |
| manifest current patent section md path | `True` | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/latest_current_patent_experiment_section_zh.md` | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/latest_current_patent_experiment_section_zh.md` |
| current patent section status | `True` | `stage_patent_draft_ready_with_boundaries` | `stage_patent_draft_ready_with_boundaries` |
| current patent section E4 decision | `True` | `no_candidate_wait` | `no_candidate_wait` |
| current patent section unsupported multi-model claim | `True` | `Do not claim multi-model validation is complete.` | `` |
| manifest completion gap latest json path | `True` | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/latest_completion_gap_audit_current.json` | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/latest_completion_gap_audit_current.json` |
| manifest completion gap latest md path | `True` | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/latest_completion_gap_audit_current_zh.md` | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/latest_completion_gap_audit_current_zh.md` |
| current completion gap overall status | `True` | `active_not_complete` | `active_not_complete` |
| completion gap R3 status | `True` | `complete` | `complete` |
| completion gap R4 status | `True` | `complete_boundary_not_stability_pass` | `complete_boundary_not_stability_pass` |
| completion gap R5 status | `True` | `pending_no_candidate` | `pending_no_candidate` |
| completion gap E4 decision | `True` | `no_candidate_wait` | `no_candidate_wait` |
| completion gap default GPU pool availability | `True` | `False` | `False` |
| manifest online status | `True` | `start_service_required` | `start_service_required` |
| PRD queue script | `True` | `run_remaining_qwen3_patent_queue.sh` | `` |
| PRD runtime preflight | `True` | `latest_qwen3_runtime_preflight_zh.md` | `` |
| PRD formal ledger | `True` | `latest_formal_result_ledger_current_zh.md` | `` |
| PRD current patent section | `True` | `latest_current_patent_experiment_section_zh.md` | `` |
| PRD current completion gap audit | `True` | `latest_completion_gap_audit_current_zh.md` | `` |
| PRD E3 boundary diagnosis | `True` | `seed_boundary_error_diagnosis.md` | `` |
| PRD E4 readiness audit | `True` | `latest_e4_multimodel_gate_readiness_audit_zh.md` | `` |
| PRD active status | `True` | `active_not_complete` | `` |
