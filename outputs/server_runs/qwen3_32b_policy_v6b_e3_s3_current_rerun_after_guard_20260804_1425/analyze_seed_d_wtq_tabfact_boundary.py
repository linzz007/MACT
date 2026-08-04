#!/usr/bin/env python3
"""Diagnose Seed-D WTQ/TabFact after-guard boundary rows.

This is an offline artifact builder. It compares the original E3 current-only
Seed-D outputs with the S3 after-guard rerun on the same input IDs, then writes
an auditable diagnosis and a small preregistered repair-slice input package.
"""

from __future__ import annotations

import datetime as dt
import json
import re
import sys
from collections import Counter
from pathlib import Path
from statistics import mean
from typing import Any


RUN_DIR = Path(__file__).resolve().parent
SOURCE_RUN_DIR = Path("/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_multiseed_gate50_20260801_2231")
MYAGENT_CODE = Path("/home/ubuntu/lzz/MyAgent/code")
SUMMARY_DIR = RUN_DIR / "summary"
REPAIR_INPUT_DIR = RUN_DIR / "input" / "seed_d_wtq_tabfact_boundary_repair"
DATASETS = ("wtq", "tabfact")

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


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows)
    path.write_text(text, encoding="utf-8")


def value_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (list, tuple, set)):
        return ", ".join(value_text(item) for item in value)
    if isinstance(value, dict):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value)


def short_text(value: Any, limit: int = 140) -> str:
    text = re.sub(r"\s+", " ", value_text(value)).strip()
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def first_non_empty(row: dict[str, Any], *keys: str, default: str = "unknown") -> str:
    for key in keys:
        value = row.get(key)
        if value not in (None, ""):
            return str(value)
    return default


def avg(values: list[Any]) -> float:
    nums = [float(value) for value in values if value not in (None, "")]
    return mean(nums) if nums else 0.0


def row_text(row: dict[str, Any]) -> str:
    return " ".join(
        value_text(row.get(key))
        for key in ("question", "utterance", "statement", "claim")
        if row.get(key) not in (None, "")
    ).lower()


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


def classify_boundary(dataset: str, row: dict[str, Any], prediction: Any, gold: Any) -> str:
    text = row_text(row)
    pred_num = as_number(prediction)
    gold_num = as_number(gold)
    pred_text = value_text(prediction).strip().lower()
    gold_text = value_text(gold).strip().lower()

    if dataset == "wtq":
        if re.search(r"\b(rank|ranks|ranking|position|place|finish|seed|seeded|ordinal|first|second|third|last|higher|lower)\b", text):
            if pred_num is not None and gold_num is not None and abs(pred_num) == abs(gold_num) and pred_num != gold_num:
                return "wtq_rank_signed_difference_direction_boundary"
            return "wtq_rank_direction_or_ordinal_boundary"
        if re.search(r"\b(age|date|year|season|before|after|earlier|later|old|young|newest|latest)\b", text):
            return "wtq_temporal_or_age_lookup_boundary"
        if re.search(r"\b(how many|number of|count|total|sum|average|mean|difference|percent|percentage|all|both|only one)\b", text):
            return "wtq_numeric_aggregation_or_difference_boundary"
        return "wtq_entity_lookup_or_row_selection_boundary"

    if dataset == "tabfact":
        if re.search(r"\b(before|after|year|season|date|first|last|earlier|later|previous|next|recent|oldest|newest)\b", text):
            return "tabfact_temporal_order_boundary"
        if re.search(r"\b(count|number|more|less|least|most|highest|lowest|greater|fewer|only|all|both|same|different)\b", text):
            return "tabfact_numeric_or_same_row_relation_boundary"
        if gold_text in {"false", "0", "no"} and pred_text in {"true", "1", "yes"}:
            return "tabfact_false_positive_or_negation_boundary"
        if gold_text in {"true", "1", "yes"} and pred_text in {"false", "0", "no"}:
            return "tabfact_false_negative_entailment_boundary"
        return "tabfact_binary_entailment_boundary"

    return "unknown_boundary"


def row_id(row: dict[str, Any]) -> str:
    return str(row.get("id") or row.get("example_id") or row.get("table_id") or "")


