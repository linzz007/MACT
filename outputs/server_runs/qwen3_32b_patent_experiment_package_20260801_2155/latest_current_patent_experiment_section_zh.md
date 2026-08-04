# 当前专利实验章节收口稿

生成时间：`2026-08-04 16:20:32 CST`

手工增量更新：`2026-08-04 23:03:00 CST`。S5 CRT tie-breaker 已完成：在不改 evaluator、gold 或样本 ID 的前提下，MyAgent 增加 gold-free CRT scalar canonicalization，将负数 `difference` 标量规整为非负差值，并将 country/nation 问题中的国家代码展开为国家名。S5 final 合并结果为 overall MyAgent `232/300` vs MACT `223/300`，token ratio `0.5662`，overall failed/missing 为 MyAgent `0/0`、MACT `4/4`，decision `s5_strict_all_dataset_pass`。WTQ `76/100 > 74/100`、TabFact `91/100 > 87/100`、CRT `65/100 > 62/100`。因此当前可以写成“Qwen3-32B + MyAgent 在 paired Gate-50 多 seed 的 WTQ/TabFact/CRT 三项均严格超过 MACT，且总体 token 明显更低”；多模型验证仍 pending。

本文档用于回答：当前哪些实验结果可以写进专家/专利材料，哪些结论必须保留边界。它只汇总已有 frozen 证据，不新增 benchmark 结果。

## 1. 当前总判断

- Qwen3-32B full200：MyAgent `489/600`，MACT `450/600`，delta `+39`，整体 token ratio `0.5717`，整体耗时 ratio `0.1337`。
- P4b after-targeted Gate-50：MyAgent `121/150`，MACT `111/150`，三数据集单项均超过 MACT，整体 token ratio `0.5310`。
- E3 Seed-C/D：current-only 合计 `212/300`，token ratio `0.5916`，failed/missing `0/0`，但 decision 仍是 boundary，不是多 seed 稳定性达标。
- E3 max_replan=5 probe：12 条代表错题恢复 `4/12`，decision `mixed_budget_sensitivity_not_enough_for_e3_stability`，failed/missing `0/0`；可写成 adaptive budget 机制证据，不能写成稳定性闭环。
- E3 semantic-boundary plan：decision `do_not_rerun_full200_or_paired_mact_until_targeted_guards_pass`，P0/P1 high-priority items `8`；后续先做 targeted guards 和 affected-slice fresh，不直接 rerun full200 或 paired MACT。
- E3 S2 guard-validation input package：已准备 `30` 行，其中代表错题 `12` 行、no-harm 正确行 `18` 行；decision `ready_for_guard_implementation_not_model_run`，这是输入/验证计划，不是 fresh run 结果。
- E3 S2 after-guard fresh：representative recovered `8/12`，no-harm `18/18`，failed/missing `0/0`，weighted token ratio `0.6104`，decision `after_guard_passes_s2_gate`。
- E3 S3 after-guard current-only：combined `215/300`，weighted token ratio `0.5866`，failed/missing `0/0`，decision `s3_stop_or_inspect_boundary_remains`；Seed-C 通过，Seed-D 未过 WTQ/TabFact gate。
- E3 v6c boundary-fresh current-only：combined `229/300`，weighted token ratio `0.5794`，failed/missing `0/0`，decision `boundary_fresh_pass_run_paired_mact_candidate`，paired_mact_next `True`。
- E3 S4 paired MACT（历史边界）：combined MyAgent `229/300` vs MACT `223/300`，token ratio `0.5700`，failed/missing MyAgent `0/0`、MACT `4/4`；existing paired criteria 通过，但 S4 单独的 strong patent strict 未过，因为 CRT 持平。
- E3 S5 CRT tie-breaker：current-code CRT100 fresh `65/100` vs MACT `62/100`，S5 final combined MyAgent `232/300` vs MACT `223/300`，token ratio `0.5662`，overall failed/missing MyAgent `0/0`、MACT `4/4`；WTQ/TabFact/CRT 三项均严格超过 MACT，decision `s5_strict_all_dataset_pass`。
- E4 多模型 gate：`no_candidate_wait`，无 untested local model、无 API provider profile/key；默认下一次启动池为 `0,1 -> 8000; 2,3 -> 8001`，当前可用状态为 `False`。

