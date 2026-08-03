# 当前专利实验章节收口稿

生成时间：`2026-08-03 12:10:04 CST`

本文档用于回答：当前哪些实验结果可以写进专家/专利材料，哪些结论必须保留边界。它只汇总已有 frozen 证据，不新增 benchmark 结果。

## 1. 当前总判断

- Qwen3-32B full200：MyAgent `489/600`，MACT `450/600`，delta `+39`，整体 token ratio `0.5717`，整体耗时 ratio `0.1337`。
- P4b after-targeted Gate-50：MyAgent `121/150`，MACT `111/150`，三数据集单项均超过 MACT，整体 token ratio `0.5310`。
- E3 Seed-C/D：current-only 合计 `212/300`，token ratio `0.5916`，failed/missing `0/0`，但 decision 仍是 boundary，不是多 seed 稳定性达标。
- E4 多模型 gate：`no_candidate_wait`，无 untested local model、无 API provider profile/key；0-3 卡作为默认下一次启动池 `0,1 -> 8000; 2,3 -> 8001`。

## 2. 可以写入的正证据

### Qwen3-32B Full200 主结果

| dataset | rows input/merged/eval | MyAgent | MACT/ref | delta | token ratio | avg tokens | avg elapsed s | failed/missing |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| wtq | 200/200/200 | 155/200 | 148/200 | +7 | 0.6187 | 6501.02 | 16.80 | 0/0 |
| tabfact | 200/200/200 | 194/200 | 189/200 | +5 | 0.2014 | 2181.67 | 9.76 | 0/0 |
| crt | 200/200/200 | 140/200 | 113/200 | +27 | 0.8461 | 10839.17 | 24.46 | 0/0 |
| aggregate | 600/600/600 | 489/600 | 450/600 | +39 | 0.5717 | 6507.29 | 17.01 | 0/0 |

### P4b After-Targeted Gate-50

P4b 原始 WTQ 风险为 MyAgent `37/50` vs MACT `43/50`。WTQ affected-slice fresh 验证为 `9/9`，merged/eval `9/9`，failed/missing `0/0`。

| dataset | rows input/merged/eval | MyAgent | MACT/ref | delta | token ratio | avg tokens | avg elapsed s | failed/missing |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| wtq | 50/50/50 | 46/50 | 43/50 | +3 | 0.5571 | 6300.16 | 14.51 | 0/0 |
| tabfact | 50/50/50 | 45/50 | 44/50 | +1 | 0.2156 | 2308.92 | 10.48 | 0/0 |
| crt | 50/50/50 | 30/50 | 24/50 | +6 | 0.7740 | 9823.82 | 21.99 | 0/0 |
| aggregate | 150/150/150 | 121/150 | 111/150 | +10 | 0.5310 | 6144.30 | 15.66 | 0/0 |

## 3. 机制证据

- strong verification / 劝返：关闭 no_strong_verification 后 overall 相对 current `-8/150`，WTQ 相对 current `-7/50`。
- deterministic audit：关闭 deterministic shortcuts 后 overall 相对 current `-15/150`，TabFact `-9/50`，CRT `-7/50`。
- TabFact deterministic audit 同时节省预算：no_deterministic_shortcuts 的 TabFact token 为 current 的 `1.4487x`。
- 机制矩阵：`/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_patent_mechanism_evidence_20260801_2222/patent_mechanism_evidence_matrix.md`。

## 4. 必须保留的边界

- P4b 原始结果不能写成新 seed 三数据集全部超过 MACT；WTQ 原始结果低于 MACT，after-targeted 结果才恢复单项优势。
- E3 Seed-C/D current-only 不能写成多 seed 稳定超过 MACT；它们没有同 seed paired MACT，且 decision 为 `stop_or_inspect`。
- E4 不能写成多模型已验证；当前只是 readiness audit，结论是没有可启动候选。
- 不能把 full200/gate 结果写成全量官方测试集完成。

### E3 Boundary 表

#### seed-c

| dataset | rows input/merged/eval | MyAgent | MACT/ref | delta | token ratio | avg tokens | avg elapsed s | failed/missing |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| wtq | 50/50/50 | 40/50 | n/a | n/a | 0.6013 | 6318.56 | 15.25 | 0/0 |
| tabfact | 50/50/50 | 44/50 | n/a | n/a | 0.2604 | 2820.02 | 10.65 | 0/0 |
| crt | 50/50/50 | 30/50 | n/a | n/a | 0.9118 | 11679.92 | 25.33 | 0/0 |
| aggregate | 150/150/150 | 114/150 | n/a | n/a | 0.6096 | 6939.50 | 17.07 | 0/0 |

