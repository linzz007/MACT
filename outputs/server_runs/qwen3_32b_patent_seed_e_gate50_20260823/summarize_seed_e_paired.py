#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


RUN_DIR = Path(__file__).resolve().parent
TASKS = ("wtq", "tabfact", "crt")


def count_correct(summary: dict[str, Any]) -> tuple[int, int]:
    rows = int(summary.get("num_with_gold") or summary.get("num_samples") or 0)
    correct = int(round(float(summary.get("primary_accuracy") or 0.0) * rows))
    return correct, rows


def main() -> None:
    path = RUN_DIR / "seed_e_paired_gate50_summary.json"
    summary = json.loads(path.read_text(encoding="utf-8"))
    strictly_above = 0
    at_least = 0
    lines = [
        "# Seed-E Paired Gate-50 Summary",
        "",
        f"Run dir: `{RUN_DIR}`",
        "",
        "| Dataset | MyAgent | MACT | Delta | Token Ratio | Failed MyAgent / MACT | Missing MyAgent / MACT |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for dataset in TASKS:
        item = summary["datasets"][dataset]
        my = item["myagent"]
        ma = item["mact"]
        my_correct, rows = count_correct(my)
        mact_correct, _ = count_correct(ma)
        if my_correct > mact_correct:
            strictly_above += 1
        if my_correct >= mact_correct:
            at_least += 1
        lines.append(
            f"| {dataset} | {my_correct}/{rows} | {mact_correct}/{rows} | {my_correct - mact_correct:+d} | "
            f"{item.get('token_ratio_myagent_to_mact'):.4f} | "
            f"{my.get('num_failed_exec')}/{ma.get('num_failed_exec')} | "
            f"{my.get('num_missing_answer')}/{ma.get('num_missing_answer')} |"
        )
    overall = summary["overall"]
    my_correct, rows = count_correct(overall["myagent"])
    mact_correct, _ = count_correct(overall["mact"])
    summary["datasets_myagent_strictly_above_mact"] = strictly_above
    summary["datasets_myagent_at_least_mact_recomputed"] = at_least
    summary["strict_all_dataset_superiority"] = strictly_above == len(TASKS)
    path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines.extend(
        [
            "",
            f"Overall: MyAgent `{my_correct}/{rows}` vs MACT `{mact_correct}/{rows}`, token ratio `{summary.get('token_ratio_myagent_to_mact'):.4f}`.",
            f"Datasets MyAgent > MACT: `{strictly_above}/3`.",
            f"Datasets MyAgent >= MACT: `{at_least}/3`.",
            f"Accepted by existing paired criteria: `{summary.get('accepted')}`.",
            f"Strict all-dataset superiority goal met: `{strictly_above == len(TASKS)}`.",
        ]
    )
    md_path = RUN_DIR / "seed_e_paired_gate50_summary.md"
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("wrote", md_path)


if __name__ == "__main__":
    main()