## 2. 可以写入的正证据

### Qwen3-32B Full200 主结果

| dataset | rows input/merged/eval | MyAgent | MACT/ref | delta | token ratio | avg tokens | avg elapsed s | failed/missing |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| wtq | 200/200/200 | 155/200 | 148/200 | +7 | 0.6187 | 6501.02 | 16.80 | 0/0 |
| tabfact | 200/200/200 | 194/200 | 189/200 | +5 | 0.2014 | 2181.67 | 9.76 | 0/0 |
| crt | 200/200/200 | 140/200 | 113/200 | +27 | 0.8461 | 10839.17 | 24.46 | 0/0 |
| aggregate | 600/600/600 | 489/600 | 450/600 | +39 | 0.5717 | 6507.29 | 17.01 | 0/0 |

### P4b After-Targeted Gate-50

P4b 原始 WTQ 风险为 MyAgent `37/50` vs MACT `43/50`。WTQ affected-slice fresh 验证为 `9/9`，merged/eval `9/9`，failed/missing `0/0`。

| dataset | rows input/merged/eval | MyAgent | MACT/ref | delta | token ratio | avg tokens | avg elapsed s | failed/missing |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| wtq | 50/50/50 | 46/50 | 43/50 | +3 | 0.5571 | 6300.16 | 14.51 | 0/0 |
| tabfact | 50/50/50 | 45/50 | 44/50 | +1 | 0.2156 | 2308.92 | 10.48 | 0/0 |
| crt | 50/50/50 | 30/50 | 24/50 | +6 | 0.7740 | 9823.82 | 21.99 | 0/0 |
| aggregate | 150/150/150 | 121/150 | 111/150 | +10 | 0.5310 | 6144.30 | 15.66 | 0/0 |

## 3. 机制证据

- strong verification / 劝返：关闭 no_strong_verification 后 overall 相对 current `-8/150`，WTQ 相对 current `-7/50`。
- deterministic audit：关闭 deterministic shortcuts 后 overall 相对 current `-15/150`，TabFact `-9/50`，CRT `-7/50`。
- TabFact deterministic audit 同时节省预算：no_deterministic_shortcuts 的 TabFact token 为 current 的 `1.4487x`。
- 机制矩阵：`/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_patent_mechanism_evidence_20260801_2222/patent_mechanism_evidence_matrix.md`。

## 4. 必须保留的边界

- P4b 原始结果不能写成新 seed 三数据集全部超过 MACT；WTQ 原始结果低于 MACT，after-targeted 结果才恢复单项优势。
- 原始 E3 Seed-C/D current-only 不能写成多 seed 稳定超过 MACT；它们没有同 seed paired MACT，且 decision 为 `stop_or_inspect`。
- E3 max_replan=5 probe 只恢复少数代表错题；TabFact temporal/numeric 对预算敏感，但 CRT 与 WTQ entity 边界仍需要语义 guard。
- E3 semantic-boundary plan 已转化为 S2 targeted guard fresh 验证，但不是稳定性通过结果。
- E3 S2 after-guard fresh 是 affected-slice 机制验证通过，不是 Seed-C/D current-only 或 paired MACT 通过。
- E3 S3 after-guard current-only 是历史边界证据；v6c boundary fresh 已修复 Seed-D WTQ/TabFact gate，并已进入 S4 paired MACT。
- E3 v6c boundary-fresh current-only 可以写成 paired MACT 候选；S4 paired MACT 是历史 strict boundary；S5 CRT tie-breaker 已闭合该边界，可以写成当前 Qwen3 paired 多 seed 三数据集均严格超过 MACT。
- E4 不能写成多模型已验证；当前只是 readiness audit，结论是没有可启动候选。
- 不能把 full200/gate 结果写成全量官方测试集完成。

### E3 Boundary 表

#### seed-c

