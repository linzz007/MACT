# 正式实验结果表模板与执行判定台账

创建时间：2026-08-01 22:52 CST

用途：后续每完成一个 fresh/gate 实验，都按本文模板补齐行数、准确率、token、耗时、失败/缺答案、判定和证据路径。这个文件本身不是新实验结果；`pending` 行不能写成已完成。

## 每个完成实验必须保留的字段

| field | meaning |
|---|---|
| stage | 实验阶段，例如 WTQ targeted fresh、Seed-C paired Gate-50 |
| dataset | `wtq` / `tabfact` / `crt` / `wtq_tabfact_crt` |
| input rows | 输入 JSONL 行数 |
| merged rows | MyAgent 或 MACT merged JSONL 行数 |
| eval rows | eval JSON 中 `num_samples` 或 `num_with_gold` |
| MyAgent correct | MyAgent 正确数 |
| MACT/reference correct | 同 ID MACT 正确数，或 gate reference |
| token ratio | MyAgent token / MACT token，或 MyAgent token / MACT full200 reference |
| avg tokens | 平均 token |
| avg elapsed s | 平均耗时 |
| failed/missing | `num_failed_exec` / `num_missing_answer` |
| decision | `pass` / `inspect` / `no-go` / `paired accepted` 等 |
| evidence | JSON/MD 结果文件路径 |
| git commit | 结果同步后的 MACT/MyAgent commit |

## 已冻结主结果

| stage | dataset | input/merged/eval | MyAgent | MACT | token ratio | avg tokens | avg elapsed s | failed/missing | decision |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| Qwen3-32B full200 anchor | WTQ | 200/200/200 | 155/200 | 148/200 | 0.6187 | 6501.03 | 16.80 | 0/0 | complete |
| Qwen3-32B full200 anchor | TabFact | 200/200/200 | 194/200 | 189/200 | 0.2014 | 2181.67 | 9.76 | 0/0 | complete |
| Qwen3-32B full200 anchor | CRT | 200/200/200 | 140/200 | 113/200 | 0.8461 | 10839.17 | 24.46 | 0/0 | complete |
| Qwen3-32B full200 anchor | Aggregate | 600/600/600 | 489/600 | 450/600 | 0.5717 | 6507.29 | 17.01 | 0/0 | complete |

证据：

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_all200_acceptance_20260731_132611/qwen3_policy_v6b_all200_acceptance_summary.json
```

## 待跑结果表

| stage | status | dataset | required rows | pass condition | evidence when complete |
|---|---|---|---:|---|---|
| WTQ targeted fresh affected slice | pending runtime | WTQ | 9 | merged/eval `9/9`，failed/missing `0/0`，correct `>=7/9`，优先 `9/9` | `p4b_wtq_targeted_fresh_summary.json/md` |
| P4b WTQ after-fix full50 | pending after targeted pass | WTQ | 50 | MyAgent `>43/50`，token ratio `<0.75`，failed/missing `0/0` | `p4b_after_wtq_targeted_paired_summary.json/md` |
| E3 Seed-C current-only Gate-50 | pending runtime | WTQ/TabFact/CRT | 150 | `decision=run_paired_mact`，failed/missing `0/0`，token 低于 MACT full200 reference | `summary/seed_c_myagent_gate50_summary.json/md` |
| E3 Seed-C paired Gate-50 | pending after current-only pass | WTQ/TabFact/CRT | 150 | 强结论需 `strict_all_dataset_superiority=true`；existing paired accepted 只能支持 overall/token | `summary/seed_c_paired_gate50_summary.json/md` |
| E3 Seed-D current-only Gate-50 | pending runtime | WTQ/TabFact/CRT | 150 | `decision=run_paired_mact`，failed/missing `0/0`，token 低于 MACT full200 reference | `summary/seed_d_myagent_gate50_summary.json/md` |
| E3 Seed-D paired Gate-50 | pending after current-only pass | WTQ/TabFact/CRT | 150 | 强结论需 `strict_all_dataset_superiority=true`；existing paired accepted 只能支持 overall/token | `summary/seed_d_paired_gate50_summary.json/md` |
| 新模型 Gate funnel | pending new candidate | WTQ/TabFact/CRT | 30 -> 150 -> 450 -> 600 | Gate-10/50/150 逐级通过后才进入 paired-200 | `MACT outputs/server_runs/<model_tag>_gate*/gate*_summary.json/md` |

## 执行判定台账

| ID | decision | status | evidence / reason |
|---|---|---|---|
| D0 | Qwen3-32B full200 作为 v1 prototype anchor | accepted | 三数据集 full200 单项超过 MACT，overall token ratio `0.5717` |
| D1 | 不能只凭 P4b 宣称新 seed 三项全胜 | accepted | P4b overall 过，但 WTQ `37/50 < 43/50` |
| D2 | WTQ after-fix full50 之前必须先跑 targeted fresh | pending runtime | E2 目前是 offline projection，必须 fresh 验证 |
| D3 | E3 先跑 current-only，再决定是否跑 MACT baseline | prepared | Seed-C/Seed-D 输入和 runner 已准备，避免浪费 MACT runtime |
| D4 | 新模型不直接 full200，走 Gate-10/50/150/paired-200 | accepted | 历史小模型 no-go；gate 脚本和 manifest 已准备 |

## 填表后必须同步

每完成一个阶段：

```bash
git -C /home/ubuntu/lzz/MACT add -f outputs/server_runs/<run_dir>
git -C /home/ubuntu/lzz/MACT commit -m "results: add <stage>"
git -C /home/ubuntu/lzz/MACT push origin main

git -C /home/ubuntu/lzz/MyAgent add docs/server/server_codex_reports/current-qwen3-mact-experiment-prd.md
git -C /home/ubuntu/lzz/MyAgent commit -m "docs: record <stage>"
git -C /home/ubuntu/lzz/MyAgent push origin codex/selective-risk-collaboration
```

如果 fresh run 导致代码变化，再把相应 MyAgent 代码和测试一并提交。
