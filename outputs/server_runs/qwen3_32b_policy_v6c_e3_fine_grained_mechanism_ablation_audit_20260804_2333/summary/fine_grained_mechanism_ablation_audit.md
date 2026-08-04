# Fine-grained Mechanism Ablation Audit

Generated: `2026-08-04 23:36:10 CST`

Decision: `fine_grained_mechanism_evidence_ready_for_qwen3_patent_scope_with_evidence_retention_boundary_and_e4_pending`

Frozen-artifact audit that consolidates run-based coarse ablations, fresh S2 guard before/after evidence, and S5 CRT canonicalizer replay. No model run is started by this artifact.

## Key Conclusion

The Qwen3 patent-scope mechanism evidence is strong enough to draft around selective risk collaboration / persuasion-back, deterministic audit, CRT scalar canonicalization, and budget control. Evidence-retention can be cited as supporting evidence with an explicit boundary because a standalone no-evidence-retention causal ablation has not been run.

## Run-based Coarse Ablation

| variant | correct | current ref | delta vs current | token/current | WTQ delta | TabFact delta | CRT delta |
|---|---:|---:|---:|---:|---:|---:|---:|
| legacy | 109/150 | 117/150 | -8 | 0.3302 | -7 | -1 | +0 |
| no_strong_verification | 109/150 | 117/150 | -8 | 0.3303 | -7 | -1 | +0 |
| no_deterministic_shortcuts | 102/150 | 117/150 | -15 | 1.0252 | +1 | -9 | -7 |

Interpretation:

- `no_strong_verification` loses `8/150`, concentrated in WTQ `-7/50`; this is the cleanest run-based evidence for risk collaboration / persuasion-back.
- `no_deterministic_shortcuts` loses `15/150`, with TabFact `-9/50` and CRT `-7/50`; TabFact token/current rises to `1.4487` in the source artifact.
- These ablations are disagreement-enriched diagnostic slices, so they support mechanism contribution rather than random-seed generalization by themselves.

## Fresh S2 Guard Before/After

| metric | baseline | after guard | delta |
|---|---:|---:|---:|
| representative recovered | 4/12 | 8/12 | +4 |
| no-harm correct | 17/18 | 18/18 | +1 |
| failed/missing | 0/0 | 0/0 | 0 |
| weighted token ratio | 0.6975 | 0.6104 | -0.0871 |
| avg elapsed seconds | 23.23 | 16.14 | -7.09 |

| dataset | representative delta | no-harm delta | token ratio baseline -> after |
|---|---:|---:|---:|
| wtq | +1 | +0 | 0.7208 -> 0.6832 |
| tabfact | +1 | +0 | 0.3489 -> 0.2720 |
| crt | +2 | +1 | 0.8782 -> 0.7514 |

## S5 CRT Scalar Canonicalization

| evidence | result |
|---|---:|
| replay rows | 100 |
| replay MyAgent vs MACT | 64/100 vs 62/100 |
| replay flips | 3 total; 2 wrong-to-correct; 0 correct-to-wrong |
| affected-slice fresh | new 16/25 vs old 12/25 vs MACT 12/25 |
| full CRT100 fresh | MyAgent 65/100 vs MACT 62/100; token ratio 0.7979 |

## Claim Readiness

| mechanism | status | patent-use boundary |
|---|---|---|
| risk_collaboration_and_persuasion_back | `run_based_and_fresh_supported` | The coarse no_strong_verification and legacy variants are identical on this slice, so this supports module-level persuasion-back/risk-collaboration contribution, not each individual verifier rule independently. |
| deterministic_audit | `run_based_strong` | WTQ deterministic shortcuts are mixed in the coarse slice; strongest evidence is TabFact and CRT. |
| evidence_retention | `associative_plus_fresh_guard_supported` | There is no standalone no_evidence_retention run-based ablation yet. Use this as supporting evidence, not as a sole causal proof if claims need narrow evidence-retention isolation. |
| crt_scalar_output_canonicalization | `patch_replay_and_fresh_supported` | This is output normalization/scalar canonicalization, not a new broad reasoning module. |
| budget_control | `supported` | CRT token savings are weaker than WTQ/TabFact; use aggregate and per-dataset ratios explicitly. |

## Remaining Boundaries

- E4 multi-model gate remains `no_candidate_wait`; can_start_gate10_now=`False`, untested_local_models=`0`, api_keys_present=`0`.
- Optional only if claim drafting requires standalone isolation of evidence retention. Current evidence is associative plus fresh no-harm/guard support.

## Source Artifacts

- `mechanism_matrix_json`: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_patent_mechanism_evidence_20260801_2222/patent_mechanism_evidence_matrix.json`
- `mechanism_matrix_md`: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_patent_mechanism_evidence_20260801_2222/patent_mechanism_evidence_matrix.md`
- `s2_baseline_json`: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_e3_guard_validation_current_baseline_20260804_1142/summary/e3_guard_validation_current_baseline_summary.json`
- `s2_baseline_md`: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_e3_guard_validation_current_baseline_20260804_1142/summary/e3_guard_validation_current_baseline_summary.md`
- `s2_after_guard_json`: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_e3_guard_validation_after_guard_20260804_1203/summary/e3_guard_validation_after_guard_summary.json`
- `s2_after_guard_md`: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_e3_guard_validation_after_guard_20260804_1203/summary/e3_guard_validation_after_guard_summary.md`
- `s5_replay_json`: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6c_e3_s5_crt_tiebreaker_diag_20260804_2225/summary/s5_crt_canonicalizer_replay_summary.json`
- `s5_replay_md`: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6c_e3_s5_crt_tiebreaker_diag_20260804_2225/summary/s5_crt_canonicalizer_replay_summary.md`
- `s5_affected_json`: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6c_e3_s5_crt_tiebreaker_diag_20260804_2225/summary/s5_affected_slice_real_rerun_summary.json`
- `s5_affected_md`: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6c_e3_s5_crt_tiebreaker_diag_20260804_2225/summary/s5_affected_slice_real_rerun_summary.md`
- `s5_final_json`: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6c_e3_s5_crt_tiebreaker_diag_20260804_2225/summary/e3_s5_final_combined_summary.json`
- `s5_final_md`: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6c_e3_s5_crt_tiebreaker_diag_20260804_2225/summary/e3_s5_final_combined_summary.md`
- `e4_readiness_json`: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/latest_e4_multimodel_gate_readiness_audit.json`
- `e4_readiness_md`: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/latest_e4_multimodel_gate_readiness_audit_zh.md`
