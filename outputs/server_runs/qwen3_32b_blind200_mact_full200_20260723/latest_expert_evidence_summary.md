# Qwen3-32B vs MACT 阶段证据摘要

## 可写结论

- canonical full200：myAgent 453/600 (75.5%) vs MACT 450/600 (75.0%)，平均 token 为 MACT 的 57.1%。
- current CRT staged composite：myAgent 456/600 (76.0%) vs MACT 450/600 (75.0%)，平均 token 约为 MACT 的 57.1%。
- 当前 evidence_complete=true，可作为专家/专利材料中的阶段性 paired evidence。

## 必须写明的限制

- strict acceptance：未通过；full200 中 myAgent 不低于 MACT 的数据集数为 1/3。
- 不能写成三个数据集全部超过 MACT，也不能写成 full200 对 MACT 全面显著胜出。
- WTQ 和 TabFact 是 full200 单项短板，优势主要来自 CRT。

## WTQ 修复判断

- WTQ representative100：新 myAgent 与旧 myAgent 同为 69.0%，MACT 为 79.0%；恢复 3 条、回退 3 条、净收益 0 条。
- 因此 WTQ extreme/only 全局行修复不应继续作为下一阶段主线扩大。

## 下一步

- 等待新增/挂载候选模型或提供外部 API key；当前不要重启旧 Qwen3-32B/no-go 模型做重复实验。
- 新候选进入后，先跑 Gate-10 / Gate-50；只有 Gate-50 接近或超过 Qwen3-32B reference，才扩 Gate-150 / Paired-200。
