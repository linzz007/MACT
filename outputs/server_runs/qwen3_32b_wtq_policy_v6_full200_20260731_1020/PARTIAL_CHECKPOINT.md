# WTQ policy v6 full200 partial checkpoint

- Updated: 2026-07-31 11:10 CST
- Completed raw rows at checkpoint: 107/200
- Partial current accuracy: 82/107
- Same-ID old MyAgent: 72/107
- Same-ID MACT: 82/107
- Current avg tokens: 6392.86; MACT avg tokens: 10629.88; token ratio: 0.6014
- Failures / missing answers: 0 / 0
- Comparison file: `wtq_policy_v6_partial107_comparison.json`
- Runner was intentionally stopped after partial analysis; this checkpoint is not a full200 acceptance result.
- Stop reason: partial run exposed two WTQ regressions (`nu-4268`, `nu-484`). MyAgent v6b fixes were committed in `490c352`; rerun WTQ in a fresh v6b directory rather than resuming this v6 raw file.
