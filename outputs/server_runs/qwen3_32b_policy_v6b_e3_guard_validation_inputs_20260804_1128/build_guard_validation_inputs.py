#!/usr/bin/env python3
"""Build the E3 affected-slice/no-harm guard-validation input package."""

from __future__ import annotations

import datetime as dt
import importlib.util
import json
from collections import Counter
from pathlib import Path
from typing import Any


RUN_DIR = Path(__file__).resolve().parent
SUMMARY_DIR = RUN_DIR / "summary"
INPUT_DIR = RUN_DIR / "input"
MULTISEED_RUN = Path(
    "/home/ubuntu/lzz/MACT/outputs/server_runs/"
    "qwen3_32b_policy_v6b_multiseed_gate50_20260801_2231"
)
BUDGET_PROBE_RUN = Path(
    "/home/ubuntu/lzz/MACT/outputs/server_runs/"
    "qwen3_32b_policy_v6b_e3_boundary_budget_probe_20260804_1035"
)
SEMANTIC_PLAN_RUN = Path(
    "/home/ubuntu/lzz/MACT/outputs/server_runs/"
    "qwen3_32b_policy_v6b_e3_semantic_boundary_plan_20260804_1110"
)
BUDGET_SUMMARY = BUDGET_PROBE_RUN / "summary" / "e3_boundary_budget_probe_summary.json"
SEMANTIC_PLAN = SEMANTIC_PLAN_RUN / "summary" / "e3_semantic_boundary_plan.json"
DIAG_MODULE_PATH = MULTISEED_RUN / "analyze_seed_boundary_errors.py"

DATASETS = ("wtq", "tabfact", "crt")
SEEDS = ("seed_c", "seed_d")

NO_HARM_SPECS = [
    {
        "dataset": "crt",
        "target_category": "crt_multi_step_numeric_composition_boundary",
        "priority": "P0",
        "count": 2,
        "proxy_categories": [],
        "reason": "P0 zero-recovery CRT numeric composition guard no-harm control.",
    },
    {
        "dataset": "wtq",
        "target_category": "wtq_entity_lookup_or_row_selection_boundary",
        "priority": "P0",
        "count": 2,
        "proxy_categories": [],
        "reason": "P0 zero-recovery WTQ entity/row-selection guard no-harm control.",
    },
    {
        "dataset": "crt",
        "target_category": "crt_span_or_universal_quantifier_boundary",
        "priority": "P0",
        "count": 2,
        "proxy_categories": [],
        "reason": "P0 zero-recovery CRT answer-contract guard no-harm control.",
    },
    {
        "dataset": "tabfact",
        "target_category": "tabfact_false_negative_entailment_boundary",
        "priority": "P0",
        "count": 2,
        "proxy_categories": [
            "tabfact_entity_attribute_same_row_boundary",
            "tabfact_binary_entailment_boundary",
        ],
        "reason": "P0 false-negative entailment has no correctly classified row under the mismatch-only label; proxy uses same-row/binary-entailment correct rows.",
    },
    {
        "dataset": "crt",
        "target_category": "crt_table_reasoning_or_entity_boundary",
        "priority": "P1",
        "count": 2,
        "proxy_categories": [],
        "reason": "P1 high-volume CRT table/entity grounding no-harm control.",
    },
    {
        "dataset": "wtq",
        "target_category": "wtq_numeric_aggregation_or_difference_boundary",
        "priority": "P1",
        "count": 2,
        "proxy_categories": [],
        "reason": "P1 high-volume WTQ aggregation/difference guard no-harm control.",
    },
    {
        "dataset": "crt",
        "target_category": "crt_percentage_complement_or_aggregation_boundary",
        "priority": "P1",
        "count": 2,
        "proxy_categories": [],
        "reason": "P1 CRT percentage/complement guard no-harm control.",
    },
    {
        "dataset": "wtq",
        "target_category": "wtq_temporal_or_age_lookup_boundary",
        "priority": "P1",
        "count": 2,
        "proxy_categories": [],
        "reason": "P1 mixed budget/semantic WTQ temporal guard no-harm control.",
    },
    {
        "dataset": "tabfact",
        "target_category": "tabfact_temporal_order_boundary",
        "priority": "P2",
        "count": 1,
        "proxy_categories": [],
        "reason": "P2 budget-sensitive TabFact temporal recovery no-harm control.",
    },
    {
        "dataset": "tabfact",
        "target_category": "tabfact_numeric_count_or_comparison_boundary",
        "priority": "P2",
        "count": 1,
        "proxy_categories": [],
        "reason": "P2 budget-sensitive TabFact numeric/count recovery no-harm control.",
    },
]


