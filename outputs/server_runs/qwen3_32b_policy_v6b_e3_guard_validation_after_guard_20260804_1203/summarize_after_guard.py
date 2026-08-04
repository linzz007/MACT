#!/usr/bin/env python3
"""Summarize the E3 S2 guard-validation after-guard rerun."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


RUN_DIR = Path(__file__).resolve().parent
BASELINE_SUMMARIZER = Path(
    "/home/ubuntu/lzz/MACT/outputs/server_runs/"
    "qwen3_32b_policy_v6b_e3_guard_validation_current_baseline_20260804_1142/"
    "summarize_current_baseline.py"
)


def load_baseline_summarizer():
    spec = importlib.util.spec_from_file_location("e3_baseline_summary", BASELINE_SUMMARIZER)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load baseline summarizer: {BASELINE_SUMMARIZER}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    summary_mod = load_baseline_summarizer()
    summary_mod.RUN_DIR = RUN_DIR
    summary_mod.OUTPUT_ROOT = RUN_DIR / "myagent_after_guard"
    summary_mod.SUMMARY_DIR = RUN_DIR / "summary"

    summary = summary_mod.build_summary()
    summary["artifact_name"] = "e3_guard_validation_after_guard_summary"
    summary["scope"] = (
        "Fresh after-guard run on the 30-row E3 S2 guard-validation input package. "
        "This run evaluates gold-free semantic guards for WTQ multi-condition lookup, "
        "TabFact numbered same-team relation, CRT numeric outlier detection, CRT top-k "
        "years-played averages, and CRT constructor retirement-reason percentage."
    )
    if summary["decision"] == "baseline_passes_s2_gate_without_new_guard":
        summary["decision"] = "after_guard_passes_s2_gate"
    elif summary["decision"] == "baseline_needs_guard_implementation":
        summary["decision"] = "after_guard_needs_followup"
    summary["baseline_run"] = (
        "/home/ubuntu/lzz/MACT/outputs/server_runs/"
        "qwen3_32b_policy_v6b_e3_guard_validation_current_baseline_20260804_1142"
    )
    summary["guard_change_scope"] = [
        "WTQ multi-condition target-column lookup",
        "TabFact numbered same-team relation audit",
        "CRT numeric outlier yes/no audit",
        "CRT top-k years-played average",
        "CRT constructor retirement-reason percentage",
    ]

    summary_dir = RUN_DIR / "summary"
    summary_mod.write_json(summary_dir / "e3_guard_validation_after_guard_summary.json", summary)
    markdown = summary_mod.render_markdown(summary)
    markdown = markdown.replace(
        "# E3 Guard Validation Current Baseline Summary",
        "# E3 Guard Validation After-Guard Summary",
    )
    (summary_dir / "e3_guard_validation_after_guard_summary.md").write_text(
        markdown,
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
