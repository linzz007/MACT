# Patent-Facing Mechanism Evidence Matrix

Created: 2026-08-01 22:22 CST

This document combines frozen full200 results, run-based coarse Gate-50 ablations, and offline attribution. It is written for patent/expert evidence, not as a replacement for future fresh validation.

## Full200 Anchor

| metric | value |
|---|---:|
| MyAgent correct | 489/600 |
| MACT correct | 450/600 |
| delta | +39 |
| token ratio | 0.5717 |
| elapsed ratio | 0.1337 |
| MyAgent failures / missing | 0 / 0 |

## Run-Based Coarse Ablation

Diagnostic Gate-50 is disagreement-enriched. It supports mechanism contribution, not random-seed generalization.

| variant | correct | current ref | delta vs current | token/current | token/MACT |
|---|---:|---:|---:|---:|---:|
| legacy | 109/150 | 117/150 | -8 | 0.3302 | 0.2051 |
| no_strong_verification | 109/150 | 117/150 | -8 | 0.3303 | 0.2052 |
| no_deterministic_shortcuts | 102/150 | 117/150 | -15 | 1.0252 | 0.6368 |

Per-dataset deltas:

| variant | WTQ | TabFact | CRT |
|---|---:|---:|---:|
| legacy | -7/50 | -1/50 | +0/50 |
| no_strong_verification | -7/50 | -1/50 | +0/50 |
| no_deterministic_shortcuts | +1/50 | -9/50 | -7/50 |

## Offline Attribution

| dataset | current | old | MACT | net vs old | net vs MACT | gain vs old | harm vs old |
|---|---:|---:|---:|---:|---:|---:|---:|
| wtq | 155/200 | 131/200 | 148/200 | +24 | +7 | 25 | 1 |
| tabfact | 194/200 | 185/200 | 189/200 | +9 | +5 | 9 | 0 |
| crt | 140/200 | 137/200 | 113/200 | +3 | +27 | 6 | 3 |

Gain family counts:

- wtq: risk_level=25, evidence_source=24, strong_verification=24, evidence_retention=16, deterministic_audit=1
- tabfact: evidence_retention=9, risk_level=9, deterministic_audit=8
- crt: evidence_retention=6, risk_level=6, evidence_source=2, strong_verification=2

## Patent Mechanism Evidence

### risk_collaboration_and_persuasion_back

- coarse_ablation.no_strong_verification: overall -8/150 vs current reference
- coarse_ablation.no_strong_verification.wtq: -7/50 vs current reference
- offline_attribution.wtq.gain_vs_old: 24/25 gain rows tagged strong_verification and 16/25 tagged evidence_retention
- Boundary: The coarse slice is diagnostic and disagreement-enriched; it supports mechanism contribution, not a random-seed generalization estimate.

### deterministic_audit

- coarse_ablation.no_deterministic_shortcuts: overall -15/150 vs current reference
- coarse_ablation.no_deterministic_shortcuts.tabfact: -9/50 vs current reference and 1.4487x current tokens
- coarse_ablation.no_deterministic_shortcuts.crt: -7/50 vs current reference
- offline_attribution.tabfact.gain_vs_old: 8/9 gain rows tagged deterministic_audit
- Boundary: WTQ deterministic shortcuts are mixed on this coarse slice; the strongest deterministic-audit evidence is TabFact and CRT.

### evidence_retention

- offline_attribution.wtq.gain_vs_old: 16/25 gain rows tagged evidence_retention
- offline_attribution.tabfact.gain_vs_old: 9/9 gain rows tagged evidence_retention
- offline_attribution.crt.current_only_vs_mact: 37/40 current-only rows tagged evidence_retention
- Boundary: Evidence-retention attribution is associative unless followed by a fine-grained no_evidence_retention ablation.

### budget_control

- full200 aggregate token ratio current/MACT = 0.5717
- full200 aggregate elapsed ratio current/MACT = 0.1337
- coarse deterministic audit on TabFact improves accuracy while avoiding the high token path
- Boundary: CRT token savings are weaker than WTQ/TabFact; formal claims should use overall token reduction and per-dataset ratios.

## Remaining E2 Work

- Run WTQ targeted fresh validation on Qwen3-32B.
- Run WTQ after-targeted P4b full50 only if targeted fresh passes.
- Add fine-grained no_evidence_retention or no_wtq_verifier_override ablation only if fresh WTQ remains ambiguous.
