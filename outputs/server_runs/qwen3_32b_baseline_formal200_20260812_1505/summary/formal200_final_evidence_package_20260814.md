# 面向专利编写的 Formal-200 最终证据包

生成日期：2026-08-14 CST

运行目录：

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_baseline_formal200_20260812_1505/
```

用途：把当前可用于论文/专利撰写的 MyAgent vs MACT 实验证据集中到一个可引用文件中。这里记录的是“证据状态”，不是继续优化计划。

## 1. 当前结论

Qwen3-32B Formal-200 主目标已达成：MyAgent 在 WTQ、TabFact、CRT 三个数据集以及总体准确率上均超过 MACT，同时 token 和耗时显著更低。

| 方法 | WTQ | TabFact | CRT | Overall | Avg Token | Token Ratio vs MACT | Avg Time | Time Ratio vs MACT | Fail/Missing |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| MyAgent final | 157/200 = 0.7850 | 190/200 = 0.9500 | 133/200 = 0.6650 | 480/600 = 0.8000 | 6293.12 | 0.5560 | 16.749s | 0.1320 | 0/0 |
| MACT | 156/200 = 0.7800 | 185/200 = 0.9250 | 124/200 = 0.6200 | 465/600 = 0.7750 | 11318.89 | 1.0000 | 126.861s | 1.0000 | 4/4 |
| Direct-CoT | 126/200 = 0.6300 | 149/200 = 0.7450 | 111/200 = 0.5550 | 386/600 = 0.6433 | 712.67 | 0.0630 | 2.552s | 0.0201 | 1/1 |
| Single-Agent Pandas | 138/200 = 0.6900 | 159/200 = 0.7950 | 124/200 = 0.6200 | 421/600 = 0.7017 | 1074.24 | 0.0949 | 7.601s | 0.0599 | 22/28 |

可写结论：

- MyAgent 相比 MACT：总体 `+15/600`，三个数据集均不低于 MACT，且全部超过。
- MyAgent 平均 token 约为 MACT 的 `55.60%`，平均耗时约为 MACT 的 `13.20%`。
- MyAgent 对比 Direct-CoT 和 Single-Agent Pandas 也有明显准确率优势，说明提升不是简单直接提示或单一 Pandas 工具调用带来的。

## 2. 主实验文件

| 项 | 文件 |
|---|---|
| WTQ final MyAgent eval | `diagnostics/wtq_formal200_patch_7168923/eval/wtq_qwen3-32b-local_eval.json` |
| TabFact final MyAgent eval | `diagnostics/tabfact_formal200_patch_5e3e0e8/eval/tabfact_qwen3-32b-local_eval.json` |
| CRT final MyAgent eval | `myagent_formal200/eval/crt_qwen3-32b-local_eval.json` |
| MACT eval | `eval/*_mact_formal200_eval.json` |
| Direct-CoT eval | `direct_cot_formal200/eval/*_qwen3-32b-local_eval.json` |
| Single-Agent Pandas eval | `single_agent_pandas_formal200/eval/*_qwen3-32b-local_eval.json` |
| 机器可读证据 JSON | `summary/formal200_final_evidence_package_20260814.json` |

注意：`summary/main_baseline_summary.md` 是早期 baseline 表，保留历史用途；当前正式引用应使用本文件。

## 3. 机制证据

### 3.1 确定性验证 / 答案规范化

这是当前最强的机制消融证据。

| 证据 | 结果 | 解释 |
|---|---:|---|
| Gate-50 legacy/no-strong reference | 116/150 = 0.7733 | 当前 ablation50 上的可比参考 |
| No deterministic shortcuts | 106/150 = 0.7067 | 去掉确定性 shortcut 后准确率明显下降 |
| Token 变化 | 2516 -> 7465 | 去掉 shortcut 后平均 token 约增加 2 倍以上 |
| TabFact focused table filters | 10/10 | 新增表格确定性规则在目标切片无回归 |
| TabFact focused temporal/rank filters | 15/15 | 时间/排名规则在目标切片无回归 |
| WTQ focused deterministic slices | 6/6, 2/2, 8/8 | WTQ shortcut、count/date、table-filter 切片均通过 |

专利可写点：在表格问答中先使用受限的结构化语义检验器处理高置信可判定问题，只有低置信或复杂问题才进入高成本 LLM 推理，从而同时提高准确率并降低 token。

### 3.2 选择性强验证 / 协作机制

当前证据是“存在机制，但 Gate-50 消融不够能隔离收益”。2026-08-23 已补齐 `no_question_routing`、`no_risk_scoring`、`no_table_compression` 三个机制隔离开关和 ablation50 运行脚本，但尚未执行。

| 证据 | 结果 | 解释 |
|---|---:|---|
| Legacy collaboration | 116/150 = 0.7733 | Gate-50 参考 |
| No strong verification | 116/150 = 0.7733 | 与 legacy 相同，当前切片未隔离强验证收益 |
| TabFact trigger-71 strong vs no-strong control | 51/71 vs 51/71 | 强验证挽回 7 行但回退 7 行，且 token 大幅增加 |

结论：不能把“强验证必然提升准确率”写成强结论。更稳妥的专利表述是“基于风险门控的选择性协作机制，用于在高风险样本上触发额外核查；当前正式收益主要由确定性验证和低成本路径控制体现，强验证分支需要更精细的接受门控”。

### 3.3 表格压缩 / 证据保留

当前正式结果支持效率效果。2026-08-23 已补 `--disable_table_compression` 开关和 `run_ablation_no_table_compression50.sh`，但该消融还未运行。

可写证据：

- MyAgent final token ratio to MACT 是 `0.5560`。
- MyAgent final time ratio to MACT 是 `0.1320`。
- 输出行保留 `compression_info`、`evidence_pack`、`risk_assessment`、`deterministic_shortcut_reason`、`strong_verification_reason` 等可审计字段。

限制：`no_table_compression` 开关已准备但未执行，因此当前还不能把 token 降低完全归因于某一个压缩模块。

## 4. WTQ 泛化边界

WTQ deterministic shortcut 泛化诊断已完成，文件：

```text
summary/wtq_shortcut_generalization_20260814.md
diagnostics/wtq_shortcut_generalization_20260814/
```

| Split | Shortcut hits | Correct hits | Wrong hits | Accuracy on hits |
|---|---:|---:|---:|---:|
| formal200 | 31 | 28 | 3 | 0.9032 |
| blind200_v1 | 19 | 18 | 1 | 0.9474 |
| frozen150 | 32 | 24 | 8 | 0.7500 |
| full_unseen | 438 | 290 | 148 | 0.6621 |
| full_unseen_minus_formal200 | 407 | 262 | 145 | 0.6437 |

结论：WTQ shortcut 在 formal200 和 blind200 上是有效证据，但在全量 unseen 上不能盲目扩张。专利/论文中应把它写成“有高置信门控的确定性验证机制”，不能写成无限泛化的规则库。

## 5. 多模型 gate 边界

已有历史 gate50 no-go 摘要可作为模型边界证据：

| 模型 | Overall | Avg Token | Token Ratio vs MACT | Decision |
|---|---:|---:|---:|---|
| Qwen3-14B-AWQ | 108/150 = 0.7200 | 7344.51 | 0.6521 | no-go |
| Qwen2.5-14B-Instruct-AWQ | 107/150 = 0.7133 | 7308.35 | 0.6489 | no-go |
| Qwen2.5-3B-Instruct | 89/150 = 0.5933 | 7298.51 | 0.6480 | no-go |

文件：

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/multimodel_gate50_summaries_20260730_1948/
```

结论：较小或量化模型能运行但准确率不够。当前专利/论文主模型应限定为 Qwen3-32B，其他模型作为适用边界，不作为同等收益证明。

## 6. 多 seed 稳定性

当前多 seed 证据是“部分完成”，不能宣称广泛稳定 superiority。

| 证据 | 结果 | 解释 |
|---|---:|---|
| P4b paired new-seed Gate-50 | MyAgent 112/150 vs MACT 111/150 | 一个新 seed paired 小样本通过，MyAgent 在 2/3 数据集不低于 MACT |
| Seed-C current-only Gate-50 | 114/150 | 无失败，token 低；没有 paired MACT |
| Seed-D current-only Gate-50 | 98/150 | 暴露 WTQ/TabFact 稳定性边界 |
| Seed-C/D boundary diagnosis | 212/300 = 0.7067 | 语义准确率是边界，不是运行失败 |
| Boundary fresh combined | 229/300, token ratio 0.5794 | 可作为 paired MACT candidate，但还不是 paired superiority 证据 |
| Seed-E paired Gate-50 package | prepared, not executed | 已固定 3 个数据集各 50 行输入和 4567 端点脚本 |

文件：

```text
outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/p4b_paired_gate50_summary.md
outputs/server_runs/qwen3_32b_policy_v6b_multiseed_gate50_20260801_2231/summary/
outputs/server_runs/qwen3_32b_policy_v6c_seed_d_boundary_fresh_20260804_1549/summary/
outputs/server_runs/qwen3_32b_patent_seed_e_gate50_20260823/
```

下一步如果要补强多 seed：优先执行已准备好的 Seed-E Gate-50 paired 小样本，或对 Seed-C/D fresh candidate 跑 paired MACT。不要直接全量多 seed full200。

## 7. 专利说明书初稿素材

### 技术问题

现有表格问答多智能体方法在复杂表格推理中能取得较好准确率，但存在 token 消耗高、耗时长、失败样本多、难以判断何时需要协作核查的问题。简单直接提示或单工具 Pandas 基线准确率不足，完整多智能体协作又成本较高。

### 技术方案

MyAgent 可表述为一种面向表格问答的选择性风险协作方法，包括：

1. 对输入问题和表格结构生成问题类型、风险等级、证据缺口和操作风险特征。
2. 对高置信结构化问题先执行确定性语义验证和答案规范化。
3. 对无法确定的样本进入压缩后的表格证据构造和 LLM 推理路径。
4. 对高风险样本选择性触发额外核查或协作验证。
5. 输出最终答案时保留证据包、压缩信息、风险评估、shortcut 原因、强验证原因等可审计元数据。

### 技术效果

在 Qwen3-32B Formal-200 上，MyAgent 相比 MACT：

- 总体准确率从 `0.7750` 提升到 `0.8000`。
- WTQ、TabFact、CRT 三个数据集均超过 MACT。
- 平均 token 降至 MACT 的 `55.60%`。
- 平均耗时降至 MACT 的 `13.20%`。
- MyAgent `0/0` fail/missing，MACT `4/4` fail/missing。

### 可主张但需谨慎限定的权利要求方向

- 风险门控的选择性协作流程。
- 带证据保留的表格压缩与问题类型路由。
- 面向表格语义的确定性验证和答案规范化模块。
- 基于高置信 verifier 的低成本跳过 LLM 推理机制。
- 输出中保留审计元数据以支持后验错误诊断和动态门控。

### 不应夸大的点

- 不应宣称所有模型均超过 MACT；小模型 gate50 是 no-go。
- 不应宣称全量 WTQ shortcut 泛化可靠；全量 unseen 命中精度不足。
- 不应宣称强验证分支已被 ablation 证明独立提升准确率；当前强验证消融仍需更好切片。
- 不应宣称已完成所有多 seed paired 稳定性实验；当前只有一个 paired new-seed Gate-50 和若干 current-only/boundary 证据。

## 8. 完成度审计

| 目标项 | 状态 | 证据 |
|---|---|---|
| Qwen3 full200 超过 MACT | 完成 | 本文件第 1 节 |
| 三个 baseline | 完成 | MACT、Direct-CoT、Single-Agent Pandas |
| token/time/fail 汇报 | 完成 | 本文件第 1 节 |
| WTQ 泛化诊断 | 完成，作为边界证据 | `wtq_shortcut_generalization_20260814.md` |
| 机制消融 | 部分完成 | deterministic shortcut 充分；strong verification 结果不足；routing/risk/compression 开关和脚本已准备但未执行 |
| 多模型 gate | 完成，作为 no-go 边界 | `multimodel_gate50_summaries_20260730_1948/` |
| 多 seed 稳定性 | 部分完成 | P4b paired newseed + Seed-C/D current-only + Seed-E prepared |
| 专利说明书初稿证据 | 初稿证据已整理 | 本文件第 7 节 |

## 9. 推荐下一步

1. 不继续优化 TabFact/WTQ 单数据集分数，先冻结 Qwen3-32B formal200 主结果。
2. 若要补机制消融，优先运行已准备好的 `run_ablation_no_question_routing50.sh`、`run_ablation_no_risk_scoring50.sh`、`run_ablation_no_table_compression50.sh`。
3. 若要补多 seed，优先执行已准备好的 `qwen3_32b_patent_seed_e_gate50_20260823` paired Gate-50 包，或对已通过 candidate 的 Seed-C/D fresh 数据跑 paired MACT。
4. 若要进入专利撰写，先基于本文件第 7 节写正式中文专利说明书，再把“不应夸大的点”放入实验局限。
