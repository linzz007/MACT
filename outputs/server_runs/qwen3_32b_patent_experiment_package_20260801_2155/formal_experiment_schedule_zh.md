# 正式实验排期与成本控制方案

本文档用于把专利/专家所需实验拆成可停止、可复核、可逐步扩样的流程，避免把所有模型、所有样本一次性 full run。

当前状态更新：A/B 已在 2026-08-03 完成。WTQ targeted fresh 为 `9/9`，P4b after-targeted full50 后总表为 MyAgent `121/150` vs MACT `111/150`，overall token ratio `0.5310`，failed/missing `0/0`，WTQ/TabFact/CRT 单项均超过 MACT。E3 Seed-C/D current-only 也已完成并形成边界诊断；E4 多模型 gate 最新状态为 `no_candidate_wait`。

基线成本估计来自 Qwen3-32B full200 已冻结结果：

| dataset | MyAgent avg tokens | MyAgent avg elapsed s | MACT avg tokens | MACT avg elapsed s |
|---|---:|---:|---:|---:|
| WTQ | 6501.03 | 16.80 | 10508.03 | 114.78 |
| TabFact | 2181.67 | 9.76 | 10830.83 | 103.16 |
| CRT | 10839.17 | 24.46 | 12809.99 | 163.68 |
| weighted | 6507.29 | 17.01 | 11382.95 | 127.21 |

这些是单行平均值；实际 wall time 会受 endpoint 数量、GPU 状态、失败重试和 MACT runner 串并行影响。

## A. 已完成项：WTQ Targeted Fresh

目的：验证 E2 targeted fixes 不是离线投影假象。

输入：

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/input/wtq_p4b_targeted_fix_affected_slice.jsonl
```

执行：

```bash
bash /home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/run_myagent_wtq_targeted_fix_slice.sh
```

规模：9 行，预计 MyAgent 约 `58.5k` tokens，单 endpoint 按 full200 均值约 `2.5` 分钟模型侧运行时间，不含服务启动。

通过条件：

| item | threshold |
|---|---|
| merged/eval rows | 9/9 |
| failed/missing | 0/0 |
| correct | >= 7/9，优先目标 9/9 |

当前结果：`9/9`，merged/eval `9/9`，failed/missing `0/0`，decision=`pass`。

输出：

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/p4b_wtq_targeted_fresh_summary.json
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/p4b_wtq_targeted_fresh_summary.md
```

停止规则：若未来重跑低于 `7/9`，不扩 WTQ full50，先做 fresh wrong ids 诊断。

## B. 已完成项：WTQ After-Fix P4b Full50

目的：在同一 P4b WTQ 新 seed 上验证 targeted fixes 后是否超过 MACT `43/50`。

执行条件：A 阶段 `decision=pass`。

输入：

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/input/wtq_newseed_gate50.jsonl
```

建议输出目录：

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/myagent_current_after_wtq_targeted_fix/
```

执行：

```bash
bash /home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/run_myagent_wtq_after_targeted_fix_full50.sh
```

该脚本会先检查 A 阶段 `p4b_wtq_targeted_fresh_summary.json` 是否 `decision=pass`，再跑 WTQ full50，并自动生成 after-targeted paired summary。

规模：50 行，预计 MyAgent 约 `325.1k` tokens，单 endpoint 按 full200 均值约 `14.0` 分钟模型侧运行时间。

通过条件：

| item | threshold |
|---|---|
| MyAgent WTQ correct | > 43/50 |
| token ratio vs MACT WTQ P4b | < 0.75，目标保持约 0.60 |
| failed/missing | 0/0 |

当前结果：WTQ `46/50` vs MACT `43/50`，token ratio `0.5571`，failed/missing `0/0`；P4b after-targeted aggregate MyAgent `121/150` vs MACT `111/150`，overall token ratio `0.5310`，三数据集单项均超过 MACT。

停止规则：若未来重跑没有超过 `43/50`，先更新 WTQ 风险诊断，不进入更大新 seed。

输出：

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/p4b_after_wtq_targeted_paired_summary.json
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/p4b_after_wtq_targeted_paired_summary.md
```

## C. 机制消融

目的：给专利材料提供因果证据，证明效果来自选择性风险协作/劝返机制，而不是单纯模型能力或样本修补。

已具备 coarse evidence：

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_coarse_ablation_gate50_20260801_0040/
```

补强顺序：