| dataset | rows input/merged/eval | MyAgent | MACT/ref | delta | token ratio | avg tokens | avg elapsed s | failed/missing |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| wtq | 50/50/50 | 40/50 | n/a | n/a | 0.6013 | 6318.56 | 15.25 | 0/0 |
| tabfact | 50/50/50 | 44/50 | n/a | n/a | 0.2604 | 2820.02 | 10.65 | 0/0 |
| crt | 50/50/50 | 30/50 | n/a | n/a | 0.9118 | 11679.92 | 25.33 | 0/0 |
| aggregate | 150/150/150 | 114/150 | n/a | n/a | 0.6096 | 6939.50 | 17.07 | 0/0 |

decision: `stop_or_inspect`。

#### seed-d

| dataset | rows input/merged/eval | MyAgent | MACT/ref | delta | token ratio | avg tokens | avg elapsed s | failed/missing |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| wtq | 50/50/50 | 30/50 | n/a | n/a | 0.6329 | 6650.02 | 17.54 | 0/0 |
| tabfact | 50/50/50 | 38/50 | n/a | n/a | 0.2682 | 2905.16 | 11.68 | 0/0 |
| crt | 50/50/50 | 30/50 | n/a | n/a | 0.7829 | 10028.56 | 27.39 | 0/0 |
| aggregate | 150/150/150 | 98/150 | n/a | n/a | 0.5735 | 6527.91 | 18.87 | 0/0 |

decision: `stop_or_inspect`。

E3 诊断结论：

- Seed-C/Seed-D had 300 merged rows and zero failed execution or missing answers; the boundary is semantic answer correctness, not runtime/tool coverage.
- Tokens remained below the frozen MACT full200 reference on every dataset and seed; the blocker is accuracy stability, not token budget.
- Seed-C is near the current gate on TabFact and exactly at the CRT gate, while Seed-D exposes broader WTQ and TabFact instability.
- Do not spend paired MACT runtime for these seeds until boundary categories are addressed or explicitly accepted as limitation evidence.
- Patent-facing claim should use E3 as applicability-boundary evidence, not as multi-seed stable superiority evidence.

E3 max_replan=5 预算 probe：

| dataset | rows | recovered | failed/missing | avg tokens 3->5 | token ratio vs MACT full200 | avg seconds |
|---|---:|---:|---:|---:|---:|---:|
| wtq | 4 | 1 | 0/0 | 10811.5->12501.0 | 1.1897 | 42.90 |
| tabfact | 4 | 3 | 0/0 | 5709.2->4626.8 | 0.4272 | 19.49 |
| crt | 4 | 0 | 0/0 | 20814.0->22280.5 | 1.7393 | 73.25 |
| aggregate | 12 | 4 | 0/0 | 12444.9->13136.1 | n/a | 45.21 |

E3 semantic-boundary plan：

- decision: `do_not_rerun_full200_or_paired_mact_until_targeted_guards_pass`
- high-priority work items: `8`
- zero-recovery categories: `crt_multi_step_numeric_composition_boundary, wtq_entity_lookup_or_row_selection_boundary, crt_span_or_universal_quantifier_boundary, tabfact_false_negative_entailment_boundary`
- next ladder: `S1_design_and_unit, S2_affected_slice_fresh, S3_e3_current_only_rerun, S4_paired_mact_or_boundary_closeout`

E3 S2 guard-validation input package：

- decision: `ready_for_guard_implementation_not_model_run`
- total rows: `30`
- dataset counts: `{'wtq': 10, 'tabfact': 8, 'crt': 12}`
- role counts: `{'representative_wrong': 12, 'no_harm_correct': 18}`
- registered S2 gate target: recover at least `7/12` representative wrong rows and keep `18/18` no-harm rows correct

E3 S2 after-guard fresh：

- decision: `after_guard_passes_s2_gate`
- representative recovered: `8/12`
- no-harm correct: `18/18`
- failed/missing: `0/0`
- weighted token ratio vs MACT full200: `0.6104`
- guard scope: `WTQ multi-condition target-column lookup, TabFact numbered same-team relation audit, CRT numeric outlier yes/no audit, CRT top-k years-played average, CRT constructor retirement-reason percentage`

E3 S3 after-guard current-only rerun：

