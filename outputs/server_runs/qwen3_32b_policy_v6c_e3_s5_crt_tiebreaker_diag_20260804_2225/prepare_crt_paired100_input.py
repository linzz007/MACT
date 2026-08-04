#!/usr/bin/env python3
"""Prepare combined Seed-C/Seed-D CRT Gate-50 input for S5 full paired rerun."""

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


def main() -> None:
    combined: list[dict[str, Any]] = []
    manifest: dict[str, Any] = {
        "run_dir": str(RUN_DIR),
        "selection_rule": "seed_c CRT gate50 followed by seed_d CRT gate50 from the frozen E3 source input",
        "seeds": {},
    }
    for seed in SEEDS:
        source_path = SOURCE_INPUT / seed / f"crt_{seed}_gate50.jsonl"
        rows = read_jsonl(source_path)
        combined.extend(rows)
        manifest["seeds"][seed] = {
            "source_path": str(source_path),
            "rows": len(rows),
            "first_id": rows[0].get("id") if rows else "",
            "last_id": rows[-1].get("id") if rows else "",
        }
    output_path = RUN_DIR / "input" / "paired_crt100" / "crt_s5_paired100_seed_c_seed_d.jsonl"
    write_jsonl(output_path, combined)
    manifest["combined_output_path"] = str(output_path)
    manifest["combined_rows"] = len(combined)
    manifest_path = RUN_DIR / "input" / "paired_crt100" / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
