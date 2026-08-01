# 正式实验排期与成本控制方案

本文档用于把专利/专家所需实验拆成可停止、可复核、可逐步扩样的流程，避免把所有模型、所有样本一次性 full run。

基线成本估计来自 Qwen3-32B full200 已冻结结果：

| dataset | MyAgent avg tokens | MyAgent avg elapsed s | MACT avg tokens | MACT avg elapsed s |
|---|---:|---:|---:|---:|
| WTQ | 6501.03 | 16.80 | 10508.03 | 114.78 |
| TabFact | 2181.67 | 9.76 | 10830.83 | 103.16 |
| CRT | 10839.17 | 24.46 | 12809.99 | 163.68 |
| weighted | 6507.29 | 17.01 | 11382.95 | 127.21 |

这些是单行平均值；实际 wall time 会受 endpoint 数量、GPU 状态、失败重试和 MACT runner 串并行影响。

## A. 立即恢复项：WTQ Targeted Fresh

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

输出：

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/p4b_wtq_targeted_fresh_summary.json
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/p4b_wtq_targeted_fresh_summary.md
```

停止规则：若低于 `7/9`，不扩 WTQ full50，先做 fresh wrong ids 诊断。

## B. WTQ After-Fix P4b Full50

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

停止规则：若没有超过 `43/50`，先更新 WTQ 风险诊断，不进入更大新 seed。

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

该目录已准备 Seed-C/Seed-D，各数据集 50 行输入、manifest、校验脚本、MyAgent runner、MACT runner 和 paired compare runner；模型执行仍 pending。

执行顺序：

| stage | rows | estimated MyAgent tokens | purpose |
|---|---:|---:|---|
| Seed-C Gate-50 | 150 | ~976k | 新 seed 小样本总体稳定性 |
| Seed-D Gate-50 | 150 | ~976k | 第二组新 seed 稳定性 |
| Selected Gate-150 | 450 | ~2.93M | 只在前两组稳定后扩大 |

判断：

1. 不要求每组每个数据集都大幅领先，但 WTQ 不能连续明显落后且无法解释。
2. overall 必须稳定高于 MACT/Qwen reference，token 必须明显低于 MACT。
3. 任何 seed 出现 failed/missing > 2%，先排查 runner/endpoint，不把该结果写成模型效果。
4. 若 current-only summary 的 decision 是 `stop_or_inspect`，不跑 MACT baseline，先诊断该 seed 的 MyAgent 错误。

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

当前本机除 Qwen3-32B 外的已知模型均为 no-go；新增模型或 API key 出现后再启动 gate。

## F. 正式收口

收口条件：

1. Qwen3-32B full200 主证据保持三数据集单项超过 MACT、token 明显低。
2. WTQ targeted fresh 与 WTQ P4b after-fix full50 给出明确结论。
3. 至少 2 个机制模块有消融或离线归因证据。
4. 至少 1 组额外 seed 或 1 个额外模型完成 gate 结论。
5. 所有新增结果有 JSON/MD、路径索引、失败/缺答案、token、耗时和 git 提交号。

未满足 F 之前，当前目标保持 active，不写“正式实验完成”。
