# Qwen3-32B E3 Fine-grained Mechanism Ablation Audit

Created: 2026-08-04 23:33 CST

This directory consolidates already-frozen mechanism evidence for the patent-facing MyAgent vs MACT package. It does not start a model run.

## Purpose

The prior mechanism matrix already had full200, coarse ablation, and offline attribution evidence. This audit adds a clearer fine-grained closeout by aligning:

- run-based coarse Gate-50 ablations,
- fresh S2 guard-validation baseline vs after-guard results,
- S5 CRT scalar canonicalizer replay and fresh CRT100 strict-pass evidence,
- E4 multi-model readiness boundary.

## Output

```text
summary/fine_grained_mechanism_ablation_audit.json
summary/fine_grained_mechanism_ablation_audit.md
```

Decision:

```text
fine_grained_mechanism_evidence_ready_for_qwen3_patent_scope_with_evidence_retention_boundary_and_e4_pending
```

## Key Evidence

| mechanism | evidence |
|---|---|
| risk collaboration / persuasion-back | `no_strong_verification` loses `8/150`, concentrated in WTQ `-7/50`; S2 fresh guards improve representative recovery from `4/12` to `8/12` |
| deterministic audit | `no_deterministic_shortcuts` loses `15/150`; TabFact `-9/50`, CRT `-7/50` |
| evidence retention | supported by offline attribution plus S2 no-harm `17/18 -> 18/18`; no standalone no-evidence-retention ablation yet |
| CRT scalar canonicalization | replay `64/100 > 62/100`, affected-slice fresh `16/25` vs old `12/25`, full CRT100 fresh `65/100 > 62/100` |
| budget control | full200 token ratio `0.5717`, S5 paired multi-seed token ratio `0.5662` |

## Boundary

E4 remains `no_candidate_wait`: no new local model path or API provider/key exists, so Gate-10 should not start yet.
