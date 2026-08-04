# 当前专利实验完成度审计

生成时间：`2026-08-04 10:50:28 CST`

本文档用于回答：当前距离完整专利实验材料还差什么。它从 current/latest 证据自动汇总，不新增 benchmark 结果。

## 当前结论

当前目标状态：`active_not_complete`。Qwen3-32B full200 和 P4b after-targeted 已是正证据；E3 Seed-C/D 是边界证据；E4 状态为 `pending_no_candidate`，artifact decision 为 `no_candidate_wait`，尚无额外模型/API 候选。

## 环境复核

| item | result |
|---|---|
| source | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/latest_e4_multimodel_gate_readiness_audit.json` |
| checked at | `2026-08-04 10:49:21 CST` |
| default GPU pool | `0,1 -> 8000; 2,3 -> 8001` |
| default pool available | `False` |
| visible model/runner processes | `2` |

| GPU | memory MiB | util % |
|---:|---:|---:|
| 0 | 45815 | 0 |
| 1 | 45815 | 0 |
| 2 | 45839 | 0 |
| 3 | 45839 | 0 |
| 4 | 42031 | 100 |
| 5 | 42031 | 10 |
| 6 | 42031 | 100 |
| 7 | 42031 | 100 |

## 要求逐项审计

| ID | 要求 | 当前状态 | 关键证据 | 缺口 |
|---|---|---|---|---|
| R1 | Qwen3-32B full200 anchor evidence shows MyAgent exceeds MACT on WTQ, TabFact, and CRT, with lower token usage and zero failed/missing answers. | `complete` | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_all200_acceptance_20260731_132611/qwen3_policy_v6b_all200_acceptance_summary.json`<br>`/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_all200_acceptance_20260731_132611/qwen3_policy_v6b_patent_evidence_index.md` | none |
| R2 | Mechanism evidence supports selective risk collaboration / persuasion-back rather than sample hardcoding. | `substantially_complete` | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_patent_mechanism_evidence_20260801_2222/patent_mechanism_evidence_matrix.json`<br>`/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_patent_mechanism_evidence_20260801_2222/patent_mechanism_evidence_matrix.md`<br>`/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_coarse_ablation_gate50_20260801_0040/coarse_ablation_gate50_summary.md` | Fine-grained verifier-override/evidence-retention ablations remain optional unless more causal granularity is needed for claim drafting. |
| R3 | WTQ P4b new-seed risk is diagnosed and closed with fresh Qwen validation before using after-targeted P4b as positive evidence. | `complete` | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/p4b_paired_gate50_summary.json`<br>`/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/p4b_wtq_targeted_fresh_summary.json`<br>`/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/p4b_after_wtq_targeted_paired_summary.json` | none |
| R4 | Multi-seed work explains whether the effect is stable beyond the frozen full200 and P4b seed. | `complete_boundary_not_stability_pass` | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_multiseed_gate50_20260801_2231/summary/seed_boundary_error_diagnosis.json`<br>`/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_multiseed_gate50_20260801_2231/summary/seed_boundary_error_diagnosis.md`<br>`/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_e3_boundary_budget_probe_20260804_1035/summary/e3_boundary_budget_probe_summary.json`<br>`/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_e3_boundary_budget_probe_20260804_1035/summary/e3_boundary_budget_probe_summary.md` | Seed-C/Seed-D are boundary evidence, not multi-seed stable superiority evidence. The max_replan=5 probe recovered a minority of representative wrong rows, so adaptive budgeting is useful for selected categories but does not close E3 stability. |
| R5 | Multi-model gate must test model externality through Gate-10 -> Gate-50 -> Gate-150 -> paired-200 without rerunning known no-go models. | `pending_no_candidate` | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/latest_e4_multimodel_gate_readiness_audit.json`<br>`/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/latest_e4_multimodel_gate_readiness_audit_zh.md` | No untested local model path or API provider profile/key exists. Do not start E4 Gate-10 until a new candidate appears. |
| R6 | Expert/patent package and Chinese patent disclosure draft must exist, point to auditable evidence, and separate supported claims from boundaries. | `stage_patent_draft_ready_with_boundaries` | `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/latest_current_patent_experiment_section.json`<br>`/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/latest_current_patent_experiment_section_zh.md`<br>`/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/patent_disclosure_draft_zh.md`<br>`/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/latest_formal_result_ledger_current.json` | Final closeout still needs an E4 candidate result or explicit acceptance of the no-candidate boundary. |
| R7 | Process/result context remains in the single MyAgent PRD and MACT artifacts, with sync to GitHub after each update. | `complete_for_prior_pushed_state_this_audit_requires_commit_push` | `/home/ubuntu/lzz/MyAgent/docs/server/server_codex_reports/current-qwen3-mact-experiment-prd.md`<br>`/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/evidence_manifest.json`<br>`/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/SHA256SUMS` | This generated audit itself must be committed and pushed after generation; final proof is git local/remote HEAD equality. |

## 关键数字

| scope | result |
|---|---|
| full200 aggregate | MyAgent `489/600` vs MACT `450/600`, token ratio `0.5717`, elapsed ratio `0.1337`, failed/missing `0/0` |
| P4b original WTQ risk | MyAgent `37/50` vs MACT `43/50` |
| WTQ targeted fresh | `9/9`, merged/eval `9/9`, failed/missing `0/0`, decision `pass` |
| P4b after-targeted aggregate | MyAgent `121/150` vs MACT `111/150`, token ratio `0.5310`, failed/missing `0/0` |
| E3 Seed-C/D boundary aggregate | `212/300`, wrong `88`, weighted token ratio `0.5916`, failed/missing `0/0`, verification `pass` |
| E3 max_replan=5 boundary probe | recovered `4/12` original wrong rows, decision `mixed_budget_sensitivity_not_enough_for_e3_stability`, failed/missing `0/0`, avg tokens `12444.9->13136.1` |
| E4 readiness | decision `no_candidate_wait`; can_start_gate10_now `False`, local models `4`, untested local models `0`, API keys/profiles `0/0` |

## 下一步

- Do not rerun known no-go models. Wait for a new local model path or API provider profile/key before E4 Gate-10.
- Use latest_current_patent_experiment_section_zh.md for current expert/patent discussion, with E3 and E4 boundaries explicitly preserved.
- If further Qwen3 optimization is requested, use the E3 max_replan=5 probe to separate adaptive-budget categories from semantic-guard categories, instead of re-optimizing the passing full200/P4b-after-targeted anchors.

## 当前可写

- Qwen3-32B full200 stage: MyAgent beats MACT on WTQ, TabFact, and CRT with lower aggregate tokens.
- P4b new-seed Gate-50 supports overall/token evidence but exposes WTQ risk.
- WTQ targeted fresh closure has completed, and P4b after-targeted Gate-50 shows all-dataset superiority.
- E3 Seed-C current-only Gate-50 is a documented stability boundary: overall 114/150, decision stop_or_inspect.
- E3 Seed-D current-only Gate-50 is a second documented stability boundary: overall 98/150, decision stop_or_inspect.
- E3 Seed-C/Seed-D offline boundary diagnosis has explained the current-gate boundary as semantic accuracy stability, not runtime/tool failure or token-budget failure.
- E4 latest readiness audit has completed with no untested local model path and no API provider profile, so no Gate-10 should be started yet.
- The current patent experiment section has been consolidated as draft-ready evidence with explicit unsupported-claim boundaries.

## 当前不能写

- A viable additional model gate has completed.
- The final experiment package closeout has completed after either an E4 candidate result or explicit acceptance of the no-candidate boundary.
