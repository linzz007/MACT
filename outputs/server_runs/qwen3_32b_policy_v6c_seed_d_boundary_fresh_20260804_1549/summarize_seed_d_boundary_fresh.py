#!/usr/bin/env python3
"""Summarize Seed-D WTQ/TabFact boundary fresh rerun.

This run verifies the current MyAgent code after v6c boundary shortcuts on the
Seed-D WTQ/TabFact Gate-50 inputs. Seed-D CRT and Seed-C rows are inherited
from the prior S3 run and are explicitly marked as inherited evidence.
"""

from __future__ import annotations

import datetime as dt
import json
import subprocess
from pathlib import Path
from typing import Any


RUN_DIR = Path(__file__).resolve().parent
S3_RUN_DIR = Path("/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_e3_s3_current_rerun_after_guard_20260804_1425")
SOURCE_RUN_DIR = Path("/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_multiseed_gate50_20260801_2231")
MYAGENT_ROOT = Path("/home/ubuntu/lzz/MyAgent")
MACT_ROOT = Path("/home/ubuntu/lzz/MACT")
OUTPUT_ROOT = RUN_DIR / "myagent_seed_d_boundary_fresh"
SUMMARY_DIR = RUN_DIR / "summary"
MODEL = "qwen3-32b-local"
MACT_AVG = {"wtq": 10508.03, "tabfact": 10830.825, "crt": 12809.985}
THRESHOLDS = {"wtq": 35, "tabfact": 45, "crt": 30}
TASKS = ("wtq", "tabfact", "crt")


def count_jsonl(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(1 for line in path.open(encoding="utf-8") if line.strip())


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def git_commit(repo: Path) -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=repo, text=True).strip()
    except Exception:
        return "unknown"


def correct_count(ev: dict[str, Any]) -> int:
    rows = int(ev.get("num_with_gold") or ev.get("num_samples") or 0)
    return int(round(float(ev.get("primary_accuracy") or 0.0) * rows))


def fresh_item(task: str) -> dict[str, Any]:
    input_path = SOURCE_RUN_DIR / "input" / "seed_d" / f"{task}_seed_d_gate50.jsonl"
    merged_path = OUTPUT_ROOT / "merged" / f"{task}_{MODEL}.jsonl"
    eval_path = OUTPUT_ROOT / "eval" / f"{task}_{MODEL}_eval.json"
    ev = read_json(eval_path)
    rows = int(ev.get("num_with_gold") or ev.get("num_samples") or 0)
    correct = correct_count(ev)
    avg_tokens = float(ev.get("avg_total_tokens") or 0.0)
    failed = int(ev.get("num_failed_exec") or 0)
    missing = int(ev.get("num_missing_answer") or 0)
    token_ratio = avg_tokens / MACT_AVG[task]
    return {
        "evidence_mode": "fresh_v6c_boundary_rerun",
        "input_path": str(input_path),
        "merged_path": str(merged_path),
        "eval_path": str(eval_path),
        "input_rows": count_jsonl(input_path),
        "merged_rows": count_jsonl(merged_path),
        "eval_rows": int(ev.get("num_samples") or 0),
        "num_with_gold": rows,
        "correct": correct,
        "exact_correct": int(round(float(ev.get("exact_match") or 0.0) * rows)),
        "accuracy": float(ev.get("primary_accuracy") or 0.0),
        "exact_match": float(ev.get("exact_match") or 0.0),
        "avg_total_tokens": avg_tokens,
        "mact_avg_tokens_full200_reference": MACT_AVG[task],
        "token_ratio_to_mact_full200": token_ratio,
        "avg_elapsed_seconds": float(ev.get("avg_elapsed_seconds") or 0.0),
        "num_failed_exec": failed,
        "num_missing_answer": missing,
        "num_em_mismatch": int(ev.get("num_em_mismatch") or 0),
        "threshold_correct": THRESHOLDS[task],
        "passed_current_seed_gate": (
            count_jsonl(input_path) == 50
            and count_jsonl(merged_path) == 50
            and int(ev.get("num_samples") or 0) == 50
            and failed == 0
            and missing == 0
            and token_ratio < 1.0
            and correct >= THRESHOLDS[task]
        ),
    }