decision: `stop_or_inspect`。

#### seed-d

| dataset | rows input/merged/eval | MyAgent | MACT/ref | delta | token ratio | avg tokens | avg elapsed s | failed/missing |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| wtq | 50/50/50 | 30/50 | n/a | n/a | 0.6329 | 6650.02 | 17.54 | 0/0 |
| tabfact | 50/50/50 | 38/50 | n/a | n/a | 0.2682 | 2905.16 | 11.68 | 0/0 |
| crt | 50/50/50 | 30/50 | n/a | n/a | 0.7829 | 10028.56 | 27.39 | 0/0 |
| aggregate | 150/150/150 | 98/150 | n/a | n/a | 0.5735 | 6527.91 | 18.87 | 0/0 |

decision: `stop_or_inspect`。

E3 诊断结论：

- Seed-C/Seed-D had 300 merged rows and zero failed execution or missing answers; the boundary is semantic answer correctness, not runtime/tool coverage.
- Tokens remained below the frozen MACT full200 reference on every dataset and seed; the blocker is accuracy stability, not token budget.
- Seed-C is near the current gate on TabFact and exactly at the CRT gate, while Seed-D exposes broader WTQ and TabFact instability.
- Do not spend paired MACT runtime for these seeds until boundary categories are addressed or explicitly accepted as limitation evidence.
- Patent-facing claim should use E3 as applicability-boundary evidence, not as multi-seed stable superiority evidence.

## 5. 正式实验表状态

| stage | status | patent use |
|---|---|---|
| E0 full200 anchor | `complete` | main positive evidence |
| E1 WTQ P4b risk diagnosis | `complete` | risk and boundary diagnosis |
| E2 WTQ targeted fresh and after-targeted full50 | `complete` | targeted mechanism repair evidence |
| E3 multi-seed current-only boundary diagnosis | `complete_boundary_evidence` | applicability boundary, not stability proof |
| E4 multi-model gate | `pending_no_candidate` | future external validity evidence after new model/API appears |
| E5/E6 patent experiment section and disclosure draft | `current_section_consolidated` | draft-ready with explicit unsupported claims |
| E7 final experiment package closeout | `pending` | requires at least E4 candidate or explicit acceptance of no-candidate boundary |

## 6. 下一步触发规则

- If GPUs 0-3 remain free and a new candidate model/API appears, start Gate-10 on 0,1 and 2,3 through prepare_model_gate_run.py; do not consume 4-7 unless explicitly reassigned.
- If no new model/API exists, do not rerun known no-go models; continue drafting with E4 marked pending/no-candidate.
- If more Qwen optimization is requested, target E3 boundary categories instead of re-optimizing already-passing full200/P4b-after-targeted rows.

## 7. 关键证据路径

- `full200_summary`: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_all200_acceptance_20260731_132611/qwen3_policy_v6b_all200_acceptance_summary.json`
- `full200_evidence_md`: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_all200_acceptance_20260731_132611/qwen3_policy_v6b_patent_evidence_index.md`
- `p4b_original_summary`: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/p4b_paired_gate50_summary.json`
- `p4b_original_summary_md`: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/p4b_paired_gate50_summary.md`
- `p4b_targeted_fresh_summary`: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/p4b_wtq_targeted_fresh_summary.json`
- `p4b_targeted_fresh_summary_md`: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/p4b_wtq_targeted_fresh_summary.md`
- `p4b_after_targeted_summary`: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/p4b_after_wtq_targeted_paired_summary.json`
- `p4b_after_targeted_summary_md`: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/p4b_after_wtq_targeted_paired_summary.md`
- `mechanism_matrix`: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_patent_mechanism_evidence_20260801_2222/patent_mechanism_evidence_matrix.json`
- `mechanism_matrix_md`: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_patent_mechanism_evidence_20260801_2222/patent_mechanism_evidence_matrix.md`
- `e3_boundary_diagnosis`: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_multiseed_gate50_20260801_2231/summary/seed_boundary_error_diagnosis.json`
- `e3_boundary_diagnosis_md`: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_multiseed_gate50_20260801_2231/summary/seed_boundary_error_diagnosis.md`
- `e4_readiness`: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/latest_e4_multimodel_gate_readiness_audit.json`
- `e4_readiness_md`: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/latest_e4_multimodel_gate_readiness_audit_zh.md`
- `formal_ledger`: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/latest_formal_result_ledger_current.json`
- `formal_ledger_md`: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/latest_formal_result_ledger_current_zh.md`
