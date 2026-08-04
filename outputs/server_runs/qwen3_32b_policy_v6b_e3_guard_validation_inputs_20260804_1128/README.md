# Qwen3-32B Policy v6b E3 Guard Validation Inputs

This directory prepares the S2 affected-slice/no-harm validation inputs for the E3 semantic-boundary plan.
It does not run a model. It packages rows that should be used after implementing targeted gold-free semantic guards.

Artifacts:

- `input/wtq_e3_guard_validation.jsonl`
- `input/tabfact_e3_guard_validation.jsonl`
- `input/crt_e3_guard_validation.jsonl`
- `input/input_manifest.json`
- `summary/e3_guard_validation_input_plan.json`
- `summary/e3_guard_validation_input_plan.md`
- `tests/test_build_guard_validation_inputs.py`

Current gate:

- total rows: `30`
- representative wrong rows: `12`
- no-harm correct rows: `18`
- future S2 fresh run should recover at least `7/12` representative wrong rows and keep `18/18` no-harm rows correct.

Source evidence:

- multiseed run: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_multiseed_gate50_20260801_2231`
- budget probe: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_e3_boundary_budget_probe_20260804_1035/summary/e3_boundary_budget_probe_summary.json`
- semantic-boundary plan: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_e3_semantic_boundary_plan_20260804_1110/summary/e3_semantic_boundary_plan.json`
