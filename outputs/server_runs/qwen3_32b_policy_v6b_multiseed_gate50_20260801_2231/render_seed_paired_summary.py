#!/usr/bin/env python3
"""Render a compact markdown summary for one E3 paired Gate-50 seed."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


RUN_DIR = Path(__file__).resolve().parent
TASKS = ("wtq", "tabfact", "crt")


def count_correct(item: dict[str, Any], system: str) -> tuple[int, int]:
    evaluation = item[system]
    rows = int(evaluation.get("num_with_gold") or evaluation.get("num_samples") or 0)
    correct = int(evaluation.get("correct") or round(float(evaluation.get("primary_accuracy") or 0.0) * rows))
    return correct, rows


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(f"usage: {Path(sys.argv[0]).name} <seed_c|seed_d>")
    seed_label = sys.argv[1]
    if seed_label not in {"seed_c", "seed_d"}:
        raise SystemExit("seed label must be seed_c or seed_d")

    summary_path = RUN_DIR / "summary" / f"{seed_label}_paired_gate50_summary.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))

    strictly_above = 0
    at_least = 0
    lines = [
        f"# E3 Paired Gate-50 Summary: {seed_label}",
        "",
        f"Run dir: `{RUN_DIR}`",
        "",
        "| Dataset | MyAgent | MACT | Delta | Token Ratio | Failed MyAgent / MACT | Missing MyAgent / MACT | Paired myOnly / mactOnly |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for task in TASKS:
        item = summary["datasets"][task]
        my_correct, rows = count_correct(item, "myagent")
        mact_correct, _ = count_correct(item, "mact")
        if my_correct > mact_correct:
            strictly_above += 1
        if my_correct >= mact_correct:
            at_least += 1
        ratio = item.get("token_ratio_myagent_to_mact")
        paired = item.get("paired") or {}
        lines.append(
            f"| {task} | {my_correct}/{rows} | {mact_correct}/{rows} | {my_correct - mact_correct:+d} | "
            f"{ratio:.4f} | {item['myagent'].get('num_failed_exec')}/{item['mact'].get('num_failed_exec')} | "
            f"{item['myagent'].get('num_missing_answer')}/{item['mact'].get('num_missing_answer')} | "
            f"{paired.get('myagent_only')}/{paired.get('mact_only')} |"
        )

    overall = summary["overall"]
    my_correct, rows = count_correct(overall, "myagent")
    mact_correct, _ = count_correct(overall, "mact")
    strict_goal = strictly_above == len(TASKS)
    token_ratio = summary.get("token_ratio_myagent_to_mact")
    summary["datasets_myagent_strictly_above_mact"] = strictly_above
    summary["datasets_myagent_at_least_mact_recomputed"] = at_least
    summary["strict_all_dataset_superiority"] = strict_goal
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines.extend(
        [
            "",
            f"Overall: MyAgent `{my_correct}/{rows}` vs MACT `{mact_correct}/{rows}`, token ratio `{token_ratio:.4f}`.",
            f"Datasets MyAgent > MACT: `{strictly_above}/3`.",
            f"Datasets MyAgent >= MACT: `{at_least}/3`.",
            f"Accepted by existing paired criteria: `{summary.get('accepted')}`.",
            f"Strict all-dataset superiority goal met: `{strict_goal}`.",
        ]
    )
    md_path = RUN_DIR / "summary" / f"{seed_label}_paired_gate50_summary.md"
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("wrote", md_path)


if __name__ == "__main__":
    main()
