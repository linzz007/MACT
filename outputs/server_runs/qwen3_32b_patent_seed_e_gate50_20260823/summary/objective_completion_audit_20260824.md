# Objective Completion Audit: Patent-Facing MyAgent vs MACT Evidence

Generated: 2026-08-24 CST

This audit checks the active objective requirement by requirement against files that currently exist in the workspace. It is intentionally conservative: a requirement is not marked complete unless the current artifacts prove it.

## Current State

| Area | Status | Evidence |
|---|---|---|
| Qwen3-32B Formal-200 MyAgent > MACT | Complete | `../qwen3_32b_baseline_formal200_20260812_1505/summary/formal200_final_evidence_package_20260814.md` |
| Formal-200 efficiency | Complete | MyAgent avg token `6293.12` vs MACT `11318.89`; time `16.749s` vs `126.861s` in final evidence package |
| WTQ generalization diagnostic | Complete as boundary evidence | `../qwen3_32b_baseline_formal200_20260812_1505/summary/wtq_shortcut_generalization_20260814.md` |
| Mechanism ablation | Complete for Gate-50 core mechanisms, partial for strong/risk claims | PRD records deterministic shortcut, no-question-routing, no-risk-scoring, no-table-compression, no-strong evidence |
| Multi-model gate | Complete as no-go boundary evidence | `../multimodel_gate50_summaries_20260730_1948/` |
| Seed-E paired stability | Complete but negative | `seed_e_paired_gate50_summary.md`: MyAgent `95/150`, MACT `105/150` |
| Seed-E failure-cluster diagnosis | Complete | `summary/seed_e_failure_cluster_diagnostic.md/json` |
| Answer-contract mechanism implementation | Locally implemented, focused rerun pending | MyAgent local commit `622be3a`; offline validation in `summary/answer_contract_patch_offline_validation.md/json` |
| Answer-contract focused rerun | Prepared, not executed | `run_answer_contract_focused_validation.sh`; current sandbox cannot reach `127.0.0.1:8000/8001` |
| Patent-facing supplement draft | Complete as draft evidence, not legal final | `summary/patent_spec_draft_seed_e_supplement_20260824.md` |
| Single PRD tracking | Complete and current locally | `/home/ubuntu/lzz/MyAgent/docs/server/server_codex_reports/current-baseline-experiment-execution-plan.md` |
| GitHub synchronization | Incomplete | MyAgent ahead origin by local commits; MACT ahead origin by local commits; current sandbox cannot resolve `github.com` |

## Requirement-Level Audit

### 1. Formal Result Package

Requirement: show that the project has a locked Qwen3-32B result where MyAgent exceeds MACT on WTQ, TabFact, CRT, and overall, with token/time/failure metrics.

Status: complete.

Evidence:

- `formal200_final_evidence_package_20260814.md`
- MyAgent final: WTQ `157/200`, TabFact `190/200`, CRT `133/200`, overall `480/600 = 0.8000`
- MACT: WTQ `156/200`, TabFact `185/200`, CRT `124/200`, overall `465/600 = 0.7750`
- MyAgent token ratio `0.5560`, time ratio `0.1320`, fail/missing `0/0` vs MACT `4/4`

### 2. WTQ Generalization

Requirement: provide a diagnostic showing whether WTQ deterministic shortcuts generalize beyond the formal split.

Status: complete as boundary evidence.

Evidence:

- `wtq_shortcut_generalization_20260814.md`
- Formal200 shortcut hit accuracy `28/31 = 0.9032`
- Blind200_v1 shortcut hit accuracy `18/19 = 0.9474`
- Full unseen shortcut hit accuracy `290/438 = 0.6621`

Interpretation: useful on locked/blind samples, unsafe for blind full-pool expansion. Claims must describe high-confidence gated deterministic verification, not an unrestricted WTQ rule library.

### 3. Mechanism Ablation

Requirement: support patent mechanisms with ablations or focused slices.

Status: mostly complete for core mechanisms; partial for strong verification and risk scoring.

Evidence:

- Deterministic shortcut ablation: Gate-50 drops from `116/150` to `106/150` and token rises strongly when removed.
- Question routing ablation: accuracy unchanged but avg token rises to `8353.59`.
- No risk scoring: accuracy `122/150` but avg token `6664.23`, so risk scoring should be framed as cost/path control rather than direct accuracy gain on this split.
- No table compression: accuracy `116/150`, avg token `7612.96`, and two WTQ context-limit failures.
- Strong verification remains inconclusive: trigger-71 strong/no-strong both `51/71`.

