#!/usr/bin/env python3
"""Tests for the E3 guard-validation input package builder."""

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from collections import Counter
from pathlib import Path


RUN_DIR = Path(__file__).resolve().parents[1]
BUILDER_PATH = RUN_DIR / "build_guard_validation_inputs.py"


def load_builder():
    spec = importlib.util.spec_from_file_location("build_guard_validation_inputs", BUILDER_PATH)
    if spec is None or spec.loader is None:
        raise AssertionError(f"Cannot import builder from {BUILDER_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_jsonl(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


class GuardValidationInputsTest(unittest.TestCase):
    def test_build_package_counts_traceability_and_no_harm(self) -> None:
        builder = load_builder()
        with tempfile.TemporaryDirectory() as tmp_dir:
            output_dir = Path(tmp_dir)
            summary = builder.build_package(output_dir)

            self.assertEqual(summary["total_rows"], 30)
            self.assertEqual(
                summary["role_counts"],
                {"representative_wrong": 12, "no_harm_correct": 18},
            )
            self.assertEqual(
                summary["dataset_counts"],
                {"wtq": 10, "tabfact": 8, "crt": 12},
            )
            self.assertEqual(summary["duplicate_source_keys"], [])
            self.assertEqual(summary["validation_decision"], "ready_for_guard_implementation_not_model_run")
            self.assertEqual(summary["gate_targets"]["representative_wrong_recovery_min"], 7)
            self.assertEqual(summary["gate_targets"]["no_harm_correct_min"], 18)

            manifest = json.loads((output_dir / "input" / "input_manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["total_rows"], 30)
            self.assertEqual(manifest["dataset_counts"], summary["dataset_counts"])

            all_rows: list[dict] = []
            for dataset, expected_count in {"wtq": 10, "tabfact": 8, "crt": 12}.items():
                rows = read_jsonl(output_dir / "input" / f"{dataset}_e3_guard_validation.jsonl")
                self.assertEqual(len(rows), expected_count)
                all_rows.extend(rows)

            role_counts = Counter(row["validation_metadata"]["slice_role"] for row in all_rows)
            self.assertEqual(dict(role_counts), {"representative_wrong": 12, "no_harm_correct": 18})

            source_keys = [
                tuple(row["validation_metadata"][key] for key in ("source_seed", "source_dataset", "source_id"))
                for row in all_rows
            ]
            self.assertEqual(len(source_keys), len(set(source_keys)))

            for row in all_rows:
                meta = row["validation_metadata"]
                self.assertIn(meta["priority"], {"P0", "P1", "P2"})
                self.assertEqual(row["source_dataset"], meta["source_dataset"])
                if meta["slice_role"] == "representative_wrong":
                    self.assertFalse(meta["source_correct"])
                if meta["slice_role"] == "no_harm_correct":
                    self.assertTrue(meta["source_correct"])

            proxy_rows = [
                row
                for row in all_rows
                if row["validation_metadata"].get("no_harm_proxy_for")
                == "tabfact_false_negative_entailment_boundary"
            ]
            self.assertEqual(len(proxy_rows), 2)


if __name__ == "__main__":
    unittest.main()
