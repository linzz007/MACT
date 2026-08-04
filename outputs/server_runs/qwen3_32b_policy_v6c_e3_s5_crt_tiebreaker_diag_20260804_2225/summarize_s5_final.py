#!/usr/bin/env python3
"""Build final S5 summary: S4 WTQ/TabFact plus S5 full CRT rerun."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


RUN_DIR = Path(__file__).resolve().parent
MYAGENT_ROOT = Path("/home/ubuntu/lzz/MyAgent")
S4_RUN = Path("/home/ubuntu/lzz/MACT/outputs/server_runs/qwen3_32b_policy_v6c_e3_s4_paired_mact_20260804_1626")
S5_CRT = RUN_DIR / "myagent_s5_crt_paired100_full_rerun" / "merged" / "crt_qwen3-32b-local.jsonl"
SEEDS = ("seed_c", "seed_d")

sys.path.insert(0, str(MYAGENT_ROOT / "code"))
from evaluate_results import dataset_accuracy, load_jsonl, summarize_rows  # noqa: E402


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def correct_count(summary: dict[str, Any]) -> int:
    if "correct" in summary:
        return int(summary["correct"])
    rows = int(summary.get("num_with_gold") or summary.get("num_samples") or 0)
    return int(round(float(summary.get("primary_accuracy") or 0.0) * rows))


def mact_crt_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for seed in SEEDS:
        path = S4_RUN / "mact" / seed / f"crt_mact_{seed}_gate50.jsonl"
        rows.extend(load_jsonl(str(path)))
    return rows


def s4_seed_failure_counts(task: str) -> dict[str, int]:
    counts = {
        "myagent_failed": 0,
        "mact_failed": 0,
        "myagent_missing": 0,
        "mact_missing": 0,
    }
    for seed in SEEDS:
        seed_summary = load_json(S4_RUN / "summary" / f"{seed}_paired_gate50_summary.json")
        source = seed_summary["datasets"][task]
        counts["myagent_failed"] += int(source["myagent"].get("num_failed_exec") or 0)
        counts["mact_failed"] += int(source["mact"].get("num_failed_exec") or 0)
        counts["myagent_missing"] += int(source["myagent"].get("num_missing_answer") or 0)
        counts["mact_missing"] += int(source["mact"].get("num_missing_answer") or 0)
    return counts


def paired_counts(my_rows: list[dict[str, Any]], mact_rows: list[dict[str, Any]]) -> dict[str, int]:
    my_index = {str(row["id"]): row for row in my_rows}
    mact_index = {str(row["id"]): row for row in mact_rows}
    if set(my_index) != set(mact_index):
        raise SystemExit("S5 CRT and MACT CRT IDs do not match.")
    counts = {"both_correct": 0, "myagent_only": 0, "mact_only": 0, "both_wrong": 0}
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
    return counts


def render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# E3 S5 Final Summary: Qwen3-32B MyAgent vs MACT",
        "",
        f"Run dir: `{RUN_DIR}`",
        "",
        "S5 keeps the accepted S4 paired WTQ/TabFact results and replaces only the tied CRT component with the S5 current-code full CRT100 rerun.",
        "",
        "| Dataset | MyAgent | MACT | Delta | MyAgent Avg Tokens | MACT Avg Tokens | Token Ratio | Strict Win |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for task in ("wtq", "tabfact", "crt"):
        item = summary["datasets"][task]
        lines.append(
            f"| {task} | {item['myagent_correct']}/{item['rows']} | {item['mact_correct']}/{item['rows']} | "
            f"{item['delta_correct']:+d} | {item['myagent_avg_total_tokens']:.2f} | "
            f"{item['mact_avg_total_tokens']:.2f} | {item['token_ratio_myagent_to_mact']:.4f} | "
            f"{item['strictly_above_mact']} |"
        )
    overall = summary["overall"]
    lines.extend(
        [
            "",
            f"Overall: MyAgent `{overall['myagent_correct']}/{overall['rows']}` vs MACT `{overall['mact_correct']}/{overall['rows']}`, delta `{overall['delta_correct']:+d}`.",
            f"Overall token ratio MyAgent/MACT: `{overall['token_ratio_myagent_to_mact']:.4f}`.",
            f"Overall failed/missing: MyAgent `{overall['myagent_failed']}/{overall['myagent_missing']}`, MACT `{overall['mact_failed']}/{overall['mact_missing']}`.",
            f"Strict all-dataset superiority: `{summary['strict_all_dataset_superiority']}`.",
            f"Accepted by existing selective-risk criteria: `{summary['accepted_existing_paired_criteria']}`.",
            "",
            "## CRT S5 Details",
            "",
            f"- S5 CRT full rerun: `{summary['datasets']['crt']['myagent_correct']}/100` vs MACT `{summary['datasets']['crt']['mact_correct']}/100`.",
            f"- Paired counts: `{summary['datasets']['crt']['paired_counts']}`.",
            f"- MyAgent failed/missing: `{summary['datasets']['crt']['myagent_failed']}/{summary['datasets']['crt']['myagent_missing']}`.",
            f"- MACT failed/missing: `{summary['datasets']['crt']['mact_failed']}/{summary['datasets']['crt']['mact_missing']}`.",
            "",
            "## Mechanism Change",
            "",
            "- Added gold-free CRT scalar canonicalization for negative numeric `difference` answers and country-code answers in country/nation questions.",
            "- Validation traces: `summary/s5_crt_canonicalizer_replay_summary.*`, `summary/s5_affected_slice_real_rerun_summary.*`, and `myagent_s5_crt_paired100_full_rerun/eval/crt_qwen3-32b-local_eval.json`.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    s4 = load_json(S4_RUN / "summary" / "e3_s4_paired_combined_summary.json")
    s5_crt_rows = load_jsonl(str(S5_CRT))
    mact_rows = mact_crt_rows()
    s5_crt_summary, _ = summarize_rows(s5_crt_rows)
    mact_crt_summary, _ = summarize_rows(mact_rows)

    datasets: dict[str, dict[str, Any]] = {}
    for task in ("wtq", "tabfact"):
        source = s4["datasets"][task]
        failures = s4_seed_failure_counts(task)
        datasets[task] = {
            "rows": source["rows"],
            "myagent_correct": source["myagent_correct"],
            "mact_correct": source["mact_correct"],
            "delta_correct": source["delta_correct"],
            "myagent_avg_total_tokens": source["myagent_avg_total_tokens"],
            "mact_avg_total_tokens": source["mact_avg_total_tokens"],
            "token_ratio_myagent_to_mact": source["token_ratio_myagent_to_mact"],
            "myagent_failed": failures["myagent_failed"],
            "mact_failed": failures["mact_failed"],
            "myagent_missing": failures["myagent_missing"],
            "mact_missing": failures["mact_missing"],
            "strictly_above_mact": source["strictly_above_mact"],
            "source": "s4_paired_combined_summary",
        }

    crt_rows = int(s5_crt_summary["num_with_gold"])
    crt_my = correct_count(s5_crt_summary)
    crt_mact = correct_count(mact_crt_summary)
    datasets["crt"] = {
        "rows": crt_rows,
        "myagent_correct": crt_my,
        "mact_correct": crt_mact,
        "delta_correct": crt_my - crt_mact,
        "myagent_avg_total_tokens": s5_crt_summary["avg_total_tokens"],
        "mact_avg_total_tokens": mact_crt_summary["avg_total_tokens"],
        "token_ratio_myagent_to_mact": s5_crt_summary["avg_total_tokens"] / mact_crt_summary["avg_total_tokens"],
        "myagent_failed": s5_crt_summary["num_failed_exec"],
        "mact_failed": mact_crt_summary["num_failed_exec"],
        "myagent_missing": s5_crt_summary["num_missing_answer"],
        "mact_missing": mact_crt_summary["num_missing_answer"],
        "strictly_above_mact": crt_my > crt_mact,
        "paired_counts": paired_counts(s5_crt_rows, mact_rows),
        "source": str(S5_CRT),
    }

    total_rows = sum(item["rows"] for item in datasets.values())
    total_my = sum(item["myagent_correct"] for item in datasets.values())
    total_mact = sum(item["mact_correct"] for item in datasets.values())
    my_tokens = sum(item["myagent_avg_total_tokens"] * item["rows"] for item in datasets.values()) / total_rows
    mact_tokens = sum(item["mact_avg_total_tokens"] * item["rows"] for item in datasets.values()) / total_rows
    failed_my = sum(item["myagent_failed"] for item in datasets.values())
    failed_mact = sum(item["mact_failed"] for item in datasets.values())
    missing_my = sum(item["myagent_missing"] for item in datasets.values())
    missing_mact = sum(item["mact_missing"] for item in datasets.values())
    strict_all = all(item["strictly_above_mact"] for item in datasets.values())
    accepted = (
        total_my >= total_mact
        and sum(item["myagent_correct"] >= item["mact_correct"] for item in datasets.values()) >= 2
        and my_tokens / mact_tokens <= 0.75
        and failed_my / max(1, total_rows) <= 0.02
    )
    summary = {
        "artifact_name": "e3_s5_final_qwen3_myagent_vs_mact",
        "run_dir": str(RUN_DIR),
        "s4_source_summary": str(S4_RUN / "summary" / "e3_s4_paired_combined_summary.json"),
        "datasets": datasets,
        "overall": {
            "rows": total_rows,
            "myagent_correct": total_my,
            "mact_correct": total_mact,
            "delta_correct": total_my - total_mact,
            "myagent_avg_total_tokens": my_tokens,
            "mact_avg_total_tokens": mact_tokens,
            "token_ratio_myagent_to_mact": my_tokens / mact_tokens,
            "myagent_failed": failed_my,
            "mact_failed": failed_mact,
            "myagent_missing": missing_my,
            "mact_missing": missing_mact,
        },
        "strict_all_dataset_superiority": strict_all,
        "accepted_existing_paired_criteria": accepted,
        "decision": "s5_strict_all_dataset_pass" if strict_all and accepted else "s5_incomplete_or_boundary",
    }
    out_json = RUN_DIR / "summary" / "e3_s5_final_combined_summary.json"
    out_md = RUN_DIR / "summary" / "e3_s5_final_combined_summary.md"
    out_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    out_md.write_text(render_markdown(summary), encoding="utf-8")
    final_md = RUN_DIR / "s5_final_result.md"
    final_md.write_text(render_markdown(summary), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
