# Qwen3-32B Patent Experiment Package

Created: 2026-08-01 21:55 CST

This directory is the current expert/patent-facing experiment package for the
MyAgent selective risk collaboration / persuasion-back work. It indexes frozen
Qwen3-32B evidence, P4b new-seed diagnosis, WTQ targeted-fix projection, and the
remaining validation work.

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
- The patent-facing mechanism evidence matrix now combines full200, coarse
  ablation, and offline attribution evidence.
- E3 multi-seed Gate-50 inputs and runners are prepared for Seed-C/Seed-D; no
  model rows have been run yet in that package.
- The latest completion-gap audit records that the active goal is not complete:
  fresh WTQ closure, multi-seed execution, and one viable multi-model gate remain
  missing.
- The claim-to-evidence traceability matrix maps six patent claim families to
  mechanisms, evidence files, support strength, and remaining gaps.
- The formal result-table template defines the exact fields and decision ledger
  to fill after each pending fresh/gate run.
- The remaining-Qwen3 queue script now provides a guarded executable entry for
  WTQ fresh closure and E3 Seed-C/Seed-D validation.
- Runtime preflight records endpoint/GPU/process readiness before any queue run
  and blocks queue execution when target GPUs show residual runtime state.
- Fresh Qwen affected-slice validation is still pending because local vLLM
  endpoints are down and GPUs have residual memory without visible compute PIDs.
  Latest recorded preflight: `qwen3_runtime_preflight_20260801_233405.json/md`.
- The current formal-result ledger is generated from frozen JSON sources and
  keeps pending stages explicit rather than mixing them with completed results.
  Latest generated ledger: `formal_result_ledger_current_20260801_233858.json/md`.
- The latest consistency audit passes with 0 errors and 1 warning for the
  still-blocked online runtime: `patent_package_consistency_audit_20260801_233902.json/md`.
- The checksum manifest lets a restored server verify that package files and
  existing referenced evidence files were recovered without corruption.
  Use `latest_patent_package_checksums.json/md` and `SHA256SUMS`.
