# 面向专家/专利的实验包索引

创建时间：2026-08-01 21:55 CST

本实验包用于支撑“面向表格问答/表格事实验证的选择性风险协作与劝返机制”专利方向。它不是新的 benchmark run，而是把当前已经完成的 MyAgent vs MACT 证据、诊断、消融和下一步验证入口汇总成一份可复核索引。

## 1. 当前阶段结论

当前可以写成阶段性结论：

> 在 Qwen3-32B 本地模型和同口径 full200 评测下，MyAgent 在 WTQ、TabFact、CRT 三个数据集单项均超过 MACT，整体 token 明显低于 MACT，并且 MyAgent 失败/缺答案为 0。

不能写成最终结论：

> 多模型、多 seed、fresh targeted 验证已经全部完成。

原因：P4b 新 seed Gate-50 虽然 overall 通过 existing paired gate，但 WTQ 单项原始结果是 MyAgent `37/50` vs MACT `43/50`。E1/E2 已经完成诊断和离线投影，但 fresh Qwen targeted run 尚未执行。

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

边界：这是 offline projection，不是 fresh model run。fresh 验证入口：

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/input/wtq_p4b_targeted_fix_affected_slice.jsonl
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/run_myagent_wtq_targeted_fix_slice.sh
```

## 7. 当前未完成项

| item | reason | next action |
|---|---|---|
| WTQ targeted fresh Qwen validation | endpoint 8000/8001 down，GPU 有 residual memory | 服务器清理/扩容后先跑 9-row affected slice |
| P4b WTQ after-fix full50 | 需要 affected-slice fresh 先验证机制方向 | affected-slice 过后再重跑 WTQ full50 |
| 多 seed 稳定性 | E3 Seed-C/Seed-D 输入和 runner 已准备，但尚未执行模型 | 服务器恢复后先跑 current-only Gate-50；通过后再跑同 ID MACT baseline |
| 多模型 gate | 当前只有 Qwen3-32B 真正有效 | 新本地模型/API key 出现后按 Gate-10 -> Gate-50 -> Gate-150 执行 |
| 细粒度消融 | coarse 消融已有，但 verifier override/evidence retention 细粒度 causal 证据仍可增强 | 需要时新增开关并跑 targeted ablation |

E3 multi-seed 准备包：

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_multiseed_gate50_20260801_2231/
```

该包已生成 Seed-C/Seed-D 各 WTQ/TabFact/CRT `50` 行输入，总计 `300` 行，并通过 `verify_multiseed_package.py` 校验。它只是准备包，不包含模型运行结果。

## 8. 专家可复核路径

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
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/completion_gap_audit_20260801_2244_zh.md
```

权利要求-机制-证据可追踪矩阵：

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/claim_evidence_traceability_20260801_2248_zh.md
```

正式实验结果表模板：

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/formal_result_tables_template_20260801_2252_zh.md
```
