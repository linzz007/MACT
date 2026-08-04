#!/usr/bin/env python3
"""Summarize the real S5 affected-slice rerun against old MyAgent and MACT."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


RUN_DIR = Path(__file__).resolve().parent
MYAGENT_ROOT = Path("/home/ubuntu/lzz/MyAgent")
S3_RUN = Path("/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6b_e3_s3_current_rerun_after_guard_20260804_1425")
S4_RUN = Path("/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6c_e3_s4_paired_mact_20260804_1626")
S5_MERGED = RUN_DIR / "myagent_s5_affected_slice" / "merged" / "crt_qwen3-32b-local.jsonl"
SEEDS = ("seed_c", "seed_d")

sys.path.insert(0, str(MYAGENT_ROOT / "code"))
from evaluate_results import (  # noqa: E402
    dataset_accuracy,
    gold_for_em,
    load_jsonl,
    prediction_for_em,
    summarize_rows,
)


def old_myagent_path(seed: str) -> Path:
    return S3_RUN / "myagent_s3_after_guard" / seed / "merged" / "crt_qwen3-32b-local.jsonl"


def mact_path(seed: str) -> Path:
    return S4_RUN / "mact" / seed / f"crt_mact_{seed}_gate50.jsonl"


def token_total(row: dict[str, Any]) -> int:
    api = row.get("api_metrics") or {}
    if api:
        return int(api.get("total_tokens") or (api.get("prompt_tokens") or 0) + (api.get("completion_tokens") or 0))
    llm = row.get("llm_metrics") or {}
    return int(llm.get("total_tokens_est") or 0)


def row_seed(row: dict[str, Any]) -> str:
    row_id = str(row.get("id") or "")
    manifest = json.loads((RUN_DIR / "input" / "affected_slice" / "manifest.json").read_text(encoding="utf-8"))
    for seed, item in manifest["seeds"].items():
        if row_id in item["ids"]:
            return seed
    raise KeyError(f"Cannot locate seed for {row_id}")


def render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# S5 CRT Affected-slice Real Rerun",
        "",
        f"Run dir: `{RUN_DIR}`",
        "",
        "| System | Correct | Accuracy | Avg Tokens | Failed | Missing |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for label in ("old_myagent", "new_myagent_s5", "mact"):
        item = summary["systems"][label]
        lines.append(
            f"| {label} | {item['correct']}/{item['rows']} | {item['accuracy']:.4f} | "
            f"{item['avg_total_tokens']:.2f} | {item['num_failed_exec']} | {item['num_missing_answer']} |"
        )
    paired = summary["paired_new_vs_mact"]
    lines.extend(
        [
            "",
            "## New MyAgent vs MACT",
            "",
            f"- both_correct: `{paired['both_correct']}`",
            f"- myagent_only: `{paired['myagent_only']}`",
            f"- mact_only: `{paired['mact_only']}`",
            f"- both_wrong: `{paired['both_wrong']}`",
            f"- delta_correct: `{summary['systems']['new_myagent_s5']['correct'] - summary['systems']['mact']['correct']:+d}`",
            "",
            "## Changed Correctness vs Old MyAgent",
            "",
        ]
    )
    for row in summary["correctness_changes"]:
        lines.append(
            f"- `{row['seed']} {row['id']}`: old `{row['old_correct']}` -> new `{row['new_correct']}`, "
            f"MACT `{row['mact_correct']}`, old `{row['old_prediction']}`, new `{row['new_prediction']}`, gold `{row['gold_answer']}`."
        )
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    new_rows = load_jsonl(str(S5_MERGED))
    old_rows: dict[str, dict[str, Any]] = {}
    mact_rows: dict[str, dict[str, Any]] = {}
    for seed in SEEDS:
        old_rows.update({str(row["id"]): row for row in load_jsonl(str(old_myagent_path(seed)))})
        mact_rows.update({str(row["id"]): row for row in load_jsonl(str(mact_path(seed)))})
    new_index = {str(row["id"]): row for row in new_rows}
    ids = sorted(new_index)

    if any(row_id not in old_rows for row_id in ids) or any(row_id not in mact_rows for row_id in ids):
        raise SystemExit("S5 affected slice IDs must exist in both old MyAgent and MACT paired CRT outputs.")

    old_slice = [old_rows[row_id] for row_id in ids]
    mact_slice = [mact_rows[row_id] for row_id in ids]
    new_summary, _ = summarize_rows(new_rows)
    old_summary, _ = summarize_rows(old_slice)
    mact_summary, _ = summarize_rows(mact_slice)

    paired = {"both_correct": 0, "myagent_only": 0, "mact_only": 0, "both_wrong": 0}
    correctness_changes: list[dict[str, Any]] = []
    per_case: list[dict[str, Any]] = []
    for row_id in ids:
        new_row = new_index[row_id]
        old_row = old_rows[row_id]
        mact_row = mact_rows[row_id]
        old_correct = dataset_accuracy(old_row)
        new_correct = dataset_accuracy(new_row)
        mact_correct = dataset_accuracy(mact_row)
        if new_correct and mact_correct:
            paired["both_correct"] += 1
        elif new_correct:
            paired["myagent_only"] += 1
        elif mact_correct:
            paired["mact_only"] += 1
        else:
            paired["both_wrong"] += 1
        case = {
            "seed": row_seed(new_row),
            "id": row_id,
            "question": new_row.get("question"),
            "gold_answer": gold_for_em(new_row),
            "old_prediction": prediction_for_em(old_row),
            "new_prediction": prediction_for_em(new_row),
            "mact_prediction": prediction_for_em(mact_row),
            "old_correct": old_correct,
            "new_correct": new_correct,
            "mact_correct": mact_correct,
            "new_final_value": new_row.get("final_value"),
            "new_final_answer": new_row.get("final_answer"),
            "new_deterministic_shortcut_applied": new_row.get("deterministic_shortcut_applied"),
            "new_deterministic_shortcut_reason": new_row.get("deterministic_shortcut_reason"),
            "new_strong_verification_applied": new_row.get("strong_verification_applied"),
            "new_token_total": token_total(new_row),
            "new_elapsed_seconds_total": new_row.get("elapsed_seconds_total"),
        }
        per_case.append(case)
        if old_correct != new_correct or old_row.get("final_value") != new_row.get("final_value"):
            correctness_changes.append(case)

    def system_item(rows: list[dict[str, Any]], summary: dict[str, Any]) -> dict[str, Any]:
        correct = sum(1 for row in rows if dataset_accuracy(row))
        return {
            "rows": len(rows),
            "correct": correct,
            "accuracy": correct / len(rows) if rows else 0.0,
            "avg_total_tokens": summary["avg_total_tokens"],
            "avg_elapsed_seconds": summary["avg_elapsed_seconds"],
            "num_failed_exec": summary["num_failed_exec"],
            "num_missing_answer": summary["num_missing_answer"],
        }

    summary = {
        "run_dir": str(RUN_DIR),
        "s5_merged_path": str(S5_MERGED),
        "systems": {
            "old_myagent": system_item(old_slice, old_summary),
            "new_myagent_s5": system_item(new_rows, new_summary),
            "mact": system_item(mact_slice, mact_summary),
        },
        "paired_new_vs_mact": paired,
        "correctness_changes": correctness_changes,
        "per_case": per_case,
    }
    out_json = RUN_DIR / "summary" / "s5_affected_slice_real_rerun_summary.json"
    out_md = RUN_DIR / "summary" / "s5_affected_slice_real_rerun_summary.md"
    out_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    out_md.write_text(render_markdown(summary), encoding="utf-8")
    print(json.dumps({key: summary[key] for key in ("systems", "paired_new_vs_mact")}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
