# 面向专家/专利的实验包索引

创建时间：2026-08-01 21:55 CST

本实验包用于支撑“面向表格问答/表格事实验证的选择性风险协作与劝返机制”专利方向。它不是新的 benchmark run，而是把当前已经完成的 MyAgent vs MACT 证据、诊断、消融和下一步验证入口汇总成一份可复核索引。

## 1. 当前阶段结论

当前可以写成阶段性结论：

> 在 Qwen3-32B 本地模型和同口径 full200 评测下，MyAgent 在 WTQ、TabFact、CRT 三个数据集单项均超过 MACT，整体 token 明显低于 MACT，并且 MyAgent 失败/缺答案为 0。

不能写成最终结论：

> 多模型验证已经完成，或多 seed 已稳定超过 MACT。

原因：P4b 原始新 seed Gate-50 虽然 overall 通过 existing paired gate，但 WTQ 单项原始结果是 MyAgent `37/50` vs MACT `43/50`。E1/E2 已经完成诊断、fresh affected-slice `9/9` 和 after-targeted P4b full50；after-targeted 总表为 MyAgent `121/150` vs MACT `111/150`，三数据集单项均超过 MACT。E3 Seed-C/Seed-D current-only 已完成并形成稳定性边界诊断，不是多 seed 稳定通过证据；E3 max_replan=5 budget probe 恢复 `4/12` 代表错题，可写成 adaptive budget 机制证据；E3 semantic-boundary plan 已把未恢复类别转成 P0/P1 语义 guard 与 affected-slice 验证漏斗，且 S2 after-guard fresh 已通过 `8/12` representative recovery 与 `18/18` no-harm gate。当前下一步是 S3 Seed-C/D current-only 复跑，仍不能直接写成多 seed 稳定超过 MACT；E4 readiness audit 为 `no_candidate_wait`，还没有额外模型/API 结果。

## 2. 主结果证据

来源：

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_all200_acceptance_20260731_132611/qwen3_policy_v6b_all200_acceptance_summary.json
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_all200_acceptance_20260731_132611/qwen3_policy_v6b_patent_evidence_index.md
```

| dataset | rows | MyAgent | MACT | delta | token ratio | elapsed ratio | MyAgent failed/missing |
|---|---:|---:|---:|---:|---:|---:|---:|
| WTQ | 200 | 155/200 | 148/200 | +7 | 0.6187 | 0.1464 | 0/0 |
| TabFact | 200 | 194/200 | 189/200 | +5 | 0.2014 | 0.0946 | 0/0 |
| CRT | 200 | 140/200 | 113/200 | +27 | 0.8461 | 0.1495 | 0/0 |
| Aggregate | 600 | 489/600 | 450/600 | +39 | 0.5717 | 0.1337 | 0/0 |

该结果用于支撑“原型阶段有效”和“预算显著降低”的效果描述。

## 3. 机制证据

| mechanism | 实验/诊断证据 | 专利写法 |
|---|---|---|
| 风险分层路由 | full200 aggregate token ratio `0.5717`，elapsed ratio `0.1337` | 先判断样本风险，再决定是否进入高成本验证/协作 |
| 证据保留与压缩控制 | WTQ full200 `155/200 > 148/200`；E1 显示新 seed 风险不是单纯行缺失 | 压缩不是固定裁剪，而是保留与问题形态相关的关键行列 |
| 确定性语义审计 | coarse no-shortcut 使 TabFact 从 `48/50` 降到 `39/50`，CRT 从 `37/50` 降到 `30/50` | 对可结构化验证的模式直接做表格一致性审计 |
| 冲突检测与劝返 | WTQ verifier/candidate 分歧诊断；E2 targeted fixes 覆盖 conflict/answer contract 类错误 | 不是无条件相信审阅器，而是用答案形态、证据和冲突类型约束接管 |
| 预算感知协作 | full200 token/elapsed 均低于 MACT | 只在高风险样本触发昂贵路径，低风险走轻量路径 |

## 4. 消融和归因

coarse diagnostic Gate-50 来源：

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_coarse_ablation_gate50_20260801_0040/coarse_ablation_gate50_summary.md
```

