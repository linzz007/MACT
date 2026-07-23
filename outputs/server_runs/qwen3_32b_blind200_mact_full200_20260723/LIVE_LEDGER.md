# Qwen3-32B Blind200 MACT Full200 Ledger

最后更新：2026-07-23 16:50:49 CST

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
| WTQ | `wtq_mact_full200.jsonl` | 200/200 | complete; 5 context overflow failures |
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
| 2026-07-23 15:17:48 CST | WTQ | 150/200 | `nu-4291` | ok | row146-row150 ok; last row token 7621; elapsed 58.9s |
| 2026-07-23 15:20:10 CST | WTQ | 151/200 | `nu-2973` | ok | row151 ok; last row token 8857; elapsed 100.5s |
| 2026-07-23 15:20:10 CST | WTQ | 152/200 | `nu-1313` | ok | row152 ok; last row token 11224; elapsed 98.6s |
| 2026-07-23 15:23:22 CST | WTQ | 153/200 | `nu-3488` | ok | row153 already included in raw checkpoint; last row token 5876; elapsed 43.4s |
| 2026-07-23 15:36:06 CST | WTQ | 154/200 | `nu-1030` | ok | row154 ok; last row token 28688; elapsed 286.6s |
| 2026-07-23 15:36:06 CST | WTQ | 155/200 | `nu-3027` | ok | row155 ok; last row token 8149; elapsed 77.4s |
| 2026-07-23 15:36:06 CST | WTQ | 156/200 | `nu-3487` | failed | context overflow: input 6145 + max_tokens 2048 > 8192 |
| 2026-07-23 15:36:06 CST | WTQ | 157/200 | `nu-1424` | ok | row157 ok; last row token 12536; elapsed 132.3s |
| 2026-07-23 15:36:06 CST | WTQ | 158/200 | `nu-4318` | ok | row158 ok; last row token 12200; elapsed 43.5s |
| 2026-07-23 15:36:06 CST | WTQ | 159/200 | `nu-2547` | ok | row159 ok; last row token 6919; elapsed 54.6s |
| 2026-07-23 15:36:06 CST | WTQ | 160/200 | `nu-2981` | ok | row160 ok; last row token 6861; elapsed 56.8s |
| 2026-07-23 15:36:06 CST | WTQ | 161/200 | `nu-2032` | ok | row161 ok; last row token 11062; elapsed 191.8s |
| 2026-07-23 15:38:28 CST | WTQ | 162/200 | `nu-1761` | ok | row162 ok; last row token 9027; elapsed 124.9s |
| 2026-07-23 15:40:06 CST | WTQ | 163/200 | `nu-3074` | ok | row163 ok; last row token 6026; elapsed 53.1s |
| 2026-07-23 15:40:06 CST | WTQ | 164/200 | `nu-2506` | ok | row164 ok; last row token 5781; elapsed 44.1s |
| 2026-07-23 15:42:35 CST | WTQ | 165/200 | `nu-65` | ok | row165 ok; last row token 15989; elapsed 114.2s |
| 2026-07-23 15:47:28 CST | WTQ | 166/200 | `nu-1446` | ok | row166 ok; last row token 21356; elapsed 284.3s |
| 2026-07-23 15:48:48 CST | WTQ | 167/200 | `nu-1246` | ok | row167 ok; last row token 8842; elapsed 94.9s |
| 2026-07-23 15:50:28 CST | WTQ | 168/200 | `nu-267` | ok | row168 ok; last row token 7529; elapsed 87.4s |
| 2026-07-23 15:51:30 CST | WTQ | 169/200 | `nu-4092` | ok | row169 ok; last row token 6851; elapsed 73.9s |
| 2026-07-23 15:56:46 CST | WTQ | 170/200 | `nu-107` | ok | row170 ok; last row token 7174; elapsed 48.0s |
| 2026-07-23 15:56:46 CST | WTQ | 171/200 | `nu-543` | ok | row171 ok; last row token 9311; elapsed 102.5s |
| 2026-07-23 15:56:46 CST | WTQ | 172/200 | `nu-3982` | ok | row172 ok; last row token 7084; elapsed 97.7s |
| 2026-07-23 15:56:46 CST | WTQ | 173/200 | `nu-721` | ok | row173 ok; last row token 8239; elapsed 97.7s |
| 2026-07-23 16:03:17 CST | WTQ | 174/200 | `nu-4162` | ok | row174 ok; last row token 15162; elapsed 286.9s |
| 2026-07-23 16:05:22 CST | WTQ | 175/200 | `nu-641` | ok | row175 ok; last row token 16995; elapsed 202.7s |
| 2026-07-23 16:11:12 CST | WTQ | 176/200 | `nu-1615` | ok | row176 ok; last row token 6561; elapsed 68.9s |
| 2026-07-23 16:11:12 CST | WTQ | 177/200 | `nu-1845` | ok | row177 ok; last row token 8050; elapsed 86.1s |
| 2026-07-23 16:11:12 CST | WTQ | 178/200 | `nu-888` | ok | row178 ok; last row token 2259; elapsed 21.3s |
| 2026-07-23 16:12:29 CST | WTQ | 179/200 | `nu-1498` | ok | row179 ok; last row token 17523; elapsed 220.9s |
| 2026-07-23 16:14:02 CST | WTQ | 180/200 | `nu-53` | ok | row180 ok; last row token 10299; elapsed 114.9s |
| 2026-07-23 16:20:50 CST | WTQ | 181/200 | `nu-2144` | ok | row181 ok; last row token 10515; elapsed 108.9s |
| 2026-07-23 16:20:50 CST | WTQ | 182/200 | `nu-717` | ok | row182 ok; last row token 5679; elapsed 28.6s |
| 2026-07-23 16:20:50 CST | WTQ | 183/200 | `nu-1970` | ok | row183 ok; last row token 7539; elapsed 93.1s |
| 2026-07-23 16:20:50 CST | WTQ | 184/200 | `nu-1915` | ok | row184 ok; last row token 8304; elapsed 106.3s |
| 2026-07-23 16:21:56 CST | WTQ | 185/200 | `nu-2183` | ok | row185 ok; last row token 7935; elapsed 100.8s |
| 2026-07-23 16:21:56 CST | WTQ | 186/200 | `nu-889` | ok | row186 ok; last row token 2344; elapsed 14.9s |
| 2026-07-23 16:27:54 CST | WTQ | 187/200 | `nu-3891` | ok | row187 ok; last row token 8200; elapsed 103.5s |
| 2026-07-23 16:27:54 CST | WTQ | 188/200 | `nu-996` | ok | row188 ok; last row token 15058; elapsed 117.3s |
| 2026-07-23 16:27:54 CST | WTQ | 189/200 | `nu-1317` | ok | row189 ok; last row token 6105; elapsed 44.1s |
| 2026-07-23 16:27:54 CST | WTQ | 190/200 | `nu-1421` | ok | row190 ok; last row token 9670; elapsed 66.2s |
| 2026-07-23 16:29:10 CST | WTQ | 191/200 | `nu-2934` | ok | row191 ok; last row token 7751; elapsed 57.6s |
| 2026-07-23 16:34:59 CST | WTQ | 192/200 | `nu-207` | ok | row192 ok; last row token 20731; elapsed 285.9s |
| 2026-07-23 16:34:59 CST | WTQ | 193/200 | `nu-1686` | ok | row193 ok; last row token 6364; elapsed 47.0s |
| 2026-07-23 16:34:59 CST | WTQ | 194/200 | `nu-2172` | ok | row194 ok; last row token 9746; elapsed 62.2s |
| 2026-07-23 16:48:31 CST | WTQ | 195/200 | `nu-2483` | ok | row195 ok; last row token 9850; elapsed 99.2s |
| 2026-07-23 16:48:31 CST | WTQ | 196/200 | `nu-2120` | ok | row196 ok; last row token 16805; elapsed 192.2s |
| 2026-07-23 16:48:31 CST | WTQ | 197/200 | `nu-1657` | ok | row197 ok; last row token 6708; elapsed 56.9s |
| 2026-07-23 16:48:31 CST | WTQ | 198/200 | `nu-983` | ok | row198 ok; last row token 23692; elapsed 138.0s |
| 2026-07-23 16:48:31 CST | WTQ | 199/200 | `nu-3200` | ok | row199 ok; last row token 6841; elapsed 72.4s |
| 2026-07-23 16:48:31 CST | WTQ | 200/200 | `nu-2332` | ok | row200 ok; last row token 10496; elapsed 78.9s; END_WTQ_FULL200 2026-07-23 16:45:33 CST |
| 2026-07-23 16:50:49 CST | WTQ | 200/200 | eval/paired | complete | generated `wtq_mact_full200_eval.json`, `wtq_mact_full200_errors.jsonl`, `wtq_mact_full200_paired.json`; paired myAgent 131/200 vs MACT 148/200; token ratio 0.5926 |

## 已知 core100 结论

```text
myAgent: 237/300 = 0.7900
MACT:    227/300 = 0.7567
token ratio: 0.5913
```

WTQ 的 `nu-4299` 和 `nu-2633` 在 seed 中保留为 MACT context length failure；full200 tail 新增 `nu-3290`、`nu-3139`、`nu-3487` 同类失败。不能删除或重跑后静默替换；若后续 repair，必须另行标注 repaired 口径。

WTQ full200 paired result:

```text
myAgent: 131/200 = 0.6550
MACT:    148/200 = 0.7400
token ratio: 0.5926
paired disagreement: both_correct=108, myagent_only=23, mact_only=40, neither=29
```

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