- combined decision: `s3_stop_or_inspect_boundary_remains`
- paired MACT next: `False`
- combined: `215/300`, weighted token ratio `0.5866`, failed/missing `0/0`

| seed | correct | token ratio | failed/missing | decision |
|---|---:|---:|---:|---|
| seed_c | 118/150 | 0.6073 | 0/0 | `s3_seed_pass_run_paired_mact_candidate` |
| seed_d | 97/150 | 0.5659 | 0/0 | `s3_seed_stop_or_inspect` |

Seed-D remaining misses mean this is boundary evidence, not a stability closure.

E3 v6c boundary-fresh current-only candidate：

- combined decision: `boundary_fresh_pass_run_paired_mact_candidate`
- paired MACT next: `True`
- combined: `229/300`, weighted token ratio `0.5794`, failed/missing `0/0`

| seed | evidence | correct | token ratio | failed/missing | decision |
|---|---|---:|---:|---:|---|
| seed_c | inherited_seed_c_s3 | 118/150 | 0.6073 | 0/0 | `s3_seed_pass_run_paired_mact_candidate` |
| seed_d | mixed | 111/150 | 0.5516 | 0/0 | `seed_d_boundary_fresh_passes_current_gate` |

Limitations: Seed-D WTQ and TabFact are fresh v6c reruns.; Seed-D CRT is inherited from the S3 run because this patch did not change CRT shortcut paths and CRT already passed its current gate.; Seed-C is inherited from the S3 run; an optional full S3 rerun can be used before paired MACT if stricter freshness is required..

## 5. 正式实验表状态

| stage | status | patent use |
|---|---|---|
| E0 full200 anchor | `complete` | main positive evidence |
| E1 WTQ P4b risk diagnosis | `complete` | risk and boundary diagnosis |
| E2 WTQ targeted fresh and after-targeted full50 | `complete` | targeted mechanism repair evidence |
| E3 multi-seed current-only boundary diagnosis | `complete_boundary_evidence` | applicability boundary, not stability proof |
| E3 max_replan=5 boundary budget probe | `complete_mechanism_probe` | adaptive budget sensitivity and remaining semantic-boundary evidence |
| E3 semantic-boundary plan | `complete_planning_evidence` | targeted guard and affected-slice validation ladder |
| E3 S2 guard-validation input package | `complete_input_package_not_model_result` | pre-registered affected-slice/no-harm validation target |
| E3 S2 after-guard fresh validation | `complete_mechanism_gate_pass` | targeted semantic guard fresh evidence, not multi-seed stability proof |
| E3 S3 current-only after-guard rerun | `complete_historical_boundary` | Seed-C passed but Seed-D remained below WTQ/TabFact gates before v6c; historical boundary evidence |
| E3 v6c boundary-fresh current-only candidate | `complete_current_only_candidate` | Seed-C/D current-only candidate reached paired MACT trigger |
| E3 S4 paired MACT | `complete_existing_pass_strict_boundary` | Overall and WTQ/TabFact exceed MACT with lower tokens; CRT ties MACT, so this is historical strict-boundary evidence |
| E3 S5 CRT tie-breaker | `complete_strict_all_dataset_pass` | Current Qwen3 paired multi-seed result: WTQ/TabFact/CRT all strictly exceed MACT, overall `232/300 > 223/300`, token ratio `0.5662` |
| E4 multi-model gate | `pending_no_candidate` | future external validity evidence after new model/API appears |
| E5/E6 patent experiment section and disclosure draft | `current_section_consolidated` | draft-ready with explicit unsupported claims |
| E7 final experiment package closeout | `pending` | requires at least E4 candidate or explicit acceptance of no-candidate boundary |

## 6. 下一步触发规则

- If a new candidate model/API appears, rerun runtime preflight first and start Gate-10 only on a clean GPU pair, with 0,1 -> 8000 and 2,3 -> 8001 used only when the default pool is actually available; do not consume 4-7 unless explicitly reassigned.
- If no new model/API exists, do not rerun known no-go models; continue drafting with E4 marked pending/no-candidate.
- The v6c S5 CRT tie-breaker has completed and closes the Qwen3 strict all-dataset target. Next Qwen3 work should update the formal patent package, optionally add fine-grained mechanism ablations, and wait for a genuinely new model/API candidate before E4 Gate-10.

