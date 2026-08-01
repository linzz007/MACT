# Qwen3 剩余专利实验队列运行手册

用途：服务器扩容或清空恢复后，用最小可执行入口继续补齐专利实验数据。本文档不替代唯一 PRD；实验结论仍更新到：

```text
/home/ubuntu/lzz/MyAgent/docs/server/server_codex_reports/current-qwen3-mact-experiment-prd.md
```

## 1. 当前总目标

当前目标是完善面向专利编写的 MyAgent vs MACT 实验数据体系：在已达标的 Qwen3-32B full200 主证据基础上，补齐 WTQ fresh 闭环、多 seed 稳定性、机制证据边界、多模型 gate 和正式实验表格，而不是继续无边界优化某一个数据集。

完成判定：

| item | pass condition |
|---|---|
| Qwen3-32B full200 主证据 | 已完成：WTQ/TabFact/CRT 单项均超过 MACT，总体 token ratio `0.5717` |
| WTQ targeted fresh | 9-row affected slice 真实 Qwen run `>=7/9`，failed/missing `0/0` |
| P4b WTQ after-fix full50 | affected-slice 通过后再跑，目标 MyAgent `>43/50`，token ratio `<0.75` |
| E3 multi-seed | Seed-C/Seed-D 先跑 MyAgent current-only；只有 decision=`run_paired_mact` 才跑 MACT |
| 多模型 gate | 新模型或 API 出现后按 Gate-10 -> Gate-50 -> Gate-150；只给最终候选补 paired-200 |
| 归档同步 | 每个完成阶段都保留 eval、merged 行数、token、耗时、失败/缺答案、JSON/MD 路径和 git commit |

## 2. 启动 Qwen3 服务

如果只使用用户当前指定的 GPU `6,7`，开一个服务即可：

```bash
cd /home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_multiseed_gate50_20260801_2231
bash start_qwen3_service.sh 6,7 8000
```

如果 GPU `4,5,6,7` 都干净，可以开两个服务加速；两个命令要放在两个终端或后台会话中：

```bash
cd /home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_multiseed_gate50_20260801_2231
bash start_qwen3_service.sh 4,5 8000
bash start_qwen3_service.sh 6,7 8001
```

健康检查：

```bash
curl -sS -H 'Authorization: Bearer local-vllm-key-change-me' http://127.0.0.1:8000/v1/models
curl -sS -H 'Authorization: Bearer local-vllm-key-change-me' http://127.0.0.1:8001/v1/models
```

只有一个服务时，后续队列使用：

```bash
export VLLM_ENDPOINTS=http://127.0.0.1:8000/v1
```

两个服务时：

```bash
export VLLM_ENDPOINTS=http://127.0.0.1:8000/v1,http://127.0.0.1:8001/v1
```

## 3. 推荐一键队列

队列脚本：

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/run_remaining_qwen3_patent_queue.sh
```

先跑 WTQ fresh 闭环：

```bash
bash /home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/run_remaining_qwen3_patent_queue.sh --phase wtq --checkpoint
```

再跑 Seed-C：

```bash
bash /home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/run_remaining_qwen3_patent_queue.sh --phase seed_c --checkpoint
```

再跑 Seed-D：

```bash
bash /home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/run_remaining_qwen3_patent_queue.sh --phase seed_d --checkpoint
```

如果服务器稳定且希望串行一次跑完剩余 Qwen3 验证：

```bash
bash /home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/run_remaining_qwen3_patent_queue.sh --phase all --checkpoint
```

## 4. 队列停机条件

| phase | automatic stop |
|---|---|
| WTQ targeted fresh | `p4b_wtq_targeted_fresh_summary.json` 不是 `decision=pass`，或不是 9/9 行，或 failed/missing 非 0 |
| P4b WTQ full50 | 只有 targeted fresh pass 才会启动 |
| Seed-C/D current-only | `summary/<seed>_myagent_gate50_summary.json` 不是 `decision=run_paired_mact` 就不跑 MACT |
| Seed-C/D paired MACT | MACT 三数据集和 compare 完成后只打印结论，不自动扩大 Gate-150 |

## 5. 完成后必须补写的位置

每次队列完成一个阶段后，先看正式结果表模板：

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/formal_result_tables_template_20260801_2252_zh.md
```

再更新唯一 PRD：

```text
/home/ubuntu/lzz/MyAgent/docs/server/server_codex_reports/current-qwen3-mact-experiment-prd.md
```

需要保留字段：

```text
input rows
merged rows
eval rows
correct
avg_total_tokens
avg_elapsed_seconds
num_failed_exec
num_missing_answer
token_ratio
decision
evidence_json
evidence_md
git_commit
```