专利机制证据矩阵：

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_patent_mechanism_evidence_20260801_2222/patent_mechanism_evidence_matrix.md
```

关键结论：

1. `legacy` 和 `no_strong_verification` 在 diagnostic slice 上相对 current 的最大差距集中在 WTQ，支持 strong verification / 劝返路径对 WTQ 的贡献。
2. `no_deterministic_shortcuts` 使 TabFact 从 current ref `48/50` 降至 `39/50`，token 变为 current 的 `1.4487x`，说明 deterministic audit 同时提高准确率并降低 token。
3. `no_deterministic_shortcuts` 使 CRT 从 `37/50` 降至 `30/50`，说明 deterministic audit 是跨数据集模块，不是 TabFact 特例。
4. 机制矩阵把 full200 anchor、coarse ablation 和 offline attribution 合并，明确风险协作/劝返、确定性审计、证据保留和预算控制四类专利机制的证据与边界。

限制：这是 diagnostic slice，不是随机新 seed 泛化实验。正式材料中应表述为机制归因证据，不应单独作为泛化准确率。

## 5. 新 seed 证据与 WTQ 风险

P4b 来源：

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/p4b_paired_gate50_summary.md
```

| dataset | MyAgent | MACT | delta | token ratio | failed/missing |
|---|---:|---:|---:|---:|---:|
| WTQ | 37/50 | 43/50 | -6 | 0.5980 | 0/0 |
| TabFact | 45/50 | 44/50 | +1 | 0.2156 | 0/0 |
| CRT | 30/50 | 24/50 | +6 | 0.7740 | 0/0 |
| Overall | 112/150 | 111/150 | +1 | 0.5444 | 0/0 |

解释：P4b overall 和 token 通过 existing paired gate，但 WTQ 单项暴露泛化风险，因此不能把 P4b 写成“新 seed 三数据集全部单项超过 MACT”。

## 6. E1/E2 WTQ 后续诊断

E1 诊断：

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/p4b_wtq_discordant_diagnosis.md
```

配对混淆：`both_correct=34`、`myagent_only=3`、`mact_only=9`、`both_wrong=4`。

E2 targeted fix 投影：

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/p4b_wtq_targeted_fix_projection.md
```

投影结果：WTQ P4b 从 `37/50` 投影到 `46/50`，`wrong_to_correct=9`，`correct_to_wrong=0`。

fresh affected-slice 验证已经完成：

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/p4b_wtq_targeted_fresh_summary.json
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/p4b_wtq_targeted_fresh_summary.md
```

结果：`9/9`，merged/eval `9/9`，failed/missing `0/0`，decision=`pass`。

P4b after-targeted full50 也已完成：

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/p4b_after_wtq_targeted_paired_summary.json
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/p4b_after_wtq_targeted_paired_summary.md
```

| dataset | MyAgent | MACT | delta | token ratio | failed/missing |
|---|---:|---:|---:|---:|---:|
| WTQ | 46/50 | 43/50 | +3 | 0.5571 | 0/0 |
| TabFact | 45/50 | 44/50 | +1 | 0.2156 | 0/0 |
| CRT | 30/50 | 24/50 | +6 | 0.7740 | 0/0 |
| Overall | 121/150 | 111/150 | +10 | 0.5310 | 0/0 |

保留的边界：E2 证明的是 P4b WTQ targeted 机制闭环和 after-targeted new-seed 小样本正证据，不等于多 seed 稳定性或多模型验证。

