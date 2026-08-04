# 当前专利实验完成度审计

生成时间：`2026-08-04 16:20:38 CST`

手工增量更新：`2026-08-04 23:36:00 CST`。S5 CRT tie-breaker 已完成，结果保存在 `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6c_e3_s5_crt_tiebreaker_diag_20260804_2225/summary/e3_s5_final_combined_summary.json` 与 `.md`。总体 MyAgent `232/300` vs MACT `223/300`，token ratio `0.5662`，overall failed/missing 为 MyAgent `0/0`、MACT `4/4`。WTQ `76/100 > 74/100`、TabFact `91/100 > 87/100`、CRT `65/100 > 62/100`，decision `s5_strict_all_dataset_pass`。新增 fine-grained mechanism ablation audit：`/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6c_e3_fine_grained_mechanism_ablation_audit_20260804_2333/summary/fine_grained_mechanism_ablation_audit.md`，decision=`fine_grained_mechanism_evidence_ready_for_qwen3_patent_scope_with_evidence_retention_boundary_and_e4_pending`。下一步缺口从 “可选细粒度消融” 改为 “E4 no-candidate 边界；如专利代理人要求，再补 standalone no-evidence-retention”。

本文档用于回答：当前距离完整专利实验材料还差什么。它从 current/latest 证据自动汇总，不新增 benchmark 结果。

## 当前结论

当前目标状态：`qwen3_strict_goal_complete_e4_pending`。Qwen3-32B full200、P4b after-targeted、E3 S2 after-guard fresh、E3 v6c boundary-fresh current-only candidate、S4 paired MACT existing-criteria pass、S5 CRT tie-breaker strict pass 与 fine-grained mechanism audit 已是正证据；当前 Qwen3 + MyAgent 在 paired 多 seed WTQ/TabFact/CRT 三项均严格超过 MACT，且总体 token 明显更低。E4 状态为 `pending_no_candidate`，artifact decision 为 `no_candidate_wait`，尚无额外模型/API 候选。

## 环境复核