Interpretation: patent writing should emphasize selective routing, compression, deterministic validation, answer-contract validation, and audit metadata. Strong verification and risk scoring must be worded cautiously.

### 4. Multi-Model Gate

Requirement: verify whether the system works under smaller/quantized models or define the boundary.

Status: complete as no-go boundary evidence.

Evidence:

- `multimodel_gate50_summaries_20260730_1948/`
- Qwen3-14B-AWQ, Qwen2.5-14B-AWQ, and Qwen2.5-3B all no-go on Gate-50 summaries.

Interpretation: current formal claim should be Qwen3-32B scoped. Smaller/quantized model results are boundary evidence, not equal-strength support.

### 5. Multi-Seed Stability

Requirement: strengthen evidence beyond a single formal split.

Status: partial and currently mixed.

Evidence:

- P4b paired new-seed Gate-50 narrowly passed historically.
- Seed-C/D current-only and boundary summaries exist.
- Seed-E paired Gate-50 is complete and negative:
  - WTQ: MyAgent `31/50`, MACT `37/50`
  - TabFact: MyAgent `40/50`, MACT `42/50`
  - CRT: MyAgent `24/50`, MACT `26/50`
  - Overall: MyAgent `95/150`, MACT `105/150`

Interpretation: multi-seed robustness cannot be claimed yet. Seed-E is a useful failure-cluster and stability-boundary dataset.

### 6. Answer-Contract Mechanism

Requirement: convert Seed-E failure clusters into patent-describable mechanisms and evidence.

Status: implemented locally with offline validation; focused model validation pending.

Evidence:

- MyAgent local commit `622be3a` implements:
  - WTQ abbreviation-preserving output
  - CRT average/mean 3-decimal contract
  - CRT proportion fraction formatting
  - scalar NaN invalidation
  - CRT numeric execution candidate preservation
- `answer_contract_patch_offline_validation.md/json`
  - `nu-3415`: `China -> CHN`
  - `crt-280`: `0.16666666666666666 -> 1/6`
  - `crt-502` and `crt-290`: require focused rerun because previous generated code internally rounded to 2 decimals
- Unit tests passed: `python -m unittest discover -s tests -p 'test_myagent_pipeline.py'` with `248` tests.

Pending:

- Focused runner cannot execute in current sandbox because loopback to `127.0.0.1:8000/8001` fails.
- Prepared command:

```bash
cd /home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_patent_seed_e_gate50_20260823
bash run_answer_contract_focused_validation.sh
```

### 7. Patent Draft Evidence

Requirement: have Chinese patent-facing PRD/draft material summarizing target, subgoals, completed work, evidence files, mechanisms, limitations, and next steps.

Status: complete as draft evidence, not legal final.

Evidence:

- `formal200_final_evidence_package_20260814.md`
- `summary/patent_spec_draft_seed_e_supplement_20260824.md`
- Single PRD: `/home/ubuntu/lzz/MyAgent/docs/server/server_codex_reports/current-baseline-experiment-execution-plan.md`

Interpretation: enough to start formal patent drafting, but final legal drafting still needs human/legal review.

### 8. GitHub Synchronization

Requirement: keep MyAgent and MACT synchronized to GitHub because the server is unstable.

Status: incomplete in the current environment.

Evidence:

- MyAgent branch `codex/selective-risk-collaboration` is ahead of origin.
- MACT branch `main` is ahead of origin.
- `getent hosts github.com` returns no host and `git push` fails with `Could not resolve hostname github.com`.

Required commands when DNS/network is restored:

```bash
git -C /home/ubuntu/lzz/MyAgent push origin codex/selective-risk-collaboration
git -C /home/ubuntu/lzz/MACT push origin main
```

## Remaining Work Before Goal Completion

The active objective should not be marked complete until all of the following are true:

1. Pending MyAgent and MACT local commits are pushed to GitHub.
2. Answer-contract focused validation is executed against local Qwen3-32B services and summarized.
3. The PRD is updated with the focused validation outcome.
4. If focused validation is positive, a follow-up Seed-F or Seed-G Gate-50 paired run is executed or explicitly deferred with a documented experiment plan.
5. The patent supplement is either converted into a formal Chinese patent draft or explicitly accepted as the current non-legal draft artifact.

## Next Best Action

When loopback and GitHub DNS are available:

1. Push both repositories.
2. Run `bash run_answer_contract_focused_validation.sh`.
3. Commit and push `diagnostics/answer_contract_patch_focused_20260824/` and `summary/answer_contract_patch_focused_summary.md/json`.
4. Update the PRD with the focused validation result.

If loopback remains unavailable but filesystem access remains available, continue with offline-only patent drafting or a full objective evidence index.
