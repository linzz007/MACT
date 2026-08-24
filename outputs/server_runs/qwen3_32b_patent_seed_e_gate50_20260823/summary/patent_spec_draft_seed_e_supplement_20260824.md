# 专利说明书初稿补充证据：Seed-E 稳定性与答案契约机制

生成日期：2026-08-24 CST

本文件是 `formal200_final_evidence_package_20260814.md` 的补充，不替代 Formal-200 主证据包。用途是把 Seed-E paired 负面结果、失败簇诊断、answer-contract 修复和后续实验口径整理成专利说明书初稿可直接引用的证据。

## 1. 当前权威结论

Qwen3-32B Formal-200 主实验已经达标：

| 方法 | WTQ | TabFact | CRT | Overall | Avg Token | Avg Time | Fail/Missing |
|---|---:|---:|---:|---:|---:|---:|---:|
| MyAgent final | 157/200 | 190/200 | 133/200 | 480/600 = 0.8000 | 6293.12 | 16.749s | 0/0 |
| MACT | 156/200 | 185/200 | 124/200 | 465/600 = 0.7750 | 11318.89 | 126.861s | 4/4 |

该结果可以支持“在 Qwen3-32B Formal-200 口径下，MyAgent 同时超过 MACT 准确率并显著降低 token/耗时”的主张。

但 Seed-E paired Gate-50 没有通过稳定性验证：

| Dataset | MyAgent | MACT | Delta | Token Ratio |
|---|---:|---:|---:|---:|
| WTQ | 31/50 | 37/50 | -6 | 0.6456 |
| TabFact | 40/50 | 42/50 | -2 | 0.2408 |
| CRT | 24/50 | 26/50 | -2 | 0.8757 |
| Overall | 95/150 | 105/150 | -10 | 0.6019 |

Seed-E 结论：MyAgent 在该新 seed 上仍保持 token 与失败率优势，但不具备 paired superiority。专利/论文中应把它写成稳定性边界和机制迭代证据，不应写成多 seed 全面通过。

## 2. 可写入专利的技术问题

现有多智能体表格问答系统的问题包括：

- 高成本协作路径对所有样本都调用多个推理步骤，token 与耗时高。
- 简单直接提示或单一 Pandas 工具在复杂表格推理上准确率不足。
- 复杂表格问题存在答案形态错误，例如国家缩写、比例分数、数值精度、yes/no 标签漂移等。
- 强验证或多路径验证在部分样本上能纠错，但也可能覆盖原本正确的结构化执行答案。
- 表格压缩、路由、风险评分和确定性验证各自的贡献需要可审计记录，否则难以形成可复现实验证据。

## 3. 方法初稿

MyAgent 可描述为一种“面向表格问答的选择性风险协作与答案契约验证方法”。核心流程：

1. 接收问题和表格，构建表格 schema、数据集 profile、答案契约和缺失值标记。
2. 基于问题语义和表格结构进行路由，区分简单查找、复杂数值推理、事实验证和 CRT 组合推理。
3. 对表格进行问题相关压缩，保留与目标问题相关的行列证据，同时记录 `compression_info`。
4. 对高置信、可形式化验证的问题执行确定性表格检验，包括 WTQ/TabFact/CRT 的计数、比较、日期、排名、比例和答案形态规则。
5. 对无法确定的样本执行受约束代码生成，要求输出 `final_answer_value`，并用答案契约验证形态、精度、标签、列表/元组长度和 NaN。
6. 对高风险或候选冲突样本触发选择性强验证，但在 CRT 数值题中保护有效的结构化代码执行候选，避免自然语言 verifier 覆盖精确计算。
7. 输出最终答案，并记录候选答案、风险评估、shortcut 原因、强验证原因、证据包和 token/time 统计。

## 4. Answer-Contract 机制补充

Seed-E 失败簇暴露了一个可写入专利的局部机制：答案契约不只检查“有没有答案”，还检查“答案形态是否符合问题要求”。

本轮本地实现的 answer-contract 修复包括：

- WTQ 缩写要求：当问题包含 `use abbreviation` 或 `abbreviation` 时，国家名与三字母代码之间按请求形态归一化，例如 `China -> CHN`。
- CRT 数值精度：未明确指定精度的 average/mean 题默认保留 3 位小数，避免过度舍入。
- CRT 比例格式：proportion 题中可把精确小数转为分数，例如 `0.16666666666666666 -> 1/6`。
- NaN 防护：标量 `NaN` 判为无效，触发重规划，而不是作为有效答案写出。
- CRT 数值执行保护：在 average/proportion/ratio/percent 数值题中，若代码执行候选有效且与强 verifier 数值冲突，默认保留结构化代码执行结果。

