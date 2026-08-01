# 专利说明书初稿

标题建议：一种面向表格问答和表格事实验证任务的选择性风险协作与劝返方法、装置、设备及存储介质。

## 1. 技术领域

本方案属于自然语言处理、表格问答、表格事实验证、多智能体协作推理和大语言模型成本控制领域，尤其涉及一种在表格推理任务中根据样本风险选择性触发协作、审计和劝返的推理方法。

## 2. 背景问题

现有表格推理系统通常存在两类问题：

1. 单一路径推理成本低，但在复杂比较、时间顺序、计数、极值和多实体约束场景下容易遗漏关键行列或输出不符合答案契约。
2. 多智能体或多轮协作路径准确率可能更高，但大量样本都进入高成本流程，导致 token 和耗时显著增加。

本项目的实验显示，MACT 作为强协作 baseline 在部分新 seed WTQ 样本上具有优势，但整体 token 和耗时显著更高。MyAgent 的目标不是无条件增加协作，而是将协作限定在有必要的高风险样本，并对低风险或结构化场景使用确定性审计。

## 3. 技术方案

本方案包括以下模块：

1. 风险分层路由模块：根据问题文本、表格结构、估计触达单元格、答案契约、任务类型和历史执行信号，判断样本为轻量、中等、高风险或 fallback。
2. 证据保留与压缩控制模块：在压缩表格前识别比较、时间、极值、计数、否定和多实体问题，保留关键行、候选行、晚列证据和全局上下文，避免答案证据被裁剪。
3. 确定性语义审计模块：对可结构化判断的问题直接从表格执行规则审计，例如同行多条件、列值计数、实体属性、数值差、时间差、overtime 标记、listed-after 目标列和 ordinal phrase 匹配。
4. 冲突检测与劝返模块：生成器、代码执行、候选答案、审阅器或强验证器之间发生冲突时，不直接接受任一方，而是根据答案形态、表格证据、问题语义和置信度决定是否由审阅器/验证器接管。
5. 预算感知协作模块：仅在风险或冲突达到阈值时触发昂贵协作路径，低风险样本保留简单执行或确定性 shortcut。

## 4. 方法流程

1. 接收表格、问题和任务类型，生成答案契约，确定输出是标量、列表、二元标签或元组。
2. 对问题进行风险评估，识别比较、时间、极值、计数、否定、多实体和答案形态风险。
3. 根据风险选择表格压缩策略；若存在全局比较或时间邻接风险，则保留全局行或关键候选行列。
4. 对可确定性审计的问题先执行结构化审计；若命中且答案契约通过，则直接输出。
5. 对未命中 shortcut 或高风险样本，执行 LLM planner/code 路径并得到候选答案。
6. 对高风险或候选冲突样本触发 verifier/thinking path，产生独立候选。
7. 通过劝返规则判断是否保留原候选、接受 verifier 候选或进入 fallback。
8. 输出最终答案、答案契约校验结果、token、耗时、失败/缺答案状态和可复核 metadata。

## 5. 关键创新点

1. 选择性协作：不是所有样本都进行多智能体协作，而是按风险和冲突触发。
2. 受控劝返：不是无条件相信 verifier，而是要求高置信、表内证据支持、答案形态合理，并避免覆盖受保护的确定性 shortcut。
3. 证据保留式压缩：压缩策略受问题类型控制，保留可能承载答案的全局行、候选行和晚列。
4. 确定性语义审计：将部分表格事实判断从自由文本推理转为可复核的表格一致性校验。
5. 预算感知实验漏斗：新模型和新样本先经过 Gate-10/Gate-50/Gate-150，只让入围候选进入 paired-200，降低正式实验成本。

## 6. 当前实验效果

Qwen3-32B full200 主结果：

| dataset | MyAgent | MACT | delta | token ratio |
|---|---:|---:|---:|---:|
| WTQ | 155/200 | 148/200 | +7 | 0.6187 |
| TabFact | 194/200 | 189/200 | +5 | 0.2014 |
| CRT | 140/200 | 113/200 | +27 | 0.8461 |
| Aggregate | 489/600 | 450/600 | +39 | 0.5717 |

该结果说明：在当前 Qwen3-32B full200 阶段，MyAgent 三数据集单项均超过 MACT，同时整体 token 为 MACT 的约 `57.17%`，整体耗时为 MACT 的约 `13.37%`。

新 seed P4b 结果：