def with_input_metadata(input_row: dict[str, Any], source_row: dict[str, Any], status: str, category: str) -> dict[str, Any]:
    copied = dict(input_row)
    copied["seed_d_boundary_metadata"] = {
        "source_stage": "E3 S3 after-guard Seed-D WTQ/TabFact boundary diagnosis",
        "status": status,
        "category": category,
        "old_current_correct": bool(source_row["old_correct"]),
        "after_guard_correct": bool(source_row["new_correct"]),
        "old_prediction_for_em": value_text(source_row["old_prediction"]),
        "after_guard_prediction_for_em": value_text(source_row["new_prediction"]),
        "gold_for_em": value_text(source_row["gold"]),
        "repair_policy": "gold-free semantic guard candidate; metadata is for audit only and must not be read by the model runner",
    }
    return copied


def compare_dataset(dataset: str, old_summary: dict[str, Any], new_summary: dict[str, Any]) -> dict[str, Any]:
    input_path = SOURCE_RUN_DIR / "input" / "seed_d" / f"{dataset}_seed_d_gate50.jsonl"
    old_path = SOURCE_RUN_DIR / "myagent_current" / "seed_d" / "merged" / f"{dataset}_qwen3-32b-local.jsonl"
    new_path = RUN_DIR / "myagent_s3_after_guard" / "seed_d" / "merged" / f"{dataset}_qwen3-32b-local.jsonl"
    eval_path = RUN_DIR / "myagent_s3_after_guard" / "seed_d" / "eval" / f"{dataset}_qwen3-32b-local_eval.json"

    input_rows = {row_id(row): row for row in read_jsonl(input_path)}
    old_rows = {row_id(row): row for row in load_jsonl(str(old_path))}
    new_rows = {row_id(row): row for row in load_jsonl(str(new_path))}
    ids = list(input_rows)

    if set(ids) != set(old_rows) or set(ids) != set(new_rows):
        raise SystemExit(f"{dataset}: input/old/new ID sets do not match")

    rows: list[dict[str, Any]] = []
    transitions: Counter[str] = Counter()
    category_counts: Counter[str] = Counter()
    wrong_category_counts: Counter[str] = Counter()
    status_inputs: dict[str, list[dict[str, Any]]] = {
        "recovered": [],
        "regressed": [],
        "stable_wrong": [],
        "stable_right": [],
    }

    for rid in ids:
        input_row = input_rows[rid]
        old_row = old_rows[rid]
        new_row = new_rows[rid]
        old_correct = bool(dataset_accuracy(old_row))
        new_correct = bool(dataset_accuracy(new_row))
        if old_correct and new_correct:
            status = "stable_right"
        elif old_correct and not new_correct:
            status = "regressed"
        elif not old_correct and new_correct:
            status = "recovered"
        else:
            status = "stable_wrong"

        gold = gold_for_em(new_row)
        new_prediction = prediction_for_em(new_row)
        old_prediction = prediction_for_em(old_row)
        category = classify_boundary(dataset, new_row, new_prediction, gold)
        metrics = _token_metrics(new_row)
        old_metrics = _token_metrics(old_row)
        transitions[status] += 1
        category_counts[category] += 1
        if not new_correct:
            wrong_category_counts[category] += 1

        item = {
            "dataset": dataset,
            "id": rid,
            "status": status,
            "category": category,
            "question_or_statement": short_text(new_row.get("question") or new_row.get("statement") or new_row.get("utterance"), 220),
            "old_prediction": old_prediction,
            "new_prediction": new_prediction,
            "gold": gold,
            "old_correct": old_correct,
            "new_correct": new_correct,
            "risk_level": first_non_empty(new_row, "risk_level"),
            "problem_tags": new_row.get("problem_tags"),
            "deterministic_shortcut_applied": bool(new_row.get("deterministic_shortcut_applied")),
            "deterministic_shortcut_reason": short_text(new_row.get("deterministic_shortcut_reason"), 160),
            "strong_verification_applied": bool(new_row.get("strong_verification_applied")),
            "strong_verification_reason": short_text(new_row.get("strong_verification_reason"), 160),
            "agreement_decision": first_non_empty(new_row, "agreement_decision"),
            "critic_verdict": first_non_empty(new_row, "critic_verdict"),
            "cross_validation_verdict": first_non_empty(new_row, "cross_validation_verdict"),
            "old_total_tokens": old_metrics.get("total"),
            "new_total_tokens": metrics.get("total"),
            "old_elapsed_seconds": old_row.get("elapsed_seconds_total"),
            "new_elapsed_seconds": new_row.get("elapsed_seconds_total"),
        }
        rows.append(item)
        status_inputs[status].append(with_input_metadata(input_row, item, status, category))

    new_correct = sum(1 for row in rows if row["new_correct"])
    old_correct = sum(1 for row in rows if row["old_correct"])
    gate_threshold = int(new_summary["datasets"][dataset]["threshold_correct"])
    gate_deficit = max(0, gate_threshold - new_correct)
    wrong_rows = [row for row in rows if not row["new_correct"]]
    priority_statuses = {"stable_wrong", "regressed"}
    priority_rows = [
        row
        for row in rows
        if row["status"] in priority_statuses and row["category"] in set(dict(wrong_category_counts.most_common(4)))
    ]
    priority_rows = sorted(
        priority_rows,
        key=lambda row: (
            0 if row["status"] == "regressed" else 1,
            -(row["new_total_tokens"] or 0),
            row["id"],
        ),
    )

    write_jsonl(REPAIR_INPUT_DIR / f"{dataset}_seed_d_after_guard_wrong.jsonl", status_inputs["stable_wrong"] + status_inputs["regressed"])
    write_jsonl(REPAIR_INPUT_DIR / f"{dataset}_seed_d_after_guard_no_harm_correct.jsonl", status_inputs["stable_right"] + status_inputs["recovered"])
    write_jsonl(REPAIR_INPUT_DIR / f"{dataset}_seed_d_after_guard_priority_probe.jsonl", [with_input_metadata(input_rows[row["id"]], row, row["status"], row["category"]) for row in priority_rows[: min(16, len(priority_rows))]])

    return {
        "dataset": dataset,
        "paths": {
            "input": str(input_path),
            "old_current_merged": str(old_path),
            "after_guard_merged": str(new_path),
            "after_guard_eval": str(eval_path),
        },
        "coverage": {
            "input_rows": len(input_rows),
            "old_rows": len(old_rows),
            "new_rows": len(new_rows),
            "eval_rows": read_json(eval_path).get("num_samples"),
            "id_set_match": True,
        },
        "summary": {
            "old_correct": old_correct,
            "after_guard_correct": new_correct,
            "delta_correct": new_correct - old_correct,
            "threshold_correct": gate_threshold,
            "gate_deficit": gate_deficit,
            "old_token_ratio_to_mact_full200": old_summary["datasets"][dataset]["token_ratio_to_mact_full200"],
            "after_guard_token_ratio_to_mact_full200": new_summary["datasets"][dataset]["token_ratio_to_mact_full200"],
            "after_guard_failed": new_summary["datasets"][dataset]["num_failed_exec"],
            "after_guard_missing": new_summary["datasets"][dataset]["num_missing_answer"],
        },
        "transition_counts": dict(transitions),
        "after_guard_wrong_category_counts": dict(wrong_category_counts.most_common()),
        "all_row_category_counts": dict(category_counts.most_common()),
        "token_profile": {
            "wrong_avg_after_guard_tokens": avg([row["new_total_tokens"] for row in wrong_rows]),
            "right_avg_after_guard_tokens": avg([row["new_total_tokens"] for row in rows if row["new_correct"]]),
            "regressed_avg_after_guard_tokens": avg([row["new_total_tokens"] for row in rows if row["status"] == "regressed"]),
            "recovered_avg_after_guard_tokens": avg([row["new_total_tokens"] for row in rows if row["status"] == "recovered"]),
        },
        "repair_slice_outputs": {
            "wrong_or_regressed": str(REPAIR_INPUT_DIR / f"{dataset}_seed_d_after_guard_wrong.jsonl"),
            "no_harm_correct": str(REPAIR_INPUT_DIR / f"{dataset}_seed_d_after_guard_no_harm_correct.jsonl"),
            "priority_probe": str(REPAIR_INPUT_DIR / f"{dataset}_seed_d_after_guard_priority_probe.jsonl"),
        },
        "wrong_rows": wrong_rows,
        "priority_probe_rows": priority_rows[: min(16, len(priority_rows))],
    }


