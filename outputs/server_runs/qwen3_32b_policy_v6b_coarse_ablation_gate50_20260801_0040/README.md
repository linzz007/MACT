# Qwen3-32B Coarse Ablation Diagnostic Gate-50

Created: 2026-08-01 00:40 CST

Purpose: run low-cost diagnostic Gate-50 ablations before any full200 causal ablation. This slice prioritizes current/old/MACT disagreement rows, so it is useful for mechanism diagnosis but not a fresh random generalization estimate.

Variants:

- `legacy`: `--collaboration-mode legacy`
- `no_strong_verification`: `--disable-strong-verification`
- `no_deterministic_shortcuts`: `--disable-deterministic-shortcuts`

Input files:

- `input/wtq_diagnostic_gate50.jsonl`
- `input/tabfact_diagnostic_gate50.jsonl`
- `input/crt_diagnostic_gate50.jsonl`

Run order:

1. Start Qwen3-32B vLLM on GPU 6,7, port 8000.
2. Run `bash run_legacy_gate50.sh`.
3. Run `python summarize_ablation_gate50.py --variant legacy`.
4. Checkpoint to GitHub.
5. Repeat for `no_strong_verification` and `no_deterministic_shortcuts`.

Acceptance for this diagnostic stage:

- Every variant must produce merged/eval for WTQ, TabFact, and CRT, each with 50 rows.
- Every summary must include accuracy, token, elapsed, failed, and missing counts.
- If a variant is much worse than current on this diagnostic slice, it supports the corresponding mechanism claim and may not need full200 expansion.
