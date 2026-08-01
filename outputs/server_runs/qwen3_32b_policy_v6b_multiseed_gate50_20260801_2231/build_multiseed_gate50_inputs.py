#!/usr/bin/env python3
"""Build non-overlapping Gate-50 inputs for additional Qwen3-32B seeds."""

from __future__ import annotations

import json
import random
from pathlib import Path
from typing import Any


RUN_DIR = Path(__file__).resolve().parent
MYAGENT_ROOT = Path("/home/ubuntu/lzz/MyAgent")
MACT_RUNS = Path("/home/ubuntu/lzz/MACT/outputs/server_runs")
P4B_RUN = MACT_RUNS / "qwen3_32b_policy_v6b_newseed_gate50_20260801_0305"
COARSE_RUN = MACT_RUNS / "qwen3_32b_policy_v6b_coarse_ablation_gate50_20260801_0040"

LIMIT_PER_DATASET = 50
SEEDS = {
    "seed_c": 20260802,
    "seed_d": 20260803,
}
TASKS = ("wtq", "tabfact", "crt")

DATASETS = {
    "wtq": {
        "source_path": MYAGENT_ROOT / "datasets_ready/full/wtq_unseen.jsonl",
        "exclusion_paths": [
            MACT_RUNS / "qwen3_32b_wtq_policy_v6b_full200_20260731_1115/input/wtq_full200.jsonl",
            COARSE_RUN / "input/wtq_diagnostic_gate50.jsonl",
            P4B_RUN / "input/wtq_newseed_gate50.jsonl",
            P4B_RUN / "input/wtq_p4b_targeted_fix_affected_slice.jsonl",
        ],
    },
    "tabfact": {
        "source_path": MYAGENT_ROOT / "datasets_ready/full/tabfact_test.jsonl",
        "exclusion_paths": [
            MACT_RUNS / "qwen3_32b_tabfact_policy_v6b_full200_20260731_1255/input/tabfact_full200.jsonl",
            COARSE_RUN / "input/tabfact_diagnostic_gate50.jsonl",
            P4B_RUN / "input/tabfact_newseed_gate50.jsonl",
            P4B_RUN / "input/tabfact_p4a_fix_affected_slice.jsonl",
        ],
    },
    "crt": {
        "source_path": MYAGENT_ROOT / "datasets_ready/full/crt.jsonl",
        "exclusion_paths": [
            MACT_RUNS / "qwen3_32b_crt_full200_current_20260730_1822/input/crt_blind200.jsonl",
            COARSE_RUN / "input/crt_diagnostic_gate50.jsonl",
            P4B_RUN / "input/crt_newseed_gate50.jsonl",
            P4B_RUN / "input/crt_p4a_fix_affected_slice.jsonl",
        ],
    },
}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def row_id(row: dict[str, Any]) -> str:
    value = str(row.get("id") or "")
    if not value:
        raise ValueError("Every source row must have a non-empty id")
    return value


def load_exclusions(paths: list[Path]) -> tuple[set[str], list[dict[str, Any]]]:
    excluded: set[str] = set()
    details: list[dict[str, Any]] = []
    for path in paths:
        rows = read_jsonl(path)
        ids = {row_id(row) for row in rows}
        excluded.update(ids)
        details.append(
            {
                "path": str(path),
                "rows": len(rows),
                "unique_ids": len(ids),
            }
        )
    return excluded, details


def select_rows(
    *,
    rows: list[dict[str, Any]],
    task: str,
    seed: int,
    excluded: set[str],
    limit: int,
) -> list[dict[str, Any]]:
    candidates = [row for row in rows if row_id(row) not in excluded]
    rng = random.Random(seed * 100 + TASKS.index(task))
    rng.shuffle(candidates)
    selected = candidates[:limit]
    if len(selected) != limit:
        raise RuntimeError(
            f"{task}: expected {limit} rows, got {len(selected)} after exclusions"
        )
    ids = [row_id(row) for row in selected]
    if len(set(ids)) != len(ids):
        raise RuntimeError(f"{task}: selected duplicate ids")
    overlap = set(ids) & excluded
    if overlap:
        raise RuntimeError(f"{task}: selected rows overlap excluded ids: {sorted(overlap)[:5]}")
    return selected