| dataset | MyAgent | MACT | delta | token ratio |
|---|---:|---:|---:|---:|
| WTQ | 37/50 | 43/50 | -6 | 0.5980 |
| TabFact | 45/50 | 44/50 | +1 | 0.2156 |
| CRT | 30/50 | 24/50 | +6 | 0.7740 |
| Overall | 112/150 | 111/150 | +1 | 0.5444 |

该结果说明：当前机制 overall 和 token 仍然有效，但 WTQ 新 seed 暴露泛化风险。后续 E1/E2 已定位并修复该风险的主要机制来源。

WTQ E2 targeted projection：

| scope | current | projected | net gain | harm |
|---|---:|---:|---:|---:|
| P4b WTQ offline projection | 37/50 | 46/50 | +9 | 0 |

该投影不能替代 fresh model run，但说明 E1 诊断出的 9 条 MACT-only WTQ 错误均可由通用机制覆盖，而非样本 ID 硬编码。

机制证据矩阵：

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_patent_mechanism_evidence_20260801_2222/patent_mechanism_evidence_matrix.md
```

该矩阵将 full200 主结果、coarse Gate-50 消融和 offline attribution 合并为专利可引用证据。当前可写的机制证据包括：关闭 strong verification 在 diagnostic slice 上 overall `-8/150`，其中 WTQ `-7/50`；关闭 deterministic shortcuts overall `-15/150`，其中 TabFact `-9/50` 且 token 为 current 的 `1.4487x`，CRT `-7/50`；offline attribution 中 WTQ gain rows `24/25` 带 strong-verification tag，TabFact gain rows `8/9` 带 deterministic-audit tag。

## 7. 权利要求草案方向

权利要求与实验证据的逐项映射见：

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/claim_evidence_traceability_20260801_2248_zh.md
```

1. 一种表格推理方法，包括：接收表格和自然语言问题；生成答案契约；基于问题类型和表格结构评估风险；根据风险选择轻量路径、确定性审计路径或强验证协作路径；在候选答案冲突时执行劝返判断；输出满足答案契约的结果。
2. 根据权利要求 1 所述的方法，其中风险评估至少包括计数、时间顺序、极值比较、否定表达、多实体约束、答案形态和表格压缩风险。
3. 根据权利要求 1 所述的方法，其中表格压缩策略根据风险保留全局行、候选行、晚列证据或原始表格子集。
4. 根据权利要求 1 所述的方法，其中确定性语义审计包括同行约束、列值计数、实体属性、数值差、时间差、overtime 标记、listed-after 目标列和 ordinal/cardinal 表达匹配。
5. 根据权利要求 1 所述的方法，其中劝返判断基于 verifier 置信度、答案契约、候选答案相似度、原始表格证据和冲突类型决定是否接受 verifier 候选。
6. 根据权利要求 1 所述的方法，其中预算控制模块根据历史 token 参考值和当前风险，仅对满足触发条件的样本执行高成本协作。
7. 一种装置，包括用于执行上述方法的风险路由单元、证据压缩单元、语义审计单元、冲突劝返单元和预算控制单元。
8. 一种电子设备和计算机可读存储介质，其上存储的程序在执行时实现上述方法。

## 8. 后续需要补入的正式实验

1. WTQ affected-slice fresh Qwen 验证：验证 E2 targeted fixes 是否在真实 runner 下复现 `9/9` 修正方向。
2. P4b WTQ after-fix full50：若 affected-slice 通过，重跑同一批 WTQ 50 条，确认是否超过 MACT `43/50`。
3. 多 seed 稳定性：补至少 2 组 Gate-50 或 1 组 Gate-100/150。
4. 多模型验证：服务器扩容或 API key 可用后，至少让 1 个额外模型经过 gate 漏斗。
5. 细粒度消融：根据需要补 verifier override、evidence retention、deterministic audit 的细粒度关闭开关。

## 9. 当前写作边界

可以写：

- Qwen3-32B full200 阶段 MyAgent 三数据集均超过 MACT。
- MyAgent 在该阶段显著降低 token 和耗时。
- 机制由风险路由、证据保留、确定性审计、冲突劝返和预算控制组成。
- P4b 暴露 WTQ 新 seed 风险，E1/E2 已完成诊断和离线 targeted projection。

暂不写：

- 多模型已全面验证。
- 新 seed 三数据集已经全部稳定超过 MACT。
- E2 WTQ targeted fixes 已经完成 fresh model run。
