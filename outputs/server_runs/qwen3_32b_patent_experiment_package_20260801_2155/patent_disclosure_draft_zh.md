# 专利说明书初稿

标题建议：一种面向表格问答和表格事实验证任务的选择性风险协作与劝返方法、装置、设备及存储介质。

更新时间：2026-08-03 12:31 CST

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

## 6. 当前实验效果与实施例

以下实验均为当前已保存证据的汇总，不新增 benchmark 结果。实验任务覆盖 WTQ、TabFact 和 CRT 三类表格推理/事实验证任务，记录 input 行数、merged 行数、eval 行数、正确数、token、耗时和 failed/missing。

### 实施例一：Qwen3-32B Full200 主结果

| dataset | input/merged/eval | MyAgent | MACT | delta | token ratio | failed/missing |
|---|---:|---:|---:|---:|---:|---:|
| WTQ | 200/200/200 | 155/200 | 148/200 | +7 | 0.6187 | 0/0 |
| TabFact | 200/200/200 | 194/200 | 189/200 | +5 | 0.2014 | 0/0 |
| CRT | 200/200/200 | 140/200 | 113/200 | +27 | 0.8461 | 0/0 |
| Aggregate | 600/600/600 | 489/600 | 450/600 | +39 | 0.5717 | 0/0 |

该结果说明：在当前 Qwen3-32B full200 阶段，MyAgent 三数据集单项均超过 MACT，同时整体 token 为 MACT 的约 `57.17%`，整体耗时为 MACT 的约 `13.37%`。

### 实施例二：P4b 新 Seed 风险暴露与闭环

原始 P4b 新 seed 结果：

| dataset | input/merged/eval | MyAgent | MACT | delta | token ratio | failed/missing |
|---|---:|---:|---:|---:|---:|---:|
| WTQ | 50/50/50 | 37/50 | 43/50 | -6 | 0.5980 | 0/0 |
| TabFact | 50/50/50 | 45/50 | 44/50 | +1 | 0.2156 | 0/0 |
| CRT | 50/50/50 | 30/50 | 24/50 | +6 | 0.7740 | 0/0 |
| Overall | 150/150/150 | 112/150 | 111/150 | +1 | 0.5444 | 0/0 |

该结果说明：当前机制 overall 和 token 仍然有效，但 WTQ 新 seed 暴露泛化风险。后续 E1/E2 已定位并修复该风险的主要机制来源。

WTQ E2 targeted projection：

| scope | current | projected | net gain | harm |
|---|---:|---:|---:|---:|
| P4b WTQ offline projection | 37/50 | 46/50 | +9 | 0 |

该投影不能单独替代 fresh model run。2026-08-03 已完成 WTQ affected-slice fresh 验证，结果为 `9/9`，merged/eval `9/9`，failed/missing `0/0`；随后 P4b after-targeted full50 结果为：

| dataset | input/merged/eval | MyAgent | MACT | delta | token ratio | failed/missing |
|---|---:|---:|---:|---:|---:|---:|
| WTQ | 50/50/50 | 46/50 | 43/50 | +3 | 0.5571 | 0/0 |
| TabFact | 50/50/50 | 45/50 | 44/50 | +1 | 0.2156 | 0/0 |
| CRT | 50/50/50 | 30/50 | 24/50 | +6 | 0.7740 | 0/0 |
| Overall | 150/150/150 | 121/150 | 111/150 | +10 | 0.5310 | 0/0 |

该证据说明 E1 诊断出的 WTQ 风险可以被通用机制闭环覆盖，而非样本 ID 硬编码。

### 实施例三：多 Seed 边界诊断

E3 Seed-C/Seed-D current-only Gate-50 也已执行并形成边界证据：Seed-C `114/150`，Seed-D `98/150`，合计 `212/300`，weighted token ratio `0.5916`，failed/missing `0/0`，但二者 decision 均为 `stop_or_inspect`，因此不能写成多 seed 稳定超过 MACT。

| seed | input/merged/eval | MyAgent | token ratio | failed/missing | decision |
|---|---:|---:|---:|---:|---|
| Seed-C | 150/150/150 | 114/150 | 0.6096 | 0/0 | `stop_or_inspect` |
| Seed-D | 150/150/150 | 98/150 | 0.5735 | 0/0 | `stop_or_inspect` |
| Combined | 300/300/300 | 212/300 | 0.5916 | 0/0 | `complete_boundary_evidence` |

该实施例的用途是限定适用边界：当前问题在额外 seed 上主要体现为语义准确率稳定性，不是 runner 失败、工具不可用、缺答案或 token 预算失败。

### 实施例四：多模型 Gate Readiness

E4 多模型 readiness audit 结果为 `no_candidate_wait`：当前只发现已测试/已 no-go 的本地模型，未发现未测本地模型或 API provider profile/key，因此不能写成多模型验证已完成。

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

## 8. 后续需要补入或明确保留边界的正式实验

1. 多模型验证：新本地模型或 API key/provider profile 出现后，至少让 1 个额外模型经过 Gate-10 -> Gate-50 -> Gate-150 漏斗；当前 E4 为 `no_candidate_wait`。
2. 多 seed 稳定性正证据：E3 已经完成两组 current-only 并给出边界，但还没有形成稳定超过 MACT 的 paired seed 证据；若继续优化，先处理 E3 语义边界。
3. 细粒度消融：根据需要补 verifier override、evidence retention、deterministic audit 的细粒度关闭开关。
4. 最终实验包收口：当前实验章节已经 consolidated，但 final closeout 需要多模型候选结果，或明确接受 E4 no-candidate 作为当前外延边界。

## 8.1 证据路径索引

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_all200_acceptance_20260731_132611/qwen3_policy_v6b_all200_acceptance_summary.json
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_all200_acceptance_20260731_132611/qwen3_policy_v6b_patent_evidence_index.md
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/p4b_paired_gate50_summary.json
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/p4b_wtq_targeted_fresh_summary.json
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/p4b_after_wtq_targeted_paired_summary.json
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_multiseed_gate50_20260801_2231/summary/seed_boundary_error_diagnosis.json
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/latest_e4_multimodel_gate_readiness_audit.json
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/latest_current_patent_experiment_section_zh.md
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/latest_completion_gap_audit_current_zh.md
```

## 9. 当前写作边界

可以写：

- Qwen3-32B full200 阶段 MyAgent 三数据集均超过 MACT。
- MyAgent 在该阶段显著降低 token 和耗时。
- 机制由风险路由、证据保留、确定性审计、冲突劝返和预算控制组成。
- P4b 原始结果暴露 WTQ 新 seed 风险；E1/E2 已完成诊断、fresh affected-slice `9/9` 和 after-targeted P4b `121/150` vs MACT `111/150`。
- E3 Seed-C/Seed-D 可作为额外随机种子的适用边界证据。

暂不写：

- 多模型已全面验证。
- 新 seed 三数据集已经全部稳定超过 MACT。
- E3 Seed-C/D 已经证明多 seed 稳定超过 MACT。
