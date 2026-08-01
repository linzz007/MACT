#!/usr/bin/env python3
"""Validate the E3 multi-seed Gate-50 package before running or committing."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


RUN_DIR = Path(__file__).resolve().parent
TASKS = ("wtq", "tabfact", "crt")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def ids(path: Path) -> set[str]:
    return {str(row.get("id") or "") for row in read_jsonl(path)}


def main() -> None:
    manifest_path = RUN_DIR / "multiseed_gate50_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    errors: list[str] = []
    selected_by_task: dict[str, dict[str, set[str]]] = {task: {} for task in TASKS}

    for seed_label, seed_item in manifest["seeds"].items():
        for task in TASKS:
            item = seed_item["datasets"][task]
            input_path = Path(item["input_path"])
            rows = read_jsonl(input_path)
            row_ids = [str(row.get("id") or "") for row in rows]
            if len(rows) != 50:
                errors.append(f"{seed_label}/{task}: expected 50 rows, got {len(rows)}")
            if len(set(row_ids)) != len(row_ids):
                errors.append(f"{seed_label}/{task}: duplicate selected ids")
            excluded: set[str] = set()
            for exclusion in item["exclusions"]:
                excluded.update(ids(Path(exclusion["path"])))
            overlap = set(row_ids) & excluded
            if overlap:
                errors.append(f"{seed_label}/{task}: overlaps base exclusions: {sorted(overlap)[:5]}")
            selected_by_task[task][seed_label] = set(row_ids)

    for task in TASKS:
        labels = sorted(selected_by_task[task])
        for index, left in enumerate(labels):
            for right in labels[index + 1 :]:
                overlap = selected_by_task[task][left] & selected_by_task[task][right]
                if overlap:
                    errors.append(f"{task}: {left}/{right} selected-id overlap: {sorted(overlap)[:5]}")

    scripts = [
        "run_seed_myagent_gate50.sh",
        "run_seed_mact_gate50.sh",
        "run_seed_paired_compare.sh",
        "summarize_seed_myagent.py",
        "render_seed_paired_summary.py",
        "healthcheck_vllm.sh",
        "checkpoint_to_git.sh",
    ]
    for script in scripts:
        if not (RUN_DIR / script).exists():
            errors.append(f"missing script: {script}")

    result = {
        "run_dir": str(RUN_DIR),
        "status": "fail" if errors else "pass",
        "errors": errors,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
