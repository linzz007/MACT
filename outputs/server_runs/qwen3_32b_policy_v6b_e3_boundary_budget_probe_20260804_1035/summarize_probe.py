#!/usr/bin/env python3
"""Summarize the E3 boundary max_replan=5 probe."""

from __future__ import annotations

import importlib.util
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from statistics import mean
from typing import Any
from zoneinfo import ZoneInfo


RUN_DIR = Path(__file__).resolve().parent
SOURCE_RUN = Path(
    "/home/ubuntu/lzz/MACT/outputs/server_runs/"
    "qwen3_32b_policy_v6b_multiseed_gate50_20260801_2231"
)
MYAGENT_ROOT = Path("/home/ubuntu/lzz/MyAgent")
EVALUATOR_PATH = MYAGENT_ROOT / "code" / "evaluate_results.py"
MACT_AVG_TOKENS = {
    "wtq": 10508.03,
    "tabfact": 10830.825,
    "crt": 12809.985,
}


def load_evaluator():
    spec = importlib.util.spec_from_file_location("myagent_evaluate_results", EVALUATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load evaluator: {EVALUATOR_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


EVAL = load_evaluator()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def row_tokens(row: dict[str, Any]) -> float:
    api = row.get("api_metrics") or {}
    if api.get("total_tokens") is not None:
        return float(api["total_tokens"])
    llm = row.get("llm_metrics") or {}
    return float(llm.get("total_tokens_est") or 0.0)


def row_elapsed(row: dict[str, Any]) -> float | None:
    value = row.get("elapsed_seconds_total")
    return float(value) if value is not None else None


def avg(values: list[float | int | None]) -> float:
    nums = [float(value) for value in values if value is not None]
    return mean(nums) if nums else 0.0


def source_merged_path(seed: str, dataset: str) -> Path:
    return SOURCE_RUN / "myagent_current" / seed / "merged" / f"{dataset}_qwen3-32b-local.jsonl"


def load_source_rows() -> dict[tuple[str, str, str], dict[str, Any]]:
    result: dict[tuple[str, str, str], dict[str, Any]] = {}
    for seed in ("seed_c", "seed_d"):
        for dataset in ("wtq", "tabfact", "crt"):
            for row in read_jsonl(source_merged_path(seed, dataset)):
                row_id = str(row.get("id") or "")
                result[(seed, dataset, row_id)] = row
    return result


def dataset_merged_path(dataset: str) -> Path:
    return RUN_DIR / "myagent_max_replan5" / "merged" / f"{dataset}_qwen3-32b-local.jsonl"


def dataset_eval_path(dataset: str) -> Path:
    return RUN_DIR / "myagent_max_replan5" / "eval" / f"{dataset}_qwen3-32b-local_eval.json"


def format_value(value: Any) -> str:
    if value is None:
        return ""
    text = json.dumps(value, ensure_ascii=False) if isinstance(value, (dict, list)) else str(value)
    return text.replace("\n", " ")


def build_summary() -> dict[str, Any]:
    source_rows = load_source_rows()
    input_manifest = read_json(RUN_DIR / "input" / "input_manifest.json")
    dataset_reports: dict[str, Any] = {}
    row_reports: list[dict[str, Any]] = []
    missing_outputs: list[str] = []

    for dataset in ("wtq", "tabfact", "crt"):
        merged_path = dataset_merged_path(dataset)
        eval_path = dataset_eval_path(dataset)
        input_rows = read_jsonl(RUN_DIR / "input" / f"{dataset}_e3_boundary_budget_probe.jsonl")
        if not merged_path.exists() or not eval_path.exists():
            missing_outputs.append(dataset)
            continue

        new_rows = read_jsonl(merged_path)
        new_by_id = {str(row.get("id") or ""): row for row in new_rows}
        eval_summary = read_json(eval_path)
        dataset_row_reports: list[dict[str, Any]] = []

        for input_row in input_rows:
            metadata = input_row.get("probe_metadata") or {}
            seed = str(metadata.get("source_seed") or "")
            row_id = str(metadata.get("source_id") or input_row.get("id") or "")
            category = str(metadata.get("boundary_category") or "")
            source_row = source_rows.get((seed, dataset, row_id))
            new_row = new_by_id.get(row_id)
            if source_row is None:
                raise RuntimeError(f"Missing source row for {seed}/{dataset}/{row_id}")
            if new_row is None:
                raise RuntimeError(f"Missing probe output row for {dataset}/{row_id}")

            original_correct = bool(EVAL.dataset_accuracy(source_row))
            replan5_correct = bool(EVAL.dataset_accuracy(new_row))
            report = {
                "seed": seed,
                "dataset": dataset,
                "id": row_id,
                "category": category,
                "original_correct": original_correct,
                "replan5_correct": replan5_correct,
                "recovered": (not original_correct) and replan5_correct,
                "original_prediction_for_em": EVAL.prediction_for_em(source_row),
                "replan5_prediction_for_em": EVAL.prediction_for_em(new_row),
                "gold_for_em": EVAL.gold_for_em(new_row),
                "original_total_tokens": row_tokens(source_row),
                "replan5_total_tokens": row_tokens(new_row),
                "token_delta": row_tokens(new_row) - row_tokens(source_row),
                "original_elapsed_seconds": row_elapsed(source_row),
                "replan5_elapsed_seconds": row_elapsed(new_row),
                "risk_level": new_row.get("risk_level")
                or (new_row.get("observability") or {}).get("risk_level"),
                "route_type": new_row.get("route_type"),
                "exec_error": bool(new_row.get("exec_error")),
                "missing_answer": EVAL.prediction_for_em(new_row) in (None, ""),
            }
            dataset_row_reports.append(report)
            row_reports.append(report)

        rows = len(dataset_row_reports)
        recovered = sum(1 for row in dataset_row_reports if row["recovered"])
        correct = sum(1 for row in dataset_row_reports if row["replan5_correct"])
        original_correct = sum(1 for row in dataset_row_reports if row["original_correct"])
        original_avg_tokens = avg([row["original_total_tokens"] for row in dataset_row_reports])
        replan5_avg_tokens = avg([row["replan5_total_tokens"] for row in dataset_row_reports])
        dataset_reports[dataset] = {
            "input_rows": len(input_rows),
            "merged_rows": len(new_rows),
            "eval_num_samples": eval_summary.get("num_samples"),
            "eval_primary_accuracy": eval_summary.get("primary_accuracy"),
            "original_correct": original_correct,
            "replan5_correct": correct,
            "recovered": recovered,
            "recovery_rate_from_original_wrong": recovered / (rows - original_correct)
            if rows > original_correct
            else 0.0,
            "num_failed_exec": eval_summary.get("num_failed_exec"),
            "num_missing_answer": eval_summary.get("num_missing_answer"),
            "original_avg_total_tokens": original_avg_tokens,
            "replan5_avg_total_tokens": replan5_avg_tokens,
            "replan5_token_ratio_to_mact_full200": replan5_avg_tokens / MACT_AVG_TOKENS[dataset],
            "token_delta_vs_original_avg": replan5_avg_tokens - original_avg_tokens,
            "token_delta_ratio_vs_original": replan5_avg_tokens / original_avg_tokens
            if original_avg_tokens
            else 0.0,
            "avg_elapsed_seconds": avg([row["replan5_elapsed_seconds"] for row in dataset_row_reports]),
            "row_ids": [row["id"] for row in dataset_row_reports],
        }

    total_rows = len(row_reports)
    total_recovered = sum(1 for row in row_reports if row["recovered"])
    total_original_correct = sum(1 for row in row_reports if row["original_correct"])
    total_replan5_correct = sum(1 for row in row_reports if row["replan5_correct"])
    failed = sum(1 for row in row_reports if row["exec_error"])
    missing = sum(1 for row in row_reports if row["missing_answer"])
    category_recovery = Counter()
    category_total = Counter()
    for row in row_reports:
        category_total[row["category"]] += 1
        if row["recovered"]:
            category_recovery[row["category"]] += 1

    if missing_outputs:
        decision = "incomplete_missing_outputs"
    elif total_recovered == 0:
        decision = "semantic_boundary_not_replan_budget"
    elif total_recovered <= max(1, total_rows // 4):
        decision = "mostly_semantic_boundary_with_limited_budget_sensitivity"
    elif total_recovered < max(1, total_rows // 2):
        decision = "mixed_budget_sensitivity_not_enough_for_e3_stability"
    else:
        decision = "budget_sensitive_boundary"

    return {
        "artifact": "e3_boundary_budget_probe_summary",
        "generated_at_local": datetime.now(ZoneInfo("Asia/Shanghai")).strftime("%Y-%m-%d %H:%M:%S CST"),
        "run_dir": str(RUN_DIR),
        "source_run": str(SOURCE_RUN),
        "myagent_root": str(MYAGENT_ROOT),
        "evaluator": str(EVALUATOR_PATH),
        "scope": "12 representative wrong rows from E3 Seed-C/D, rerun with max_replan=5.",
        "decision": decision,
        "input_manifest": input_manifest,
        "aggregate": {
            "rows": total_rows,
            "original_correct": total_original_correct,
            "replan5_correct": total_replan5_correct,
            "recovered": total_recovered,
            "recovery_rate_from_original_wrong": total_recovered / (total_rows - total_original_correct)
            if total_rows > total_original_correct
            else 0.0,
            "failed": failed,
            "missing": missing,
            "avg_original_total_tokens": avg([row["original_total_tokens"] for row in row_reports]),
            "avg_replan5_total_tokens": avg([row["replan5_total_tokens"] for row in row_reports]),
            "avg_replan5_elapsed_seconds": avg([row["replan5_elapsed_seconds"] for row in row_reports]),
            "missing_outputs": missing_outputs,
            "category_recovery": {
                category: {
                    "recovered": category_recovery[category],
                    "total": category_total[category],
                    "rate": category_recovery[category] / category_total[category],
                }
                for category in sorted(category_total)
            },
        },
        "datasets": dataset_reports,
        "rows": row_reports,
    }


def render_md(summary: dict[str, Any]) -> str:
    aggregate = summary["aggregate"]
    lines = [
        "# E3 Boundary Budget Probe Summary",
        "",
        f"Generated: `{summary['generated_at_local']}`",
        "",
        "## Decision",
        "",
        f"`{summary['decision']}`",
        "",
        "This probe reran representative E3 Seed-C/D wrong rows with `max_replan=5`; the original E3 runs used `max_replan=3`.",
        "",
        "## Aggregate",
        "",
        "| rows | original correct | max_replan=5 correct | recovered | recovery rate | failed | missing | avg original tokens | avg replan5 tokens | avg replan5 seconds |",
        "|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
        "| {rows} | {original_correct} | {replan5_correct} | {recovered} | {rate:.4f} | {failed} | {missing} | {orig_tokens:.1f} | {new_tokens:.1f} | {elapsed:.2f} |".format(
            rows=aggregate["rows"],
            original_correct=aggregate["original_correct"],
            replan5_correct=aggregate["replan5_correct"],
            recovered=aggregate["recovered"],
            rate=aggregate["recovery_rate_from_original_wrong"],
            failed=aggregate["failed"],
            missing=aggregate["missing"],
            orig_tokens=aggregate["avg_original_total_tokens"],
            new_tokens=aggregate["avg_replan5_total_tokens"],
            elapsed=aggregate["avg_replan5_elapsed_seconds"],
        ),
        "",
        "## Dataset Summary",
        "",
        "| dataset | rows | eval rows | max_replan=5 correct | recovered | failed | missing | avg original tokens | avg replan5 tokens | token ratio vs MACT full200 | avg seconds |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for dataset, report in summary["datasets"].items():
        lines.append(
            "| {dataset} | {rows} | {eval_rows} | {correct} | {recovered} | {failed} | {missing} | {orig_tokens:.1f} | {new_tokens:.1f} | {ratio:.4f} | {elapsed:.2f} |".format(
                dataset=dataset,
                rows=report["input_rows"],
                eval_rows=report["eval_num_samples"],
                correct=report["replan5_correct"],
                recovered=report["recovered"],
                failed=report["num_failed_exec"],
                missing=report["num_missing_answer"],
                orig_tokens=report["original_avg_total_tokens"],
                new_tokens=report["replan5_avg_total_tokens"],
                ratio=report["replan5_token_ratio_to_mact_full200"],
                elapsed=report["avg_elapsed_seconds"],
            )
        )

    lines.extend(
        [
            "",
            "## Category Recovery",
            "",
            "| category | recovered | total | rate |",
            "|---|---:|---:|---:|",
        ]
    )
    for category, report in aggregate["category_recovery"].items():
        lines.append(
            f"| {category} | {report['recovered']} | {report['total']} | {report['rate']:.4f} |"
        )

    lines.extend(
        [
            "",
            "## Row-Level Trace",
            "",
            "| seed | dataset | id | category | original pred | replan5 pred | gold | recovered | tokens 3->5 |",
            "|---|---|---|---|---|---|---|---|---:|",
        ]
    )
    for row in summary["rows"]:
        lines.append(
            "| {seed} | {dataset} | {id} | {category} | {orig_pred} | {new_pred} | {gold} | {recovered} | {orig_tokens:.0f}->{new_tokens:.0f} |".format(
                seed=row["seed"],
                dataset=row["dataset"],
                id=row["id"],
                category=row["category"],
                orig_pred=format_value(row["original_prediction_for_em"]),
                new_pred=format_value(row["replan5_prediction_for_em"]),
                gold=format_value(row["gold_for_em"]),
                recovered="yes" if row["recovered"] else "no",
                orig_tokens=row["original_total_tokens"],
                new_tokens=row["replan5_total_tokens"],
            )
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- Recovery below a majority should not be treated as E3 stability closure; it is mechanism evidence for adaptive budgeting plus remaining semantic boundaries.",
            "- Categories with zero recovery should stay on the semantic guard backlog rather than receive more blanket replan budget.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    summary = build_summary()
    out_json = RUN_DIR / "summary" / "e3_boundary_budget_probe_summary.json"
    out_md = RUN_DIR / "summary" / "e3_boundary_budget_probe_summary.md"
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    out_md.write_text(render_md(summary), encoding="utf-8")
    print(json.dumps(summary["aggregate"], ensure_ascii=False, indent=2))
    print(out_md)


if __name__ == "__main__":
    main()
