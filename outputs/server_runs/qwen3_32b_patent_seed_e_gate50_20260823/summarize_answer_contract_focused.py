#!/usr/bin/env python3
"""Summarize focused validation for the Seed-E answer-contract patch."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any, Dict, List


RUN_DIR = Path(__file__).resolve().parent
MYAGENT_ROOT = Path("/home/ubuntu/lzz/MyAgent")
OUTPUT_ROOT = RUN_DIR / "diagnostics" / "answer_contract_patch_focused_20260824"
SUMMARY_DIR = RUN_DIR / "summary"
MODEL_NAME = "qwen3-32b-local"
TASKS = ("wtq", "crt")


def _load_eval_module():
    path = MYAGENT_ROOT / "code" / "evaluate_results.py"
    spec = importlib.util.spec_from_file_location("evaluate_results", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load evaluator from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


EVAL = _load_eval_module()


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def token_total(row: Dict[str, Any]) -> int:
    api = row.get("api_metrics") or {}
    if api.get("total_tokens") is not None:
        return int(api.get("total_tokens") or 0)
    return int((api.get("prompt_tokens") or 0) + (api.get("completion_tokens") or 0))


def short(value: Any, limit: int = 120) -> str:
    text = " ".join(str(value if value is not None else "").replace("\n", " ").split())
    return text[:limit] + ("..." if len(text) > limit else "")


def row_id(row: Dict[str, Any]) -> str:
    return str(row.get("id") or row.get("sample_id") or "")


def main() -> None:
    SUMMARY_DIR.mkdir(parents=True, exist_ok=True)
    report: Dict[str, Any] = {
        "run_dir": str(RUN_DIR),
        "output_root": str(OUTPUT_ROOT),
        "tasks": {},
    }
    markdown: List[str] = [
        "# Answer-Contract Focused Validation Summary",
        "",
        f"Run dir: `{RUN_DIR}`",
        f"Output root: `{OUTPUT_ROOT}`",
        "",
        "| Task | Rows | Old Correct | New Correct | Fixed | Regressed | New Avg Token |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]

    all_records: List[Dict[str, Any]] = []
    for task in TASKS:
        input_path = RUN_DIR / "input" / "diagnostic" / f"seed_e_answer_contract_{task}.jsonl"
        old_path = RUN_DIR / "myagent_seed_e" / "merged" / f"{task}_{MODEL_NAME}.jsonl"
        new_path = OUTPUT_ROOT / "merged" / f"{task}_{MODEL_NAME}.jsonl"
        eval_path = OUTPUT_ROOT / "eval" / f"{task}_{MODEL_NAME}_eval.json"
        for required in (input_path, old_path, new_path, eval_path):
            if not required.exists():
                raise FileNotFoundError(required)

        target_ids = [row_id(row) for row in read_jsonl(input_path)]
        old_by_id = {row_id(row): row for row in read_jsonl(old_path)}
        new_by_id = {row_id(row): row for row in read_jsonl(new_path)}
        eval_data = read_json(eval_path)

        records: List[Dict[str, Any]] = []
        for sample_id in target_ids:
            old = old_by_id[sample_id]
            new = new_by_id[sample_id]
            old_correct = bool(EVAL.dataset_accuracy(old))
            new_correct = bool(EVAL.dataset_accuracy(new))
            if not old_correct and new_correct:
                effect = "fixed"
            elif old_correct and not new_correct:
                effect = "regressed"
            elif old_correct and new_correct:
                effect = "kept_correct"
            else:
                effect = "still_wrong"
            record = {
                "id": sample_id,
                "task": task,
                "question": old.get("question") or old.get("statement"),
                "gold": EVAL.gold_for_em(old),
                "old_prediction": EVAL.prediction_for_em(old),
                "new_prediction": EVAL.prediction_for_em(new),
                "old_correct": old_correct,
                "new_correct": new_correct,
                "effect": effect,
                "old_tokens": token_total(old),
                "new_tokens": token_total(new),
                "new_route": new.get("route_type"),
                "new_risk": new.get("risk_level"),
                "new_contract": new.get("answer_contract"),
                "new_deterministic_shortcut": new.get("deterministic_shortcut_reason"),
            }
            records.append(record)
            all_records.append(record)

        fixed = sum(1 for row in records if row["effect"] == "fixed")
        regressed = sum(1 for row in records if row["effect"] == "regressed")
        old_correct_count = sum(1 for row in records if row["old_correct"])
        new_correct_count = sum(1 for row in records if row["new_correct"])
        avg_new_tokens = sum(row["new_tokens"] for row in records) / max(1, len(records))
        report["tasks"][task] = {
            "eval": eval_data,
            "rows": len(records),
            "old_correct": old_correct_count,
            "new_correct": new_correct_count,
            "fixed": fixed,
            "regressed": regressed,
            "avg_new_tokens": avg_new_tokens,
            "records": records,
        }
        markdown.append(
            f"| {task} | {len(records)} | {old_correct_count}/{len(records)} | "
            f"{new_correct_count}/{len(records)} | {fixed} | {regressed} | {avg_new_tokens:.2f} |"
        )

    total_rows = len(all_records)
    total_old = sum(1 for row in all_records if row["old_correct"])
    total_new = sum(1 for row in all_records if row["new_correct"])
    total_fixed = sum(1 for row in all_records if row["effect"] == "fixed")
    total_regressed = sum(1 for row in all_records if row["effect"] == "regressed")
    report["overall"] = {
        "rows": total_rows,
        "old_correct": total_old,
        "new_correct": total_new,
        "fixed": total_fixed,
        "regressed": total_regressed,
    }
    markdown.extend(
        [
            "",
            f"Overall: old `{total_old}/{total_rows}`, new `{total_new}/{total_rows}`, "
            f"fixed `{total_fixed}`, regressed `{total_regressed}`.",
            "",
            "## Row Details",
            "",
        ]
    )
    for record in all_records:
        markdown.append(
            f"- `{record['id']}` ({record['task']}, {record['effect']}): "
            f"{short(record['question'])}"
        )
        markdown.append(
            f"  Gold: `{short(record['gold'], 80)}`; old: "
            f"`{short(record['old_prediction'], 80)}`; new: "
            f"`{short(record['new_prediction'], 80)}`; new tokens: `{record['new_tokens']}`."
        )

    json_path = SUMMARY_DIR / "answer_contract_patch_focused_summary.json"
    md_path = SUMMARY_DIR / "answer_contract_patch_focused_summary.md"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text("\n".join(markdown) + "\n", encoding="utf-8")
    print(f"wrote {md_path}")
    print(f"wrote {json_path}")


if __name__ == "__main__":
    main()