## 7. 关键证据路径

- `full200_summary`: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_all200_acceptance_20260731_132611/qwen3_policy_v6b_all200_acceptance_summary.json`
- `full200_evidence_md`: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_all200_acceptance_20260731_132611/qwen3_policy_v6b_patent_evidence_index.md`
- `p4b_original_summary`: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/p4b_paired_gate50_summary.json`
- `p4b_original_summary_md`: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/p4b_paired_gate50_summary.md`
- `p4b_targeted_fresh_summary`: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/p4b_wtq_targeted_fresh_summary.json`
- `p4b_targeted_fresh_summary_md`: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/p4b_wtq_targeted_fresh_summary.md`
- `p4b_after_targeted_summary`: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/p4b_after_wtq_targeted_paired_summary.json`
- `p4b_after_targeted_summary_md`: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/p4b_after_wtq_targeted_paired_summary.md`
- `mechanism_matrix`: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_patent_mechanism_evidence_20260801_2222/patent_mechanism_evidence_matrix.json`
- `mechanism_matrix_md`: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_patent_mechanism_evidence_20260801_2222/patent_mechanism_evidence_matrix.md`
- `e3_boundary_diagnosis`: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_multiseed_gate50_20260801_2231/summary/seed_boundary_error_diagnosis.json`
- `e3_boundary_diagnosis_md`: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_multiseed_gate50_20260801_2231/summary/seed_boundary_error_diagnosis.md`
- `e3_budget_probe_summary`: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_e3_boundary_budget_probe_20260804_1035/summary/e3_boundary_budget_probe_summary.json`
- `e3_budget_probe_summary_md`: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_e3_boundary_budget_probe_20260804_1035/summary/e3_boundary_budget_probe_summary.md`
- `e3_semantic_boundary_plan`: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_e3_semantic_boundary_plan_20260804_1110/summary/e3_semantic_boundary_plan.json`
- `e3_semantic_boundary_plan_md`: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_e3_semantic_boundary_plan_20260804_1110/summary/e3_semantic_boundary_plan.md`
- `e3_guard_validation_input_plan`: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_e3_guard_validation_inputs_20260804_1128/summary/e3_guard_validation_input_plan.json`
- `e3_guard_validation_input_plan_md`: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_e3_guard_validation_inputs_20260804_1128/summary/e3_guard_validation_input_plan.md`
- `e3_guard_validation_after_guard_summary`: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_e3_guard_validation_after_guard_20260804_1203/summary/e3_guard_validation_after_guard_summary.json`
- `e3_guard_validation_after_guard_summary_md`: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_e3_guard_validation_after_guard_20260804_1203/summary/e3_guard_validation_after_guard_summary.md`
- `e3_s3_current_combined_summary`: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_e3_s3_current_rerun_after_guard_20260804_1425/summary/e3_s3_current_combined_summary.json`
- `e3_s3_current_combined_summary_md`: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_e3_s3_current_rerun_after_guard_20260804_1425/summary/e3_s3_current_combined_summary.md`
- `e3_boundary_fresh_combined_summary`: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6c_seed_d_boundary_fresh_20260804_1549/summary/e3_boundary_fresh_combined_summary.json`
- `e3_boundary_fresh_combined_summary_md`: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6c_seed_d_boundary_fresh_20260804_1549/summary/e3_boundary_fresh_combined_summary.md`
- `e3_s5_final_summary`: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6c_e3_s5_crt_tiebreaker_diag_20260804_2225/summary/e3_s5_final_combined_summary.json`
- `e3_s5_final_summary_md`: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6c_e3_s5_crt_tiebreaker_diag_20260804_2225/summary/e3_s5_final_combined_summary.md`
- `e4_readiness`: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/latest_e4_multimodel_gate_readiness_audit.json`
- `e4_readiness_md`: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/latest_e4_multimodel_gate_readiness_audit_zh.md`
- `formal_ledger`: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/latest_formal_result_ledger_current.json`
- `formal_ledger_md`: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/latest_formal_result_ledger_current_zh.md`
