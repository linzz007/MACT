# 专利实验完成度审计

创建时间：2026-08-01 22:44 CST
最后更新：2026-08-03 11:00 CST

这个审计用于回答“当前距离能写完整专利实验材料还差什么”。它不是新的 benchmark run，而是把当前目标拆成可验证要求，并逐项标注证据、缺口和下一步。

## 当前结论

当前目标不能标记完成。Qwen3-32B full200 主结果已经达标，WTQ fresh 闭环已完成，Seed-C/Seed-D current-only 均已执行但都形成 `stop_or_inspect` 边界；Seed-C/Seed-D 边界错误诊断和至少一个可行多模型 gate 结果仍缺失。

## 环境复核

| item | result |
|---|---|
| `8000/v1/models` | healthy，返回 `qwen3-32b-local` |
| `8001/v1/models` | healthy，返回 `qwen3-32b-local` |
| GPU 0/1/2/3 显存 | `45815/45815/45839/45839 MiB` |
| GPU 0/1/2/3 利用率 | `0%/0%/0%/0%`，当前为已加载但无请求状态 |
| GPU 6/7 显存 | 约 `42015/42011 MiB`，仍有残留 runtime |
| `nvidia-smi --query-compute-apps` | 可见 4 个 vLLM worker，对应 GPU 0/1/2/3 |
| `nvidia-smi pmon -c 1` | 可见 4 个 vLLM worker，对应 GPU 0/1/2/3 |
| runner 进程扫描 | vLLM/API server 进程可见；未发现正在运行的 benchmark runner/tqa/run_sharded_tqa |
| `fuser` | 未安装 |

解释：Qwen3-32B online queue 当前可用 GPU `0,1,2,3` 运行；GPU `6,7` 仍有残留 runtime，但不影响当前 0-3 队列。Seed-C 与 Seed-D current-only 已在该 endpoint set 上完成，并都因 `decision=stop_or_inspect` 按 gate 停在 paired MACT 前。

## 要求逐项审计

| ID | 要求 | 当前状态 | 证据 | 缺口 |
|---|---|---|---|---|
| R1 | Qwen3-32B full200 主证据三数据集超过 MACT 且 token 更低 | complete | `qwen3_policy_v6b_all200_acceptance_summary.json`；MyAgent `489/600` vs MACT `450/600`，token ratio `0.5717` | 无 |
| R2 | 机制证据能支撑“选择性风险协作 / 劝返”而不是样本硬编码 | substantially complete | 机制证据矩阵、coarse ablation、offline attribution | 细粒度 verifier override / evidence retention 消融可选补强 |
| R3 | P4b 暴露的 WTQ 新 seed 风险完成 fresh 闭环 | complete | fresh targeted affected slice `9/9`；after-targeted P4b MyAgent `121/150` vs MACT `111/150`，token ratio `0.5310`，失败/缺答案 `0/0` | 无 |
| R4 | 多 seed 稳定性证明不是单一 seed 偶然 | complete boundary, not stability pass | Seed-C current-only：WTQ `40/50`、TabFact `44/50`、CRT `30/50`、overall `114/150`、token ratio `0.6096`、失败/缺答案 `0/0`、decision=`stop_or_inspect`；Seed-D current-only：WTQ `30/50`、TabFact `38/50`、CRT `30/50`、overall `98/150`、token ratio `0.5735`、失败/缺答案 `0/0`、decision=`stop_or_inspect` | Seed-C/Seed-D 均为边界证据，不是稳定性通过；paired MACT 不需要跑，下一步做边界错误诊断或更多候选模型/seed |
| R5 | 多模型 gate 证明机制外延价值 | partial pending new candidate | 三个历史小模型 Gate-50 no-go；gate runner 已准备 | 还缺至少一个可行新模型/API 候选完成 gate |
| R6 | 专家/专利包和中文说明书初稿 | draft complete final pending | `experiment_package_index_zh.md`、`patent_disclosure_draft_zh.md`、`formal_experiment_schedule_zh.md` | Seed-C/Seed-D 边界诊断和 R5 后更新最终实验表和权利要求支撑 |
| R7 | 全部上下文写入唯一 PRD 和 MACT，并同步 GitHub | complete for current state | MyAgent `76237e4` 已推送；MACT 当前 checkpoint 为 `cc9bb83`，本次 Seed-D 包刷新提交待推送 | 本次 MACT package refresh 推送后，后续边界诊断或多模型 run 完成继续同步 |

## 下一步顺序

1. 先诊断 Seed-C/Seed-D current-only 边界错误，尤其是 Seed-D WTQ `30/50` 和 TabFact `38/50`。
2. 未来只有 current-only 过门槛的 seed 才跑同 ID MACT；Seed-C/Seed-D 当前不跑 paired MACT。
3. 新模型/API 候选出现后，走 Gate-10 -> Gate-50 -> Gate-150 -> paired-200，不直接 full200。

## 结论边界

现在可以写：Qwen3-32B full200 阶段 MyAgent 在 WTQ/TabFact/CRT 三项均超过 MACT，并且总体 token 显著更低；机制证据已经能支持“风险分层、证据保留、确定性审计、冲突劝返、预算控制”的专利方案。

现在不能写：多 seed、多模型已经全部完成，或新 seed 三数据集稳定全部超过 MACT。Seed-C/Seed-D 只能作为稳定性边界/诊断证据，不能作为 paired superiority 正证据。
