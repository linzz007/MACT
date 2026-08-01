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
patent_disclosure_draft_zh.md
next_validation_checklist_zh.md
```

Current status:

- Qwen3-32B full200 stage evidence passes all three datasets against MACT.
- P4b new-seed Gate-50 overall passes the existing paired gate, but WTQ alone
  originally lagged MACT.
- E1 WTQ discordant diagnosis is complete.
- E2 WTQ targeted fixes are implemented and projected offline to recover all 9
  P4b MACT-only WTQ rows, with 0 projected harm.
- Fresh Qwen affected-slice validation is still pending because local vLLM
  endpoints are down and GPUs have residual memory without visible compute PIDs.
