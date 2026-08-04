#!/usr/bin/env python3
"""Summarize E3 S3 current-only reruns after S2 guards passed."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
from pathlib import Path
from typing import Any


RUN_DIR = Path(__file__).resolve().parent
SOURCE_RUN_DIR = Path(
    "/home/ubuntu/lzz/MACT/outputs/server_runs/"
    "qwen3_32b_policy_v6b_multiseed_gate50_20260801_2231"
)
MYAGENT_ROOT = Path("/home/ubuntu/lzz/MyAgent")
MACT_ROOT = Path("/home/ubuntu/lzz/MACT")
MODEL = "qwen3-32b-local"
TASKS = ("wtq", "tabfact", "crt")
MACT_AVG = {"wtq": 10508.03, "tabfact": 10830.825, "crt": 12809.985}
THRESHOLDS = {"wtq": 35, "tabfact": 45, "crt": 30}


def count_jsonl(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(1 for line in path.open(encoding="utf-8") if line.strip())


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def git_commit(repo: Path) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "--short", "HEAD"],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout.strip()


def correct_count(evaluation: dict[str, Any]) -> int:
    rows = int(evaluation.get("num_with_gold") or evaluation.get("num_samples") or 0)
    return int(round(float(evaluation.get("primary_accuracy") or 0.0) * rows))


def summarize_seed(seed_label: str) -> dict[str, Any]:
    datasets: dict[str, Any] = {}
    overall_correct = 0
    overall_rows = 0
    token_num = 0.0
    token_den = 0.0
    elapsed_num = 0.0
    failed_total = 0
    missing_total = 0

    for task in TASKS:
        input_path = SOURCE_RUN_DIR / "input" / seed_label / f"{task}_{seed_label}_gate50.jsonl"
        output_root = RUN_DIR / "myagent_s3_after_guard" / seed_label
        merged_path = output_root / "merged" / f"{task}_{MODEL}.jsonl"
        eval_path = output_root / "eval" / f"{task}_{MODEL}_eval.json"
        item: dict[str, Any] = {
            "input_path": str(input_path),
            "merged_path": str(merged_path),
            "eval_path": str(eval_path),
            "input_rows": count_jsonl(input_path),
            "merged_rows": count_jsonl(merged_path),
        }
        if eval_path.exists():
            ev = read_json(eval_path)
            rows = int(ev.get("num_with_gold") or ev.get("num_samples") or 0)
            correct = correct_count(ev)
            avg_tokens = float(ev.get("avg_total_tokens") or 0.0)
            avg_elapsed = float(ev.get("avg_elapsed_seconds") or 0.0)
            token_ratio = avg_tokens / MACT_AVG[task] if MACT_AVG[task] else None
            failed = int(ev.get("num_failed_exec") or 0)
            missing = int(ev.get("num_missing_answer") or 0)
            gate_pass = all(
                [
                    item["input_rows"] == 50,
                    item["merged_rows"] == 50,
                    int(ev.get("num_samples") or 0) == 50,
                    failed == 0,
                    missing == 0,
                    token_ratio is not None and token_ratio < 1.0,
                    correct >= THRESHOLDS[task],
                ]
            )
            item.update(
                {
                    "eval_rows": int(ev.get("num_samples") or 0),
                    "num_with_gold": rows,
                    "correct": correct,
                    "accuracy": float(ev.get("primary_accuracy") or 0.0),
                    "avg_total_tokens": avg_tokens,
                    "mact_avg_tokens_full200_reference": MACT_AVG[task],
                    "token_ratio_to_mact_full200": token_ratio,
                    "avg_elapsed_seconds": avg_elapsed,
                    "num_failed_exec": failed,
                    "num_missing_answer": missing,
                    "num_em_mismatch": int(ev.get("num_em_mismatch") or 0),
                    "passed_current_seed_gate": gate_pass,
                    "threshold_correct": THRESHOLDS[task],
                }
            )
            overall_correct += correct
            overall_rows += rows
            token_num += avg_tokens * rows
            token_den += MACT_AVG[task] * rows
            elapsed_num += avg_elapsed * rows
            failed_total += failed
            missing_total += missing
        else:
            item.update(
                {
                    "eval_rows": 0,
                    "num_with_gold": 0,
                    "correct": 0,
                    "accuracy": 0.0,
                    "avg_total_tokens": 0.0,
                    "token_ratio_to_mact_full200": None,
                    "avg_elapsed_seconds": 0.0,
                    "num_failed_exec": None,
                    "num_missing_answer": None,
                    "num_em_mismatch": None,
                    "passed_current_seed_gate": False,
                    "threshold_correct": THRESHOLDS[task],
                }
            )
        datasets[task] = item

    decision = (
        "s3_seed_pass_run_paired_mact_candidate"
        if all(datasets[task]["passed_current_seed_gate"] for task in TASKS)
        else "s3_seed_stop_or_inspect"
    )
    return {
        "artifact_name": "e3_s3_current_only_seed_summary",
        "generated_at_local": dt.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z"),
        "run_dir": str(RUN_DIR),
        "source_run_dir": str(SOURCE_RUN_DIR),
        "seed_label": seed_label,
        "stage": "E3 S3 MyAgent current-only Gate-50 after S2 guards",
        "model": MODEL,
        "git_commits_at_generation": {
            "myagent": git_commit(MYAGENT_ROOT),
            "mact": git_commit(MACT_ROOT),
        },
        "datasets": datasets,
        "overall": {
            "correct": overall_correct,
            "rows": overall_rows,
            "accuracy": overall_correct / overall_rows if overall_rows else 0.0,
            "avg_total_tokens_weighted": token_num / overall_rows if overall_rows else 0.0,
            "token_ratio_to_mact_full200_weighted": token_num / token_den if token_den else None,
            "avg_elapsed_seconds_weighted": elapsed_num / overall_rows if overall_rows else 0.0,
            "failed": failed_total,
            "missing": missing_total,
        },
        "decision": decision,
    }


def render_seed_markdown(summary: dict[str, Any]) -> str:
    lines = [
        f"# E3 S3 Current-Only Summary: {summary['seed_label']}",
        "",
        f"Generated: `{summary['generated_at_local']}`",
        f"Run dir: `{RUN_DIR}`",
        "",
        "| dataset | rows input/merged/eval | correct | threshold | token ratio | avg tokens | avg seconds | failed/missing | gate |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for task in TASKS:
        item = summary["datasets"][task]
        ratio = item.get("token_ratio_to_mact_full200")
        ratio_text = f"{ratio:.4f}" if ratio is not None else "n/a"
        lines.append(
            f"| {task} | {item['input_rows']}/{item['merged_rows']}/{item['eval_rows']} | "
            f"{item['correct']}/50 | {item['threshold_correct']}/50 | {ratio_text} | "
            f"{item['avg_total_tokens']:.1f} | {item['avg_elapsed_seconds']:.2f} | "
            f"{item['num_failed_exec']}/{item['num_missing_answer']} | "
            f"{'pass' if item['passed_current_seed_gate'] else 'inspect'} |"
        )
    overall = summary["overall"]
    ratio = overall.get("token_ratio_to_mact_full200_weighted")
    ratio_text = f"{ratio:.4f}" if ratio is not None else "n/a"
    lines.extend(
        [
            "",
            f"Overall: `{overall['correct']}/{overall['rows']}`, weighted token ratio `{ratio_text}`, failed/missing `{overall['failed']}/{overall['missing']}`.",
            f"Decision: `{summary['decision']}`.",
            "",
        ]
    )
    return "\n".join(lines)


def summarize_combined() -> dict[str, Any]:
    seeds = []
    for seed in ("seed_c", "seed_d"):
        path = RUN_DIR / "summary" / f"{seed}_s3_current_summary.json"
        if path.exists():
            seeds.append(read_json(path))
        else:
            seeds.append(summarize_seed(seed))
    total_correct = sum(seed["overall"]["correct"] for seed in seeds)
    total_rows = sum(seed["overall"]["rows"] for seed in seeds)
    token_num = sum(
        seed["overall"]["avg_total_tokens_weighted"] * seed["overall"]["rows"]
        for seed in seeds
    )
    token_den = 0.0
    elapsed_num = 0.0
    failed = 0
    missing = 0
    for seed in seeds:
        for task in TASKS:
            item = seed["datasets"][task]
            token_den += MACT_AVG[task] * item["num_with_gold"]
        elapsed_num += seed["overall"]["avg_elapsed_seconds_weighted"] * seed["overall"]["rows"]
        failed += seed["overall"]["failed"]
        missing += seed["overall"]["missing"]
    both_pass = all(seed["decision"] == "s3_seed_pass_run_paired_mact_candidate" for seed in seeds)
    return {
        "artifact_name": "e3_s3_current_only_combined_summary",
        "generated_at_local": dt.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z"),
        "run_dir": str(RUN_DIR),
        "source_run_dir": str(SOURCE_RUN_DIR),
        "stage": "E3 S3 MyAgent current-only Gate-50 after S2 guards",
        "model": MODEL,
        "seeds": seeds,
        "overall": {
            "correct": total_correct,
            "rows": total_rows,
            "accuracy": total_correct / total_rows if total_rows else 0.0,
            "avg_total_tokens_weighted": token_num / total_rows if total_rows else 0.0,
            "token_ratio_to_mact_full200_weighted": token_num / token_den if token_den else None,
            "avg_elapsed_seconds_weighted": elapsed_num / total_rows if total_rows else 0.0,
            "failed": failed,
            "missing": missing,
        },
        "decision": "s3_pass_run_paired_mact_next" if both_pass else "s3_stop_or_inspect_boundary_remains",
        "paired_mact_next": both_pass,
    }


def render_combined_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# E3 S3 Current-Only Combined Summary",
        "",
        f"Generated: `{summary['generated_at_local']}`",
        "",
        "| seed | correct | token ratio | failed/missing | decision |",
        "|---|---:|---:|---:|---|",
    ]
    for seed in summary["seeds"]:
        ratio = seed["overall"].get("token_ratio_to_mact_full200_weighted")
        ratio_text = f"{ratio:.4f}" if ratio is not None else "n/a"
        lines.append(
            f"| {seed['seed_label']} | {seed['overall']['correct']}/{seed['overall']['rows']} | "
            f"{ratio_text} | {seed['overall']['failed']}/{seed['overall']['missing']} | `{seed['decision']}` |"
        )
    overall = summary["overall"]
    ratio = overall.get("token_ratio_to_mact_full200_weighted")
    ratio_text = f"{ratio:.4f}" if ratio is not None else "n/a"
    lines.extend(
        [
            "",
            f"Combined: `{overall['correct']}/{overall['rows']}`, weighted token ratio `{ratio_text}`, failed/missing `{overall['failed']}/{overall['missing']}`.",
            f"Decision: `{summary['decision']}`.",
            f"Paired MACT next: `{summary['paired_mact_next']}`.",
            "",
        ]
    )
    return "\n".join(lines)


def write_seed(seed_label: str) -> None:
    summary = summarize_seed(seed_label)
    summary_dir = RUN_DIR / "summary"
    summary_dir.mkdir(parents=True, exist_ok=True)
    (summary_dir / f"{seed_label}_s3_current_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (summary_dir / f"{seed_label}_s3_current_summary.md").write_text(
        render_seed_markdown(summary),
        encoding="utf-8",
    )
    print(json.dumps({"seed": seed_label, "decision": summary["decision"]}, ensure_ascii=False))


def write_combined() -> None:
    summary = summarize_combined()
    summary_dir = RUN_DIR / "summary"
    summary_dir.mkdir(parents=True, exist_ok=True)
    (summary_dir / "e3_s3_current_combined_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (summary_dir / "e3_s3_current_combined_summary.md").write_text(
        render_combined_markdown(summary),
        encoding="utf-8",
    )
    print(json.dumps({"combined_decision": summary["decision"]}, ensure_ascii=False))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", choices=("seed_c", "seed_d"))
    parser.add_argument("--combined", action="store_true")
    args = parser.parse_args()
    if not args.seed and not args.combined:
        raise SystemExit("provide --seed or --combined")
    if args.seed:
        write_seed(args.seed)
    if args.combined:
        write_combined()


if __name__ == "__main__":
    main()
