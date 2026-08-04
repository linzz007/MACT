#!/usr/bin/env python3
"""Extract paired CRT tie-breaker diagnostics for MyAgent vs MACT."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any


RUN_DIR = Path(__file__).resolve().parent
MACT_ROOT = Path("/home/ubuntu/lzz/MACT")
MYAGENT_ROOT = Path("/home/ubuntu/lzz/MyAgent")
S3_RUN = MACT_ROOT / "outputs/server_runs/qwen3_32b_policy_v6b_e3_s3_current_rerun_after_guard_20260804_1425"
S4_RUN = MACT_ROOT / "outputs/server_runs/qwen3_32b_policy_v6c_e3_s4_paired_mact_20260804_1626"
SEEDS = ("seed_c", "seed_d")

sys.path.insert(0, str(MYAGENT_ROOT / "code"))
from evaluate_results import (  # noqa: E402
    dataset_accuracy,
    gold_for_em,
    load_jsonl,
    prediction_for_em,
    summarize_rows,
)


def myagent_crt_path(seed: str) -> Path:
    return S3_RUN / "myagent_s3_after_guard" / seed / "merged" / "crt_qwen3-32b-local.jsonl"


def mact_crt_path(seed: str) -> Path:
    return S4_RUN / "mact" / seed / f"crt_mact_{seed}_gate50.jsonl"


def token_total(row: dict[str, Any]) -> int:
    api = row.get("api_metrics") or {}
    if api:
        return int(api.get("total_tokens") or (api.get("prompt_tokens") or 0) + (api.get("completion_tokens") or 0))
    llm = row.get("llm_metrics") or {}
    return int(llm.get("total_tokens_est") or 0)


def short_row(row: dict[str, Any], system: str) -> dict[str, Any]:
    payload = {
        "id": row.get("id"),
        "system": system,
        "question": row.get("question") or row.get("utterance"),
        "gold_answer": gold_for_em(row),
        "prediction_for_eval": prediction_for_em(row),
        "correct": dataset_accuracy(row),
        "elapsed_seconds_total": row.get("elapsed_seconds_total"),
        "token_total": token_total(row),
        "source_dataset": row.get("source_dataset"),
    }
    if system == "myagent":
        payload.update(
            {
                "final_answer": row.get("final_answer"),
                "final_value": row.get("final_value"),
                "answer_contract": row.get("answer_contract"),
                "answer_mode": row.get("answer_mode"),
                "risk_level": row.get("risk_level"),
                "deterministic_shortcut_applied": row.get("deterministic_shortcut_applied"),
                "strong_verification_applied": row.get("strong_verification_applied"),
                "route_type": row.get("route_type"),
                "exec_error": row.get("exec_error"),
            }
        )
    else:
        payload.update(
            {
                "pred_answer": row.get("pred_answer"),
                "pred_answer_all": row.get("pred_answer_all"),
                "exec_error": row.get("exec_error"),
            }
        )
    return payload


def classify_pair(my_row: dict[str, Any], mact_row: dict[str, Any]) -> str:
    my_correct = dataset_accuracy(my_row)
    mact_correct = dataset_accuracy(mact_row)
    if my_correct and mact_correct:
        return "both_correct"
    if my_correct:
        return "myagent_only"
    if mact_correct:
        return "mact_only"
    return "both_wrong"


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# Qwen3-32B CRT Tie-breaker Diagnosis",
        "",
        f"Run dir: `{RUN_DIR}`",
        "",
        "## Paired Counts",
        "",
        "| Seed | Rows | MyAgent Correct | MACT Correct | both_correct | myagent_only | mact_only | both_wrong | MyAgent Avg Tokens | MACT Avg Tokens |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for seed in SEEDS:
        item = summary["seeds"][seed]
        counts = item["paired_counts"]
        lines.append(
            f"| {seed} | {item['rows']} | {item['myagent_correct']} | {item['mact_correct']} | "
            f"{counts.get('both_correct', 0)} | {counts.get('myagent_only', 0)} | "
            f"{counts.get('mact_only', 0)} | {counts.get('both_wrong', 0)} | "
            f"{item['myagent_avg_total_tokens']:.2f} | {item['mact_avg_total_tokens']:.2f} |"
        )
    overall = summary["overall"]
    counts = overall["paired_counts"]
    lines.extend(
        [
            "",
            "## Combined",
            "",
            f"- Rows: `{overall['rows']}`",
            f"- MyAgent correct: `{overall['myagent_correct']}`",
            f"- MACT correct: `{overall['mact_correct']}`",
            f"- Paired counts: `both_correct={counts.get('both_correct', 0)}`, "
            f"`myagent_only={counts.get('myagent_only', 0)}`, "
            f"`mact_only={counts.get('mact_only', 0)}`, `both_wrong={counts.get('both_wrong', 0)}`",
            f"- Token ratio MyAgent/MACT: `{overall['token_ratio_myagent_to_mact']:.4f}`",
            "",
            "## Files",
            "",
            "- `cases/{seed}_crt_mact_only.jsonl`: MACT correct, MyAgent wrong, highest-value tie-breaker targets.",
            "- `cases/{seed}_crt_myagent_only.jsonl`: MyAgent correct, MACT wrong, no-harm guard targets.",
            "- `cases/{seed}_crt_both_wrong.jsonl`: shared failure modes for later improvement.",
            "- `summary/crt_tiebreaker_diag.json`: machine-readable summary.",
            "",
            "## Immediate Reading",
            "",
            "Current CRT is an exact tie across the two seeds. A strict all-dataset win needs at least one gold-free CRT improvement with no loss on the paired MyAgent-only cases.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    all_by_category: dict[str, list[dict[str, Any]]] = {
        "both_correct": [],
        "myagent_only": [],
        "mact_only": [],
        "both_wrong": [],
    }
    summary: dict[str, Any] = {"run_dir": str(RUN_DIR), "seeds": {}}

    for seed in SEEDS:
        my_rows = load_jsonl(str(myagent_crt_path(seed)))
        mact_rows = load_jsonl(str(mact_crt_path(seed)))
        my_index = {str(row["id"]): row for row in my_rows}
        mact_index = {str(row["id"]): row for row in mact_rows}
        if set(my_index) != set(mact_index):
            missing_my = sorted(set(mact_index) - set(my_index))
            missing_mact = sorted(set(my_index) - set(mact_index))
            raise SystemExit(f"ID mismatch for {seed}: missing_my={missing_my}, missing_mact={missing_mact}")

        by_category: dict[str, list[dict[str, Any]]] = {
            "both_correct": [],
            "myagent_only": [],
            "mact_only": [],
            "both_wrong": [],
        }
        for row_id in sorted(my_index):
            my_row = my_index[row_id]
            mact_row = mact_index[row_id]
            category = classify_pair(my_row, mact_row)
            payload = {
                "seed": seed,
                "id": row_id,
                "category": category,
                "question": my_row.get("question") or my_row.get("utterance"),
                "table_text": my_row.get("table_text"),
                "gold_answer": gold_for_em(my_row),
                "myagent": short_row(my_row, "myagent"),
                "mact": short_row(mact_row, "mact"),
            }
            by_category[category].append(payload)
            all_by_category[category].append(payload)

        for category, rows in by_category.items():
            write_jsonl(RUN_DIR / "cases" / f"{seed}_crt_{category}.jsonl", rows)

        my_summary, _ = summarize_rows(my_rows)
        mact_summary, _ = summarize_rows(mact_rows)
        counts = Counter({category: len(rows) for category, rows in by_category.items()})
        summary["seeds"][seed] = {
            "myagent_path": str(myagent_crt_path(seed)),
            "mact_path": str(mact_crt_path(seed)),
            "rows": len(my_rows),
            "myagent_correct": int(round(my_summary["primary_accuracy"] * len(my_rows))),
            "mact_correct": int(round(mact_summary["primary_accuracy"] * len(mact_rows))),
            "paired_counts": dict(counts),
            "myagent_avg_total_tokens": my_summary["avg_total_tokens"],
            "mact_avg_total_tokens": mact_summary["avg_total_tokens"],
            "token_ratio_myagent_to_mact": (
                my_summary["avg_total_tokens"] / mact_summary["avg_total_tokens"]
                if mact_summary["avg_total_tokens"]
                else None
            ),
            "myagent_avg_elapsed_seconds": my_summary["avg_elapsed_seconds"],
            "mact_avg_elapsed_seconds": mact_summary["avg_elapsed_seconds"],
        }

    for category, rows in all_by_category.items():
        write_jsonl(RUN_DIR / "cases" / f"crt_{category}_all.jsonl", rows)

    overall_counts = {category: len(rows) for category, rows in all_by_category.items()}
    overall_rows = sum(overall_counts.values())
    myagent_correct = overall_counts["both_correct"] + overall_counts["myagent_only"]
    mact_correct = overall_counts["both_correct"] + overall_counts["mact_only"]
    my_tokens = sum(
        summary["seeds"][seed]["myagent_avg_total_tokens"] * summary["seeds"][seed]["rows"]
        for seed in SEEDS
    ) / overall_rows
    mact_tokens = sum(
        summary["seeds"][seed]["mact_avg_total_tokens"] * summary["seeds"][seed]["rows"]
        for seed in SEEDS
    ) / overall_rows
    summary["overall"] = {
        "rows": overall_rows,
        "myagent_correct": myagent_correct,
        "mact_correct": mact_correct,
        "delta_correct": myagent_correct - mact_correct,
        "paired_counts": overall_counts,
        "myagent_avg_total_tokens": my_tokens,
        "mact_avg_total_tokens": mact_tokens,
        "token_ratio_myagent_to_mact": my_tokens / mact_tokens if mact_tokens else None,
    }

    summary_path = RUN_DIR / "summary" / "crt_tiebreaker_diag.json"
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (RUN_DIR / "summary" / "crt_tiebreaker_diag.md").write_text(
        render_markdown(summary),
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