def inherited_item(seed_label: str, task: str) -> dict[str, Any]:
    s3_summary = read_json(S3_RUN_DIR / "summary" / f"{seed_label}_s3_current_summary.json")
    item = dict(s3_summary["datasets"][task])
    item["evidence_mode"] = "inherited_from_s3_no_code_path_change" if seed_label == "seed_d" else "inherited_seed_c_s3"
    item["inherited_summary_path"] = str(S3_RUN_DIR / "summary" / f"{seed_label}_s3_current_summary.json")
    return item


def summarize_seed_d() -> dict[str, Any]:
    datasets = {
        "wtq": fresh_item("wtq"),
        "tabfact": fresh_item("tabfact"),
        "crt": inherited_item("seed_d", "crt"),
    }
    rows = sum(int(item["num_with_gold"]) for item in datasets.values())
    correct = sum(int(item["correct"]) for item in datasets.values())
    token_num = sum(float(item["avg_total_tokens"]) * int(item["num_with_gold"]) for item in datasets.values())
    token_den = sum(MACT_AVG[task] * int(datasets[task]["num_with_gold"]) for task in TASKS)
    elapsed_num = sum(float(item["avg_elapsed_seconds"]) * int(item["num_with_gold"]) for item in datasets.values())
    failed = sum(int(item["num_failed_exec"] or 0) for item in datasets.values())
    missing = sum(int(item["num_missing_answer"] or 0) for item in datasets.values())
    return {
        "artifact_name": "seed_d_boundary_fresh_summary",
        "generated_at_local": dt.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z"),
        "run_dir": str(RUN_DIR),
        "source_s3_run_dir": str(S3_RUN_DIR),
        "seed_label": "seed_d",
        "stage": "E3 Seed-D WTQ/TabFact fresh rerun after v6c boundary shortcuts; CRT inherited from S3",
        "model": MODEL,
        "git_commits_at_generation": {
            "myagent": git_commit(MYAGENT_ROOT),
            "mact": git_commit(MACT_ROOT),
        },
        "datasets": datasets,
        "overall": {
            "correct": correct,
            "rows": rows,
            "accuracy": correct / rows if rows else 0.0,
            "avg_total_tokens_weighted": token_num / rows if rows else 0.0,
            "token_ratio_to_mact_full200_weighted": token_num / token_den if token_den else None,
            "avg_elapsed_seconds_weighted": elapsed_num / rows if rows else 0.0,
            "failed": failed,
            "missing": missing,
        },
        "decision": "seed_d_boundary_fresh_passes_current_gate" if all(item["passed_current_seed_gate"] for item in datasets.values()) else "seed_d_boundary_fresh_stop_or_inspect",
        "paired_mact_candidate": all(item["passed_current_seed_gate"] for item in datasets.values()),
    }


def summarize_combined(seed_d: dict[str, Any]) -> dict[str, Any]:
    seed_c = read_json(S3_RUN_DIR / "summary" / "seed_c_s3_current_summary.json")
    seed_c["evidence_mode"] = "inherited_seed_c_s3"
    seeds = [seed_c, seed_d]
    rows = sum(seed["overall"]["rows"] for seed in seeds)
    correct = sum(seed["overall"]["correct"] for seed in seeds)
    token_num = sum(seed["overall"]["avg_total_tokens_weighted"] * seed["overall"]["rows"] for seed in seeds)
    token_den = 0.0
    elapsed_num = 0.0
    failed = 0
    missing = 0
    for seed in seeds:
        for task in TASKS:
            token_den += MACT_AVG[task] * seed["datasets"][task]["num_with_gold"]
        elapsed_num += seed["overall"]["avg_elapsed_seconds_weighted"] * seed["overall"]["rows"]
        failed += seed["overall"]["failed"]
        missing += seed["overall"]["missing"]
    both_pass = seed_c["decision"] == "s3_seed_pass_run_paired_mact_candidate" and seed_d["paired_mact_candidate"]
    return {
        "artifact_name": "e3_boundary_fresh_combined_summary",
        "generated_at_local": dt.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z"),
        "run_dir": str(RUN_DIR),
        "stage": "E3 combined summary with Seed-C inherited S3 and Seed-D WTQ/TabFact boundary fresh",
        "model": MODEL,
        "seeds": seeds,
        "overall": {
            "correct": correct,
            "rows": rows,
            "accuracy": correct / rows if rows else 0.0,
            "avg_total_tokens_weighted": token_num / rows if rows else 0.0,
            "token_ratio_to_mact_full200_weighted": token_num / token_den if token_den else None,
            "avg_elapsed_seconds_weighted": elapsed_num / rows if rows else 0.0,
            "failed": failed,
            "missing": missing,
        },
        "decision": "boundary_fresh_pass_run_paired_mact_candidate" if both_pass else "boundary_fresh_stop_or_inspect",
        "paired_mact_next": both_pass,
        "limitations": [
            "Seed-D WTQ and TabFact are fresh v6c reruns.",
            "Seed-D CRT is inherited from the S3 run because this patch did not change CRT shortcut paths and CRT already passed its current gate.",
            "Seed-C is inherited from the S3 run; an optional full S3 rerun can be used before paired MACT if stricter freshness is required.",
        ],
    }


