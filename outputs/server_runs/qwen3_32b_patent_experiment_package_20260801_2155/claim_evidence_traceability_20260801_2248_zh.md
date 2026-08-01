# 权利要求-机制-证据可追踪矩阵

创建时间：2026-08-01 22:48 CST

用途：把可写入专利的权利要求族，对齐到 MyAgent 机制、代码入口、实验数据和仍未闭合的风险。这个文件不是新 benchmark run，而是专利撰写用证据索引。

## 总体边界

当前可强写的是 Qwen3-32B full200 阶段证据：MyAgent `489/600` vs MACT `450/600`，总体 token ratio `0.5717`，三数据集单项均超过 MACT。当前不能强写“多 seed / 多模型 / WTQ fresh 闭环已经完成”。

## 权利要求族映射

| ID | 权利要求族 | 可写技术点 | 当前证据强度 | 关键证据 | 缺口 |
|---|---|---|---|---|---|
| C1 | 风险分层的选择性协作 | 根据问题语义、表格结构、答案契约和执行信号估计风险，再选择轻量路径、确定性审计或强验证协作 | strong stage evidence | full200 `489/600 > 450/600`，token ratio `0.5717`，elapsed ratio `0.1337` | 多 seed / 多模型执行后才能写广义稳定性 |
| C2 | 证据保留式表格压缩 | 对比较、时间、序数、计数、实体消歧等风险保留全局行、候选行、晚列和邻接行 | moderate-to-strong associative evidence | WTQ gain rows `16/25` tagged evidence_retention；TabFact gain rows `9/9` tagged evidence_retention；CRT current-only vs MACT `37/40` tagged evidence_retention | 若专利代理人要求因果证据，可补 `no_evidence_retention` 细粒度消融 |
| C3 | 确定性语义审计 | 用结构化规则校验同行约束、列值计数、实体属性、数值差、时间差、overtime、listed-after 目标列、ordinal/cardinal 匹配 | strong mechanism evidence | `no_deterministic_shortcuts` overall `-15/150`；TabFact `-9/50` 且 token/current `1.4487x`；CRT `-7/50` | WTQ specific deterministic fixes 仍待 fresh targeted run |
| C4 | 受控劝返 / verifier override | verifier 与原候选冲突时，只有置信度、答案契约、表格证据、冲突类型都满足条件才接管 | strong stage evidence with fresh gap | `no_strong_verification` overall `-8/150`，WTQ `-7/50`；WTQ `24/25` gain rows tagged strong_verification；P4b WTQ 投影 `37/50 -> 46/50` | 还要跑 WTQ 9-row targeted fresh 和 after-fix full50 |
| C5 | 答案契约 enforcement | 将最终答案约束为标量、标签、实体、元组或列表，避免解释句、错列值、错表面形态 | strong stage evidence | full200 failed/missing `0/0`；P4b WTQ 诊断包含 MyAgent concise denotation 胜过 MACT explanatory answer 的样本 | 后续每个 seed/model 继续记录 failed/missing |
| C6 | 预算感知实验漏斗 | Gate-10 -> Gate-50 -> Gate-150 -> paired-200，避免 no-go 模型直接 full run | process complete, execution pending | 历史非主模型 Gate-50 no-go 已保存；E3 Seed-C/Seed-D 已准备 current-only-before-paired 规则 | 还缺至少一个可行新模型/API 候选和 Seed-C/Seed-D 实跑 |

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
| 确定性审计 | 同行多条件、列值计数、实体属性、数值差、时间差、overtime、listed-after、ordinal/cardinal | coarse ablation 强支持 TabFact/CRT；WTQ fresh pending |
| 劝返条件 | verifier 置信度、答案契约、候选相似度、表格证据、冲突类型 | WTQ strong verification 证据充分；fresh closure pending |
| 预算控制 | 按风险触发高成本路径，按 gate 漏斗控制模型/样本扩展 | full200 token/elapsed 强支持；多模型执行 pending |

## 证据引用入口

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_all200_acceptance_20260731_132611/qwen3_policy_v6b_all200_acceptance_summary.json
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_patent_mechanism_evidence_20260801_2222/patent_mechanism_evidence_matrix.md
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_coarse_ablation_gate50_20260801_0040/coarse_ablation_gate50_summary.md
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_mechanism_attribution_20260801_0033/mechanism_attribution_summary.md
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/p4b_wtq_discordant_diagnosis.md
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/p4b_wtq_targeted_fix_projection.md
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_multiseed_gate50_20260801_2231/multiseed_gate50_manifest.json
```

## 下一步对权利要求最有价值的实验

1. WTQ targeted fresh affected slice：直接补 C4 的 fresh 缺口。
2. P4b WTQ after-fix full50：决定能否写“新 seed WTQ 风险已闭环”。
3. Seed-C/Seed-D current-only 和 paired MACT：补 C1/C6 的稳定性证据。
4. 新模型/API gate：补 C6 的模型外延证据。
