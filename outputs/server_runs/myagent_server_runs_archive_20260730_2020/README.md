# MyAgent server_runs 完整归档

生成时间：2026-07-30 20:20 Asia/Shanghai

## 覆盖范围

- 来源目录：`/home/ubuntu/lzz/MyAgent/outputs/server_runs`
- 归档内容：完整 `outputs/server_runs` 目录
- 源目录体量：`241M`
- 顶层运行目录：`43`
- 文件数：`433`
- 压缩包：`myagent_outputs_server_runs_20260730_2020.tar.gz`
- 压缩后体量：约 `27M`
- SHA256：`478205603b38f01e62f0a64230a89c3a24602fa1499235fdc56c60cc1ff2816e`

## 配套文件

- `SHA256SUMS`：压缩包校验值。
- `inventory.tsv`：按文件大小倒序列出源目录内所有文件，格式为 `bytes<TAB>relative_path`。
- `run_directories.txt`：源目录顶层 run 目录清单。
- `source_size.txt`：源目录大小快照。

## 恢复方式

从 MyAgent 仓库父目录恢复：

```bash
tar -xzf /home/ubuntu/lzz/MACT/outputs/server_runs/myagent_server_runs_archive_20260730_2020/myagent_outputs_server_runs_20260730_2020.tar.gz -C /home/ubuntu/lzz/MyAgent
```

恢复后会得到：

```text
/home/ubuntu/lzz/MyAgent/outputs/server_runs
```

## 关系说明

这个归档用于防止服务器清空导致探索性实验输出丢失，包含 smoke、Gate-50、TabFact 消融、WTQ 调参、canonical myAgent full200 raw 等本地结果。

当前专家/专利证据仍以 MACT 下已经镜像的 canonical 路径为主：

- `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_blind200_mact_full200_20260723/`
- `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_canonical_myagent_full200_raw_artifacts_20260730_2008/`

本目录是恢复包和补充上下文，不改变 canonical full200 结论。

## 安全检查

归档前已对 MyAgent `outputs/server_runs` 做窄口径敏感信息扫描，未发现 `Authorization`、`Bearer`、常见 API key 或 `PASSWORD/SECRET` 形式的命中。