离线验证文件：

```text
summary/answer_contract_patch_offline_validation.md
summary/answer_contract_patch_offline_validation.json
```

离线结果：

| ID | Dataset | Previous | Offline Canonicalized | 解释 |
|---|---|---:|---:|---|
| nu-3415 | WTQ | China | CHN | 直接答案形态修复 |
| crt-280 | CRT | 0.16666666666666666 | 1/6 | 直接比例形态修复 |
| crt-502 | CRT | 13.64 | 13.64 | 旧代码已内部 round(..., 2)，需要 focused rerun |
| crt-290 | CRT | 9.0 | 9.0 | 旧代码已内部 round(..., 2)，需要 focused rerun |

当前 focused rerun 还未执行，因为当前 sandbox 无法连接 `127.0.0.1:8000/8001`。可复用输入已准备：

```text
input/diagnostic/seed_e_answer_contract_wtq.jsonl
input/diagnostic/seed_e_answer_contract_crt.jsonl
```

## 5. 实验证据如何写

可强主张：

- 在 Qwen3-32B Formal-200 上，MyAgent 在 WTQ、TabFact、CRT 与 overall 均超过 MACT。
- MyAgent 平均 token 为 MACT 的 55.60%，平均耗时为 MACT 的 13.20%。
- 确定性 shortcut/答案规范化是当前最强机制证据；去掉 deterministic shortcuts 后 Gate-50 从 116/150 降到 106/150，token 明显上升。
- 表格压缩和路由主要支持 token、耗时和可运行性；no-table-compression 出现上下文长度失败。
- Seed-E paired 暴露稳定性边界，说明系统具备进一步机制迭代空间，而不是过拟合式宣称所有 seed 通过。

必须谨慎限定：

- 不能宣称所有模型都超过 MACT。Qwen3-14B-AWQ、Qwen2.5-14B-AWQ、Qwen2.5-3B Gate-50 均为 no-go。
- 不能宣称 WTQ shortcut 可无条件泛化到全量 unseen；全量 unseen shortcut 命中准确率不足。
- 不能宣称强验证分支独立提升准确率；trigger-71 中强验证挽回与回退相抵。
- 不能宣称风险评分独立提升准确率；no-risk 在 Gate-50 上准确率更高但 token 更高。
- 不能宣称多 seed paired 稳定性已经完全通过；Seed-E paired 明确未通过。

## 6. 建议权利要求草案方向

独立权利要求可围绕以下组合：

1. 一种表格问答方法，包括问题路由、风险评估、表格压缩、确定性验证、受约束代码生成、选择性强验证和答案契约归一化。
2. 所述答案契约包括：标签集合、标量/列表/元组形态、数值精度、比例/百分比/分数格式、缺失/NaN 判定和数据集特定输出形态。
3. 所述选择性强验证包括：仅在风险或候选冲突达到阈值时调用额外验证；并在结构化代码执行候选满足数值契约时，阻止自然语言验证候选覆盖该候选。
4. 所述确定性验证包括：根据表格列、行、日期、排名、计数、极值、差值、比例和实体缩写执行低成本校验。
5. 所述方法输出审计元数据，包括路由结果、风险等级、压缩信息、候选答案、确定性规则原因、强验证原因、token 和耗时。

从属权利要求可覆盖：

- WTQ abbreviation-preserving denotation normalization。
- CRT average/proportion/fraction/percent answer-contract normalization。
- TabFact highest/lowest/max/min/date/margin 事实验证。
- 对上下文长度风险的表格压缩和失败避免。
- 对多候选答案的 agreement decision 和 fallback trigger。

## 7. 下一步实验口径

短期：

1. 在有 loopback 的 shell 中运行 answer-contract focused validation。
2. 若 focused validation 至少修复 `nu-3415` 和 `crt-280` 且无回归，则记录为低风险机制补丁。
3. 对 `crt-502`、`crt-290` 检查新代码是否按 3 位小数重新规划；若修复则加入 Seed-E 小结。

中期：

1. 基于 Seed-E MACT-only 行继续做窄机制补丁，不做盲目全量规则扩张。
2. 做 Seed-F/G Gate-50 paired，以验证 answer-contract 和失败簇机制是否改善多 seed 稳定性。
3. 仅当新 seed 稳定性改善后，再考虑昂贵的 full200 复跑。

长期：

1. 将 Formal-200 主证据、机制消融、Seed-E 边界、多模型 no-go 和 answer-contract 机制整理成正式中文专利说明书。
2. 权利要求重点放在“选择性风险协作 + 答案契约验证 + 可审计元数据”，而不是单一规则库。
