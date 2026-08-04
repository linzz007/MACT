#!/usr/bin/env python3
"""Prepare paired CRT affected/no-harm slice inputs for S5 validation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


RUN_DIR = Path(__file__).resolve().parent
SOURCE_INPUT = Path("/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_multiseed_gate50_20260801_2231/input")
SEEDS = ("seed_c", "seed_d")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def category_ids(seed: str, category: str) -> set[str]:
    path = RUN_DIR / "cases" / f"{seed}_crt_{category}.jsonl"
    return {str(row["id"]) for row in read_jsonl(path)}


def replay_changed_ids(seed: str) -> set[str]:
    path = RUN_DIR / "summary" / "s5_crt_canonicalizer_replay_summary.json"
    if not path.exists():
        return set()
    summary = json.loads(path.read_text(encoding="utf-8"))
    return {
        str(row["id"])
        for row in summary["seeds"][seed].get("flips", [])
        if row.get("original_final_value") != row.get("patched_final_value")
    }


def main() -> None:
    manifest: dict[str, Any] = {
        "run_dir": str(RUN_DIR),
        "selection_rule": "all mact_only + all myagent_only + replay-normalized changed ids",
        "seeds": {},
    }
    all_rows: list[dict[str, Any]] = []
    for seed in SEEDS:
        ids = sorted(
            category_ids(seed, "mact_only")
            | category_ids(seed, "myagent_only")
            | replay_changed_ids(seed)
        )
        source_path = SOURCE_INPUT / seed / f"crt_{seed}_gate50.jsonl"
        source_rows = read_jsonl(source_path)
        by_id = {str(row["id"]): row for row in source_rows}
        selected = [by_id[row_id] for row_id in ids if row_id in by_id]
        missing = [row_id for row_id in ids if row_id not in by_id]
        if missing:
            raise SystemExit(f"{seed}: missing ids in source input: {missing}")
        output_path = RUN_DIR / "input" / "affected_slice" / seed / f"crt_{seed}_s5_affected.jsonl"
        write_jsonl(output_path, selected)
        all_rows.extend(selected)
        manifest["seeds"][seed] = {
            "source_path": str(source_path),
            "output_path": str(output_path),
            "ids": ids,
            "rows": len(selected),
        }

    all_output = RUN_DIR / "input" / "affected_slice" / "crt_s5_affected_all.jsonl"
    write_jsonl(all_output, all_rows)
    manifest["combined_output_path"] = str(all_output)
    manifest["combined_rows"] = len(all_rows)
    manifest_path = RUN_DIR / "input" / "affected_slice" / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
