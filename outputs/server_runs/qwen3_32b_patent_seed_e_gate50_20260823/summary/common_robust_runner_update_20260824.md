# Common Robust Runner Update: 2026-08-24

## Purpose

The experiment direction was updated so final paper/patent tables should emphasize Accuracy, Avg Token, and Avg Time, while every input row must still produce one scoreable output row. Failure/fallback details remain diagnostic fields instead of headline metrics.

This update implements the first shared robust-output layer in MyAgent without changing MACT core reasoning.

## Code Change

MyAgent commit `c45d749` (`feat: add robust scoreable fallback outputs`) adds:

- `code/robust_outputs.py`
- `tests/test_robust_outputs.py`
- integration in `code/tqa.py`
- integration in `scripts/server/run_baseline_tqa.py`
- integration in `scripts/server/run_mact_one_by_one.py`

The shared helper provides:

- dataset-aware fallback answers that do not use gold labels;
- `fallback_used`;
- `retry_count`;
- `error_type`;
- `context_overflow`;
- `execution_error`;
- nested `robust_runner` diagnostics.

## Behavior

When a row fails after the existing method-specific recovery path:

- WTQ fallback is `0` for numeric/count-like questions, otherwise `unknown`;
- TabFact fallback is `false`;
- CRT fallback is `No` for yes/no-style questions, otherwise `0`.

The row still keeps `exec_error` and diagnostic metadata, so it remains auditable. The evaluator will score the fallback prediction as correct or incorrect instead of treating the row as missing.

For MACT, this is an outer wrapper change in `scripts/server/run_mact_one_by_one.py`. It does not change MACT prompts, agents, voting, code execution policy, or reasoning parameters.

## Validation

Static validation:

```bash
python -m py_compile code/robust_outputs.py code/tqa.py scripts/server/run_baseline_tqa.py scripts/server/run_mact_one_by_one.py scripts/server/run_mact_sharded_one_by_one.py
```

Targeted tests:

```bash
python -m unittest tests.test_robust_outputs tests.test_run_baseline_tqa tests.test_run_mact_one_by_one tests.test_run_mact_sharded_one_by_one tests.test_server_runner tests.test_evaluate_results tests.test_tqa_failure_exit -v
```

Result: `36` tests passed.

## Remaining Gap

This is the output-contract layer. It does not yet implement full context truncation / prompt compression retry for every method. Existing code-execution repair remains available for Single-Agent Pandas and MyAgent internal planning; MACT still needs a bounded wrapper retry layer for context overflow if we want to fully satisfy the robust-runner recovery policy.

Next recommended step:

1. Add bounded context-overflow retry to the MACT one-by-one wrapper using reduced `max_tokens`.
2. Add a small diagnostic table summarizer for fallback/retry fields.
3. Run a 5-row smoke test that intentionally forces one fallback row and verify `num_missing_answer = 0`.