fresh 验证输入和 runner 入口保留如下：

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/input/wtq_p4b_targeted_fix_affected_slice.jsonl
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/run_myagent_wtq_targeted_fix_slice.sh
```

## 7. 当前未完成项

| item | reason | next action |
|---|---|---|
| E3 多 seed 稳定性正证据 | 旧 Seed-C/Seed-D current-only 都已完成但 decision=`stop_or_inspect`；S2 after-guard fresh 已通过，但还没有 Seed-C/D 复跑正证据 | 进入 S3：用当前 guard 重跑 Seed-C/D current-only，再按 gate 决定是否需要 paired MACT |
| 多模型 gate | 最新 E4 readiness audit 为 `no_candidate_wait`，没有 untested local model 或 API profile/key | 新本地模型/API key 出现后按 Gate-10 -> Gate-50 -> Gate-150 执行 |
| 细粒度消融 | coarse 消融已有，但 verifier override/evidence retention 细粒度 causal 证据仍可增强 | 需要时新增开关并跑 targeted ablation |
| 最终实验包收口 | 当前章节已 consolidated，但 E4 无候选导致最终外延证据仍缺 | 等 E4 candidate 或明确接受 no-candidate 边界后再做 final closeout |

E3 multi-seed 包：

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_multiseed_gate50_20260801_2231/
```

该包已生成并执行 Seed-C/Seed-D current-only Gate-50，各 WTQ/TabFact/CRT `50` 行，总计 `300` 行；Seed-C `114/150`、Seed-D `98/150`，合计 `212/300`，weighted token ratio `0.5916`，failed/missing `0/0`。离线边界诊断为 `verification_status=pass`。该包当前是适用边界证据，不是“多 seed 稳定超过 MACT”的正证据。

E3 max_replan=5 budget probe：

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_e3_boundary_budget_probe_20260804_1035/summary/e3_boundary_budget_probe_summary.md
```

该 probe 对 E3 代表错题执行 `max_replan=5` 复跑，原始 `max_replan=3` 代表错题均错，复跑恢复 `4/12`，failed/missing `0/0`，avg tokens `12444.9 -> 13136.1`。分项为 WTQ `1/4`、TabFact `3/4`、CRT `0/4`。结论是 `mixed_budget_sensitivity_not_enough_for_e3_stability`：TabFact temporal/numeric 和部分 WTQ temporal 可用 adaptive budget 解释，CRT 与 WTQ entity 仍需 semantic guard。

E3 semantic-boundary plan：

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_e3_semantic_boundary_plan_20260804_1110/summary/e3_semantic_boundary_plan.md
```

该计划不是新 benchmark run，而是把 E3 diagnosis 与 budget probe 合并成后续执行漏斗。当前 decision 为 `do_not_rerun_full200_or_paired_mact_until_targeted_guards_pass`；P0 类别包括 CRT multi-step numeric composition、WTQ entity lookup/row selection、CRT span/universal quantifier 和 TabFact false-negative entailment，均属于 budget probe 零恢复类别。S1/S2 已完成，S2 after-guard fresh 已通过；下一步是 S3 重跑 E3 current-only，S4 仅在 Seed-C/D current-only 都过 gate 后才跑 paired MACT。

E3 S2 guard-validation input package：

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_e3_guard_validation_inputs_20260804_1128/summary/e3_guard_validation_input_plan.md
```

该包是 semantic guard 的预注册验证输入。它包含 `30` 行：`12` 条代表错题和 `18` 条 no-harm 正确行；WTQ/TabFact/CRT 分别 `10/8/12` 行。S2 fresh gate 的最低目标是恢复至少 `7/12` 代表错题，同时保持 `18/18` no-harm 行正确，failed/missing 为 `0`。

E3 S2 after-guard fresh：

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_e3_guard_validation_after_guard_20260804_1203/summary/e3_guard_validation_after_guard_summary.md
```