def build_report() -> dict[str, Any]:
    generated_at = dt.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
    old_summary = read_json(SOURCE_RUN_DIR / "summary" / "seed_d_myagent_gate50_summary.json")
    new_summary = read_json(SUMMARY_DIR / "seed_d_s3_current_summary.json")
    datasets = {
        dataset: compare_dataset(dataset, old_summary, new_summary)
        for dataset in DATASETS
    }

    total_old = sum(item["summary"]["old_correct"] for item in datasets.values())
    total_new = sum(item["summary"]["after_guard_correct"] for item in datasets.values())
    total_threshold = sum(item["summary"]["threshold_correct"] for item in datasets.values())
    total_wrong = sum(len(item["wrong_rows"]) for item in datasets.values())
    total_regressed = sum(item["transition_counts"].get("regressed", 0) for item in datasets.values())
    total_recovered = sum(item["transition_counts"].get("recovered", 0) for item in datasets.values())

    manifest = {
        "artifact_name": "seed_d_wtq_tabfact_after_guard_boundary_diagnosis",
        "generated_at_local": generated_at,
        "run_dir": str(RUN_DIR),
        "source_run_dir": str(SOURCE_RUN_DIR),
        "scope": "Offline same-ID comparison of Seed-D WTQ/TabFact original E3 current-only outputs and S3 after-guard outputs. No model was run.",
        "datasets": datasets,
        "aggregate": {
            "datasets": list(DATASETS),
            "rows": 100,
            "old_correct": total_old,
            "after_guard_correct": total_new,
            "delta_correct": total_new - total_old,
            "threshold_correct": total_threshold,
            "gate_deficit": max(0, total_threshold - total_new),
            "wrong_rows": total_wrong,
            "recovered": total_recovered,
            "regressed": total_regressed,
            "decision": "diagnose_then_build_small_fresh_repair_slice",
        },
        "interpretation": [
            "After-guard S3 did not fail because of missing answers or runner errors; both WTQ and TabFact have 50/50 rows with zero failures.",
            "The Seed-D blocker is not uniform: WTQ regressed by two correct rows versus the old current-only run, while TabFact gained one correct row but remains below its gate.",
            "A direct paired MACT run is still not justified for Seed-D; the next evidence step should be a bounded affected-slice/no-harm fresh probe using the generated repair inputs.",
            "The generated repair inputs include audit metadata, but model runners must consume only the original task fields; metadata is for traceability and must not be used as a prompt feature.",
        ],
        "next_actions": [
            "Inspect the top WTQ rank/temporal/entity rows and TabFact temporal/entity relation rows for reusable, gold-free guards.",
            "Implement only mechanisms that can be described as selective-risk collaboration or deterministic semantic verification, not ID-specific fixes.",
            "Run the priority probe first; only if it recovers enough boundary rows without no-harm regressions should Seed-D WTQ/TabFact full50 be rerun.",
        ],
    }

    REPAIR_INPUT_DIR.mkdir(parents=True, exist_ok=True)
    input_manifest = {
        "generated_at_local": generated_at,
        "source_report": str(SUMMARY_DIR / "seed_d_wtq_tabfact_after_guard_boundary_diagnosis.json"),
        "warning": "seed_d_boundary_metadata is for audit only and must not be passed to the model prompt.",
        "datasets": {
            dataset: datasets[dataset]["repair_slice_outputs"]
            for dataset in DATASETS
        },
        "gate": {
            "wtq_after_guard_correct": datasets["wtq"]["summary"]["after_guard_correct"],
            "wtq_threshold_correct": datasets["wtq"]["summary"]["threshold_correct"],
            "tabfact_after_guard_correct": datasets["tabfact"]["summary"]["after_guard_correct"],
            "tabfact_threshold_correct": datasets["tabfact"]["summary"]["threshold_correct"],
        },
    }
    (REPAIR_INPUT_DIR / "input_manifest.json").write_text(json.dumps(input_manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


def markdown_table(headers: list[str], rows: list[list[Any]]) -> list[str]:
    lines = [
        "| " + " | ".join(headers) + " |",
        "|" + "|".join("---" for _ in headers) + "|",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(item) for item in row) + " |")
    return lines


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Seed-D WTQ/TabFact After-Guard Boundary Diagnosis",
        "",
        f"Generated: `{report['generated_at_local']}`",
        "",
        f"Scope: {report['scope']}",
        "",
        "## Decision",
        "",
        "`diagnose_then_build_small_fresh_repair_slice`: Seed-D WTQ/TabFact still cannot trigger paired MACT. Use the generated affected-slice inputs for the next bounded repair probe.",
        "",
        "## Aggregate",
        "",
        "| rows | old correct | after-guard correct | delta | threshold | deficit | recovered | regressed |",
        "|---:|---:|---:|---:|---:|---:|---:|---:|",
        f"| {report['aggregate']['rows']} | {report['aggregate']['old_correct']} | {report['aggregate']['after_guard_correct']} | {report['aggregate']['delta_correct']} | {report['aggregate']['threshold_correct']} | {report['aggregate']['gate_deficit']} | {report['aggregate']['recovered']} | {report['aggregate']['regressed']} |",
        "",
        "## Dataset Summary",
        "",
    ]
    dataset_rows = []
    transition_rows = []
    category_rows = []
    priority_rows = []
    for dataset, item in report["datasets"].items():
        summary = item["summary"]
        dataset_rows.append(
            [
                dataset,
                f"{item['coverage']['input_rows']}/{item['coverage']['new_rows']}/{item['coverage']['eval_rows']}",
                summary["old_correct"],
                summary["after_guard_correct"],
                summary["delta_correct"],
                summary["threshold_correct"],
                summary["gate_deficit"],
                f"{summary['after_guard_token_ratio_to_mact_full200']:.4f}",
                f"{summary['after_guard_failed']}/{summary['after_guard_missing']}",
            ]
        )
        transitions = item["transition_counts"]
        transition_rows.append(
            [
                dataset,
                transitions.get("stable_right", 0),
                transitions.get("recovered", 0),
                transitions.get("regressed", 0),
                transitions.get("stable_wrong", 0),
            ]
        )
        for category, count in item["after_guard_wrong_category_counts"].items():
            category_rows.append([dataset, category, count])
        for row in item["priority_probe_rows"][:8]:
            priority_rows.append(
                [
                    dataset,
                    row["id"],
                    row["status"],
                    row["category"],
                    short_text(row["question_or_statement"], 100),
                    short_text(row["new_prediction"], 36),
                    short_text(row["gold"], 36),
                    row["new_total_tokens"],
                ]
            )

    lines.extend(
        markdown_table(
            ["dataset", "input/merged/eval", "old correct", "after-guard correct", "delta", "threshold", "deficit", "token ratio", "failed/missing"],
            dataset_rows,
        )
    )
    lines.extend(["", "## Same-ID Transitions", ""])
    lines.extend(markdown_table(["dataset", "stable right", "recovered", "regressed", "stable wrong"], transition_rows))
    lines.extend(["", "## Wrong Boundary Categories", ""])
    lines.extend(markdown_table(["dataset", "category", "wrong rows"], category_rows))
    lines.extend(["", "## Priority Probe Rows", ""])
    lines.extend(markdown_table(["dataset", "id", "status", "category", "question/statement", "prediction", "gold", "tokens"], priority_rows))
    lines.extend(["", "## Generated Repair Inputs", ""])
    for dataset, item in report["datasets"].items():
        outputs = item["repair_slice_outputs"]
        lines.append(f"- {dataset} wrong/regressed: `{outputs['wrong_or_regressed']}`")
        lines.append(f"- {dataset} no-harm correct: `{outputs['no_harm_correct']}`")
        lines.append(f"- {dataset} priority probe: `{outputs['priority_probe']}`")
    lines.extend(["", "## Interpretation", ""])
    lines.extend(f"- {item}" for item in report["interpretation"])
    lines.extend(["", "## Next Actions", ""])
    lines.extend(f"- {item}" for item in report["next_actions"])
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    report = build_report()
    json_path = SUMMARY_DIR / "seed_d_wtq_tabfact_after_guard_boundary_diagnosis.json"
    md_path = SUMMARY_DIR / "seed_d_wtq_tabfact_after_guard_boundary_diagnosis.md"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(report), encoding="utf-8")
    print(
        json.dumps(
            {
                "json": str(json_path),
                "md": str(md_path),
                "repair_input_dir": str(REPAIR_INPUT_DIR),
                "decision": report["aggregate"]["decision"],
                "after_guard_correct": report["aggregate"]["after_guard_correct"],
                "threshold_correct": report["aggregate"]["threshold_correct"],
                "gate_deficit": report["aggregate"]["gate_deficit"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
