# Patent Package Consistency Audit

Generated: `2026-08-04 14:20:33 CST`

| item | value |
|---|---|
| overall status | `pass` |
| errors | `0` |
| warnings | `0` |
| MyAgent HEAD | `5097ede` |
| MACT HEAD | `dfe6861` |

## Errors

- none

## Warnings

- none

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
| preflight status matches ledger | `True` | `ready_existing_endpoint` | `ready_existing_endpoint` |
| preflight generated_at matches ledger | `True` | `2026-08-04 10:49:03 CST` | `2026-08-04 10:49:03 CST` |
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
| manifest E3 semantic plan json path | `True` | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_e3_semantic_boundary_plan_20260804_1110/summary/e3_semantic_boundary_plan.json` | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_e3_semantic_boundary_plan_20260804_1110/summary/e3_semantic_boundary_plan.json` |
| manifest E3 semantic plan md path | `True` | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_e3_semantic_boundary_plan_20260804_1110/summary/e3_semantic_boundary_plan.md` | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_e3_semantic_boundary_plan_20260804_1110/summary/e3_semantic_boundary_plan.md` |
| manifest E3 semantic plan decision | `True` | `do_not_rerun_full200_or_paired_mact_until_targeted_guards_pass` | `do_not_rerun_full200_or_paired_mact_until_targeted_guards_pass` |
| manifest E3 semantic plan high-priority count | `True` | `8` | `8` |
| manifest E3 guard validation json path | `True` | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_e3_guard_validation_inputs_20260804_1128/summary/e3_guard_validation_input_plan.json` | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_e3_guard_validation_inputs_20260804_1128/summary/e3_guard_validation_input_plan.json` |
| manifest E3 guard validation md path | `True` | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_e3_guard_validation_inputs_20260804_1128/summary/e3_guard_validation_input_plan.md` | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_e3_guard_validation_inputs_20260804_1128/summary/e3_guard_validation_input_plan.md` |
| manifest E3 guard validation decision | `True` | `ready_for_guard_implementation_not_model_run` | `ready_for_guard_implementation_not_model_run` |
| manifest E3 guard validation total rows | `True` | `30` | `30` |
| manifest E3 guard validation representative rows | `True` | `12` | `12` |
| manifest E3 guard validation no-harm rows | `True` | `18` | `18` |
| manifest E3 after-guard json path | `True` | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_e3_guard_validation_after_guard_20260804_1203/summary/e3_guard_validation_after_guard_summary.json` | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_e3_guard_validation_after_guard_20260804_1203/summary/e3_guard_validation_after_guard_summary.json` |
| manifest E3 after-guard md path | `True` | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_e3_guard_validation_after_guard_20260804_1203/summary/e3_guard_validation_after_guard_summary.md` | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_e3_guard_validation_after_guard_20260804_1203/summary/e3_guard_validation_after_guard_summary.md` |
| manifest E3 after-guard decision | `True` | `after_guard_passes_s2_gate` | `after_guard_passes_s2_gate` |
| manifest E3 after-guard rows | `True` | `30` | `30` |
| manifest E3 after-guard representative recovered | `True` | `8` | `8` |
| manifest E3 after-guard no-harm correct | `True` | `18` | `18` |
| manifest E3 after-guard failed | `True` | `0` | `0` |
| manifest E3 after-guard missing | `True` | `0` | `0` |
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
| current patent section E3 guard validation rows | `True` | `30` | `30` |
| current patent section E3 after-guard decision | `True` | `after_guard_passes_s2_gate` | `after_guard_passes_s2_gate` |
| current patent section E3 after-guard recovered | `True` | `8` | `8` |
| current patent section E3 after-guard no-harm | `True` | `18` | `18` |
| current patent section unsupported multi-model claim | `True` | `Do not claim multi-model validation is complete.` | `` |
| manifest completion gap latest json path | `True` | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/latest_completion_gap_audit_current.json` | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/latest_completion_gap_audit_current.json` |
| manifest completion gap latest md path | `True` | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/latest_completion_gap_audit_current_zh.md` | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/latest_completion_gap_audit_current_zh.md` |
| current completion gap overall status | `True` | `active_not_complete` | `active_not_complete` |
| completion gap R3 status | `True` | `complete` | `complete` |
| completion gap R4 status | `True` | `complete_boundary_not_stability_pass` | `complete_boundary_not_stability_pass` |
| completion gap R5 status | `True` | `pending_no_candidate` | `pending_no_candidate` |
| completion gap E4 decision | `True` | `no_candidate_wait` | `no_candidate_wait` |
| completion gap semantic plan decision | `True` | `do_not_rerun_full200_or_paired_mact_until_targeted_guards_pass` | `do_not_rerun_full200_or_paired_mact_until_targeted_guards_pass` |
| completion gap guard validation decision | `True` | `ready_for_guard_implementation_not_model_run` | `ready_for_guard_implementation_not_model_run` |
| completion gap guard validation rows | `True` | `30` | `30` |
| completion gap after-guard decision | `True` | `after_guard_passes_s2_gate` | `after_guard_passes_s2_gate` |
| completion gap after-guard recovered | `True` | `8` | `8` |
| completion gap after-guard no-harm | `True` | `18` | `18` |
| completion gap default GPU pool availability | `True` | `False` | `False` |
| manifest goal blocker latest json path | `True` | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/latest_goal_blocker_audit_current.json` | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/latest_goal_blocker_audit_current.json` |
| manifest goal blocker latest md path | `True` | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/latest_goal_blocker_audit_current_zh.md` | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/latest_goal_blocker_audit_current_zh.md` |
| goal blocker status recommendation | `True` | `blocked_waiting_external_state` | `blocked_waiting_external_state` |
| goal blocker names | `True` | `['No viable E4 multi-model candidate', 'Qwen3 runtime readiness']` | `['No viable E4 multi-model candidate', 'Qwen3 runtime readiness']` |
| goal blocker E4 decision | `True` | `no_candidate_wait` | `no_candidate_wait` |
| goal blocker E4 can start | `True` | `False` | `False` |
| goal blocker runtime status | `True` | `ready_existing_endpoint` | `ready_existing_endpoint` |
| goal blocker no-candidate markdown | `True` | `E4 没有可用多模型候选` | `` |
| goal blocker runtime markdown | `True` | `Qwen3 runtime 已恢复` | `` |
| claim traceability WTQ closure | `True` | `WTQ targeted fresh 与 P4b after-targeted 闭环已经完成` | `` |
| claim traceability E3 boundary | `True` | `E3 Seed-C/D current-only 已完成并形成边界证据` | `` |
| claim traceability E3 semantic plan | `True` | `E3 semantic-boundary plan` | `` |
| formal schedule E3 boundary | `True` | `S2 after-guard fresh 已证明当前 P0/P1 gold-free guard` | `` |
| patent disclosure full200 | `True` | `Aggregate | 600/600/600 | 489/600 | 450/600 | +39 | 0.5717 | 0/0` | `` |
| patent disclosure P4b closure | `True` | `Overall | 150/150/150 | 121/150 | 111/150 | +10 | 0.5310 | 0/0` | `` |
| patent disclosure E3 boundary | `True` | `Combined | 300/300/300 | 212/300 | 0.5916 | 0/0 | `complete_boundary_evidence`` | `` |
| patent disclosure E4 boundary | `True` | `E4 多模型 readiness audit 结果为 `no_candidate_wait`` | `` |
| patent disclosure evidence paths | `True` | `latest_completion_gap_audit_current_zh.md` | `` |
| manifest online status | `True` | `ready_existing_endpoint` | `ready_existing_endpoint` |
| PRD queue script | `True` | `run_remaining_qwen3_patent_queue.sh` | `` |
| PRD runtime preflight | `True` | `latest_qwen3_runtime_preflight_zh.md` | `` |
| PRD formal ledger | `True` | `latest_formal_result_ledger_current_zh.md` | `` |
| PRD current patent section | `True` | `latest_current_patent_experiment_section_zh.md` | `` |
| PRD current completion gap audit | `True` | `latest_completion_gap_audit_current_zh.md` | `` |
| PRD goal blocker audit | `True` | `latest_goal_blocker_audit_current_zh.md` | `` |
| PRD E3 boundary diagnosis | `True` | `seed_boundary_error_diagnosis.md` | `` |
| PRD E3 semantic boundary plan | `True` | `e3_semantic_boundary_plan.md` | `` |
| PRD E3 guard validation input plan | `True` | `e3_guard_validation_input_plan.md` | `` |
| PRD E3 guard validation after guard | `True` | `after_guard_passes_s2_gate` | `` |
| PRD E4 readiness audit | `True` | `latest_e4_multimodel_gate_readiness_audit_zh.md` | `` |
| PRD active status | `True` | `active_not_complete` | `` |