def load_diagnosis_module():
    spec = importlib.util.spec_from_file_location("seed_boundary_diagnosis", DIAG_MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load diagnosis module from {DIAG_MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


DIAG = load_diagnosis_module()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def source_input_path(seed: str, dataset: str) -> Path:
    return MULTISEED_RUN / "input" / seed / f"{dataset}_{seed}_gate50.jsonl"


def source_merged_path(seed: str, dataset: str) -> Path:
    return MULTISEED_RUN / "myagent_current" / seed / "merged" / f"{dataset}_qwen3-32b-local.jsonl"


def by_id(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {str(row.get("id")): row for row in rows}


def source_key(seed: str, dataset: str, row_id: str) -> str:
    return f"{seed}/{dataset}/{row_id}"


def value_text(value: Any) -> str:
    return DIAG.value_text(value)


def row_prediction(row: dict[str, Any]) -> Any:
    return DIAG.prediction_for_em(row)


def row_gold(row: dict[str, Any]) -> Any:
    return DIAG.gold_for_em(row)


def row_tokens(row: dict[str, Any]) -> Any:
    return DIAG._token_metrics(row).get("total")


def category_index(plan: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {str(item["category"]): item for item in plan.get("category_plan", [])}


def load_source_inputs() -> tuple[
    dict[tuple[str, str], dict[str, dict[str, Any]]],
    dict[tuple[str, str], dict[str, dict[str, Any]]],
]:
    input_rows: dict[tuple[str, str], dict[str, dict[str, Any]]] = {}
    merged_rows: dict[tuple[str, str], dict[str, dict[str, Any]]] = {}
    for seed in SEEDS:
        for dataset in DATASETS:
            input_rows[(seed, dataset)] = by_id(read_jsonl(source_input_path(seed, dataset)))
            merged_rows[(seed, dataset)] = by_id(read_jsonl(source_merged_path(seed, dataset)))
    return input_rows, merged_rows


def source_metadata(
    *,
    seed: str,
    dataset: str,
    row_id: str,
    merged: dict[str, Any],
    category: str,
    priority: str,
    track: str,
    slice_role: str,
    selection_reason: str,
    budget_row: dict[str, Any] | None = None,
    no_harm_proxy_for: str | None = None,
) -> dict[str, Any]:
    correct = bool(DIAG.dataset_accuracy(merged))
    metadata = {
        "validation_name": "e3_guard_validation_inputs",
        "slice_role": slice_role,
        "source_run": str(MULTISEED_RUN),
        "source_seed": seed,
        "source_dataset": dataset,
        "source_id": row_id,
        "source_key": source_key(seed, dataset, row_id),
        "boundary_category": category,
        "priority": priority,
        "track": track,
        "source_correct": correct,
        "selection_reason": selection_reason,
        "original_prediction_for_em": row_prediction(merged),
        "gold_for_em": row_gold(merged),
        "final_answer": merged.get("final_answer"),
        "final_value": merged.get("final_value"),
        "risk_level": merged.get("risk_level") or (merged.get("observability") or {}).get("risk_level"),
        "route_type": merged.get("route_type"),
        "total_tokens": row_tokens(merged),
        "elapsed_seconds_total": merged.get("elapsed_seconds_total"),
        "exec_error": bool(merged.get("exec_error")),
        "missing_answer": row_prediction(merged) in (None, ""),
    }
    if no_harm_proxy_for:
        metadata["no_harm_proxy_for"] = no_harm_proxy_for
    if budget_row:
        metadata.update(
            {
                "max_replan5_recovered": bool(budget_row.get("recovered")),
                "max_replan5_correct": bool(budget_row.get("replan5_correct")),
                "max_replan5_prediction_for_em": budget_row.get("replan5_prediction_for_em"),
                "max_replan5_total_tokens": budget_row.get("replan5_total_tokens"),
                "max_replan5_elapsed_seconds": budget_row.get("replan5_elapsed_seconds"),
            }
        )
    return metadata


def build_representative_rows(
    *,
    budget_summary: dict[str, Any],
    category_by_name: dict[str, dict[str, Any]],
    source_inputs: dict[tuple[str, str], dict[str, dict[str, Any]]],
    source_merged: dict[tuple[str, str], dict[str, dict[str, Any]]],
) -> list[dict[str, Any]]:
    budget_rows = {
        source_key(str(row["seed"]), str(row["dataset"]), str(row["id"])): row
        for row in budget_summary.get("rows", [])
    }
    representative_rows = []
    for item in budget_summary.get("input_manifest", {}).get("representative_rows", []):
        seed = str(item["seed"])
        dataset = str(item["dataset"])
        row_id = str(item["id"])
        category = str(item["category"])
        plan_item = category_by_name[category]
        key = (seed, dataset)
        if row_id not in source_inputs[key]:
            raise RuntimeError(f"Missing representative source input row: {seed}/{dataset}/{row_id}")
        if row_id not in source_merged[key]:
            raise RuntimeError(f"Missing representative source merged row: {seed}/{dataset}/{row_id}")
        source_row = dict(source_inputs[key][row_id])
        source_row["source_dataset"] = dataset
        source_row["validation_metadata"] = source_metadata(
            seed=seed,
            dataset=dataset,
            row_id=row_id,
            merged=source_merged[key][row_id],
            category=category,
            priority=str(plan_item["priority"]),
            track=str(plan_item["track"]),
            slice_role="representative_wrong",
            selection_reason="Representative wrong row selected by the E3 max_replan=5 budget probe.",
            budget_row=budget_rows.get(source_key(seed, dataset, row_id)),
        )
        if source_row["validation_metadata"]["source_correct"]:
            raise RuntimeError(f"Representative row is unexpectedly correct: {seed}/{dataset}/{row_id}")
        representative_rows.append(source_row)
    return representative_rows


def correct_candidates(
    *,
    dataset: str,
    categories: list[str],
    source_inputs: dict[tuple[str, str], dict[str, dict[str, Any]]],
    source_merged: dict[tuple[str, str], dict[str, dict[str, Any]]],
    used_keys: set[str],
) -> list[tuple[str, str, str, dict[str, Any], dict[str, Any]]]:
    rows: list[tuple[str, str, str, dict[str, Any], dict[str, Any]]] = []
    for seed in SEEDS:
        for row_id, merged in source_merged[(seed, dataset)].items():
            key = source_key(seed, dataset, row_id)
            if key in used_keys or not DIAG.dataset_accuracy(merged):
                continue
            category = DIAG.classify_boundary(dataset, merged, row_prediction(merged), row_gold(merged))
            if category not in categories:
                continue
            rows.append((seed, row_id, category, source_inputs[(seed, dataset)][row_id], merged))
    return sorted(rows, key=lambda item: (item[0], item[2], item[1]))


def build_no_harm_rows(
    *,
    category_by_name: dict[str, dict[str, Any]],
    source_inputs: dict[tuple[str, str], dict[str, dict[str, Any]]],
    source_merged: dict[tuple[str, str], dict[str, dict[str, Any]]],
    used_keys: set[str],
) -> list[dict[str, Any]]:
    no_harm_rows: list[dict[str, Any]] = []
    for spec in NO_HARM_SPECS:
        dataset = str(spec["dataset"])
        target_category = str(spec["target_category"])
        categories = [target_category] + [str(item) for item in spec["proxy_categories"]]
        candidates = correct_candidates(
            dataset=dataset,
            categories=categories,
            source_inputs=source_inputs,
            source_merged=source_merged,
            used_keys=used_keys,
        )
        if len(candidates) < int(spec["count"]):
            raise RuntimeError(
                f"Not enough no-harm candidates for {target_category}: "
                f"need {spec['count']}, got {len(candidates)}"
            )
        for seed, row_id, actual_category, source_input, merged in candidates[: int(spec["count"])]:
            key = source_key(seed, dataset, row_id)
            used_keys.add(key)
            source_row = dict(source_input)
            source_row["source_dataset"] = dataset
            source_row["validation_metadata"] = source_metadata(
                seed=seed,
                dataset=dataset,
                row_id=row_id,
                merged=merged,
                category=actual_category,
                priority=str(spec["priority"]),
                track=str(category_by_name.get(target_category, {}).get("track") or "no_harm_control"),
                slice_role="no_harm_correct",
                selection_reason=str(spec["reason"]),
                no_harm_proxy_for=target_category if actual_category != target_category else None,
            )
            no_harm_rows.append(source_row)
    return no_harm_rows


def summarize(rows: list[dict[str, Any]], output_dir: Path, plan: dict[str, Any]) -> dict[str, Any]:
    source_keys = [row["validation_metadata"]["source_key"] for row in rows]
    duplicate_source_keys = sorted(key for key, count in Counter(source_keys).items() if count > 1)
    dataset_counts = {dataset: 0 for dataset in DATASETS}
    for row in rows:
        dataset_counts[str(row["validation_metadata"]["source_dataset"])] += 1
    role_counts = dict(Counter(row["validation_metadata"]["slice_role"] for row in rows))
    category_counts = dict(Counter(row["validation_metadata"]["boundary_category"] for row in rows).most_common())
    no_harm_proxy_counts = dict(
        Counter(
            row["validation_metadata"].get("no_harm_proxy_for")
            for row in rows
            if row["validation_metadata"].get("no_harm_proxy_for")
        ).most_common()
    )
    representative_recovered = sum(
        1
        for row in rows
        if row["validation_metadata"]["slice_role"] == "representative_wrong"
        and row["validation_metadata"].get("max_replan5_recovered")
    )
    representative_zero_recovery = [
        row["validation_metadata"]["source_key"]
        for row in rows
        if row["validation_metadata"]["slice_role"] == "representative_wrong"
        and not row["validation_metadata"].get("max_replan5_recovered")
    ]
    row_index = [
        {
            "source_key": row["validation_metadata"]["source_key"],
            "dataset": row["validation_metadata"]["source_dataset"],
            "id": row["validation_metadata"]["source_id"],
            "slice_role": row["validation_metadata"]["slice_role"],
            "category": row["validation_metadata"]["boundary_category"],
            "priority": row["validation_metadata"]["priority"],
            "source_correct": row["validation_metadata"]["source_correct"],
            "max_replan5_recovered": row["validation_metadata"].get("max_replan5_recovered"),
            "no_harm_proxy_for": row["validation_metadata"].get("no_harm_proxy_for"),
        }
        for row in rows
    ]
    return {
        "artifact_name": "e3_guard_validation_input_plan",
        "generated_at_local": dt.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z"),
        "run_dir": str(output_dir),
        "scope": "Input/package artifact only. It does not run models or change benchmark results.",
        "source_multiseed_run": str(MULTISEED_RUN),
        "source_budget_probe_summary": str(BUDGET_SUMMARY),
        "source_semantic_boundary_plan": str(SEMANTIC_PLAN),
        "upstream_decision": plan.get("current_decision"),
        "validation_decision": "ready_for_guard_implementation_not_model_run",
        "total_rows": len(rows),
        "dataset_counts": dataset_counts,
        "role_counts": role_counts,
        "category_counts": category_counts,
        "no_harm_proxy_counts": no_harm_proxy_counts,
        "duplicate_source_keys": duplicate_source_keys,
        "representative_wrong_budget_probe_recovered": representative_recovered,
        "representative_wrong_budget_probe_zero_recovery_keys": representative_zero_recovery,
        "gate_targets": {
            "representative_wrong_recovery_min": 7,
            "representative_wrong_recovery_note": "Future guard fresh run should recover at least 7/12 representative wrong rows; max_replan=5 alone recovered 4/12.",
            "no_harm_correct_min": 18,
            "failed_missing_max": 0,
            "token_ratio_to_mact_full200_max": 1.0,
            "rerun_escalation": "Only run S3 E3 current-only rerun or paired MACT if this S2 affected slice passes.",
        },
        "row_index": row_index,
    }


def markdown_summary(summary: dict[str, Any]) -> str:
    lines = [
        "# E3 Guard Validation Input Plan",
        "",
        f"- Generated: `{summary['generated_at_local']}`",
        f"- Decision: `{summary['validation_decision']}`",
        f"- Scope: {summary['scope']}",
        f"- Total rows: `{summary['total_rows']}`",
        "",
        "## Dataset Counts",
        "",
        "| dataset | rows |",
        "| --- | ---: |",
    ]
    for dataset, count in summary["dataset_counts"].items():
        lines.append(f"| {dataset} | {count} |")
    lines.extend(
        [
            "",
            "## Role Counts",
            "",
            "| role | rows |",
            "| --- | ---: |",
        ]
    )
    for role, count in summary["role_counts"].items():
        lines.append(f"| {role} | {count} |")
    lines.extend(
        [
            "",
            "## Gate Targets",
            "",
            f"- Representative wrong recovery minimum: `{summary['gate_targets']['representative_wrong_recovery_min']}/12`.",
            f"- No-harm correct minimum: `{summary['gate_targets']['no_harm_correct_min']}/18`.",
            f"- Failed/missing maximum: `{summary['gate_targets']['failed_missing_max']}`.",
            f"- Token ratio to MACT full200 reference maximum: `< {summary['gate_targets']['token_ratio_to_mact_full200_max']}`.",
            "",
            "## Row Index",
            "",
            "| source_key | role | category | priority | source_correct | max_replan5_recovered | proxy_for |",
            "| --- | --- | --- | --- | ---: | ---: | --- |",
        ]
    )
    for row in summary["row_index"]:
        lines.append(
            "| {source_key} | {slice_role} | {category} | {priority} | {source_correct} | {recovered} | {proxy} |".format(
                source_key=row["source_key"],
                slice_role=row["slice_role"],
                category=row["category"],
                priority=row["priority"],
                source_correct=str(row["source_correct"]).lower(),
                recovered="" if row["max_replan5_recovered"] is None else str(row["max_replan5_recovered"]).lower(),
                proxy=row.get("no_harm_proxy_for") or "",
            )
        )
    lines.append("")
    return "\n".join(lines)


def readme_text(summary: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Qwen3-32B Policy v6b E3 Guard Validation Inputs",
            "",
            "This directory prepares the S2 affected-slice/no-harm validation inputs for the E3 semantic-boundary plan.",
            "It does not run a model. It packages rows that should be used after implementing targeted gold-free semantic guards.",
            "",
            "Artifacts:",
            "",
            "- `input/wtq_e3_guard_validation.jsonl`",
            "- `input/tabfact_e3_guard_validation.jsonl`",
            "- `input/crt_e3_guard_validation.jsonl`",
            "- `input/input_manifest.json`",
            "- `summary/e3_guard_validation_input_plan.json`",
            "- `summary/e3_guard_validation_input_plan.md`",
            "- `tests/test_build_guard_validation_inputs.py`",
            "",
            "Current gate:",
            "",
            f"- total rows: `{summary['total_rows']}`",
            "- representative wrong rows: `12`",
            "- no-harm correct rows: `18`",
            "- future S2 fresh run should recover at least `7/12` representative wrong rows and keep `18/18` no-harm rows correct.",
            "",
            "Source evidence:",
            "",
            f"- multiseed run: `{MULTISEED_RUN}`",
            f"- budget probe: `{BUDGET_SUMMARY}`",
            f"- semantic-boundary plan: `{SEMANTIC_PLAN}`",
            "",
        ]
    )


def build_package(output_dir: Path | str = RUN_DIR) -> dict[str, Any]:
    output_path = Path(output_dir)
    plan = read_json(SEMANTIC_PLAN)
    budget_summary = read_json(BUDGET_SUMMARY)
    category_by_name = category_index(plan)
    source_inputs, source_merged = load_source_inputs()

    rows = build_representative_rows(
        budget_summary=budget_summary,
        category_by_name=category_by_name,
        source_inputs=source_inputs,
        source_merged=source_merged,
    )
    used_keys = {row["validation_metadata"]["source_key"] for row in rows}
    rows.extend(
        build_no_harm_rows(
            category_by_name=category_by_name,
            source_inputs=source_inputs,
            source_merged=source_merged,
            used_keys=used_keys,
        )
    )
    rows.sort(
        key=lambda row: (
            DATASETS.index(row["validation_metadata"]["source_dataset"]),
            0 if row["validation_metadata"]["slice_role"] == "representative_wrong" else 1,
            row["validation_metadata"]["priority"],
            row["validation_metadata"]["boundary_category"],
            row["validation_metadata"]["source_seed"],
            row["validation_metadata"]["source_id"],
        )
    )

    summary = summarize(rows, output_path, plan)
    if summary["duplicate_source_keys"]:
        raise RuntimeError(f"Duplicate source keys: {summary['duplicate_source_keys']}")

    for dataset in DATASETS:
        dataset_rows = [row for row in rows if row["validation_metadata"]["source_dataset"] == dataset]
        write_jsonl(output_path / "input" / f"{dataset}_e3_guard_validation.jsonl", dataset_rows)
    write_json(output_path / "input" / "input_manifest.json", summary)
    write_json(output_path / "summary" / "e3_guard_validation_input_plan.json", summary)
    (output_path / "summary").mkdir(parents=True, exist_ok=True)
    (output_path / "summary" / "e3_guard_validation_input_plan.md").write_text(
        markdown_summary(summary),
        encoding="utf-8",
    )
    (output_path / "README.md").write_text(readme_text(summary), encoding="utf-8")
    return summary


def main() -> None:
    summary = build_package(RUN_DIR)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
