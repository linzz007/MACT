# Qwen3-32B Blind200 MACT Full200 Ledger

最后更新：2026-07-23 15:08:55 CST

## 目标

在已完成 `core100` 的基础上，补跑 blind_holdout_200 后 100 条 MACT 输出，形成 Qwen3-32B 下 WTQ / TabFact / CRT 三数据集同 ID `blind200` paired 主证据。

本目录只保存 MACT 侧 raw/log/eval/paired/summary。myAgent 侧 blind200 输出继续使用 MyAgent 仓库中已经完成的 200 行结果。

## 数据口径

| item | value |
|---|---|
| model | Qwen3-32B local |
| served name | `qwen3-32b-local` |
| endpoint | `http://127.0.0.1:8000/v1` |
| dataset split | `/home/ubuntu/lzz/MyAgent/datasets_ready/blind_holdout_200_v1_2026-06-27/*.jsonl` |
| target rows | 200 per dataset |
| seed | copied from `qwen3_32b_blind200_mact_core100_20260722` |
| resume behavior | `--limit 200 --resume`, start index equals existing output line count |

## 当前状态

| dataset | output | rows | status |
|---|---|---:|---|
| WTQ | `wtq_mact_full200.jsonl` | 145/200 | running; row124 and row133 context overflow failures |
| TabFact | `tabfact_mact_full200.jsonl` | 100/200 | seeded from core100; tail100 pending |
| CRT | `crt_mact_full200.jsonl` | 100/200 | seeded from core100; tail100 pending |

## 进度记录

| time | dataset | rows | last id | status | notes |
|---|---|---:|---|---|---|
| 2026-07-23 13:25:38 CST | all | 100/200 each | seed | seeded | copied core100 raw/log/summary |
| 2026-07-23 13:33:25 CST | WTQ | 100/200 | seed | started | host-level `setsid -f bash run_wtq_resume.sh`; healthcheck ok |
| 2026-07-23 13:36:06 CST | WTQ | 101/200 | `nu-4099` | ok | token 8735; elapsed 84.3s |
| 2026-07-23 13:43:32 CST | WTQ | 104/200 | `nu-3939` | ok | row101-row104 all ok; last row token 16520; elapsed 173.7s |
| 2026-07-23 13:55:24 CST | WTQ | 109/200 | `nu-712` | ok | row101-row109 all ok; last row token 7551; elapsed 98.8s |
| 2026-07-23 14:08:29 CST | WTQ | 116/200 | `nu-2903` | ok | row101-row116 all ok; last row token 11749; elapsed 132.6s |
| 2026-07-23 14:15:29 CST | WTQ | 120/200 | `nu-3399` | ok | row101-row120 all ok; last row token 8017; elapsed 102.6s |
| 2026-07-23 14:24:07 CST | WTQ | 124/200 | `nu-3290` | failed | context overflow: input 6145 + max_tokens 2048 > 8192 |
| 2026-07-23 14:24:07 CST | WTQ | 125/200 | `nu-3922` | ok | runner continued after row124; last row token 8291; elapsed 116.7s |
| 2026-07-23 14:24:07 CST | WTQ | 126/200 | `nu-3527` | ok | runner continued; last row token 7678; elapsed 76.6s |
| 2026-07-23 14:37:48 CST | WTQ | 131/200 | `nu-1298` | ok | row127-row131 ok; last row token 6794; elapsed 67.1s |
| 2026-07-23 14:39:01 CST | WTQ | 133/200 | `nu-3139` | failed | context overflow: input 6145 + max_tokens 2048 > 8192 |
| 2026-07-23 14:55:56 CST | WTQ | 138/200 | `nu-824` | ok | row134-row138 ok; last row token 19077; elapsed 307.0s |
| 2026-07-23 15:08:55 CST | WTQ | 144/200 | `nu-976` | ok | row139-row144 ok; last row token 11989; elapsed 130.1s |
| 2026-07-23 15:08:55 CST | WTQ | 145/200 | `nu-2426` | ok | row145 ok; last row token 10617; elapsed 111.2s |

## 已知 core100 结论

```text
myAgent: 237/300 = 0.7900
MACT:    227/300 = 0.7567
token ratio: 0.5913
```

WTQ 的 `nu-4299` 和 `nu-2633` 在 seed 中保留为 MACT context length failure；full200 tail 新增 `nu-3290`、`nu-3139` 同类失败。不能删除或重跑后静默替换；若后续 repair，必须另行标注 repaired 口径。

## 运行入口

```bash
setsid -f bash /home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_blind200_mact_full200_20260723/run_wtq_resume.sh
setsid -f bash /home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_blind200_mact_full200_20260723/run_tabfact_resume.sh
setsid -f bash /home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_blind200_mact_full200_20260723/run_crt_resume.sh
```

建议一次只跑一个数据集，避免同一个 Qwen3-32B vLLM 服务被多个 MACT 长任务压垮。

## 恢复规则

1. 先在 MyAgent 仓库确认服务健康：

```bash
cd /home/ubuntu/lzz/MyAgent
source /home/ubuntu/miniconda3/etc/profile.d/conda.sh
conda activate lzz-agent
source configs/server/qwen3_32b_2gpu_local.env
bash scripts/server/healthcheck_vllm_pool.sh configs/server/qwen3_32b_2gpu_local.env
```

2. 再检查行数：

```bash
wc -l /home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_blind200_mact_full200_20260723/*_mact_full200.jsonl
```

3. 行数少于 200 时，用对应 `run_*_resume.sh` 继续。

4. 每完成约 10 行或一个数据集，提交并推送 MACT `main`，再更新 MyAgent PRD。
