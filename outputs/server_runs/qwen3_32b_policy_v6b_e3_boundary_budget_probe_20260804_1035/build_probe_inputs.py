#!/usr/bin/env python3
"""Build representative E3 boundary probe inputs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


RUN_DIR = Path(__file__).resolve().parent
SOURCE_RUN = Path(
    "/home/ubuntu/lzz/MACT/outputs/server_runs/"
    "qwen3_32b_policy_v6b_multiseed_gate50_20260801_2231"
)
MYAGENT_ROOT = Path("/home/ubuntu/lzz/MyAgent")

REPRESENTATIVE_ROWS = [
    ("seed_c", "wtq", "nu-1456", "wtq_temporal_or_age_lookup_boundary"),
    ("seed_c", "wtq", "nu-2577", "wtq_entity_lookup_or_row_selection_boundary"),
    ("seed_c", "tabfact", "tabfact-test-9637", "tabfact_false_negative_entailment_boundary"),
    ("seed_c", "tabfact", "tabfact-test-8555", "tabfact_temporal_order_boundary"),
    ("seed_c", "crt", "crt-325", "crt_multi_step_numeric_composition_boundary"),
    ("seed_c", "crt", "crt-0", "crt_span_or_universal_quantifier_boundary"),
    ("seed_d", "wtq", "nu-515", "wtq_temporal_or_age_lookup_boundary"),
    ("seed_d", "wtq", "nu-3380", "wtq_entity_lookup_or_row_selection_boundary"),
    ("seed_d", "tabfact", "tabfact-test-12194", "tabfact_temporal_order_boundary"),
    ("seed_d", "tabfact", "tabfact-test-1383", "tabfact_numeric_count_or_comparison_boundary"),
    ("seed_d", "crt", "crt-121", "crt_multi_step_numeric_composition_boundary"),
    ("seed_d", "crt", "crt-303", "crt_span_or_universal_quantifier_boundary"),
]


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def by_id(path: Path) -> dict[str, dict[str, Any]]:
    return {str(row.get("id")): row for row in read_jsonl(path)}


def source_input_path(seed: str, dataset: str) -> Path:
    return SOURCE_RUN / "input" / seed / f"{dataset}_{seed}_gate50.jsonl"


def source_merged_path(seed: str, dataset: str) -> Path:
    return SOURCE_RUN / "myagent_current" / seed / "merged" / f"{dataset}_qwen3-32b-local.jsonl"


def main() -> None:
    rows_by_dataset: dict[str, list[dict[str, Any]]] = {"wtq": [], "tabfact": [], "crt": []}
    inputs_cache: dict[tuple[str, str], dict[str, dict[str, Any]]] = {}
    merged_cache: dict[tuple[str, str], dict[str, dict[str, Any]]] = {}

    for seed, dataset, row_id, category in REPRESENTATIVE_ROWS:
        key = (seed, dataset)
        inputs_cache.setdefault(key, by_id(source_input_path(seed, dataset)))
        merged_cache.setdefault(key, by_id(source_merged_path(seed, dataset)))

        if row_id not in inputs_cache[key]:
            raise RuntimeError(f"Missing source input row: {seed}/{dataset}/{row_id}")
        if row_id not in merged_cache[key]:
            raise RuntimeError(f"Missing source merged row: {seed}/{dataset}/{row_id}")

        source_input = dict(inputs_cache[key][row_id])
        source_merged = merged_cache[key][row_id]
        source_input["source_dataset"] = dataset
        source_input["probe_metadata"] = {
            "probe_name": "e3_boundary_budget_probe",
            "source_run": str(SOURCE_RUN),
            "source_seed": seed,
            "source_dataset": dataset,
            "source_id": row_id,
            "boundary_category": category,
            "original_max_replan": 3,
            "probe_max_replan": 5,
            "original_prediction_for_em": source_merged.get("final_value")
            if source_merged.get("final_value") is not None
            else source_merged.get("final_answer"),
            "original_final_answer": source_merged.get("final_answer"),
            "original_final_value": source_merged.get("final_value"),
            "original_gold_answer": source_merged.get("gold_answer")
            if source_merged.get("gold_answer") is not None
            else source_merged.get("answer"),
            "original_total_tokens": (source_merged.get("api_metrics") or {}).get("total_tokens")
            or (source_merged.get("llm_metrics") or {}).get("total_tokens_est"),
            "original_elapsed_seconds": source_merged.get("elapsed_seconds_total"),
            "original_risk_level": source_merged.get("risk_level")
            or (source_merged.get("observability") or {}).get("risk_level"),
            "original_route_type": source_merged.get("route_type"),
        }
        rows_by_dataset[dataset].append(source_input)

    for dataset, rows in rows_by_dataset.items():
        ids = [str(row.get("id")) for row in rows]
        if len(ids) != len(set(ids)):
            raise RuntimeError(f"Duplicate probe ids for {dataset}: {ids}")
        write_jsonl(RUN_DIR / "input" / f"{dataset}_e3_boundary_budget_probe.jsonl", rows)

    summary = {
        "artifact": "e3_boundary_budget_probe_inputs",
        "source_run": str(SOURCE_RUN),
        "run_dir": str(RUN_DIR),
        "datasets": {dataset: len(rows) for dataset, rows in rows_by_dataset.items()},
        "total_rows": sum(len(rows) for rows in rows_by_dataset.values()),
        "representative_rows": [
            {
                "seed": seed,
                "dataset": dataset,
                "id": row_id,
                "category": category,
            }
            for seed, dataset, row_id, category in REPRESENTATIVE_ROWS
        ],
    }
    (RUN_DIR / "input" / "input_manifest.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