def render_summary(manifest: dict[str, Any]) -> str:
    lines = [
        "# E3 Multi-Seed Gate-50 Input Generation",
        "",
        f"Run dir: `{RUN_DIR}`",
        "",
        "Purpose: prepare two additional non-overlapping Gate-50 seeds for Qwen3-32B MyAgent vs MACT stability validation.",
        "",
        "| Seed | Dataset | Source Rows | Base Excluded IDs | Prior Seed Excluded IDs | Candidate Rows | Selected Rows | Input |",
        "|---|---|---:|---:|---:|---:|---:|---|",
    ]
    for seed_label, seed_item in manifest["seeds"].items():
        for task in TASKS:
            item = seed_item["datasets"][task]
            lines.append(
                f"| {seed_label} | {task} | {item['source_rows']} | "
                f"{item['base_excluded_unique_ids']} | {item['prior_seed_excluded_unique_ids']} | "
                f"{item['candidate_rows_after_exclusion']} | {item['selected_rows']} | "
                f"`{item['input_path']}` |"
            )
    lines.extend(
        [
            "",
            "Sampling rule: deterministic shuffle over the full dataset with fixed seed, after excluding frozen full200, coarse diagnostic Gate-50, P4b new-seed Gate-50, targeted affected slices, and prior seeds in this package.",
            "",
            "Execution is pending because the local Qwen3-32B endpoints were unavailable when this package was created.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    manifest: dict[str, Any] = {
        "run_name": RUN_DIR.name,
        "run_dir": str(RUN_DIR),
        "created_at_local": "2026-08-01 22:31 CST",
        "stage": "E3 multi-seed Gate-50 preparation",
        "purpose": "Additional random-seed stability validation for patent-facing MyAgent selective risk collaboration evidence.",
        "limit_per_dataset": LIMIT_PER_DATASET,
        "seeds": {},
        "global_validation": {},
    }
    selected_by_task: dict[str, set[str]] = {task: set() for task in TASKS}

    for seed_label, seed in SEEDS.items():
        seed_manifest: dict[str, Any] = {
            "seed": seed,
            "datasets": {},
        }
        for task in TASKS:
            spec = DATASETS[task]
            source_rows = read_jsonl(spec["source_path"])
            base_excluded, exclusion_details = load_exclusions(spec["exclusion_paths"])
            prior_seed_excluded = set(selected_by_task[task])
            excluded = base_excluded | prior_seed_excluded
            selected_rows = select_rows(
                rows=source_rows,
                task=task,
                seed=seed,
                excluded=excluded,
                limit=LIMIT_PER_DATASET,
            )
            selected_ids = [row_id(row) for row in selected_rows]
            selected_by_task[task].update(selected_ids)
            output_path = RUN_DIR / "input" / seed_label / f"{task}_{seed_label}_gate50.jsonl"
            write_jsonl(output_path, selected_rows)

            seed_manifest["datasets"][task] = {
                "source_path": str(spec["source_path"]),
                "source_rows": len(source_rows),
                "exclusions": exclusion_details,
                "base_excluded_unique_ids": len(base_excluded),
                "prior_seed_excluded_unique_ids": len(prior_seed_excluded),
                "total_excluded_unique_ids": len(excluded),
                "candidate_rows_after_exclusion": len(source_rows) - len(excluded),
                "input_path": str(output_path),
                "selected_rows": len(selected_rows),
                "selected_ids": selected_ids,
            }
        manifest["seeds"][seed_label] = seed_manifest

    manifest["global_validation"] = {
        "seeds": list(SEEDS),
        "datasets": list(TASKS),
        "rows_per_dataset_per_seed": LIMIT_PER_DATASET,
        "total_input_rows": len(SEEDS) * len(TASKS) * LIMIT_PER_DATASET,
        "cross_seed_overlap_by_dataset": {
            task: 0 for task in TASKS
        },
    }
    (RUN_DIR / "multiseed_gate50_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (RUN_DIR / "input_generation_summary.md").write_text(
        render_summary(manifest),
        encoding="utf-8",
    )
    print(json.dumps(manifest["global_validation"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