| item | result |
|---|---|
| source | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/latest_e4_multimodel_gate_readiness_audit.json` |
| checked at | `2026-08-04 10:49:21 CST` |
| default GPU pool | `0,1 -> 8000; 2,3 -> 8001` |
| default pool available | `False` |
| visible model/runner processes | `2` |

| GPU | memory MiB | util % |
|---:|---:|---:|
| 0 | 45815 | 0 |
| 1 | 45815 | 0 |
| 2 | 45839 | 0 |
| 3 | 45839 | 0 |
| 4 | 42031 | 100 |
| 5 | 42031 | 10 |
| 6 | 42031 | 100 |
| 7 | 42031 | 100 |

## 要求逐项审计

| ID | 要求 | 当前状态 | 关键证据 | 缺口 |
|---|---|---|---|---|
| R1 | Qwen3-32B full200 anchor evidence shows MyAgent exceeds MACT on WTQ, TabFact, and CRT, with lower token usage and zero failed/missing answers. | `complete` | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_all200_acceptance_20260731_132611/qwen3_policy_v6b_all200_acceptance_summary.json`<br>`/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_all200_acceptance_20260731_132611/qwen3_policy_v6b_patent_evidence_index.md` | none |
| R2 | Mechanism evidence supports selective risk collaboration / persuasion-back rather than sample hardcoding. | `complete_for_current_qwen3_patent_scope_with_boundary` | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_patent_mechanism_evidence_20260801_2222/patent_mechanism_evidence_matrix.json`<br>`/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_patent_mechanism_evidence_20260801_2222/patent_mechanism_evidence_matrix.md`<br>`/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_coarse_ablation_gate50_20260801_0040/coarse_ablation_gate50_summary.md`<br>`/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6c_e3_fine_grained_mechanism_ablation_audit_20260804_2333/summary/fine_grained_mechanism_ablation_audit.json`<br>`/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6c_e3_fine_grained_mechanism_ablation_audit_20260804_2333/summary/fine_grained_mechanism_ablation_audit.md` | Mechanism evidence is draft-ready for Qwen3 scope. Standalone no-evidence-retention or no-WTQ-verifier-override ablations are optional only if narrower causal isolation is requested. |
| R3 | WTQ P4b new-seed risk is diagnosed and closed with fresh Qwen validation before using after-targeted P4b as positive evidence. | `complete` | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/p4b_paired_gate50_summary.json`<br>`/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/p4b_wtq_targeted_fresh_summary.json`<br>`/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/p4b_after_wtq_targeted_paired_summary.json` | none |
| R4 | Multi-seed work explains whether the effect is stable beyond the frozen full200 and P4b seed. | `complete_strict_all_dataset_pass` | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_multiseed_gate50_20260801_2231/summary/seed_boundary_error_diagnosis.json`<br>`/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_multiseed_gate50_20260801_2231/summary/seed_boundary_error_diagnosis.md`<br>`/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_e3_boundary_budget_probe_20260804_1035/summary/e3_boundary_budget_probe_summary.json`<br>`/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_e3_boundary_budget_probe_20260804_1035/summary/e3_boundary_budget_probe_summary.md`<br>`/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_e3_semantic_boundary_plan_20260804_1110/summary/e3_semantic_boundary_plan.json`<br>`/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_e3_semantic_boundary_plan_20260804_1110/summary/e3_semantic_boundary_plan.md`<br>`/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_e3_guard_validation_inputs_20260804_1128/summary/e3_guard_validation_input_plan.json`<br>`/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_e3_guard_validation_inputs_20260804_1128/summary/e3_guard_validation_input_plan.md`<br>`/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_e3_guard_validation_after_guard_20260804_1203/summary/e3_guard_validation_after_guard_summary.json`<br>`/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_e3_guard_validation_after_guard_20260804_1203/summary/e3_guard_validation_after_guard_summary.md`<br>`/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_e3_s3_current_rerun_after_guard_20260804_1425/summary/e3_s3_current_combined_summary.json`<br>`/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_e3_s3_current_rerun_after_guard_20260804_1425/summary/e3_s3_current_combined_summary.md`<br>`/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6c_seed_d_boundary_fresh_20260804_1549/summary/e3_boundary_fresh_combined_summary.json`<br>`/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6c_seed_d_boundary_fresh_20260804_1549/summary/e3_boundary_fresh_combined_summary.md`<br>`/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6c_e3_s5_crt_tiebreaker_diag_20260804_2225/summary/e3_s5_final_combined_summary.json`<br>`/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6c_e3_s5_crt_tiebreaker_diag_20260804_2225/summary/e3_s5_final_combined_summary.md` | S5 paired multi-seed strict target complete: overall MyAgent `232/300` vs MACT `223/300`, token ratio `0.5662`; WTQ/TabFact/CRT all strictly exceed MACT. Remaining gap is E4 external model evidence, not Qwen3 strict performance. |
| R5 | Multi-model gate must test model externality through Gate-10 -> Gate-50 -> Gate-150 -> paired-200 without rerunning known no-go models. | `pending_no_candidate` | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/latest_e4_multimodel_gate_readiness_audit.json`<br>`/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/latest_e4_multimodel_gate_readiness_audit_zh.md` | No untested local model path or API provider profile/key exists. Do not start E4 Gate-10 until a new candidate appears. |
| R6 | Expert/patent package and Chinese patent disclosure draft must exist, point to auditable evidence, and separate supported claims from boundaries. | `stage_patent_draft_ready_with_boundaries` | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/latest_current_patent_experiment_section.json`<br>`/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/latest_current_patent_experiment_section_zh.md`<br>`/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/patent_disclosure_draft_zh.md`<br>`/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/latest_formal_result_ledger_current.json` | Final closeout still needs an E4 candidate result or explicit acceptance of the no-candidate boundary. |
| R7 | Process/result context remains in the single MyAgent PRD and MACT artifacts, with sync to GitHub after each update. | `complete_for_prior_pushed_state_this_audit_requires_commit_push` | `/home/ubuntu/lzz/MyAgent/docs/server/server_codex_reports/current-qwen3-mact-experiment-prd.md`<br>`/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/evidence_manifest.json`<br>`/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/SHA256SUMS` | This generated audit itself must be committed and pushed after generation; final proof is git local/remote HEAD equality. |

## 关键数字

| scope | result |
|---|---|
| full200 aggregate | MyAgent `489/600` vs MACT `450/600`, token ratio `0.5717`, elapsed ratio `0.1337`, failed/missing `0/0` |
| P4b original WTQ risk | MyAgent `37/50` vs MACT `43/50` |
| WTQ targeted fresh | `9/9`, merged/eval `9/9`, failed/missing `0/0`, decision `pass` |
| P4b after-targeted aggregate | MyAgent `121/150` vs MACT `111/150`, token ratio `0.5310`, failed/missing `0/0` |
| E3 Seed-C/D boundary aggregate | `212/300`, wrong `88`, weighted token ratio `0.5916`, failed/missing `0/0`, verification `pass` |
| E3 max_replan=5 boundary probe | recovered `4/12` original wrong rows, decision `mixed_budget_sensitivity_not_enough_for_e3_stability`, failed/missing `0/0`, avg tokens `12444.9->13136.1` |
| E3 semantic-boundary plan | decision `do_not_rerun_full200_or_paired_mact_until_targeted_guards_pass`, high-priority work items `8`, zero-recovery categories `4`, next ladder `S1_design_and_unit, S2_affected_slice_fresh, S3_e3_current_only_rerun, S4_paired_mact_or_boundary_closeout` |
| E3 S2 guard-validation input package | decision `ready_for_guard_implementation_not_model_run`, rows `30`, dataset counts `{'wtq': 10, 'tabfact': 8, 'crt': 12}`, role counts `{'representative_wrong': 12, 'no_harm_correct': 18}`, registered gate target recover `7/12` and no-harm `18/18` |
| E3 S2 after-guard fresh | decision `after_guard_passes_s2_gate`, recovered `8/12`, no-harm `18/18`, failed/missing `0/0`, weighted token ratio `0.6104` |
| E3 S3 after-guard current-only | combined `215/300`, weighted token ratio `0.5866`, failed/missing `0/0`, decision `s3_stop_or_inspect_boundary_remains`, paired MACT next `False` |
| E3 v6c boundary-fresh current-only | combined `229/300`, weighted token ratio `0.5794`, failed/missing `0/0`, decision `boundary_fresh_pass_run_paired_mact_candidate`, paired MACT next `True` |
| E3 S4 paired MACT | combined MyAgent `229/300` vs MACT `223/300`, token ratio `0.5700`, MyAgent failed/missing `0/0`, MACT failed/missing `4/4`, decision `s4_paired_pass_existing_criteria_not_strict`; WTQ/TabFact strict pass, CRT `62/100` vs `62/100` tie |
| E3 S5 CRT tie-breaker final | combined MyAgent `232/300` vs MACT `223/300`, token ratio `0.5662`, MyAgent failed/missing `0/0`, MACT failed/missing `4/4`, decision `s5_strict_all_dataset_pass`; WTQ `76/100 > 74/100`, TabFact `91/100 > 87/100`, CRT `65/100 > 62/100` |
| E3 fine-grained mechanism audit | decision `fine_grained_mechanism_evidence_ready_for_qwen3_patent_scope_with_evidence_retention_boundary_and_e4_pending`; `no_strong_verification` `-8/150`; `no_deterministic_shortcuts` `-15/150`; S2 guard `4/12 -> 8/12` representative recovery and `17/18 -> 18/18` no-harm; S5 CRT scalar canonicalization full CRT100 `65/100 > 62/100` |
| E4 readiness | decision `no_candidate_wait`; can_start_gate10_now `False`, local models `4`, untested local models `0`, API keys/profiles `0/0` |

## 下一步

- Do not rerun known no-go models. Wait for a new local model path or API provider profile/key before E4 Gate-10.
- Use latest_current_patent_experiment_section_zh.md for current expert/patent discussion, with E3 and E4 boundaries explicitly preserved.
- Use the fine-grained mechanism audit as the current Qwen3 mechanism closeout; only run standalone no-evidence-retention or no-WTQ-verifier-override if a patent drafting question specifically requires narrower causal isolation.

## 当前可写

- Qwen3-32B full200 stage: MyAgent beats MACT on WTQ, TabFact, and CRT with lower aggregate tokens.
- P4b new-seed Gate-50 supports overall/token evidence but exposes WTQ risk.
- WTQ targeted fresh closure has completed, and P4b after-targeted Gate-50 shows all-dataset superiority.
- E3 Seed-C current-only Gate-50 is a documented stability boundary: overall 114/150, decision stop_or_inspect.
- E3 Seed-D current-only Gate-50 is a second documented stability boundary: overall 98/150, decision stop_or_inspect.
- E3 S3 after-guard current-only rerun has completed: Seed-C passes, Seed-D remains inspect, combined 215/300 with weighted token ratio 0.5866 and failed/missing 0/0.
- E3 v6c boundary-fresh current-only candidate has completed: Seed-C inherited 118/150, Seed-D fresh/inherited 111/150, combined 229/300 with weighted token ratio 0.5794 and failed/missing 0/0.
- E3 S4 paired MACT has completed and passes existing paired criteria: combined MyAgent 229/300 vs MACT 223/300, token ratio 0.5700, MyAgent failed/missing 0/0; WTQ and TabFact strictly exceed MACT, while CRT ties MACT.
- E3 S5 CRT tie-breaker has completed and passes the current Qwen3 strong strict target: combined MyAgent 232/300 vs MACT 223/300, token ratio 0.5662, MyAgent failed/missing 0/0, WTQ/TabFact/CRT all strictly exceed MACT.
- E3 fine-grained mechanism audit has completed and is draft-ready for Qwen3 patent scope, with evidence-retention causal isolation explicitly bounded.
- E3 Seed-C/Seed-D offline boundary diagnosis has explained the current-gate boundary as semantic accuracy stability, not runtime/tool failure or token-budget failure.
- E4 latest readiness audit has completed with no untested local model path and no API provider profile, so no Gate-10 should be started yet.
- The current patent experiment section has been consolidated as draft-ready evidence with explicit unsupported-claim boundaries.

## 当前不能写

- E3 S4 alone can be described as all-dataset strict superiority; actual S4 result is WTQ/TabFact strict pass and CRT tie. The all-dataset strict claim must cite S5, not S4.
- A viable additional model gate has completed.
- A standalone no-evidence-retention causal ablation has completed; current evidence-retention support is attribution plus fresh no-harm/guard evidence.
- The final experiment package closeout has completed after either an E4 candidate result or explicit acceptance of the no-candidate boundary.
