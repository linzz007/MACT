# Qwen3-32B Policy v6b Patent Evidence Index

Created: 2026-08-01 00:33 CST

## Purpose

This document freezes the current Qwen3-32B + MyAgent policy-v6b/current result as the v1 prototype evidence for the selective risk collaboration / persuasion-back patent direction.

It is an evidence index, not a new experiment. The source metrics come from:

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_all200_acceptance_20260731_132611/qwen3_policy_v6b_all200_acceptance_summary.json
```

## Frozen Result

| Dataset | MyAgent | MACT | Delta | Token Ratio | Failure / Missing |
|---|---:|---:|---:|---:|---:|
| WTQ | 155/200 | 148/200 | +7 | 0.6187 | 0 / 0 |
| TabFact | 194/200 | 189/200 | +5 | 0.2014 | 0 / 0 |
| CRT | 140/200 | 113/200 | +27 | 0.8461 | 0 / 0 |
| Aggregate | 489/600 | 450/600 | +39 | 0.5717 | 0 / 0 |

Current staged conclusion: under the same full200 validation scope, MyAgent exceeds MACT on all three datasets and uses substantially fewer weighted average tokens overall.

## Mechanism-Level Evidence Map

| Mechanism | Patent-Relevant Claim | Observed Evidence | Main Code / Report Entry |
|---|---|---|---|
| Risk-stratified execution | Route samples by estimated complexity/risk so low-risk cases avoid expensive multi-agent paths and high-risk cases receive extra checking | Overall token ratio 0.5717 while preserving 0 failure / 0 missing answers | MyAgent PRD section 1.1 and 1.2 |
| Evidence retention under compression | Preserve globally relevant rows for comparative / temporal / extremal WTQ questions instead of over-compressing away answer-bearing context | WTQ improved from old 131/200 to current 155/200, exceeding MACT 148/200 | MyAgent `code/my_agents.py`, WTQ policy-v6b comparison |
| High-confidence verifier persuasion-back | When generator answer and verifier conflict under narrow answer-shape constraints, accept verifier only if original table evidence supports it | WTQ policy-v6b accepted narrow negated-year conflicts without adding failed/missing rows | MyAgent `code/my_agents.py`, WTQ policy-v6b comparison |
| Deterministic semantic audit | For low-risk TabFact patterns, answer directly from table structure instead of spending LLM calls | TabFact improved from v6 185/200 to v6b 194/200, exceeding MACT 189/200; token ratio 0.2014 | MyAgent `code/my_agents.py`, TabFact policy-v6b comparison |
| Same-row and count consistency checks | Reject claims whose mentioned cells exist in the table but not in the same row, or whose count assertion conflicts with exact table counts | TabFact v6b gained 9 over old MyAgent with 0 old-correct/current-wrong in the full200 comparison | TabFact policy-v6b comparison transitions |
| Budget-aware validation | Apply expensive collaboration only where risk justifies it, preserving accuracy gains while reducing elapsed time | Aggregate elapsed ratio 0.1337 vs MACT | All200 acceptance summary |

## Coarse Diagnostic Gate-50 Ablation Evidence

Source:

```text
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_coarse_ablation_gate50_20260801_0040/coarse_ablation_gate50_summary.json
/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_coarse_ablation_gate50_20260801_0040/coarse_ablation_gate50_summary.md
```

This Gate-50 slice is diagnostic: it prioritizes current / old / MACT disagreement rows, so it supports mechanism attribution but should not be presented as fresh random-seed generalization.

| Variant | Dataset | Variant Correct | Current Ref | Delta vs Current | Token Ratio vs Current | Failure / Missing |
|---|---|---:|---:|---:|---:|---:|
| legacy | WTQ | 25/50 | 32/50 | -7 | 0.3799 | 0 / 0 |
| legacy | TabFact | 47/50 | 48/50 | -1 | 0.9523 | 0 / 0 |
| legacy | CRT | 37/50 | 37/50 | +0 | 0.1930 | 0 / 0 |
| no_strong_verification | WTQ | 25/50 | 32/50 | -7 | 0.3800 | 0 / 0 |
| no_strong_verification | TabFact | 47/50 | 48/50 | -1 | 0.9523 | 0 / 0 |
| no_strong_verification | CRT | 37/50 | 37/50 | +0 | 0.1930 | 0 / 0 |
| no_deterministic_shortcuts | WTQ | 33/50 | 32/50 | +1 | 0.9507 | 0 / 0 |
| no_deterministic_shortcuts | TabFact | 39/50 | 48/50 | -9 | 1.4487 | 0 / 0 |
| no_deterministic_shortcuts | CRT | 30/50 | 37/50 | -7 | 0.9926 | 0 / 0 |

Mechanism interpretation:

1. `legacy` and `no_strong_verification` have the same diagnostic result. The largest gap is WTQ `-7/50` versus current reference, supporting the claim that strong verification / persuasion-back primarily protects complex WTQ cases.
2. `no_deterministic_shortcuts` drops TabFact from `48/50` to `39/50` while token use rises to `1.4487x` current. This supports deterministic semantic audit as both an accuracy and cost-control mechanism.
3. The same no-shortcut variant drops CRT from `37/50` to `30/50`, so deterministic audit should be described as a cross-dataset module instead of a TabFact-only patch.
4. All three coarse variants have failure / missing answer `0 / 0`; the observed differences are mechanism effects under the diagnostic slice rather than execution failures.

## Current Limitations

1. This evidence uses a frozen 600-row validation scope. It is strong stage evidence but not yet the final formal experiment package.
2. Some gains were derived from error diagnosis on the same full200 scope. They are mechanism-level rather than answer hardcoding, but new-seed validation is still required.
3. CRT token savings are modest: 0.8461 of MACT. The aggregate token result is clearly lower because WTQ and TabFact have much larger savings.
4. Multi-model generality still needs gate-based validation after server expansion or API key availability.

## Next Required Traces

| Phase | Required Trace |
|---|---|
| P1 patent skeleton | PRD section describing technical problem, modules, protectable claims, and evidence support |
| P2 ablation design | Ablation matrix with switches and run commands |
| P3 offline attribution | Per-mechanism gain / harm / token impact table from existing artifacts |
| P4 new seed validation | Fresh seed run directory with JSON/MD summary |
| P5 multi-model gate | Gate-10 / Gate-50 / Gate-150 summaries and no-go/pass decisions |
