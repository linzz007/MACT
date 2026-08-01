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

```bash
cd /home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305
bash start_qwen3_67_service.sh
```

健康检查：

```bash
curl -sS -H 'Authorization: Bearer local-vllm-key-change-me' http://127.0.0.1:8000/v1/models
```

## 3. 先跑 WTQ affected-slice fresh 验证

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

## 4. 再决定是否重跑 P4b WTQ full50

只有 affected-slice fresh 结果证明方向有效，才重跑 WTQ full50 after-fix：

```bash
# 可复用 run_myagent_p4a_current.sh 中的 WTQ 段，输出目录必须新建：
# myagent_current_after_wtq_targeted_fix/
```

重跑后比较：

- MyAgent WTQ after-fix 是否超过 MACT `43/50`。
- token ratio 是否仍明显低于 MACT。
- failed/missing 是否仍为 `0/0`。

## 5. 同步规则

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
