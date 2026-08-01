# 专利实验完成度审计

创建时间：2026-08-01 22:44 CST

这个审计用于回答“当前距离能写完整专利实验材料还差什么”。它不是新的 benchmark run，而是把当前目标拆成可验证要求，并逐项标注证据、缺口和下一步。

## 当前结论

当前目标不能标记完成。Qwen3-32B full200 主结果已经达标，但 fresh WTQ 闭环、多 seed 执行和至少一个可行多模型 gate 结果仍缺失。

## 环境复核

| item | result |
|---|---|
| `8000/v1/models` | connection refused |
| `8001/v1/models` | connection refused |
| GPU 6/7 显存 | `42031/42027 MiB` |
| GPU 6/7 利用率 | `100%/100%` |
| `nvidia-smi --query-compute-apps` | 无可见 PID |
| `nvidia-smi pmon -c 1` | 无可见 PID |
| runner 进程扫描 | 未发现 vLLM/API server/MACT runner/tqa/run_sharded_tqa |
| `fuser` | 未安装 |

解释：按用户当前约束只使用 GPU `6,7` 时，现在不能可靠启动 Qwen3-32B fresh run。这个状态更像 GPU runtime/driver 残留，不是可安全关闭的实验进程。

## 要求逐项审计

| ID | 要求 | 当前状态 | 证据 | 缺口 |
|---|---|---|---|---|
| R1 | Qwen3-32B full200 主证据三数据集超过 MACT 且 token 更低 | complete | `qwen3_policy_v6b_all200_acceptance_summary.json`；MyAgent `489/600` vs MACT `450/600`，token ratio `0.5717` | 无 |
| R2 | 机制证据能支撑“选择性风险协作 / 劝返”而不是样本硬编码 | substantially complete | 机制证据矩阵、coarse ablation、offline attribution | 细粒度 verifier override / evidence retention 消融可选补强 |
| R3 | P4b 暴露的 WTQ 新 seed 风险完成 fresh 闭环 | incomplete runtime pending | P4b overall 过，但 WTQ `37/50 < 43/50`；E1 诊断和 E2 投影已完成 | 还要跑 9-row targeted fresh；通过后跑 WTQ after-fix full50 |
| R4 | 多 seed 稳定性证明不是单一 seed 偶然 | prepared not executed | E3 Seed-C/Seed-D 输入和 runner 已准备，总计 `300` 行，校验通过 | 还要实际跑 Seed-C/Seed-D current-only 和必要的 paired MACT |
| R5 | 多模型 gate 证明机制外延价值 | partial pending new candidate | 三个历史小模型 Gate-50 no-go；gate runner 已准备 | 还缺至少一个可行新模型/API 候选完成 gate |
| R6 | 专家/专利包和中文说明书初稿 | draft complete final pending | `experiment_package_index_zh.md`、`patent_disclosure_draft_zh.md`、`formal_experiment_schedule_zh.md` | R3/R4/R5 后更新最终实验表和权利要求支撑 |
| R7 | 全部上下文写入唯一 PRD 和 MACT，并同步 GitHub | complete for current state | MyAgent `6c8bf70`，MACT `0843894` 已推送 | 后续 fresh run 完成后继续同步 |

## 下一步顺序

1. GPU `6,7` 清理/扩容后，先跑 WTQ targeted fresh affected slice。
2. affected slice 通过后，跑 P4b WTQ after-fix full50 和 paired comparison。
3. 跑 E3 Seed-C/Seed-D current-only Gate-50；只有 current-only 过门槛的 seed 才跑同 ID MACT。
4. 新模型/API 候选出现后，走 Gate-10 -> Gate-50 -> Gate-150 -> paired-200，不直接 full200。

## 结论边界

现在可以写：Qwen3-32B full200 阶段 MyAgent 在 WTQ/TabFact/CRT 三项均超过 MACT，并且总体 token 显著更低；机制证据已经能支持“风险分层、证据保留、确定性审计、冲突劝返、预算控制”的专利方案。

现在不能写：多 seed、多模型、fresh WTQ 闭环已经全部完成，或新 seed 三数据集稳定全部超过 MACT。
