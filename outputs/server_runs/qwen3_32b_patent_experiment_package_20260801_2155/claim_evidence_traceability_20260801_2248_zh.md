# 权利要求-机制-证据可追踪矩阵

创建时间：2026-08-01 22:48 CST
更新时间：2026-08-04 23:52 CST

用途：把可写入专利的权利要求族，对齐到 MyAgent 机制、代码入口、实验数据和仍未闭合的风险。这个文件不是新 benchmark run，而是专利撰写用证据索引。

## 总体边界

当前可强写的是 Qwen3-32B full200 阶段证据：MyAgent `489/600` vs MACT `450/600`，总体 token ratio `0.5717`，三数据集单项均超过 MACT。WTQ targeted fresh 与 P4b after-targeted 闭环已经完成，可作为新 seed 风险修复证据。E3 Seed-C/D current-only 已完成并形成边界证据；E3 max_replan=5 probe 恢复代表错题 `4/12`，可写成预算敏感性和 adaptive replan 机制证据；E3 semantic-boundary plan 已把零恢复类别转成 P0 语义 guard 与 affected-slice fresh 漏斗，且 S2 after-guard fresh 已通过 `8/12` representative recovery 与 `18/18` no-harm gate。S3 after-guard current-only rerun 暴露 Seed-D WTQ/TabFact 边界：combined `215/300`、token ratio `0.5866`、failed/missing `0/0`。v6c boundary-fresh current-only 候选已完成：Seed-D `111/150`，combined `229/300`、token ratio `0.5794`、failed/missing `0/0`、decision `boundary_fresh_pass_run_paired_mact_candidate`。S4 paired MACT 已完成 existing criteria pass：overall MyAgent `229/300` vs MACT `223/300`，token ratio `0.5700`，WTQ/TabFact 严格超过 MACT，CRT 持平。S5 CRT tie-breaker 已闭合 strong strict 目标：overall MyAgent `232/300` vs MACT `223/300`，token ratio `0.5662`，overall failed/missing MyAgent `0/0`、MACT `4/4`，WTQ/TabFact/CRT 三项均严格超过 MACT。fine-grained mechanism audit 已完成，decision=`fine_grained_mechanism_evidence_ready_for_qwen3_patent_scope_with_evidence_retention_boundary_and_e4_pending`。2026-08-04 23:52 E4 readiness 仍为 `no_candidate_wait`，local models `4`、untested local models `0`、API keys/provider profiles `0/0`，不能写成多模型已验证。

## 权利要求族映射