def markdown_table(headers: list[str], rows: list[list[Any]]) -> list[str]:
    lines = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    for row in rows:
        lines.append("| " + " | ".join(str(value) for value in row) + " |")
    return lines


def render_seed_d(summary: dict[str, Any]) -> str:
    rows = []
    for task in TASKS:
        item = summary["datasets"][task]
        rows.append(
            [
                task,
                item["evidence_mode"],
                f"{item['input_rows']}/{item['merged_rows']}/{item['eval_rows']}",
                f"{item['correct']}/50",
                f"{item['threshold_correct']}/50",
                f"{item['token_ratio_to_mact_full200']:.4f}",
                f"{item['avg_total_tokens']:.1f}",
                f"{item['avg_elapsed_seconds']:.2f}",
                f"{item['num_failed_exec']}/{item['num_missing_answer']}",
                "pass" if item["passed_current_seed_gate"] else "inspect",
            ]
        )
    overall = summary["overall"]
    lines = [
        "# Seed-D Boundary Fresh Summary",
        "",
        f"Generated: `{summary['generated_at_local']}`",
        "",
    ]
    lines.extend(markdown_table(["dataset", "evidence", "input/merged/eval", "correct", "threshold", "token ratio", "avg tokens", "avg seconds", "failed/missing", "gate"], rows))
    lines.extend(
        [
            "",
            f"Overall: `{overall['correct']}/{overall['rows']}`, token ratio `{overall['token_ratio_to_mact_full200_weighted']:.4f}`, failed/missing `{overall['failed']}/{overall['missing']}`.",
            f"Decision: `{summary['decision']}`.",
            "",
        ]
    )
    return "\n".join(lines)


def render_combined(summary: dict[str, Any]) -> str:
    rows = []
    for seed in summary["seeds"]:
        ratio = seed["overall"]["token_ratio_to_mact_full200_weighted"]
        rows.append(
            [
                seed["seed_label"],
                seed.get("evidence_mode", "mixed"),
                f"{seed['overall']['correct']}/{seed['overall']['rows']}",
                f"{ratio:.4f}",
                f"{seed['overall']['failed']}/{seed['overall']['missing']}",
                seed["decision"],
            ]
        )
    overall = summary["overall"]
    lines = [
        "# E3 Boundary Fresh Combined Summary",
        "",
        f"Generated: `{summary['generated_at_local']}`",
        "",
    ]
    lines.extend(markdown_table(["seed", "evidence", "correct", "token ratio", "failed/missing", "decision"], rows))
    lines.extend(
        [
            "",
            f"Combined: `{overall['correct']}/{overall['rows']}`, token ratio `{overall['token_ratio_to_mact_full200_weighted']:.4f}`, failed/missing `{overall['failed']}/{overall['missing']}`.",
            f"Decision: `{summary['decision']}`, paired_mact_next=`{summary['paired_mact_next']}`.",
            "",
            "## Limitations",
            "",
        ]
    )
    lines.extend(f"- {item}" for item in summary["limitations"])
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    SUMMARY_DIR.mkdir(parents=True, exist_ok=True)
    seed_d = summarize_seed_d()
    combined = summarize_combined(seed_d)
    (SUMMARY_DIR / "seed_d_boundary_fresh_summary.json").write_text(json.dumps(seed_d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (SUMMARY_DIR / "seed_d_boundary_fresh_summary.md").write_text(render_seed_d(seed_d), encoding="utf-8")
    (SUMMARY_DIR / "e3_boundary_fresh_combined_summary.json").write_text(json.dumps(combined, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (SUMMARY_DIR / "e3_boundary_fresh_combined_summary.md").write_text(render_combined(combined), encoding="utf-8")
    print(json.dumps({"seed_d": seed_d["decision"], "combined": combined["decision"], "paired_mact_next": combined["paired_mact_next"], "combined_correct": combined["overall"]["correct"], "combined_rows": combined["overall"]["rows"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
