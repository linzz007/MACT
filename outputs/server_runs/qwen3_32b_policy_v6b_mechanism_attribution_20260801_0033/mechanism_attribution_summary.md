# Qwen3-32B Policy v6b Mechanism Attribution

Created: 2026-08-01 00:33 CST

## Method

This is an offline associative attribution over frozen artifacts. It aligns current, old MyAgent, and MACT rows by ID, then counts mechanism metadata on transition sets. It does not replace causal ablation runs; it tells us where the current gains are concentrated before spending GPU time.

## Summary

| Dataset | Current | Old MyAgent | MACT | Net vs Old | Net vs MACT | Gain vs Old | Harm vs Old | Current-only vs MACT | MACT-only |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| wtq | 155/200 | 131/200 | 148/200 | +24 | +7 | 25 | 1 | 24 | 17 |
| tabfact | 194/200 | 185/200 | 189/200 | +9 | +5 | 9 | 0 | 7 | 2 |
| crt | 140/200 | 137/200 | 113/200 | +3 | +27 | 6 | 3 | 40 | 13 |

## Gain Concentration

### wtq

- gain_vs_old: 25
- harm_vs_old: 1
- avg tokens on gain rows: current 7156.28, old 6618.76

Top families on gain rows:
- risk_level: 25
- evidence_source: 24
- strong_verification: 24
- evidence_retention: 16
- deterministic_audit: 1

Top tags on gain rows:
- evidence_source:strong_verification_consensus: 24
- risk_level:high: 23
- strong_verification:wtq_high_risk_denotation: 22
- evidence_retention:expanded_context_block_global_rows: 9
- evidence_retention:strict_cell_block_global_rows: 6
- risk_level:light: 1
- strong_verification:post_risk_requires_fallback: 1
- risk_level:fallback: 1
- deterministic_audit:WTQ existing total row metric selected deterministically.: 1
- evidence_retention:expanded_context_block_global_rows_global_columns: 1

### tabfact

- gain_vs_old: 9
- harm_vs_old: 0
- avg tokens on gain rows: current 736.11, old 3365.22

Top families on gain rows:
- evidence_retention: 9
- risk_level: 9
- deterministic_audit: 8

Top tags on gain rows:
- evidence_retention:expanded_context_block_global_rows: 7
- risk_level:high: 7
- risk_level:medium: 2
- deterministic_audit:TabFact retirement threshold count checked deterministically.: 1
- deterministic_audit:TabFact country pair affiliation checked deterministically.: 1
- deterministic_audit:TabFact zero gold medal count checked deterministically.: 1
- deterministic_audit:TabFact all games before date result checked deterministically.: 1
- deterministic_audit:TabFact second-smallest metric row checked deterministically.: 1
- evidence_retention:expanded_context_block_global_rows_global_columns: 1
- deterministic_audit:TabFact venue competition date checked deterministically.: 1

### crt

- gain_vs_old: 6
- harm_vs_old: 3
- avg tokens on gain rows: current 6936.00, old 7281.17

Top families on gain rows:
- evidence_retention: 6
- risk_level: 6
- evidence_source: 2
- strong_verification: 2

Top tags on gain rows:
- evidence_retention:expanded_context_block_global_rows: 6
- risk_level:medium: 4
- evidence_source:strong_verification_consensus: 2
- strong_verification:crt_closed_choice_verification: 2
- risk_level:high: 2

## Interpretation

- WTQ gains concentrate in high-risk rows with strong verification and evidence-retention metadata; this supports the risk-collaboration / persuasion-back claim, but causal confirmation still needs `no_strong_verification`, `no_wtq_verifier_override`, and `no_evidence_retention` ablations.
- TabFact gains concentrate in deterministic audit and global-row evidence retention; gain rows are much cheaper than old MyAgent rows, supporting the low-risk direct-audit claim.
- CRT already exceeded MACT before v6b; current-vs-old gains are smaller and mixed with harms, so CRT should be treated as supportive evidence rather than the main patent novelty proof.

## Next Step

Run P2 coarse Gate-50 ablations when model service is available: `legacy`, `no_strong_verification`, and `no_deterministic_shortcuts`. Add fine-grained switches only after the coarse ablations show the need for causal separation.