| ID | 权利要求族 | 可写技术点 | 当前证据强度 | 关键证据 | 缺口 |
|---|---|---|---|---|---|
| C1 | 风险分层的选择性协作 | 根据问题语义、表格结构、答案契约和执行信号估计风险，再选择轻量路径、确定性审计或强验证协作 | strong stage evidence | full200 `489/600 > 450/600`，token ratio `0.5717`，elapsed ratio `0.1337`；P4b after-targeted `121/150 > 111/150`；E3 budget probe 显示部分类别可由更高 replan 预算恢复；E3 S2 after-guard fresh `8/12` representative recovered、`18/18` no-harm | E3 已给出 targeted mechanism 正证据和边界，但还不是稳定性正证据；多模型执行后才能写广义模型外延 |
| C2 | 证据保留式表格压缩 | 对比较、时间、序数、计数、实体消歧等风险保留全局行、候选行、晚列和邻接行 | moderate-to-strong supporting evidence with explicit causal boundary | WTQ gain rows `16/25` tagged evidence_retention；TabFact gain rows `9/9` tagged evidence_retention；CRT current-only vs MACT `37/40` tagged evidence_retention；fine-grained audit 将该项归为 attribution + S2 fresh no-harm/guard support | 若专利代理人要求独立因果证据，可补 standalone `no_evidence_retention` 细粒度消融 |
| C3 | 确定性语义审计 | 用结构化规则校验同行约束、列值计数、实体属性、数值差、时间差、overtime、listed-after 目标列、ordinal/cardinal 匹配 | strong mechanism evidence | `no_deterministic_shortcuts` overall `-15/150`；TabFact `-9/50` 且 token/current `1.4487x`；CRT `-7/50`；WTQ targeted fresh `9/9`；E3 S2 after-guard fresh 覆盖 WTQ 多条件 lookup、TabFact 同队编号关系、CRT outlier/top-k/percentage guard；fine-grained audit 将 deterministic audit 标记为 `run_based_strong` | 如专利代理人需要更窄因果拆分，可选补 no-WTQ-deterministic 细粒度消融 |
| C4 | 受控劝返 / verifier override | verifier 与原候选冲突时，只有置信度、答案契约、表格证据、冲突类型都满足条件才接管 | strong stage evidence with fresh closure | `no_strong_verification` overall `-8/150`，WTQ `-7/50`；WTQ `24/25` gain rows tagged strong_verification；P4b WTQ fresh `9/9`；after-targeted P4b `121/150 > 111/150`；E3 semantic-boundary plan 和 S2 after-guard fresh 给出 P0/P1 guard 漏斗闭环；fine-grained audit 中 S2 guard recovery `4/12 -> 8/12` 且 no-harm `17/18 -> 18/18`；v6c boundary-fresh current-only combined `229/300`；S4 paired MACT overall `229/300 > 223/300`；S5 final overall `232/300 > 223/300` 且三数据集 strict pass | 当前 WTQ fresh、E3 S2 affected-slice、S4 paired、S5 strict all-dataset 和 fine-grained audit 缺口已闭合；剩余为可选细粒度 verifier override 因果拆分和 E4 外部模型证据 |
| C5 | 答案契约 enforcement | 将最终答案约束为标量、标签、实体、元组或列表，避免解释句、错列值、错表面形态 | strong stage evidence | full200 failed/missing `0/0`；P4b WTQ 诊断包含 MyAgent concise denotation 胜过 MACT explanatory answer 的样本 | 后续每个 seed/model 继续记录 failed/missing |
| C6 | 预算感知实验漏斗 | Gate-10 -> Gate-50 -> Gate-150 -> paired-200，避免 no-go 模型直接 full run；对预算敏感类别可自适应提高 replan，上限不能无差别放大 | process complete with Qwen3 strict pass and mechanism closeout, E4 pending | 历史非主模型 Gate-50 no-go 已保存；E3 Seed-C/D current-only 已按 gate 完成并停止，合计 `212/300`、failed/missing `0/0`、verification `pass`；E3 max_replan=5 probe 恢复 `4/12`，failed/missing `0/0`；E3 semantic-boundary plan 决定先过 S1/S2 再进入 E3 rerun；S2 after-guard fresh 已通过 `after_guard_passes_s2_gate`；S3 after-guard current-only combined `215/300` 暴露边界；v6c boundary-fresh combined `229/300`、token ratio `0.5794`、failed/missing `0/0`，decision 为 `boundary_fresh_pass_run_paired_mact_candidate`；S4 paired MACT decision `s4_paired_pass_existing_criteria_not_strict`；S5 final decision `s5_strict_all_dataset_pass`；fine-grained audit 记录 S2 token ratio `0.6975 -> 0.6104` 和 S5 overall token ratio `0.5662` | 还缺至少一个可行新模型/API 候选；Qwen3 strict all-dataset 和机制审计缺口已闭合 |

## 可以写入独立权利要求的主线

建议独立权利要求围绕以下组合写：

1. 接收表格、自然语言问题和任务类型。
2. 生成答案契约并进行风险评估。
3. 根据风险选择轻量执行、确定性审计或强验证协作。
4. 在候选答案冲突时执行受控劝返。
5. 输出满足答案契约的答案，并记录 token、耗时、失败/缺答案和证据 metadata。

该主线由 C1、C3、C4、C5 共同支撑，当前已有 full200 主证据和机制消融证据。

