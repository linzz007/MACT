#!/usr/bin/env python3
"""Replay the S5 CRT scalar canonicalizer on existing MyAgent CRT outputs."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


RUN_DIR = Path(__file__).resolve().parent
MACT_ROOT = Path("/home/ubuntu/lzz/MACT")
MYAGENT_ROOT = Path("/home/ubuntu/lzz/MyAgent")
S3_RUN = MACT_ROOT / "outputs/server_runs/qwen3_32b_policy_v6b_e3_s3_current_rerun_after_guard_20260804_1425"
S4_RUN = MACT_ROOT / "outputs/server_runs/qwen3_32b_policy_v6c_e3_s4_paired_mact_20260804_1626"
SEEDS = ("seed_c", "seed_d")

sys.path.insert(0, str(MYAGENT_ROOT / "code"))
from evaluate_results import dataset_accuracy, load_jsonl, summarize_rows  # noqa: E402
from my_agents import _canonicalize_crt_scalar  # noqa: E402


def myagent_crt_path(seed: str) -> Path:
    return S3_RUN / "myagent_s3_after_guard" / seed / "merged" / "crt_qwen3-32b-local.jsonl"


def mact_crt_path(seed: str) -> Path:
    return S4_RUN / "mact" / seed / f"crt_mact_{seed}_gate50.jsonl"


def normalize_row(row: dict[str, Any]) -> dict[str, Any]:
    patched = dict(row)
    contract = patched.get("answer_contract") or {}
    if patched.get("source_dataset") == "crt" and contract.get("kind") == "scalar":
        original = patched.get("final_value")
        normalized = _canonicalize_crt_scalar(
            original,
            str(patched.get("question") or ""),
            None,
        )
        if normalized != original:
            patched["final_value"] = normalized
            patched["final_answer"] = str(normalized).strip()
            patched["s5_crt_canonicalizer_patch"] = {
                "original_final_value": original,
                "patched_final_value": normalized,
                "rule": "crt_scalar_difference_abs_or_country_code_expansion",
            }
    return patched


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def compare_seed(seed: str, patched_rows: list[dict[str, Any]], mact_rows: list[dict[str, Any]]) -> dict[str, Any]:
    my_index = {str(row["id"]): row for row in patched_rows}
    mact_index = {str(row["id"]): row for row in mact_rows}
    counts = {"both_correct": 0, "myagent_only": 0, "mact_only": 0, "both_wrong": 0}
    flips: list[dict[str, Any]] = []
    original_index = {str(row["id"]): row for row in load_jsonl(str(myagent_crt_path(seed)))}
    for row_id in sorted(my_index):
        my_correct = dataset_accuracy(my_index[row_id])
        mact_correct = dataset_accuracy(mact_index[row_id])
        if my_correct and mact_correct:
            counts["both_correct"] += 1
        elif my_correct:
            counts["myagent_only"] += 1
        elif mact_correct:
            counts["mact_only"] += 1
        else:
            counts["both_wrong"] += 1
        original_correct = dataset_accuracy(original_index[row_id])
        if my_correct != original_correct or my_index[row_id].get("s5_crt_canonicalizer_patch"):
            flips.append(
                {
                    "seed": seed,
                    "id": row_id,
                    "question": my_index[row_id].get("question"),
                    "gold_answer": my_index[row_id].get("gold_answer") or my_index[row_id].get("answer"),
                    "original_final_value": original_index[row_id].get("final_value"),
                    "patched_final_value": my_index[row_id].get("final_value"),
                    "original_correct": original_correct,
                    "patched_correct": my_correct,
                    "mact_correct": mact_correct,
                    "mact_pred_answer": mact_index[row_id].get("pred_answer"),
                }
            )
    my_summary, _ = summarize_rows(patched_rows)
    mact_summary, _ = summarize_rows(mact_rows)
    return {
        "rows": len(patched_rows),
        "myagent_correct": int(round(my_summary["primary_accuracy"] * len(patched_rows))),
        "mact_correct": int(round(mact_summary["primary_accuracy"] * len(mact_rows))),
        "paired_counts": counts,
        "myagent_avg_total_tokens": my_summary["avg_total_tokens"],
        "mact_avg_total_tokens": mact_summary["avg_total_tokens"],
        "token_ratio_myagent_to_mact": my_summary["avg_total_tokens"] / mact_summary["avg_total_tokens"],
        "flips": flips,
    }


def render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# S5 CRT Canonicalizer Patch Replay",
        "",
        f"Run dir: `{RUN_DIR}`",
        "",
        "This replay applies only the new CRT scalar canonicalization rules to existing MyAgent outputs.",
        "It does not use gold answers during patching and does not rerun the model.",
        "",
        "| Seed | MyAgent Patched | MACT | Delta | both_correct | myagent_only | mact_only | both_wrong | Token Ratio | Flips |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for seed in SEEDS:
        item = summary["seeds"][seed]
        counts = item["paired_counts"]
        lines.append(
            f"| {seed} | {item['myagent_correct']}/{item['rows']} | {item['mact_correct']}/{item['rows']} | "
            f"{item['myagent_correct'] - item['mact_correct']:+d} | {counts['both_correct']} | "
            f"{counts['myagent_only']} | {counts['mact_only']} | {counts['both_wrong']} | "
            f"{item['token_ratio_myagent_to_mact']:.4f} | {len(item['flips'])} |"
        )
    overall = summary["overall"]
    lines.extend(
        [
            "",
            f"Combined CRT: MyAgent patched `{overall['myagent_correct']}/{overall['rows']}` vs MACT `{overall['mact_correct']}/{overall['rows']}`, delta `{overall['delta_correct']:+d}`, token ratio `{overall['token_ratio_myagent_to_mact']:.4f}`.",
            "",
            "## Changed Cases",
            "",
        ]
    )
    for flip in overall["flips"]:
        lines.extend(
            [
                f"- `{flip['seed']} {flip['id']}`: `{flip['original_final_value']}` -> `{flip['patched_final_value']}`, "
                f"MyAgent `{flip['original_correct']}` -> `{flip['patched_correct']}`, MACT `{flip['mact_correct']}`.",
            ]
        )
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    summary: dict[str, Any] = {"run_dir": str(RUN_DIR), "seeds": {}}
    all_flips: list[dict[str, Any]] = []
    total_rows = total_my = total_mact = 0
    weighted_my_tokens = weighted_mact_tokens = 0.0
    overall_counts = {"both_correct": 0, "myagent_only": 0, "mact_only": 0, "both_wrong": 0}

    for seed in SEEDS:
        rows = load_jsonl(str(myagent_crt_path(seed)))
        patched_rows = [normalize_row(row) for row in rows]
        patched_path = RUN_DIR / "patched_myagent" / seed / "crt_qwen3-32b-local_s5_canonicalizer_replay.jsonl"
        write_jsonl(patched_path, patched_rows)
        mact_rows = load_jsonl(str(mact_crt_path(seed)))
        item = compare_seed(seed, patched_rows, mact_rows)
        item["patched_myagent_path"] = str(patched_path)
        summary["seeds"][seed] = item
        all_flips.extend(item["flips"])
        total_rows += item["rows"]
        total_my += item["myagent_correct"]
        total_mact += item["mact_correct"]
        weighted_my_tokens += item["myagent_avg_total_tokens"] * item["rows"]
        weighted_mact_tokens += item["mact_avg_total_tokens"] * item["rows"]
        for key, value in item["paired_counts"].items():
            overall_counts[key] += value

    my_tokens = weighted_my_tokens / total_rows
    mact_tokens = weighted_mact_tokens / total_rows
    summary["overall"] = {
        "rows": total_rows,
        "myagent_correct": total_my,
        "mact_correct": total_mact,
        "delta_correct": total_my - total_mact,
        "paired_counts": overall_counts,
        "myagent_avg_total_tokens": my_tokens,
        "mact_avg_total_tokens": mact_tokens,
        "token_ratio_myagent_to_mact": my_tokens / mact_tokens,
        "flips": all_flips,
    }
    summary_path = RUN_DIR / "summary" / "s5_crt_canonicalizer_replay_summary.json"
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (RUN_DIR / "summary" / "s5_crt_canonicalizer_replay_summary.md").write_text(
        render_markdown(summary),
        encoding="utf-8",
    )
    print(json.dumps(summary["overall"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
