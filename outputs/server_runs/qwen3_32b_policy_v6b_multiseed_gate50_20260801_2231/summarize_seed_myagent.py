#!/usr/bin/env python3
"""Summarize one MyAgent E3 Gate-50 seed before running MACT baseline."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


RUN_DIR = Path(__file__).resolve().parent
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


def correct_count(evaluation: dict[str, Any]) -> int:
    rows = int(evaluation.get("num_with_gold") or evaluation.get("num_samples") or 0)
    return int(round(float(evaluation.get("primary_accuracy") or 0.0) * rows))


def summarize(seed_label: str) -> dict[str, Any]:
    datasets: dict[str, Any] = {}
    overall_correct = 0
    overall_rows = 0
    token_num = 0.0
    token_den = 0.0
    elapsed_num = 0.0

    for task in TASKS:
        input_path = RUN_DIR / "input" / seed_label / f"{task}_{seed_label}_gate50.jsonl"
        merged_path = RUN_DIR / "myagent_current" / seed_label / "merged" / f"{task}_{MODEL}.jsonl"
        eval_path = RUN_DIR / "myagent_current" / seed_label / "eval" / f"{task}_{MODEL}_eval.json"
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
                    "passed_current_seed_gate": all(
                        [
                            item["input_rows"] == 50,
                            item["merged_rows"] == 50,
                            int(ev.get("num_samples") or 0) == 50,
                            failed == 0,
                            missing == 0,
                            token_ratio is not None and token_ratio < 1.0,
                            correct >= THRESHOLDS[task],
                        ]
                    ),
                }
            )
            overall_correct += correct
            overall_rows += rows
            token_num += avg_tokens * rows
            token_den += MACT_AVG[task] * rows
            elapsed_num += avg_elapsed * rows
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
                }
            )
        datasets[task] = item

    return {
        "run_dir": str(RUN_DIR),
        "seed_label": seed_label,
        "stage": "E3 MyAgent current-only Gate-50",
        "model": MODEL,
        "datasets": datasets,
        "overall": {
            "correct": overall_correct,
            "rows": overall_rows,
            "accuracy": overall_correct / overall_rows if overall_rows else 0.0,
            "avg_total_tokens_weighted": token_num / overall_rows if overall_rows else 0.0,
            "token_ratio_to_mact_full200_weighted": token_num / token_den if token_den else None,
            "avg_elapsed_seconds_weighted": elapsed_num / overall_rows if overall_rows else 0.0,
        },
        "decision": "run_paired_mact" if all(datasets[task]["passed_current_seed_gate"] for task in TASKS) else "stop_or_inspect",
    }


def render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        f"# E3 MyAgent Gate-50 Summary: {summary['seed_label']}",
        "",
        f"Run dir: `{RUN_DIR}`",
        "",
        "| Dataset | Rows input/merged/eval | Correct | Accuracy | Token Ratio vs MACT full200 | Avg Tokens | Avg Elapsed s | Failed | Missing | Gate |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for task in TASKS:
        item = summary["datasets"][task]
        ratio = item.get("token_ratio_to_mact_full200")
        ratio_text = f"{ratio:.4f}" if ratio is not None else "n/a"
        lines.append(
            f"| {task} | {item['input_rows']}/{item['merged_rows']}/{item['eval_rows']} | "
            f"{item['correct']}/50 | {item['accuracy']:.4f} | {ratio_text} | "
            f"{item['avg_total_tokens']:.1f} | {item['avg_elapsed_seconds']:.2f} | "
            f"{item['num_failed_exec']} | {item['num_missing_answer']} | "
            f"{'pass' if item['passed_current_seed_gate'] else 'inspect'} |"
        )
    overall = summary["overall"]
    ratio = overall.get("token_ratio_to_mact_full200_weighted")
    lines.extend(
        [
            "",
            f"Overall: MyAgent `{overall['correct']}/{overall['rows']}`, token ratio vs MACT full200 `{ratio:.4f}`." if ratio is not None else f"Overall: MyAgent `{overall['correct']}/{overall['rows']}`, token ratio vs MACT full200 `n/a`.",
            f"Decision: `{summary['decision']}`.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(f"usage: {Path(sys.argv[0]).name} <seed_c|seed_d>")
    seed_label = sys.argv[1]
    if seed_label not in {"seed_c", "seed_d"}:
        raise SystemExit("seed label must be seed_c or seed_d")
    summary = summarize(seed_label)
    summary_dir = RUN_DIR / "summary"
    summary_dir.mkdir(parents=True, exist_ok=True)
    json_path = summary_dir / f"{seed_label}_myagent_gate50_summary.json"
    md_path = summary_dir / f"{seed_label}_myagent_gate50_summary.md"
    json_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(summary), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
