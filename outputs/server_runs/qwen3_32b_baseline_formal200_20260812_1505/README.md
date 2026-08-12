# Qwen3-32B Baseline Formal-200 Package

Prepared run directory: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_baseline_formal200_20260812_1505`

This package is GPU-ready but does not start any model by itself. Wait until the Qwen3-32B endpoint(s) are available, then run scripts from this directory.

## Execution Order

1. `bash healthcheck_services.sh`
2. `bash run_smoke_direct_cot.sh`
3. `bash run_smoke_single_agent_pandas.sh`
4. Inspect smoke `merged/` and `eval/`; stop if row count is not exactly 5 per dataset.
5. `bash run_formal_myagent.sh`
6. `bash run_formal_direct_cot.sh`
7. `bash run_formal_single_agent_pandas.sh`
8. `bash run_mact_wtq_formal200.sh`
9. `bash run_mact_tabfact_formal200.sh`
10. `bash run_mact_crt_formal200.sh`
11. `bash run_eval_and_summary.sh`

## Ablation Scripts

Run these after the main Formal-200 table is stable:

- `bash run_ablation_legacy50.sh`
- `bash run_ablation_no_strong50.sh`
- `bash run_ablation_no_deterministic_shortcuts50.sh`

Current limitation: no-question-routing and no-table-compression/evidence-retention switches are not present in the current codebase. Treat them as pending implementation or document the limitation if time is tight.

## Output Layout

- `input/formal200/`: fixed 200-row inputs per dataset.
- `input/smoke5/`: fixed 5-row smoke inputs per dataset.
- `input/ablation50/`: fixed 50-row ablation inputs per dataset.
- `myagent_formal200/`
- `direct_cot_formal200/`
- `single_agent_pandas_formal200/`
- `mact/`
- `ablation/`
- `summary/main_baseline_summary.md`