| order | ablation | sample policy | stop rule |
|---|---|---|---|
| 1 | current vs legacy | 已有 Gate-50 / frozen artifacts | 只整理，不重跑 |
| 2 | no strong verification | 已有 Gate-50 / frozen artifacts | 若贡献清晰，不扩 full200 |
| 3 | no deterministic shortcuts | 已有 Gate-50 / frozen artifacts | 若贡献清晰，不扩 full200 |
| 4 | no WTQ verifier override | 只在 WTQ discordant / targeted slice 上新增细粒度开关 | 若收益小或不稳定，不扩样 |
| 5 | no evidence retention | 只在 WTQ high-risk slice 上新增细粒度开关 | 若收益小或不稳定，不扩样 |

原则：机制消融优先使用 frozen raw/eval 和小样本 targeted slice；只有能明确支持专利权利要求的消融才扩大到 Gate-50。

## D. 多 Seed 稳定性

目的：证明结果不是单一 full200 或单一 P4b seed 的偶然。

当前准备包：

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_multiseed_gate50_20260801_2231/
```

该目录已准备并执行 Seed-C/Seed-D，各数据集 50 行输入、manifest、校验脚本、MyAgent runner、MACT runner 和 paired compare runner 均已保存。2026-08-03 已完成 current-only Gate-50：Seed-C `114/150`，Seed-D `98/150`，合计 `212/300`，weighted token ratio `0.5916`，failed/missing `0/0`，row-level verification `pass`。二者 decision 均为 `stop_or_inspect`，因此 paired MACT 按 gate 规则不继续消耗。

执行状态：

| stage | rows | result | token ratio | decision | purpose |
|---|---:|---:|---:|---|---|
| Seed-C current-only Gate-50 | 150 | 114/150 | 0.6096 | `stop_or_inspect` | 新 seed 小样本边界诊断 |
| Seed-D current-only Gate-50 | 150 | 98/150 | 0.5735 | `stop_or_inspect` | 第二组新 seed 边界诊断 |
| Seed-C/D combined diagnosis | 300 | 212/300 | 0.5916 | `complete_boundary_evidence` | 说明边界来自语义准确率稳定性，不是 runtime/tool/token 问题 |
| Selected Gate-150 | 450 | not started | n/a | `not_triggered` | 只有当前置 seed 形成稳定性正证据后才扩大 |

判断：

1. 不要求每组每个数据集都大幅领先，但 WTQ 不能连续明显落后且无法解释。
2. overall 必须稳定高于 MACT/Qwen reference，token 必须明显低于 MACT。
3. 任何 seed 出现 failed/missing > 2%，先排查 runner/endpoint，不把该结果写成模型效果。
4. 若 current-only summary 的 decision 是 `stop_or_inspect`，不跑 MACT baseline，先诊断该 seed 的 MyAgent 错误。

当前结论：E3 已经完成，但它是适用边界证据，不是“多 seed 稳定超过 MACT”的正证据。若继续优化，应针对 `seed_boundary_error_diagnosis.json/md` 中的语义错误类别做小范围机制修复，再重新进入 current-only gate。

## E. 多模型 Gate

目的：证明机制具有模型外延价值，同时控制服务器成本。

漏斗：

```text
Gate-10 -> Gate-50 -> Gate-150 -> paired-200
```

停止规则：

| gate | stop condition |
|---|---|
| Gate-10 | 失败/缺答案多、明显低于 Qwen3-32B reference、API healthcheck 不通过 |
| Gate-50 | overall 不超过 reference 或 token 不具备优势 |
| Gate-150 | 未达到 paired-200 门槛，或只有单数据集偶然领先 |
| paired-200 | 只给通过 Gate-150 的候选跑，不做全模型枚举 |

当前本机除 Qwen3-32B 外的已知模型均为 no-go；最新 E4 readiness audit 为 `no_candidate_wait`，未发现未测本地模型/API profile/key。新增模型或 API key 出现后再启动 gate；本地模型启动前必须重跑 runtime preflight，只有确认 GPU pair 干净时才使用 `0,1 -> 8000` 与 `2,3 -> 8001` 的默认池。最新记录中 `0-3` 为无可见进程但驱动侧高显存/高利用状态，`4-7` 仍有约 `42GB/卡` 占用，因此不能直接启动在线实验。

## F. 正式收口

收口条件：

1. Qwen3-32B full200 主证据保持三数据集单项超过 MACT、token 明显低。
2. WTQ targeted fresh 与 WTQ P4b after-fix full50 已给出明确结论。
3. 至少 2 个机制模块有消融或离线归因证据。
4. 至少 1 组额外 seed 稳定性正证据或 1 个额外模型完成 gate 结论；当前 E3 是边界证据，E4 是 no-candidate。
5. 所有新增结果有 JSON/MD、路径索引、失败/缺答案、token、耗时和 git 提交号。

未满足 F 之前，当前目标保持 active，不写“正式实验完成”。
