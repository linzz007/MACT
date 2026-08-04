#!/usr/bin/env python3
"""Summarize E3 S2 guard-validation current-policy baseline."""

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
INPUT_RUN = Path(
    "/home/ubuntu/lzz/MACT/outputs/server_runs/"
    "qwen3_32b_policy_v6b_e3_guard_validation_inputs_20260804_1128"
)
MYAGENT_ROOT = Path("/home/ubuntu/lzz/MyAgent")
EVALUATOR_PATH = MYAGENT_ROOT / "code" / "evaluate_results.py"
OUTPUT_ROOT = RUN_DIR / "myagent_current_baseline"
SUMMARY_DIR = RUN_DIR / "summary"
TASKS = ("wtq", "tabfact", "crt")
MACT_AVG_TOKENS = {
    "wtq": 10508.03,
    "tabfact": 10830.825,
    "crt": 12809.985,
}
REPRESENTATIVE_RECOVERY_MIN = 7
NO_HARM_CORRECT_MIN = 18


def load_evaluator():
    spec = importlib.util.spec_from_file_location("myagent_evaluate_results", EVALUATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load evaluator: {EVALUATOR_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


EVAL = load_evaluator()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def row_id(row: dict[str, Any]) -> str:
    return str(row.get("id") or row.get("example_id") or row.get("table_id") or "")


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


def prediction(row: dict[str, Any]) -> Any:
    return EVAL.prediction_for_em(row)


def gold(row: dict[str, Any]) -> Any:
    return EVAL.gold_for_em(row)


def input_path(dataset: str) -> Path:
    return INPUT_RUN / "input" / f"{dataset}_e3_guard_validation.jsonl"


def merged_path(dataset: str) -> Path:
    return OUTPUT_ROOT / "merged" / f"{dataset}_qwen3-32b-local.jsonl"


def eval_path(dataset: str) -> Path:
    return OUTPUT_ROOT / "eval" / f"{dataset}_qwen3-32b-local_eval.json"


def build_summary() -> dict[str, Any]:
    source_manifest = read_json(INPUT_RUN / "summary" / "e3_guard_validation_input_plan.json")
    datasets: dict[str, Any] = {}
    rows: list[dict[str, Any]] = []
    missing_outputs: list[str] = []

    for dataset in TASKS:
        in_rows = read_jsonl(input_path(dataset))
        if not merged_path(dataset).exists() or not eval_path(dataset).exists():
            missing_outputs.append(dataset)
            continue
        merged_rows = read_jsonl(merged_path(dataset))
        merged_by_id = {row_id(row): row for row in merged_rows}
        eval_summary = read_json(eval_path(dataset))
        dataset_rows: list[dict[str, Any]] = []
        missing_ids: list[str] = []

        for input_row in in_rows:
            meta = input_row["validation_metadata"]
            rid = str(meta["source_id"])
            output_row = merged_by_id.get(rid)
            if output_row is None:
                missing_ids.append(rid)
                continue
            correct = bool(EVAL.dataset_accuracy(output_row))
            slice_role = str(meta["slice_role"])
            report = {
                "source_key": meta["source_key"],
                "dataset": dataset,
                "id": rid,
                "slice_role": slice_role,
                "category": meta["boundary_category"],
                "priority": meta["priority"],
                "source_correct": bool(meta["source_correct"]),
                "baseline_correct": correct,
                "representative_recovered": slice_role == "representative_wrong" and correct,
                "no_harm_retained": slice_role == "no_harm_correct" and correct,
                "prediction_for_em": prediction(output_row),
                "gold_for_em": gold(output_row),
                "source_prediction_for_em": meta.get("original_prediction_for_em"),
                "source_gold_for_em": meta.get("gold_for_em"),
                "max_replan5_recovered": meta.get("max_replan5_recovered"),
                "no_harm_proxy_for": meta.get("no_harm_proxy_for"),
                "total_tokens": row_tokens(output_row),
                "elapsed_seconds_total": row_elapsed(output_row),
                "risk_level": output_row.get("risk_level")
                or (output_row.get("observability") or {}).get("risk_level"),
                "route_type": output_row.get("route_type"),
                "exec_error": bool(output_row.get("exec_error")),
                "missing_answer": prediction(output_row) in (None, ""),
            }
            rows.append(report)
            dataset_rows.append(report)

        role_counts = Counter(row["slice_role"] for row in dataset_rows)
        correct_by_role = Counter()
        for row in dataset_rows:
            if row["baseline_correct"]:
                correct_by_role[row["slice_role"]] += 1
        datasets[dataset] = {
            "input_rows": len(in_rows),
            "merged_rows": len(merged_rows),
            "eval_num_samples": eval_summary.get("num_samples"),
            "eval_primary_accuracy": eval_summary.get("primary_accuracy"),
            "role_counts": dict(role_counts),
            "correct_by_role": dict(correct_by_role),
            "representative_recovered": sum(1 for row in dataset_rows if row["representative_recovered"]),
            "representative_total": role_counts.get("representative_wrong", 0),
            "no_harm_correct": sum(1 for row in dataset_rows if row["no_harm_retained"]),
            "no_harm_total": role_counts.get("no_harm_correct", 0),
            "num_failed_exec": eval_summary.get("num_failed_exec"),
            "num_missing_answer": eval_summary.get("num_missing_answer"),
            "avg_total_tokens": avg([row["total_tokens"] for row in dataset_rows]),
            "token_ratio_to_mact_full200": avg([row["total_tokens"] for row in dataset_rows])
            / MACT_AVG_TOKENS[dataset],
            "avg_elapsed_seconds": avg([row["elapsed_seconds_total"] for row in dataset_rows]),
            "missing_output_ids": missing_ids,
        }

    role_counts = Counter(row["slice_role"] for row in rows)
    category_counts = Counter(row["category"] for row in rows)
    category_correct = Counter()
    category_recovered = Counter()
    category_no_harm_retained = Counter()
    for row in rows:
        if row["baseline_correct"]:
            category_correct[row["category"]] += 1
        if row["representative_recovered"]:
            category_recovered[row["category"]] += 1
        if row["no_harm_retained"]:
            category_no_harm_retained[row["category"]] += 1

    representative_recovered = sum(1 for row in rows if row["representative_recovered"])
    no_harm_correct = sum(1 for row in rows if row["no_harm_retained"])
    failed = sum(1 for row in rows if row["exec_error"])
    missing = sum(1 for row in rows if row["missing_answer"])
    weighted_mact_tokens = sum(MACT_AVG_TOKENS[row["dataset"]] for row in rows)
    total_tokens = sum(row["total_tokens"] for row in rows)
    token_ratio = total_tokens / weighted_mact_tokens if weighted_mact_tokens else 0.0

    if missing_outputs:
        decision = "incomplete_missing_outputs"
    elif (
        representative_recovered >= REPRESENTATIVE_RECOVERY_MIN
        and no_harm_correct >= NO_HARM_CORRECT_MIN
        and failed == 0
        and missing == 0
        and token_ratio < 1.0
    ):
        decision = "baseline_passes_s2_gate_without_new_guard"
    else:
        decision = "baseline_needs_guard_implementation"

    return {
        "artifact_name": "e3_guard_validation_current_baseline_summary",
        "generated_at_local": datetime.now(ZoneInfo("Asia/Shanghai")).strftime("%Y-%m-%d %H:%M:%S CST"),
        "run_dir": str(RUN_DIR),
        "input_run": str(INPUT_RUN),
        "myagent_root": str(MYAGENT_ROOT),
        "scope": "Fresh current-policy baseline on the 30-row E3 S2 guard-validation input package. No MyAgent policy changes are introduced by this artifact.",
        "decision": decision,
        "source_input_plan": {
            "total_rows": source_manifest["total_rows"],
            "role_counts": source_manifest["role_counts"],
            "dataset_counts": source_manifest["dataset_counts"],
            "gate_targets": source_manifest["gate_targets"],
        },
        "aggregate": {
            "rows": len(rows),
            "expected_rows": source_manifest["total_rows"],
            "representative_recovered": representative_recovered,
            "representative_total": role_counts.get("representative_wrong", 0),
            "no_harm_correct": no_harm_correct,
            "no_harm_total": role_counts.get("no_harm_correct", 0),
            "failed": failed,
            "missing": missing,
            "avg_total_tokens": avg([row["total_tokens"] for row in rows]),
            "avg_elapsed_seconds": avg([row["elapsed_seconds_total"] for row in rows]),
            "token_ratio_to_mact_full200_weighted": token_ratio,
            "missing_outputs": missing_outputs,
        },
        "datasets": datasets,
        "category_results": {
            category: {
                "rows": category_counts[category],
                "correct": category_correct[category],
                "representative_recovered": category_recovered[category],
                "no_harm_retained": category_no_harm_retained[category],
            }
            for category in sorted(category_counts)
        },
        "rows": rows,
    }


def render_markdown(summary: dict[str, Any]) -> str:
    aggregate = summary["aggregate"]
    lines = [
        "# E3 Guard Validation Current Baseline Summary",
        "",
        f"Generated: `{summary['generated_at_local']}`",
        "",
        f"Decision: `{summary['decision']}`",
        "",
        summary["scope"],
        "",
        "## Aggregate",
        "",
        "| metric | value |",
        "| --- | ---: |",
        f"| rows | {aggregate['rows']}/{aggregate['expected_rows']} |",
        f"| representative recovered | {aggregate['representative_recovered']}/{aggregate['representative_total']} |",
        f"| no-harm correct | {aggregate['no_harm_correct']}/{aggregate['no_harm_total']} |",
        f"| failed/missing | {aggregate['failed']}/{aggregate['missing']} |",
        f"| avg total tokens | {aggregate['avg_total_tokens']:.2f} |",
        f"| weighted token ratio vs MACT full200 | {aggregate['token_ratio_to_mact_full200_weighted']:.4f} |",
        f"| avg elapsed seconds | {aggregate['avg_elapsed_seconds']:.2f} |",
        "",
        "## Dataset Results",
        "",
        "| dataset | rows | representative recovered | no-harm correct | failed/missing | token ratio | avg tokens | avg seconds |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for dataset, item in summary["datasets"].items():
        lines.append(
            "| {dataset} | {input_rows}/{merged_rows}/{eval_rows} | {rep}/{rep_total} | {nh}/{nh_total} | {failed}/{missing} | {ratio:.4f} | {tokens:.2f} | {elapsed:.2f} |".format(
                dataset=dataset,
                input_rows=item["input_rows"],
                merged_rows=item["merged_rows"],
                eval_rows=item["eval_num_samples"],
                rep=item["representative_recovered"],
                rep_total=item["representative_total"],
                nh=item["no_harm_correct"],
                nh_total=item["no_harm_total"],
                failed=item["num_failed_exec"],
                missing=item["num_missing_answer"],
                ratio=item["token_ratio_to_mact_full200"],
                tokens=item["avg_total_tokens"],
                elapsed=item["avg_elapsed_seconds"],
            )
        )
    lines.extend(
        [
            "",
            "## Category Results",
            "",
            "| category | rows | correct | representative recovered | no-harm retained |",
            "| --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for category, item in summary["category_results"].items():
        lines.append(
            f"| {category} | {item['rows']} | {item['correct']} | {item['representative_recovered']} | {item['no_harm_retained']} |"
        )
    lines.extend(
        [
            "",
            "## Wrong Or Harm Rows",
            "",
            "| source_key | role | category | prediction | gold |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for row in summary["rows"]:
        if row["baseline_correct"]:
            continue
        lines.append(
            "| {source_key} | {role} | {category} | `{pred}` | `{gold}` |".format(
                source_key=row["source_key"],
                role=row["slice_role"],
                category=row["category"],
                pred=str(row["prediction_for_em"]).replace("|", "\\|"),
                gold=str(row["gold_for_em"]).replace("|", "\\|"),
            )
        )
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    summary = build_summary()
    write_json(SUMMARY_DIR / "e3_guard_validation_current_baseline_summary.json", summary)
    (SUMMARY_DIR / "e3_guard_validation_current_baseline_summary.md").write_text(
        render_markdown(summary),
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
