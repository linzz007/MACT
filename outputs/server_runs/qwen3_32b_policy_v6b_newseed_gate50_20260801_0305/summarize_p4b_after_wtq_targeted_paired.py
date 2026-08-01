#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


RUN_DIR = Path(__file__).resolve().parent
path = RUN_DIR / "p4b_after_wtq_targeted_paired_summary.json"
summary = json.loads(path.read_text(encoding="utf-8"))
lines = [
    "# P4b Paired New-Seed Gate-50 Summary After WTQ Targeted Fix",
    "",
    f"Run dir: `{RUN_DIR}`",
    "",
    "| Dataset | MyAgent | MACT | Delta | Token Ratio | Failed MyAgent / MACT | Missing MyAgent / MACT |",
    "|---|---:|---:|---:|---:|---:|---:|",
]
strict_wins = 0
for ds in ("wtq", "tabfact", "crt"):
    item = summary["datasets"][ds]
    my = item["myagent"]
    ma = item["mact"]
    n = int(my.get("num_samples") or 0)
    myc = int(round(float(my.get("primary_accuracy") or 0.0) * n))
    mac = int(round(float(ma.get("primary_accuracy") or 0.0) * n))
    strict_wins += int(myc > mac)
    ratio = item.get("token_ratio_myagent_to_mact")
    lines.append(
        f"| {ds} | {myc}/{n} | {mac}/{n} | {myc-mac:+d} | {ratio:.4f} | "
        f"{my.get('num_failed_exec')}/{ma.get('num_failed_exec')} | "
        f"{my.get('num_missing_answer')}/{ma.get('num_missing_answer')} |"
    )
overall = summary["overall"]
my = overall["myagent"]
ma = overall["mact"]
n = int(my.get("num_samples") or 0)
myc = int(round(float(my.get("primary_accuracy") or 0.0) * n))
mac = int(round(float(ma.get("primary_accuracy") or 0.0) * n))
strict_all_dataset_goal = strict_wins == 3
lines += [
    "",
    f"Overall: MyAgent `{myc}/{n}` vs MACT `{mac}/{n}`, token ratio `{summary.get('token_ratio_myagent_to_mact'):.4f}`.",
    f"Datasets MyAgent > MACT: `{strict_wins}/3`.",
    f"Strict all-dataset new-seed goal met: `{strict_all_dataset_goal}`.",
    f"Accepted by existing paired criteria: `{summary.get('accepted')}`.",
]
(RUN_DIR / "p4b_after_wtq_targeted_paired_summary.md").write_text(
    "\n".join(lines) + "\n",
    encoding="utf-8",
)
print("wrote", RUN_DIR / "p4b_after_wtq_targeted_paired_summary.md")
