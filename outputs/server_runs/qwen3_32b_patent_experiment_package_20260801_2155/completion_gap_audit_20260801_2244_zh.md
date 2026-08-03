# 专利实验完成度审计

创建时间：2026-08-01 22:44 CST
最后更新：2026-08-03 09:52 CST

这个审计用于回答“当前距离能写完整专利实验材料还差什么”。它不是新的 benchmark run，而是把当前目标拆成可验证要求，并逐项标注证据、缺口和下一步。

## 当前结论

当前目标不能标记完成。Qwen3-32B full200 主结果已经达标，WTQ fresh 闭环已完成，但多 seed 执行和至少一个可行多模型 gate 结果仍缺失。

## 环境复核

| item | result |
|---|---|
| `8000/v1/models` | healthy，返回 `qwen3-32b-local` |
| `8001/v1/models` | healthy，返回 `qwen3-32b-local` |
| GPU 0/1/2/3 显存 | `45815/45815/45839/45839 MiB` |
| GPU 0/1/2/3 利用率 | `0%/0%/0%/0%`，当前为已加载但无请求状态 |
| GPU 6/7 显存 | `42011/42005 MiB`，仍有残留 runtime |
| `nvidia-smi --query-compute-apps` | 可见 4 个 vLLM worker，对应 GPU 0/1/2/3 |
| `nvidia-smi pmon -c 1` | 可见 4 个 vLLM worker，对应 GPU 0/1/2/3 |
| runner 进程扫描 | vLLM/API server 进程可见；未发现正在运行的 benchmark runner/tqa/run_sharded_tqa |
| `fuser` | 未安装 |

解释：Qwen3-32B online queue 当前可用 GPU `0,1,2,3` 运行；GPU `6,7` 仍有残留 runtime，但不影响当前 0-3 队列。

## 要求逐项审计

| ID | 要求 | 当前状态 | 证据 | 缺口 |
|---|---|---|---|---|
| R1 | Qwen3-32B full200 主证据三数据集超过 MACT 且 token 更低 | complete | `qwen3_policy_v6b_all200_acceptance_summary.json`；MyAgent `489/600` vs MACT `450/600`，token ratio `0.5717` | 无 |
| R2 | 机制证据能支撑“选择性风险协作 / 劝返”而不是样本硬编码 | substantially complete | 机制证据矩阵、coarse ablation、offline attribution | 细粒度 verifier override / evidence retention 消融可选补强 |
| R3 | P4b 暴露的 WTQ 新 seed 风险完成 fresh 闭环 | complete | fresh targeted affected slice `9/9`；after-targeted P4b MyAgent `121/150` vs MACT `111/150`，token ratio `0.5310`，失败/缺答案 `0/0` | 无 |
| R4 | 多 seed 稳定性证明不是单一 seed 偶然 | prepared runtime ready | E3 Seed-C/Seed-D 输入和 runner 已准备，总计 `300` 行，校验通过；0-3 endpoint 当前可用 | 还要实际跑 Seed-C/Seed-D current-only 和必要的 paired MACT |
| R5 | 多模型 gate 证明机制外延价值 | partial pending new candidate | 三个历史小模型 Gate-50 no-go；gate runner 已准备 | 还缺至少一个可行新模型/API 候选完成 gate |
| R6 | 专家/专利包和中文说明书初稿 | draft complete final pending | `experiment_package_index_zh.md`、`patent_disclosure_draft_zh.md`、`formal_experiment_schedule_zh.md` | R4/R5 后更新最终实验表和权利要求支撑 |
| R7 | 全部上下文写入唯一 PRD 和 MACT，并同步 GitHub | complete for current state | MyAgent `85bae0f` 已推送；MACT 当前 checkpoint 已推送到 `89f5358`，本次包刷新提交待推送 | 后续 Seed-C/Seed-D 或多模型 run 完成后继续同步 |

## 下一步顺序

1. 用当前健康的 GPU `0,1,2,3` endpoint 跑 E3 Seed-C/Seed-D current-only Gate-50。
2. 只有 current-only 过门槛的 seed 才跑同 ID MACT。
3. 新模型/API 候选出现后，走 Gate-10 -> Gate-50 -> Gate-150 -> paired-200，不直接 full200。

## 结论边界

现在可以写：Qwen3-32B full200 阶段 MyAgent 在 WTQ/TabFact/CRT 三项均超过 MACT，并且总体 token 显著更低；机制证据已经能支持“风险分层、证据保留、确定性审计、冲突劝返、预算控制”的专利方案。

现在不能写：多 seed、多模型已经全部完成，或新 seed 三数据集稳定全部超过 MACT。
