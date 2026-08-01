# 下一次验证清单

本清单用于服务器清理/扩容后继续执行，不需要重新阅读全部历史对话。

## 1. 恢复仓库

```bash
cd /home/ubuntu/lzz/MyAgent
git checkout codex/selective-risk-collaboration
git pull

cd /home/ubuntu/lzz/MACT
git checkout main
git pull
```

确认提交：

```bash
git -C /home/ubuntu/lzz/MyAgent log -1 --oneline
git -C /home/ubuntu/lzz/MACT log -1 --oneline
```

预期至少包含以下功能/证据提交；如果后续又产生了 PRD 或实验包同步提交，以 `git log -1 --oneline` 的最新输出为准：

```text
MyAgent a080844 feat: add wtq targeted semantic fixes
MACT a6d3162 results: add wtq targeted fix projection
```

## 2. 启动 Qwen3-32B 服务

优先按用户指定资源使用 GPU `6,7`。如果 6/7 不可用，先记录 GPU 状态，不要静默换口径。

先跑 runtime preflight；该命令会把 endpoint、GPU、可见进程和推荐动作写到 MACT 专利实验包：

```bash
python /home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/preflight_qwen3_runtime.py
cat /home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/latest_qwen3_runtime_preflight_zh.md
```

若输出 `blocked_gpu_runtime_residual`，不要启动模型；先等服务器清理/扩容，或由用户明确授权改用其他 GPU。

```bash
cd /home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305
bash start_qwen3_67_service.sh
```

健康检查：

```bash
curl -sS -H 'Authorization: Bearer local-vllm-key-change-me' http://127.0.0.1:8000/v1/models
```

## 3. 先跑 WTQ affected-slice fresh 验证

推荐先使用带停机条件的队列入口：

```bash
export VLLM_ENDPOINTS=http://127.0.0.1:8000/v1
bash /home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/run_remaining_qwen3_patent_queue.sh --phase wtq --checkpoint
```

队列运行手册：

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/remaining_qwen3_queue_runbook_zh.md
```

下面是等价的手动执行方式：

```bash
bash /home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/run_myagent_wtq_targeted_fix_slice.sh
```

输入：

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/input/wtq_p4b_targeted_fix_affected_slice.jsonl
```

预期行数：`9`。

验收：

1. merged/eval 均为 9 行。
2. failed/missing 为 `0/0`。
3. 正确数接近或达到 `9/9`。
4. 若低于 `7/9`，先诊断，不重跑 WTQ full50。

该脚本现在会自动调用：

```bash
python /home/ubuntu/lzz/MyAgent/scripts/server/summarize_wtq_targeted_fresh.py \
  --run-dir /home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305 \
  --output-root /home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/myagent_wtq_targeted_fix \
  --min-correct 7 \
  --fail-on-inspect
```

成功时会生成：

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/p4b_wtq_targeted_fresh_summary.json
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/p4b_wtq_targeted_fresh_summary.md
```

## 4. 再决定是否重跑 P4b WTQ full50

只有 affected-slice fresh 结果证明方向有效，才重跑 WTQ full50 after-fix：

```bash
bash /home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/run_myagent_wtq_after_targeted_fix_full50.sh
```

重跑后比较：

- MyAgent WTQ after-fix 是否超过 MACT `43/50`。
- token ratio 是否仍明显低于 MACT。
- failed/missing 是否仍为 `0/0`。

该脚本会先读取 `p4b_wtq_targeted_fresh_summary.json`，只有 `decision=pass` 且 failed/missing 为 `0/0` 时才继续跑 WTQ full50。跑完后自动调用：

```bash
bash /home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/run_p4b_after_wtq_targeted_eval_compare.sh
```

输出：

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/myagent_current_after_wtq_targeted_fix/
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/p4b_after_wtq_targeted_paired_summary.json
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/p4b_after_wtq_targeted_paired_summary.md
```

## 5. E3 multi-seed 准备入口

WTQ affected-slice 和 P4b WTQ after-fix full50 有结论后，再启动 E3 Seed-C/Seed-D。不要直接扩 full200。

推荐队列入口：

```bash
export VLLM_ENDPOINTS=http://127.0.0.1:8000/v1,http://127.0.0.1:8001/v1
bash /home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/run_remaining_qwen3_patent_queue.sh --phase seed_c --checkpoint
bash /home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/run_remaining_qwen3_patent_queue.sh --phase seed_d --checkpoint
```

下面是等价的手动执行方式：

```bash
cd /home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_multiseed_gate50_20260801_2231
python verify_multiseed_package.py
bash healthcheck_vllm.sh
bash run_seed_myagent_gate50.sh seed_c
cat summary/seed_c_myagent_gate50_summary.md
```

只有 `summary/seed_c_myagent_gate50_summary.json` 的 `decision=run_paired_mact` 时，才继续跑同 ID MACT：

```bash
bash run_seed_mact_gate50.sh seed_c wtq http://127.0.0.1:8000/v1
bash run_seed_mact_gate50.sh seed_c tabfact http://127.0.0.1:8001/v1
bash run_seed_mact_gate50.sh seed_c crt http://127.0.0.1:8000/v1
bash run_seed_paired_compare.sh seed_c
cat summary/seed_c_paired_gate50_summary.md
```

Seed-D 同理。每完成一个 seed 后立即：

```bash
bash checkpoint_to_git.sh --commit "checkpoint: e3 multiseed gate50 <stage>" --push
```

## 6. 同步规则

每次 fresh/gate run 完成后，先按正式结果表模板确认字段是否齐全：

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/formal_result_tables_template_20260801_2252_zh.md
```

任何 fresh run 结束后，先更新：

```text
/home/ubuntu/lzz/MyAgent/docs/server/server_codex_reports/current-qwen3-mact-experiment-prd.md
```

再把 MACT run 目录新增产物和 MyAgent PRD/代码同步：

```bash
cd /home/ubuntu/lzz/MACT
git add -f outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305
git commit -m "results: add wtq targeted fresh validation"
git push origin main

cd /home/ubuntu/lzz/MyAgent
git add code/my_agents.py tests/test_myagent_pipeline.py docs/server/server_codex_reports/current-qwen3-mact-experiment-prd.md
git commit -m "docs: record wtq targeted fresh validation"
git push origin codex/selective-risk-collaboration
```

如果 fresh run 没有产生代码变化，只提交 PRD。