## 适合写入从属权利要求的细节

| 从属方向 | 可写细节 | 证据状态 |
|---|---|---|
| 风险特征 | 计数、时间顺序、极值比较、否定表达、多实体约束、答案形态、压缩风险 | 已有机制描述和 full200/P4b 诊断 |
| 压缩保留策略 | 全局行、候选行、晚列、邻接行、目标列 | 已有 attribution；可选补细粒度消融 |
| 确定性审计 | 同行多条件、列值计数、实体属性、数值差、时间差、overtime、listed-after、ordinal/cardinal、CRT difference 标量规整、国家代码规整 | coarse ablation 强支持 TabFact/CRT；WTQ fresh `9/9` 已闭合；E3 S2 after-guard fresh 恢复 `8/12` 且 no-harm `18/18`；S5 CRT100 fresh `65/100 > 62/100` |
| 劝返条件 | verifier 置信度、答案契约、候选相似度、表格证据、冲突类型 | WTQ strong verification 证据充分；P4b after-targeted 已闭合 |
| 预算控制 | 按风险触发高成本路径，按 gate 漏斗控制模型/样本扩展；对预算敏感类别执行 adaptive replan | full200 token/elapsed 强支持；E3 current-only gate 规则已执行；E3 max_replan=5 probe 恢复 `4/12`，说明预算只应类别化触发；E3 semantic-boundary plan 把零恢复类别转入 guard 漏斗；S2 after-guard fresh 已通过；S3 after-guard current-only 显示 Seed-D 边界；v6c boundary-fresh 已形成 paired MACT 候选；多模型 E4 仍待新候选 |

## 证据引用入口

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_all200_acceptance_20260731_132611/qwen3_policy_v6b_all200_acceptance_summary.json
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_patent_mechanism_evidence_20260801_2222/patent_mechanism_evidence_matrix.md
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_coarse_ablation_gate50_20260801_0040/coarse_ablation_gate50_summary.md
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_mechanism_attribution_20260801_0033/mechanism_attribution_summary.md
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/p4b_wtq_discordant_diagnosis.md
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/p4b_wtq_targeted_fix_projection.md
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_multiseed_gate50_20260801_2231/multiseed_gate50_manifest.json
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_e3_boundary_budget_probe_20260804_1035/summary/e3_boundary_budget_probe_summary.md
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_e3_semantic_boundary_plan_20260804_1110/summary/e3_semantic_boundary_plan.md
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_e3_guard_validation_after_guard_20260804_1203/summary/e3_guard_validation_after_guard_summary.md
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_e3_s3_current_rerun_after_guard_20260804_1425/summary/e3_s3_current_combined_summary.md
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6c_e3_s5_crt_tiebreaker_diag_20260804_2225/summary/e3_s5_final_combined_summary.md
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6c_e3_s5_crt_tiebreaker_diag_20260804_2225/summary/s5_crt_canonicalizer_replay_summary.md
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6c_e3_s5_crt_tiebreaker_diag_20260804_2225/summary/s5_affected_slice_real_rerun_summary.md
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6c_e3_fine_grained_mechanism_ablation_audit_20260804_2333/summary/fine_grained_mechanism_ablation_audit.md
```

## 下一步对权利要求最有价值的实验

1. 新模型/API gate：补 C6 的模型外延证据；当前 2026-08-04 23:52 E4 为 `no_candidate_wait`，不能重跑已知 no-go 模型冒充新证据。
2. Qwen3 机制证据细化：S2 affected-slice fresh、S3/S4/S5 和 fine-grained mechanism audit 已完成，current Qwen3 strong all-dataset strict 已达成。若专利代理人要求更窄因果证据，下一步只补 standalone no-evidence-retention、no-WTQ-verifier-override 或 no-specific-deterministic-audit 小样本消融。
3. 细粒度消融：当前可写到“机制证据已足够支撑 Qwen3 专利范围，evidence-retention 带边界”；不要把 standalone no-evidence-retention 写成已完成。