2026-08-04 已用当前 gold-free semantic guards 跑完该 `30` 行 affected-slice/no-harm 包，decision=`after_guard_passes_s2_gate`。总体结果：representative recovered `8/12`，no-harm correct `18/18`，failed/missing `0/0`，weighted token ratio vs MACT full200 `0.6104`。分项为 WTQ `2/4` representative recovered、`6/6` no-harm；TabFact `4/4` recovered、`4/4` no-harm；CRT `2/4` recovered、`8/8` no-harm。结论：S2 已通过，下一步是 S3 Seed-C/D current-only rerun；这仍是 targeted mechanism gate，不是多 seed 稳定性正证据。

## 8. 剩余 Qwen3 队列入口

当前已恢复两个 Qwen3-32B endpoint：GPU `2,3` -> `http://127.0.0.1:8000/v1`，GPU `0,1` -> `http://127.0.0.1:8001/v1`，served model 均为 `qwen3-32b-local`。按用户要求，这两个服务保持常驻，不主动释放显存。后续若要继续小规模 sanity、消融或队列验证，优先使用带停机条件的队列脚本，而不是手工串起所有 runner：

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/run_remaining_qwen3_patent_queue.sh
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/remaining_qwen3_queue_runbook_zh.md
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/preflight_qwen3_runtime.py
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/latest_qwen3_runtime_preflight_zh.md
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/build_current_formal_result_ledger.py
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/latest_formal_result_ledger_current_zh.md
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/build_current_patent_experiment_section.py
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/latest_current_patent_experiment_section_zh.md
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/audit_patent_package_consistency.py
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/latest_patent_package_consistency_audit_zh.md
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/build_patent_package_checksums.py
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/SHA256SUMS
```

建议顺序：

```bash
export VLLM_ENDPOINTS=http://127.0.0.1:8000/v1,http://127.0.0.1:8001/v1
bash /home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/run_remaining_qwen3_patent_queue.sh --phase wtq --checkpoint

export VLLM_ENDPOINTS=http://127.0.0.1:8000/v1,http://127.0.0.1:8001/v1
bash /home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/run_remaining_qwen3_patent_queue.sh --phase seed_c --checkpoint
bash /home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/run_remaining_qwen3_patent_queue.sh --phase seed_d --checkpoint
```

该脚本会在 WTQ targeted fresh 未通过时停止，不会启动 WTQ full50；也会在 Seed-C/D current-only 未通过时停止，不会启动 MACT paired。它不会自动扩大到 Gate-150 或 full200。当前两个 endpoint 已常驻；若服务状态变化，先重跑 runtime preflight，再决定是否恢复双 endpoint。

当前正式结果台账由 `build_current_formal_result_ledger.py` 从 frozen summary、P4b summary、WTQ fresh/after-targeted、E3、E4、模板和 latest preflight 生成，用于专家/专利材料填表；它不会把 pending 项写成 completed。当前专利实验章节由 `build_current_patent_experiment_section.py` 生成，明确列出可写正证据和不能写的边界。

`audit_patent_package_consistency.py` 用于检查 PRD、manifest、latest formal ledger、latest preflight 和关键数字是否一致。在线阻塞会记录为 warning；数字或路径不一致会记录为 error。

`build_patent_package_checksums.py` 用于生成 `SHA256SUMS`，覆盖本实验包文件和 manifest 中已经存在的关键证据文件。服务器清空/迁移后，可在 `/home/ubuntu/lzz` 下执行 `sha256sum -c MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/SHA256SUMS` 校验恢复完整性。

## 9. 专家可复核路径

唯一 PRD：

```text
/home/ubuntu/lzz/MyAgent/docs/server/server_codex_reports/current-qwen3-mact-experiment-prd.md
```

本包 manifest：

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/evidence_manifest.json
```

最新完成度审计：

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/latest_completion_gap_audit_current_zh.md
```

旧 `completion_gap_audit_20260801_2244_zh.md` 只保留为历史记录；当前缺口判断以 latest current audit 为准。

权利要求-机制-证据可追踪矩阵：

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/claim_evidence_traceability_20260801_2248_zh.md
```

正式实验结果表模板：

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/formal_result_tables_template_20260801_2252_zh.md
```
