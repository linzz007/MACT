#!/usr/bin/env python3
"""Build a non-overlapping Seed-E Gate-50 input package."""

from __future__ import annotations

import json
import random
from pathlib import Path
from typing import Any


RUN_DIR = Path(__file__).resolve().parent
MYAGENT_ROOT = Path("/home/ubuntu/lzz/MyAgent")
MACT_RUNS = Path("/home/ubuntu/lzz/MACT/outputs/server_runs")
FORMAL_RUN = MACT_RUNS / "qwen3_32b_baseline_formal200_20260812_1505"
P4B_RUN = MACT_RUNS / "qwen3_32b_policy_v6b_newseed_gate50_20260801_0305"
MULTISEED_RUN = MACT_RUNS / "qwen3_32b_policy_v6b_multiseed_gate50_20260801_2231"
COARSE_RUN = MACT_RUNS / "qwen3_32b_policy_v6b_coarse_ablation_gate50_20260801_0040"

LIMIT_PER_DATASET = 50
SEED_LABEL = "seed_e"
SEED = 20260823
TASKS = ("wtq", "tabfact", "crt")

DATASETS = {
    "wtq": {
        "source_path": MYAGENT_ROOT / "datasets_ready/full/wtq_unseen.jsonl",
        "exclusion_paths": [
            FORMAL_RUN / "input/formal200/wtq.jsonl",
            FORMAL_RUN / "input/ablation50/wtq.jsonl",
            MACT_RUNS / "qwen3_32b_wtq_policy_v6b_full200_20260731_1115/input/wtq_full200.jsonl",
            COARSE_RUN / "input/wtq_diagnostic_gate50.jsonl",
            P4B_RUN / "input/wtq_newseed_gate50.jsonl",
            P4B_RUN / "input/wtq_p4b_targeted_fix_affected_slice.jsonl",
            MULTISEED_RUN / "input/seed_c/wtq_seed_c_gate50.jsonl",
            MULTISEED_RUN / "input/seed_d/wtq_seed_d_gate50.jsonl",
        ],
    },
    "tabfact": {
        "source_path": MYAGENT_ROOT / "datasets_ready/full/tabfact_test.jsonl",
        "exclusion_paths": [
            FORMAL_RUN / "input/formal200/tabfact.jsonl",
            FORMAL_RUN / "input/ablation50/tabfact.jsonl",
            MACT_RUNS / "qwen3_32b_tabfact_policy_v6b_full200_20260731_1255/input/tabfact_full200.jsonl",
            COARSE_RUN / "input/tabfact_diagnostic_gate50.jsonl",
            P4B_RUN / "input/tabfact_newseed_gate50.jsonl",
            P4B_RUN / "input/tabfact_p4a_fix_affected_slice.jsonl",
            MULTISEED_RUN / "input/seed_c/tabfact_seed_c_gate50.jsonl",
            MULTISEED_RUN / "input/seed_d/tabfact_seed_d_gate50.jsonl",
        ],
    },
    "crt": {
        "source_path": MYAGENT_ROOT / "datasets_ready/full/crt.jsonl",
        "exclusion_paths": [
            FORMAL_RUN / "input/formal200/crt.jsonl",
            FORMAL_RUN / "input/ablation50/crt.jsonl",
            MACT_RUNS / "qwen3_32b_crt_full200_current_20260730_1822/input/crt_blind200.jsonl",
            COARSE_RUN / "input/crt_diagnostic_gate50.jsonl",
            P4B_RUN / "input/crt_newseed_gate50.jsonl",
            P4B_RUN / "input/crt_p4a_fix_affected_slice.jsonl",
            MULTISEED_RUN / "input/seed_c/crt_seed_c_gate50.jsonl",
            MULTISEED_RUN / "input/seed_d/crt_seed_d_gate50.jsonl",
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
        if not path.exists():
            details.append({"path": str(path), "exists": False, "rows": 0, "unique_ids": 0})
            continue
        rows = read_jsonl(path)
        ids = {row_id(row) for row in rows}
        excluded.update(ids)
        details.append(
            {
                "path": str(path),
                "exists": True,
                "rows": len(rows),
                "unique_ids": len(ids),
            }
        )
    return excluded, details


def select_rows(rows: list[dict[str, Any]], task: str, excluded: set[str]) -> list[dict[str, Any]]:
    candidates = [row for row in rows if row_id(row) not in excluded]
    rng = random.Random(SEED * 100 + TASKS.index(task))
    rng.shuffle(candidates)
    selected = candidates[:LIMIT_PER_DATASET]
    if len(selected) != LIMIT_PER_DATASET:
        raise RuntimeError(f"{task}: expected {LIMIT_PER_DATASET}, got {len(selected)}")
    selected_ids = [row_id(row) for row in selected]
    if len(set(selected_ids)) != len(selected_ids):
        raise RuntimeError(f"{task}: duplicate selected ids")
    overlap = set(selected_ids) & excluded
    if overlap:
        raise RuntimeError(f"{task}: selected rows overlap exclusions: {sorted(overlap)[:5]}")
    return selected


def render_summary(manifest: dict[str, Any]) -> str:
    lines = [
        "# Seed-E Gate-50 Input Generation",
        "",
        f"Run dir: `{RUN_DIR}`",
        "",
        "Purpose: prepare a non-overlapping paired Gate-50 seed for Qwen3-32B MyAgent vs MACT stability validation.",
        "",
        "| Dataset | Source Rows | Excluded IDs | Candidate Rows | Selected Rows | Input |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for task in TASKS:
        item = manifest["datasets"][task]
        lines.append(
            f"| {task} | {item['source_rows']} | {item['excluded_unique_ids']} | "
            f"{item['candidate_rows_after_exclusion']} | {item['selected_rows']} | "
            f"`{item['input_path']}` |"
        )
    lines.extend(
        [
            "",
            "Sampling rule: deterministic shuffle over full dataset rows using seed `20260823`, after excluding Formal-200, ablation50, prior new-seed, targeted slices, and Seed-C/D inputs.",
            "",
            "Execution status: prepared only. No model was called while generating this package.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    manifest: dict[str, Any] = {
        "run_name": RUN_DIR.name,
        "run_dir": str(RUN_DIR),
        "created_at_local": "2026-08-23 CST",
        "stage": "Patent multi-seed Gate-50 preparation",
        "purpose": "Additional paired random-seed stability validation for patent-facing MyAgent vs MACT evidence.",
        "seed_label": SEED_LABEL,
        "seed": SEED,
        "limit_per_dataset": LIMIT_PER_DATASET,
        "datasets": {},
    }
    for task in TASKS:
        spec = DATASETS[task]
        source_rows = read_jsonl(spec["source_path"])
        excluded, exclusion_details = load_exclusions(spec["exclusion_paths"])
        selected_rows = select_rows(source_rows, task, excluded)
        output_path = RUN_DIR / "input" / f"{task}_{SEED_LABEL}_gate50.jsonl"
        write_jsonl(output_path, selected_rows)
        manifest["datasets"][task] = {
            "source_path": str(spec["source_path"]),
            "source_rows": len(source_rows),
            "exclusions": exclusion_details,
            "excluded_unique_ids": len(excluded),
            "candidate_rows_after_exclusion": len(source_rows) - len(excluded),
            "input_path": str(output_path),
            "selected_rows": len(selected_rows),
            "selected_ids": [row_id(row) for row in selected_rows],
        }
    manifest["global_validation"] = {
        "datasets": list(TASKS),
        "rows_per_dataset": LIMIT_PER_DATASET,
        "total_rows": len(TASKS) * LIMIT_PER_DATASET,
        "selected_unique_ids_by_dataset": {
            task: len(set(manifest["datasets"][task]["selected_ids"])) for task in TASKS
        },
    }
    (RUN_DIR / "seed_e_manifest.json").write_text(
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
