# Coarse Diagnostic Gate-50 Ablation Summary

Created: 2026-08-01 02:37 CST

This is a diagnostic slice that prioritizes current/old/MACT disagreement rows. It supports mechanism analysis but is not a fresh random-seed generalization estimate.

| Variant | Dataset | Variant | Current Ref | Old Ref | MACT Ref | Delta vs Current | Token Ratio vs Current | Failed | Missing |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| legacy | wtq | 25/50 | 32/50 | 8/50 | 40/50 | -7 | 0.3799 | 0 | 0 |
| legacy | tabfact | 47/50 | 48/50 | 39/50 | 43/50 | -1 | 0.9523 | 0 | 0 |
| legacy | crt | 37/50 | 37/50 | 34/50 | 15/50 | +0 | 0.1930 | 0 | 0 |
| no_strong_verification | wtq | 25/50 | 32/50 | 8/50 | 40/50 | -7 | 0.3800 | 0 | 0 |
| no_strong_verification | tabfact | 47/50 | 48/50 | 39/50 | 43/50 | -1 | 0.9523 | 0 | 0 |
| no_strong_verification | crt | 37/50 | 37/50 | 34/50 | 15/50 | +0 | 0.1930 | 0 | 0 |
| no_deterministic_shortcuts | wtq | 33/50 | 32/50 | 8/50 | 40/50 | +1 | 0.9507 | 0 | 0 |
| no_deterministic_shortcuts | tabfact | 39/50 | 48/50 | 39/50 | 43/50 | -9 | 1.4487 | 0 | 0 |
| no_deterministic_shortcuts | crt | 30/50 | 37/50 | 34/50 | 15/50 | -7 | 0.9926 | 0 | 0 |

## Interpretation

- `legacy` and `no_strong_verification` produce the same diagnostic result: WTQ 25/50, TabFact 47/50, CRT 37/50. The largest current-vs-ablation gap is WTQ -7, supporting strong verification / persuasion-back as a core WTQ contributor.
- `no_deterministic_shortcuts` sharply hurts TabFact: 39/50 vs current reference 48/50, while token usage rises to 1.4487x current. This is strong evidence that deterministic audit is both more accurate and cheaper on TabFact.
- `no_deterministic_shortcuts` also hurts CRT by -7 on this diagnostic slice, so deterministic shortcuts should be treated as a cross-dataset module, not only a TabFact patch.
- No coarse variant produced failed or missing answers.

## Next Step

Use these coarse results in the patent evidence package. Do not expand every variant to full200; only add fine-grained switches if the patent narrative needs cleaner causal separation for `no_wtq_verifier_override`, `no_evidence_retention`, or `no_tabfact_audit_v6b`.
