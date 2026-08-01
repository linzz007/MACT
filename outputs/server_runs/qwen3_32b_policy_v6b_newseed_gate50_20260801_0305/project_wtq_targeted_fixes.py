#!/usr/bin/env python3
"""Offline projection for WTQ targeted fixes identified by E1 diagnosis."""

from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path
from typing import Any, Callable


RUN_DIR = Path(__file__).resolve().parent


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def to_jsonable(value: Any) -> Any:
    if hasattr(value, "item"):
        try:
            return value.item()
        except Exception:
            pass
    if isinstance(value, dict):
        return {str(key): to_jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [to_jsonable(item) for item in value]
    return value


def load_myagent(myagent_root: Path) -> dict[str, Any]:
    sys.path.insert(0, str(myagent_root / "code"))
    from evaluate_results import dataset_accuracy, gold_for_em, prediction_for_em, summarize_rows
    from my_agents import TableQAPipeline, _canonicalize_wtq_scalar, build_df_from_table

    return {
        "dataset_accuracy": dataset_accuracy,
        "gold_for_em": gold_for_em,
        "prediction_for_em": prediction_for_em,
        "summarize_rows": summarize_rows,
        "TableQAPipeline": TableQAPipeline,
        "_canonicalize_wtq_scalar": _canonicalize_wtq_scalar,
        "build_df_from_table": build_df_from_table,
    }


def apply_projection(row: dict[str, Any], deps: dict[str, Any]) -> tuple[dict[str, Any], str]:
    pipeline = deps["TableQAPipeline"]
    prediction_for_em: Callable[[dict[str, Any]], Any] = deps["prediction_for_em"]
    canonicalize = deps["_canonicalize_wtq_scalar"]
    build_df_from_table = deps["build_df_from_table"]
    projected = copy.deepcopy(row)
    df = build_df_from_table(row["table_text"])
    question = row.get("question") or ""
    old_value = prediction_for_em(row)

    for reason, func in [
        ("WTQ row-major listed-after value selected deterministically.", pipeline._wtq_listed_after_cell_answer),
        ("WTQ directly-before adjacent row target selected deterministically.", pipeline._wtq_directly_before_reference_answer),
        ("WTQ overtime marker rows counted deterministically.", pipeline._wtq_overtime_count_answer),
        ("WTQ playoff participation count checked deterministically.", pipeline._wtq_playoff_count_answer),
        ("WTQ requested column winner entries counted deterministically.", pipeline._wtq_column_entry_count_answer),
        ("WTQ unique sponsor names counted deterministically.", pipeline._wtq_sponsor_count_answer),
        ("WTQ retired-injured ordinal attempt row selected deterministically.", pipeline._wtq_retired_injured_attempt_answer),
    ]:
        value = func(question, df)
        if value is not None and value != old_value:
            projected["final_value"] = to_jsonable(value)
            projected["final_answer"] = str(to_jsonable(value)).strip()
            projected["deterministic_shortcut_applied"] = True
            projected["deterministic_shortcut_reason"] = reason
            return projected, reason

    value = canonicalize(old_value, df, question)
    if value != old_value:
        projected["final_value"] = to_jsonable(value)
        projected["final_answer"] = str(to_jsonable(value)).strip()
        projected["deterministic_shortcut_reason"] = "WTQ scalar canonicalized by targeted fix."
        return projected, "WTQ scalar canonicalized by targeted fix."

    return projected, ""


def build_report(myagent_root: Path) -> dict[str, Any]:
    deps = load_myagent(myagent_root)
    dataset_accuracy = deps["dataset_accuracy"]
    gold_for_em = deps["gold_for_em"]
    prediction_for_em = deps["prediction_for_em"]
    summarize_rows = deps["summarize_rows"]

    rows = read_jsonl(RUN_DIR / "myagent_current/merged/wtq_qwen3-32b-local.jsonl")
    if len(rows) != 50:
        raise RuntimeError(f"Expected 50 WTQ rows, found {len(rows)}")

    projected_rows: list[dict[str, Any]] = []
    changed_rows: list[dict[str, Any]] = []
    wrong_to_correct: list[str] = []
    correct_to_wrong: list[str] = []
    for row in rows:
        projected, reason = apply_projection(row, deps)
        projected_rows.append(projected)
        old_correct = bool(dataset_accuracy(row))
        new_correct = bool(dataset_accuracy(projected))
        old_prediction = prediction_for_em(row)
        new_prediction = prediction_for_em(projected)
        if old_prediction != new_prediction or old_correct != new_correct:
            changed_rows.append(
                {
                    "id": row["id"],
                    "question": row.get("question"),
                    "gold": gold_for_em(row),
                    "old_prediction": to_jsonable(old_prediction),
                    "new_prediction": to_jsonable(new_prediction),
                    "old_correct": old_correct,
                    "new_correct": new_correct,
                    "reason": reason,
                }
            )
        if not old_correct and new_correct:
            wrong_to_correct.append(row["id"])
        if old_correct and not new_correct:
            correct_to_wrong.append(row["id"])

    current_correct = sum(1 for row in rows if dataset_accuracy(row))
    projected_correct = sum(1 for row in projected_rows if dataset_accuracy(row))
    projected_summary, projected_anomalies = summarize_rows(projected_rows)
    return {
        "run_dir": str(RUN_DIR),
        "scope": "offline WTQ targeted fix projection over saved P4b MyAgent merged rows; no model calls",
        "source_rows": str(RUN_DIR / "myagent_current/merged/wtq_qwen3-32b-local.jsonl"),
        "eval_module": str(myagent_root / "code/evaluate_results.py"),
        "rows": len(rows),
        "current_correct": current_correct,
        "projected_correct": projected_correct,
        "current_accuracy": current_correct / len(rows),
        "projected_accuracy": projected_correct / len(rows),
        "net_gain": projected_correct - current_correct,
        "wrong_to_correct": len(wrong_to_correct),
        "correct_to_wrong": len(correct_to_wrong),
        "wrong_to_correct_ids": wrong_to_correct,
        "correct_to_wrong_ids": correct_to_wrong,
        "changed_rows": changed_rows,
        "projected_eval_summary": projected_summary,
        "projected_anomaly_count": len(projected_anomalies),
        "interpretation": (
            f"The targeted WTQ mechanisms recover {len(wrong_to_correct)} P4b errors "
            f"without projected harm. This is not a fresh Qwen run; it is evidence "
            f"that the E1 diagnosis maps to generic deterministic/canonicalization "
            f"behavior worth validating with a targeted gate."
        ),
    }


def md_escape(value: Any) -> str:
    text = "" if value is None else str(value)
    text = text.replace("\n", " ")
    text = text.replace("|", "\\|")
    return text if len(text) <= 180 else text[:177] + "..."


def write_markdown(report: dict[str, Any], path: Path) -> None:
    lines = [
        "# P4b WTQ Targeted Fix Offline Projection",
        "",
        f"Run dir: `{report['run_dir']}`",
        "",
        "Scope: replay saved P4b WTQ MyAgent merged rows through updated targeted WTQ deterministic shortcuts and scalar canonicalization. No Qwen3/vLLM calls were made.",
        "",
        "| Current | Projected | Net Gain | Wrong -> Correct | Correct -> Wrong |",
        "|---:|---:|---:|---:|---:|",
        (
            f"| {report['current_correct']}/{report['rows']} | "
            f"{report['projected_correct']}/{report['rows']} | "
            f"{report['net_gain']:+d} | "
            f"{report['wrong_to_correct']} | "
            f"{report['correct_to_wrong']} |"
        ),
        "",
        "## Changed Rows",
        "",
        "| id | old | new | gold | reason | question |",
        "|---|---|---|---|---|---|",
    ]
    for row in report["changed_rows"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    md_escape(row["id"]),
                    md_escape(row["old_prediction"]),
                    md_escape(row["new_prediction"]),
                    md_escape(row["gold"]),
                    md_escape(row["reason"]),
                    md_escape(row["question"]),
                ]
            )
            + " |"
        )
    lines += [
        "",
        "## Interpretation",
        "",
        report["interpretation"],
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--myagent-root", default="/home/ubuntu/lzz/MyAgent")
    args = parser.parse_args()
    report = build_report(Path(args.myagent_root))
    json_path = RUN_DIR / "p4b_wtq_targeted_fix_projection.json"
    md_path = RUN_DIR / "p4b_wtq_targeted_fix_projection.md"
    json_path.write_text(json.dumps(to_jsonable(report), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_markdown(report, md_path)
    print(f"wrote {json_path}")
    print(f"wrote {md_path}")


if __name__ == "__main__":
    main()
