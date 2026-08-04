# Qwen3-32B E3 Boundary Budget Probe

Generated: `2026-08-04 10:35 CST`

This run is a mechanism probe, not a formal benchmark run. It reruns 12 representative wrong rows from the completed E3 Seed-C/Seed-D Gate-50 diagnosis with `max_replan=5`, compared with the original `max_replan=3` outputs.

Purpose:

- Test whether the E3 failures are mainly replan-budget-sensitive.
- Preserve row-level traces for patent-facing boundary analysis.
- Keep the already running Qwen3-32B vLLM service resident.

Runtime:

- Endpoint: `http://127.0.0.1:8000/v1`
- Served model: `qwen3-32b-local`
- MyAgent collaboration mode: `selective`
- New budget: `max_replan=5`
- Source run: `/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_multiseed_gate50_20260801_2231`

Files:

- `build_probe_inputs.py`: rebuilds the 12-row probe inputs from the E3 source run.
- `run_probe_max_replan5.sh`: runs WTQ, TabFact, and CRT probe inputs against the existing Qwen3 endpoint.
- `summarize_probe.py`: compares original E3 wrong outputs with new `max_replan=5` outputs.
- `input/*_e3_boundary_budget_probe.jsonl`: committed probe inputs.
- `myagent_max_replan5/`: raw, merged, eval, log outputs after running.
- `summary/e3_boundary_budget_probe_summary.{json,md}`: final probe summary.
