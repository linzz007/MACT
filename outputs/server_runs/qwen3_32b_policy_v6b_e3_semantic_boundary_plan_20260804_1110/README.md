# Qwen3-32B E3 Semantic Boundary Plan

Created: 2026-08-04 11:10 CST

This directory is a planning/evidence artifact for the E3 Seed-C/D boundary. It
does not run a model and does not change benchmark results.

Purpose:

- Use the completed E3 Seed-C/D boundary diagnosis and the max_replan=5 budget
  probe to decide what should be implemented or tested next.
- Separate categories that are budget-sensitive from categories that still need
  semantic guards.
- Preserve patent-writing boundaries so later drafts do not overclaim E3
  stability, CRT budget sensitivity, or multi-model validation.

Inputs:

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_multiseed_gate50_20260801_2231/summary/seed_boundary_error_diagnosis.json
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_e3_boundary_budget_probe_20260804_1035/summary/e3_boundary_budget_probe_summary.json
```

Outputs:

```text
summary/e3_semantic_boundary_plan.json
summary/e3_semantic_boundary_plan.md
```

Regenerate:

```bash
cd /home/ubuntu/lzz/MACT
/home/ubuntu/miniconda3/envs/lzz-agent/bin/python outputs/server_runs/qwen3_32b_policy_v6b_e3_semantic_boundary_plan_20260804_1110/build_semantic_boundary_plan.py
```

Current decision:

```text
do_not_rerun_full200_or_paired_mact_until_targeted_guards_pass
```

Key findings:

- E3 Seed-C/D current-only has `212/300` correct, failed/missing `0/0`, and
  weighted token ratio `0.5916`.
- max_replan=5 recovered `4/12` representative wrong rows, so adaptive budget
  helps selected categories but does not close E3 stability.
- Zero-recovery categories are CRT multi-step numeric composition, WTQ entity
  lookup/row selection, CRT span/universal quantifier, and TabFact false
  negative entailment.
- The next useful work is targeted semantic guard design and affected-slice
  validation, not another full200 rerun or paired MACT run.
