# Qwen3-32B Patent Experiment Package

Created: 2026-08-01 21:55 CST

This directory is the current expert/patent-facing experiment package for the
MyAgent selective risk collaboration / persuasion-back work. It indexes frozen
Qwen3-32B evidence, P4b new-seed diagnosis, WTQ targeted-fix closure, and the
remaining multi-seed / multi-model validation work.

This is not a new benchmark run. All numeric claims point to frozen artifacts in
`MACT/outputs/server_runs/` and the current MyAgent PRD.

Files:

```text
evidence_manifest.json
experiment_package_index_zh.md
formal_experiment_schedule_zh.md
patent_disclosure_draft_zh.md
next_validation_checklist_zh.md
completion_gap_audit_20260801_2244.json
completion_gap_audit_20260801_2244_zh.md
build_current_completion_gap_audit.py
latest_completion_gap_audit_current.json
latest_completion_gap_audit_current_zh.md
claim_evidence_traceability_20260801_2248.json
claim_evidence_traceability_20260801_2248_zh.md
formal_result_tables_template_20260801_2252.json
formal_result_tables_template_20260801_2252_zh.md
run_remaining_qwen3_patent_queue.sh
remaining_qwen3_queue_runbook_zh.md
preflight_qwen3_runtime.py
latest_qwen3_runtime_preflight.json
latest_qwen3_runtime_preflight_zh.md
build_current_formal_result_ledger.py
latest_formal_result_ledger_current.json
latest_formal_result_ledger_current_zh.md
audit_patent_package_consistency.py
latest_patent_package_consistency_audit.json
latest_patent_package_consistency_audit_zh.md
build_patent_package_checksums.py
SHA256SUMS
latest_patent_package_checksums.json
latest_patent_package_checksums_zh.md
```

Current status:

- Qwen3-32B full200 stage evidence passes all three datasets against MACT.
- P4b new-seed Gate-50 overall passes the existing paired gate, but WTQ alone
  originally lagged MACT.
- E1 WTQ discordant diagnosis is complete.
- E2 WTQ targeted fixes are implemented and projected offline to recover all 9
  P4b MACT-only WTQ rows, with 0 projected harm.
- 2026-08-03 fresh Qwen affected-slice validation passed `9/9`; the P4b
  after-targeted paired Gate-50 summary is MyAgent `121/150` vs MACT `111/150`,
  token ratio `0.5310`, failures/missing `0/0`.
- The patent-facing mechanism evidence matrix now combines full200, coarse
  ablation, offline attribution evidence, and fresh WTQ closure.
- E3 Seed-C and Seed-D current-only Gate-50 have both run `150/150` rows and
  stopped before paired MACT with `decision=stop_or_inspect`.
  Seed-C: WTQ `40/50`, TabFact `44/50`, CRT `30/50`, overall `114/150`,
  token ratio vs MACT full200 reference `0.6096`, failures/missing `0/0`.
  Seed-D: WTQ `30/50`, TabFact `38/50`, CRT `30/50`, overall `98/150`,
  token ratio vs MACT full200 reference `0.5735`, failures/missing `0/0`.
- The E3 max_replan=5 boundary budget probe reran 12 representative E3 wrong
  rows and recovered `4/12`, with failures/missing `0/0`. The decision is
  `mixed_budget_sensitivity_not_enough_for_e3_stability`: adaptive budgeting is
  useful for selected categories, but E3 remains boundary evidence rather than
  multi-seed stability closure.
- The E3 semantic-boundary plan converts the budget probe into a concrete
  next-step ladder. It marks four zero-recovery probe categories as P0 semantic
  guard work and keeps the decision
  `do_not_rerun_full200_or_paired_mact_until_targeted_guards_pass`.
  Evidence:
  `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_e3_semantic_boundary_plan_20260804_1110/summary/e3_semantic_boundary_plan.md`.
- The E3 S2 guard-validation input package is now prepared at
  `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_e3_guard_validation_inputs_20260804_1128/`.
  It contains `30` rows: `12` representative wrong rows and `18` no-harm
  correct rows, split WTQ/TabFact/CRT as `10/8/12`.
- The E3 S2 after-guard fresh run passed the affected-slice gate at
  `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_e3_guard_validation_after_guard_20260804_1203/`.
  It recovered `8/12` representative wrong rows, preserved `18/18` no-harm
  rows, had failures/missing `0/0`, and weighted token ratio `0.6104`.
  This is targeted mechanism evidence, not a multi-seed stability pass.
- The E3 S3 after-guard current-only rerun is complete at
  `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_e3_s3_current_rerun_after_guard_20260804_1425/`.
  Seed-C passed with `118/150`, token ratio `0.6073`, failed/missing `0/0`.
  Seed-D stopped for inspect with `97/150`, token ratio `0.5659`,
  failed/missing `0/0`; WTQ `28/50` and TabFact `39/50` were below the S3
  gates. Combined result is `215/300`, token ratio `0.5866`, failed/missing
  `0/0`, decision `s3_stop_or_inspect_boundary_remains`. Paired MACT was not
  started.
- The latest current completion-gap audit records that the active goal is not
  complete: Qwen3 full200, P4b after-targeted, and E3 S2 after-guard fresh are
  positive evidence; S3 still leaves Seed-D WTQ/TabFact boundary gaps, and E4
  remains pending until a new local model or API profile appears.
- The claim-to-evidence traceability matrix maps six patent claim families to
  mechanisms, evidence files, support strength, and remaining gaps.
- The formal result-table template defines the exact fields and decision ledger
  to fill after each pending fresh/gate run.
- The remaining-Qwen3 queue script now provides a guarded executable entry for
  already-completed WTQ closure and E3 Seed-C/Seed-D validation.
- Runtime preflight records endpoint/GPU/process readiness before any queue run
  and blocks queue execution when target GPUs show residual runtime state.
- Current runtime status after 2026-08-04 recovery is `ready_existing_endpoint`:
  two Qwen3-32B vLLM services are intentionally kept resident on GPU `2,3` at
  `http://127.0.0.1:8000/v1` and GPU `0,1` at
  `http://127.0.0.1:8001/v1`, served model `qwen3-32b-local`. Latest recorded
  preflight: `qwen3_runtime_preflight_20260804_104903.json/md`. Do not stop the
  services unless switching models or explicitly freeing GPU memory.
- The current formal-result ledger is generated from frozen JSON sources and
  keeps pending stages explicit rather than mixing them with completed results.
  Latest generated ledger is available through
  `latest_formal_result_ledger_current.json/md`.
- The latest consistency audit passes with 0 errors and 0 warnings:
  see `latest_patent_package_consistency_audit.json/md`.
- The checksum manifest lets a restored server verify that package files and
  existing referenced evidence files were recovered without corruption.
  Use `latest_patent_package_checksums.json/md` and `SHA256SUMS`; the latest
  JSON records the current count and missing-reference status.
