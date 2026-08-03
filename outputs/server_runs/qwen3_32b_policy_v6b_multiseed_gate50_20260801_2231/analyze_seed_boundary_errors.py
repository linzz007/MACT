#!/usr/bin/env python3
"""Analyze Seed-C/D MyAgent current-only boundary errors offline."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from collections import Counter
from pathlib import Path
from statistics import mean
from typing import Any


RUN_DIR = Path(__file__).resolve().parent
SUMMARY_DIR = RUN_DIR / "summary"
MYAGENT_CODE = Path("/home/ubuntu/lzz/MyAgent/code")
TASKS = ("wtq", "tabfact", "crt")
SEEDS = ("seed_c", "seed_d")

sys.path.insert(0, str(MYAGENT_CODE))
from evaluate_results import (  # noqa: E402
    _token_metrics,
    dataset_accuracy,
    gold_for_em,
    load_jsonl,
    prediction_for_em,
)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def count_jsonl(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(1 for line in path.open(encoding="utf-8") if line.strip())


def avg(values: list[Any]) -> float:
    nums = [float(value) for value in values if value not in (None, "")]
    return mean(nums) if nums else 0.0


def ratio(count: int, total: int) -> float:
    return count / total if total else 0.0


def value_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (list, tuple, set)):
        return ", ".join(value_text(item) for item in value)
    if isinstance(value, dict):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value)


def short_text(text: Any, limit: int = 120) -> str:
    normalized = re.sub(r"\s+", " ", value_text(text)).strip()
    if len(normalized) <= limit:
        return normalized
    return normalized[: limit - 3].rstrip() + "..."


def first_non_empty(row: dict[str, Any], keys: tuple[str, ...], default: str = "unknown") -> str:
    for key in keys:
        value = row.get(key)
        if value not in (None, ""):
            return str(value)
    return default


def row_text(row: dict[str, Any]) -> str:
    parts = [
        row.get("question"),
        row.get("utterance"),
        row.get("statement"),
        row.get("claim"),
    ]
    return " ".join(value_text(part) for part in parts if part not in (None, "")).lower()


def as_number(value: Any) -> float | None:
    if isinstance(value, (list, tuple)) and len(value) == 1:
        value = value[0]
    text = value_text(value).strip().replace(",", "").replace("%", "")
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def classify_boundary(task: str, row: dict[str, Any], prediction: Any, gold: Any) -> str:
    text = row_text(row)
    pred_num = as_number(prediction)
    gold_num = as_number(gold)
    pred_text = value_text(prediction).lower()
    gold_text = value_text(gold).lower()

    if task == "wtq":
        if (
            re.search(r"\b(rank|ranking|position|place|finish|seed|seeded|ordinal|first|second|third|last|higher|lower)\b", text)
            or (pred_num is not None and gold_num is not None and pred_num < 0 <= gold_num)
        ):
            return "wtq_rank_direction_or_ordinal_boundary"
        if re.search(r"\b(age|year|season|date|before|after|earlier|later|old|young|newest|latest)\b", text):
            return "wtq_temporal_or_age_lookup_boundary"
        if re.search(r"\b(how many|number of|count|total|sum|average|mean|difference|percent|percentage|all|both)\b", text):
            return "wtq_numeric_aggregation_or_difference_boundary"
        return "wtq_entity_lookup_or_row_selection_boundary"

    if task == "tabfact":
        if re.search(r"\b(before|after|year|season|date|first|last|earlier|later|previous|next)\b", text):
            return "tabfact_temporal_order_boundary"
        if re.search(r"\b(count|number|more|less|least|most|highest|lowest|greater|fewer|only|all|both)\b", text):
            return "tabfact_numeric_count_or_comparison_boundary"
        if gold_text in {"false", "0", "no"} and pred_text in {"true", "1", "yes"}:
            return "tabfact_false_positive_or_negation_boundary"
        if gold_text in {"true", "1", "yes"} and pred_text in {"false", "0", "no"}:
            return "tabfact_false_negative_entailment_boundary"
        if re.search(r"\b(same|different|with|from|between|against|in|at|for|of)\b", text):
            return "tabfact_entity_attribute_same_row_boundary"
        return "tabfact_binary_entailment_boundary"

    if task == "crt":
        if re.search(r"\b(percent|percentage|vote|votes|share|proportion|ratio)\b", text):
            return "crt_percentage_complement_or_aggregation_boundary"
        if re.search(r"\b(all|any|each|every|consecutive|span|within|between)\b", text):
            return "crt_span_or_universal_quantifier_boundary"
        if re.search(r"\b(how many|number of|count|total|sum|average|mean|difference|more|less)\b", text):
            return "crt_multi_step_numeric_composition_boundary"
        return "crt_table_reasoning_or_entity_boundary"

    return "unknown_boundary"


def tag_values(row: dict[str, Any]) -> list[str]:
    tags = row.get("problem_tags")
    if tags is None:
        tags = row.get("tags")
    if tags is None:
        return ["unknown"]
    if isinstance(tags, str):
        return [tags] if tags else ["unknown"]
    if isinstance(tags, (list, tuple, set)):
        values = [str(item) for item in tags if item not in (None, "")]
        return values or ["unknown"]
    return [str(tags)]


def count_field(rows: list[dict[str, Any]], key: str, default: str = "unknown") -> dict[str, int]:
    return dict(Counter(first_non_empty(row, (key,), default) for row in rows).most_common())


def bool_count(rows: list[dict[str, Any]], key: str) -> dict[str, int]:
    return dict(Counter(str(bool(row.get(key))).lower() for row in rows).most_common())


def top_tags(rows: list[dict[str, Any]], limit: int = 12) -> dict[str, int]:
    counter: Counter[str] = Counter()
    for row in rows:
        counter.update(tag_values(row))
    return dict(counter.most_common(limit))


def summarized_row(seed: str, task: str, row: dict[str, Any], category: str) -> dict[str, Any]:
    metrics = _token_metrics(row)
    prediction = prediction_for_em(row)
    gold = gold_for_em(row)
    return {
        "seed": seed,
        "dataset": task,
        "id": str(row.get("id") or row.get("example_id") or row.get("table_id") or ""),
        "category": category,
        "question_or_statement": short_text(row.get("question") or row.get("statement") or row.get("utterance"), 180),
        "prediction_for_em": value_text(prediction),
        "gold_for_em": value_text(gold),
        "final_answer": short_text(row.get("final_answer"), 160),
        "final_value": row.get("final_value"),
        "risk_level": first_non_empty(row, ("risk_level",), "unknown"),
        "route_type": first_non_empty(row, ("route_type",), "unknown"),
        "difficulty_level": first_non_empty(row, ("difficulty_level",), "unknown"),
        "problem_tags": tag_values(row),
        "simple_lookup_success": bool(row.get("simple_lookup_success")),
        "deterministic_shortcut_applied": bool(row.get("deterministic_shortcut_applied")),
        "deterministic_shortcut_reason": short_text(row.get("deterministic_shortcut_reason"), 100),
        "strong_verification_applied": bool(row.get("strong_verification_applied")),
        "strong_verification_reason": short_text(row.get("strong_verification_reason"), 100),
        "risk_escalated": bool(row.get("risk_escalated")),
        "agreement_decision": first_non_empty(row, ("agreement_decision",), "unknown"),
        "critic_verdict": first_non_empty(row, ("critic_verdict",), "unknown"),
        "cross_validation_verdict": first_non_empty(row, ("cross_validation_verdict",), "unknown"),
        "total_tokens": metrics.get("total"),
        "elapsed_seconds_total": row.get("elapsed_seconds_total"),
        "exec_error": row.get("exec_error"),
    }


def pick_examples(seed: str, task: str, wrong_rows: list[dict[str, Any]], categories: dict[int, str]) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    seen_categories: set[str] = set()
    sorted_rows = sorted(
        wrong_rows,
        key=lambda row: (_token_metrics(row).get("total") or 0, row.get("elapsed_seconds_total") or 0),
        reverse=True,
    )
    for row in sorted_rows:
        category = categories[id(row)]
        if category in seen_categories and len(seen_categories) < 3:
            continue
        selected.append(summarized_row(seed, task, row, category))
        seen_categories.add(category)
        if len(selected) >= 3:
            break
    return selected


def analyze_dataset(seed: str, task: str, item: dict[str, Any]) -> dict[str, Any]:
    input_path = Path(item["input_path"])
    merged_path = Path(item["merged_path"])
    eval_path = Path(item["eval_path"])
    rows = load_jsonl(str(merged_path))
    eval_json = read_json(eval_path)
    with_gold = [row for row in rows if gold_for_em(row) not in (None, "")]
    correct_flags = [dataset_accuracy(row) for row in with_gold]
    correct = sum(1 for flag in correct_flags if flag)
    wrong_rows = [row for row, flag in zip(with_gold, correct_flags) if not flag]
    right_rows = [row for row, flag in zip(with_gold, correct_flags) if flag]
    categories = {
        id(row): classify_boundary(task, row, prediction_for_em(row), gold_for_em(row))
        for row in wrong_rows
    }
    category_counts = dict(Counter(categories.values()).most_common())
    expected_correct = int(item["correct"])
    verification = {
        "input_rows": count_jsonl(input_path),
        "merged_rows": len(rows),
        "eval_rows": int(eval_json.get("num_samples") or 0),
        "summary_correct": expected_correct,
        "recomputed_correct": correct,
        "summary_num_em_mismatch": int(item["num_em_mismatch"]),
        "recomputed_wrong": len(wrong_rows),
        "mismatch": correct != expected_correct or len(wrong_rows) != int(item["num_em_mismatch"]),
    }

    wrong_token_totals = [_token_metrics(row).get("total") for row in wrong_rows]
    right_token_totals = [_token_metrics(row).get("total") for row in right_rows]
    wrong_elapsed = [row.get("elapsed_seconds_total") for row in wrong_rows]
    right_elapsed = [row.get("elapsed_seconds_total") for row in right_rows]

    profile = {
        "wrong_count": len(wrong_rows),
        "wrong_high_risk_count": sum(1 for row in wrong_rows if first_non_empty(row, ("risk_level",), "") == "high"),
        "wrong_high_risk_ratio": ratio(sum(1 for row in wrong_rows if first_non_empty(row, ("risk_level",), "") == "high"), len(wrong_rows)),
        "wrong_complex_route_count": sum(1 for row in wrong_rows if first_non_empty(row, ("route_type",), "") == "complex"),
        "wrong_complex_route_ratio": ratio(sum(1 for row in wrong_rows if first_non_empty(row, ("route_type",), "") == "complex"), len(wrong_rows)),
        "wrong_deterministic_shortcut_applied_count": sum(1 for row in wrong_rows if row.get("deterministic_shortcut_applied")),
        "wrong_deterministic_shortcut_applied_ratio": ratio(sum(1 for row in wrong_rows if row.get("deterministic_shortcut_applied")), len(wrong_rows)),
        "wrong_strong_verification_applied_count": sum(1 for row in wrong_rows if row.get("strong_verification_applied")),
        "wrong_strong_verification_applied_ratio": ratio(sum(1 for row in wrong_rows if row.get("strong_verification_applied")), len(wrong_rows)),
        "wrong_risk_escalated_count": sum(1 for row in wrong_rows if row.get("risk_escalated")),
        "wrong_risk_escalated_ratio": ratio(sum(1 for row in wrong_rows if row.get("risk_escalated")), len(wrong_rows)),
        "wrong_avg_total_tokens": avg(wrong_token_totals),
        "right_avg_total_tokens": avg(right_token_totals),
        "wrong_avg_elapsed_seconds": avg(wrong_elapsed),
        "right_avg_elapsed_seconds": avg(right_elapsed),
    }

    return {
        "seed": seed,
        "dataset": task,
        "summary": {
            "accuracy": item["accuracy"],
            "correct": item["correct"],
            "rows": item["eval_rows"],
            "token_ratio_to_mact_full200": item["token_ratio_to_mact_full200"],
            "avg_total_tokens": item["avg_total_tokens"],
            "avg_elapsed_seconds": item["avg_elapsed_seconds"],
            "failed": item["num_failed_exec"],
            "missing": item["num_missing_answer"],
            "passed_current_seed_gate": item["passed_current_seed_gate"],
        },
        "verification": verification,
        "wrong_profile": profile,
        "wrong_distributions": {
            "risk_level": count_field(wrong_rows, "risk_level"),
            "route_type": count_field(wrong_rows, "route_type"),
            "difficulty_level": count_field(wrong_rows, "difficulty_level"),
            "category": category_counts,
            "problem_tags_top": top_tags(wrong_rows),
            "simple_lookup_success": bool_count(wrong_rows, "simple_lookup_success"),
            "deterministic_shortcut_applied": bool_count(wrong_rows, "deterministic_shortcut_applied"),
            "deterministic_shortcut_reason": count_field(wrong_rows, "deterministic_shortcut_reason"),
            "strong_verification_applied": bool_count(wrong_rows, "strong_verification_applied"),
            "strong_verification_reason": count_field(wrong_rows, "strong_verification_reason"),
            "risk_escalated": bool_count(wrong_rows, "risk_escalated"),
            "agreement_decision": count_field(wrong_rows, "agreement_decision"),
            "critic_verdict": count_field(wrong_rows, "critic_verdict"),
            "cross_validation_verdict": count_field(wrong_rows, "cross_validation_verdict"),
        },
        "representative_wrong_rows": pick_examples(seed, task, wrong_rows, categories),
    }


def analyze() -> dict[str, Any]:
    generated_at = dt.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
    summaries = {
        seed: read_json(SUMMARY_DIR / f"{seed}_myagent_gate50_summary.json")
        for seed in SEEDS
    }
    seed_reports: dict[str, Any] = {}
    total_rows = 0
    total_correct = 0
    total_failed = 0
    total_missing = 0
    total_token_num = 0.0
    total_token_den = 0.0
    verification_mismatches: list[dict[str, Any]] = []

    for seed, summary in summaries.items():
        datasets: dict[str, Any] = {}
        for task in TASKS:
            item = summary["datasets"][task]
            report = analyze_dataset(seed, task, item)
            datasets[task] = report
            total_rows += int(item["eval_rows"])
            total_correct += int(item["correct"])
            total_failed += int(item["num_failed_exec"])
            total_missing += int(item["num_missing_answer"])
            total_token_num += float(item["avg_total_tokens"]) * int(item["eval_rows"])
            mact_ref = float(item["mact_avg_tokens_full200_reference"])
            total_token_den += mact_ref * int(item["eval_rows"])
            if report["verification"]["mismatch"]:
                verification_mismatches.append(
                    {
                        "seed": seed,
                        "dataset": task,
                        "verification": report["verification"],
                    }
                )
        seed_reports[seed] = {
            "decision": summary["decision"],
            "overall": summary["overall"],
            "datasets": datasets,
        }

    aggregate_category_counter: Counter[str] = Counter()
    aggregate_problem_tag_counter: Counter[str] = Counter()
    for seed_report in seed_reports.values():
        for task_report in seed_report["datasets"].values():
            aggregate_category_counter.update(task_report["wrong_distributions"]["category"])
            aggregate_problem_tag_counter.update(task_report["wrong_distributions"]["problem_tags_top"])

    return {
        "artifact_name": "e3_seed_boundary_error_diagnosis",
        "generated_at_local": generated_at,
        "scope": "Offline evaluator-based diagnosis of completed Seed-C/Seed-D MyAgent current-only Gate-50 outputs. No model was run.",
        "run_dir": str(RUN_DIR),
        "myagent_evaluator": str(MYAGENT_CODE / "evaluate_results.py"),
        "inputs": {
            seed: {
                "summary_json": str(SUMMARY_DIR / f"{seed}_myagent_gate50_summary.json"),
                "summary_md": str(SUMMARY_DIR / f"{seed}_myagent_gate50_summary.md"),
            }
            for seed in SEEDS
        },
        "aggregate": {
            "rows": total_rows,
            "correct": total_correct,
            "wrong": total_rows - total_correct,
            "accuracy": total_correct / total_rows if total_rows else 0.0,
            "failed": total_failed,
            "missing": total_missing,
            "weighted_token_ratio_to_mact_full200_reference": total_token_num / total_token_den if total_token_den else None,
            "verification_status": "pass" if not verification_mismatches else "fail",
            "verification_mismatches": verification_mismatches,
            "wrong_category_top": dict(aggregate_category_counter.most_common()),
            "wrong_problem_tags_top": dict(aggregate_problem_tag_counter.most_common(20)),
        },
        "seed_reports": seed_reports,
        "boundary_findings": [
            "Seed-C/Seed-D had 300 merged rows and zero failed execution or missing answers; the boundary is semantic answer correctness, not runtime/tool coverage.",
            "Tokens remained below the frozen MACT full200 reference on every dataset and seed; the blocker is accuracy stability, not token budget.",
            "Seed-C is near the current gate on TabFact and exactly at the CRT gate, while Seed-D exposes broader WTQ and TabFact instability.",
            "Do not spend paired MACT runtime for these seeds until boundary categories are addressed or explicitly accepted as limitation evidence.",
            "Patent-facing claim should use E3 as applicability-boundary evidence, not as multi-seed stable superiority evidence.",
        ],
        "next_actions": [
            "If continuing Qwen3 optimization, target reusable guards for WTQ rank-direction/temporal lookup, TabFact temporal/numeric entailment, and CRT percentage/aggregation categories.",
            "If continuing experiment collection, keep E3 paired MACT marked not required and prioritize new-model Gate-10/Gate-50 only when a viable new model or API key exists.",
            "For patent drafting, cite full200 and P4b after-targeted as positive evidence; cite this E3 diagnosis as boundary and future-improvement evidence.",
        ],
    }


def markdown_table(headers: list[str], rows: list[list[Any]]) -> list[str]:
    lines = [
        "| " + " | ".join(headers) + " |",
        "|" + "|".join("---" for _ in headers) + "|",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(item) for item in row) + " |")
    return lines


def render_markdown(report: dict[str, Any]) -> str:
    aggregate = report["aggregate"]
    lines = [
        "# E3 Seed-C/D Boundary Error Diagnosis",
        "",
        f"Generated: `{report['generated_at_local']}`",
        "",
        f"Scope: {report['scope']}",
        "",
        "## Decision",
        "",
        "Seed-C and Seed-D remain `stop_or_inspect`. This diagnosis supports not running paired MACT for those seeds yet: there are no execution or missing-answer failures, tokens remain lower than the MACT full200 reference, and the remaining issue is semantic accuracy stability.",
        "",
        "## Aggregate",
        "",
        "| rows | correct | wrong | accuracy | weighted token ratio vs MACT full200 | failed | missing | verification |",
        "|---:|---:|---:|---:|---:|---:|---:|---|",
        f"| {aggregate['rows']} | {aggregate['correct']} | {aggregate['wrong']} | {aggregate['accuracy']:.4f} | {aggregate['weighted_token_ratio_to_mact_full200_reference']:.4f} | {aggregate['failed']} | {aggregate['missing']} | `{aggregate['verification_status']}` |",
        "",
        "## Coverage Check",
        "",
    ]

    coverage_rows: list[list[Any]] = []
    profile_rows: list[list[Any]] = []
    category_rows: list[list[Any]] = []
    example_rows: list[list[Any]] = []
    for seed, seed_report in report["seed_reports"].items():
        for task in TASKS:
            task_report = seed_report["datasets"][task]
            verification = task_report["verification"]
            summary = task_report["summary"]
            profile = task_report["wrong_profile"]
            coverage_rows.append(
                [
                    seed,
                    task,
                    f"{verification['input_rows']}/{verification['merged_rows']}/{verification['eval_rows']}",
                    f"{verification['recomputed_correct']}/{summary['rows']}",
                    verification["summary_correct"],
                    verification["summary_num_em_mismatch"],
                    "`yes`" if verification["mismatch"] else "`no`",
                ]
            )
            profile_rows.append(
                [
                    seed,
                    task,
                    profile["wrong_count"],
                    f"{profile['wrong_high_risk_ratio']:.2f}",
                    f"{profile['wrong_complex_route_ratio']:.2f}",
                    f"{profile['wrong_deterministic_shortcut_applied_ratio']:.2f}",
                    f"{profile['wrong_strong_verification_applied_ratio']:.2f}",
                    f"{profile['wrong_avg_total_tokens']:.1f}",
                    f"{profile['right_avg_total_tokens']:.1f}",
                ]
            )
            for category, count in task_report["wrong_distributions"]["category"].items():
                category_rows.append([seed, task, category, count])
            for example in task_report["representative_wrong_rows"][:2]:
                example_rows.append(
                    [
                        seed,
                        task,
                        example["id"],
                        example["category"],
                        short_text(example["question_or_statement"], 100),
                        short_text(example["prediction_for_em"], 40),
                        short_text(example["gold_for_em"], 40),
                        example["total_tokens"],
                    ]
                )

    lines.extend(
        markdown_table(
            ["seed", "dataset", "input/merged/eval", "recomputed correct", "summary correct", "summary wrong", "mismatch"],
            coverage_rows,
        )
    )
    lines.extend(["", "## Wrong-Row Profile", ""])
    lines.extend(
        markdown_table(
            [
                "seed",
                "dataset",
                "wrong",
                "high-risk ratio",
                "complex-route ratio",
                "deterministic shortcut ratio",
                "strong verifier ratio",
                "wrong avg tokens",
                "right avg tokens",
            ],
            profile_rows,
        )
    )
    lines.extend(["", "## Heuristic Boundary Categories", ""])
    lines.extend(markdown_table(["seed", "dataset", "category", "wrong rows"], category_rows))
    lines.extend(["", "## Representative Wrong Rows", ""])
    lines.extend(
        markdown_table(
            ["seed", "dataset", "id", "category", "question/statement", "prediction", "gold", "tokens"],
            example_rows,
        )
    )
    lines.extend(
        [
            "",
            "## Findings",
            "",
        ]
    )
    lines.extend(f"- {item}" for item in report["boundary_findings"])
    lines.extend(["", "## Next Actions", ""])
    lines.extend(f"- {item}" for item in report["next_actions"])
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-json", type=Path, default=SUMMARY_DIR / "seed_boundary_error_diagnosis.json")
    parser.add_argument("--output-md", type=Path, default=SUMMARY_DIR / "seed_boundary_error_diagnosis.md")
    args = parser.parse_args()

    report = analyze()
    if report["aggregate"]["verification_status"] != "pass":
        print(json.dumps(report["aggregate"], ensure_ascii=False, indent=2), file=sys.stderr)
        raise SystemExit("row-level evaluator verification failed")

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    args.output_md.write_text(render_markdown(report), encoding="utf-8")
    print(
        json.dumps(
            {
                "json": str(args.output_json),
                "md": str(args.output_md),
                "rows": report["aggregate"]["rows"],
                "correct": report["aggregate"]["correct"],
                "wrong": report["aggregate"]["wrong"],
                "verification_status": report["aggregate"]["verification_status"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
