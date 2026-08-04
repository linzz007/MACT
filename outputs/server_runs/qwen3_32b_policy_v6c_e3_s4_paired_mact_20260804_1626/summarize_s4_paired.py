#!/usr/bin/env python3
"""Summarize E3 S4 paired MACT results for the v6c boundary-fresh candidate."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


RUN_DIR = Path(__file__).resolve().parent
MYAGENT_ROOT = Path("/home/ubuntu/lzz/MyAgent")
MACT_ROOT = Path("/home/ubuntu/lzz/MACT")
SOURCE_RUN = MACT_ROOT / "outputs/server_runs/qwen3_32b_policy_v6b_multiseed_gate50_20260801_2231"
S3_RUN = MACT_ROOT / "outputs/server_runs/qwen3_32b_policy_v6b_e3_s3_current_rerun_after_guard_20260804_1425"
FRESH_RUN = MACT_ROOT / "outputs/server_runs/qwen3_32b_policy_v6c_seed_d_boundary_fresh_20260804_1549"
TASKS = ("wtq", "tabfact", "crt")
SEEDS = ("seed_c", "seed_d")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def count_jsonl(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())


def correct_count(metrics: dict[str, Any]) -> int:
    if "correct" in metrics:
        return int(metrics["correct"])
    rows = int(metrics.get("num_with_gold") or metrics.get("num_samples") or 0)
    return int(round(float(metrics.get("primary_accuracy") or metrics.get("exact_match") or 0.0) * rows))


def myagent_path(seed: str, task: str) -> Path:
    if seed == "seed_c":
        return S3_RUN / "myagent_s3_after_guard" / seed / "merged" / f"{task}_qwen3-32b-local.jsonl"
    if task in {"wtq", "tabfact"}:
        return FRESH_RUN / "myagent_seed_d_boundary_fresh" / "merged" / f"{task}_qwen3-32b-local.jsonl"
    return S3_RUN / "myagent_s3_after_guard" / seed / "merged" / "crt_qwen3-32b-local.jsonl"


def mact_path(seed: str, task: str) -> Path:
    return RUN_DIR / "mact" / seed / f"{task}_mact_{seed}_gate50.jsonl"


def eval_mact(seed: str, task: str) -> Path:
    out_dir = RUN_DIR / "eval" / seed
    out_dir.mkdir(parents=True, exist_ok=True)
    eval_path = out_dir / f"{task}_mact_{seed}_gate50_eval.json"
    err_path = out_dir / f"{task}_mact_{seed}_gate50_errors.jsonl"
    with eval_path.open("w", encoding="utf-8") as handle:
        subprocess.run(
            [
                "python",
                str(MYAGENT_ROOT / "code/evaluate_results.py"),
                str(mact_path(seed, task)),
                "--error_output",
                str(err_path),
            ],
            cwd=str(MYAGENT_ROOT),
            check=True,
            stdout=handle,
            text=True,
        )
    return eval_path


def compare_seed(seed: str) -> dict[str, Any]:
    summary_path = RUN_DIR / "summary" / f"{seed}_paired_gate50_summary.json"
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    for task in TASKS:
        eval_mact(seed, task)
    subprocess.run(
        [
            "python",
            str(MYAGENT_ROOT / "code/compare_blind_results.py"),
            "--myagent_wtq",
            str(myagent_path(seed, "wtq")),
            "--myagent_tabfact",
            str(myagent_path(seed, "tabfact")),
            "--myagent_crt",
            str(myagent_path(seed, "crt")),
            "--mact_wtq",
            str(mact_path(seed, "wtq")),
            "--mact_tabfact",
            str(mact_path(seed, "tabfact")),
            "--mact_crt",
            str(mact_path(seed, "crt")),
            "--output",
            str(summary_path),
        ],
        cwd=str(MYAGENT_ROOT),
        check=True,
        stdout=subprocess.DEVNULL,
        text=True,
    )
    summary = load_json(summary_path)
    strictly_above = 0
    at_least = 0
    for task in TASKS:
        item = summary["datasets"][task]
        my_correct = correct_count(item["myagent"])
        mact_correct = correct_count(item["mact"])
        if my_correct > mact_correct:
            strictly_above += 1
        if my_correct >= mact_correct:
            at_least += 1
    summary["datasets_myagent_strictly_above_mact"] = strictly_above
    summary["datasets_myagent_at_least_mact_recomputed"] = at_least
    summary["strict_all_dataset_superiority"] = strictly_above == len(TASKS)
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    render_seed_md(seed, summary)
    return summary


def render_seed_md(seed: str, summary: dict[str, Any]) -> None:
    lines = [
        f"# E3 S4 Paired MACT Summary: {seed}",
        "",
        f"Run dir: `{RUN_DIR}`",
        "",
        "| Dataset | MyAgent | MACT | Delta | Token Ratio | Failed MyAgent / MACT | Missing MyAgent / MACT | Paired myOnly / mactOnly |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for task in TASKS:
        item = summary["datasets"][task]
        rows = int(item["myagent"].get("num_with_gold") or item["myagent"].get("num_samples") or 0)
        my_correct = correct_count(item["myagent"])
        mact_correct = correct_count(item["mact"])
        ratio = item.get("token_ratio_myagent_to_mact")
        paired = item.get("paired") or {}
        lines.append(
            f"| {task} | {my_correct}/{rows} | {mact_correct}/{rows} | {my_correct - mact_correct:+d} | "
            f"{ratio:.4f} | {item['myagent'].get('num_failed_exec')}/{item['mact'].get('num_failed_exec')} | "
            f"{item['myagent'].get('num_missing_answer')}/{item['mact'].get('num_missing_answer')} | "
            f"{paired.get('myagent_only')}/{paired.get('mact_only')} |"
        )
    overall = summary["overall"]
    rows = int(overall["myagent"].get("num_with_gold") or overall["myagent"].get("num_samples") or 0)
    lines.extend(
        [
            "",
            f"Overall: MyAgent `{correct_count(overall['myagent'])}/{rows}` vs MACT `{correct_count(overall['mact'])}/{rows}`, token ratio `{summary.get('token_ratio_myagent_to_mact'):.4f}`.",
            f"Datasets MyAgent > MACT: `{summary['datasets_myagent_strictly_above_mact']}/3`.",
            f"Datasets MyAgent >= MACT: `{summary['datasets_myagent_at_least_mact_recomputed']}/3`.",
            f"Accepted by existing paired criteria: `{summary.get('accepted')}`.",
            f"Strict all-dataset superiority goal met: `{summary['strict_all_dataset_superiority']}`.",
            "",
        ]
    )
    (RUN_DIR / "summary" / f"{seed}_paired_gate50_summary.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def check_required_rows() -> None:
    missing: list[str] = []
    for seed in SEEDS:
        for task in TASKS:
            for label, path in (("myagent", myagent_path(seed, task)), ("mact", mact_path(seed, task))):
                rows = count_jsonl(path)
                if rows != 50:
                    missing.append(f"{label} {seed} {task}: {path} rows={rows}")
    if missing:
        raise SystemExit("Need exactly 50 rows before summarizing:\n" + "\n".join(missing))


def build_combined(seed_summaries: dict[str, dict[str, Any]]) -> dict[str, Any]:
    datasets: dict[str, Any] = {}
    for task in TASKS:
        my_correct = sum(correct_count(seed_summaries[seed]["datasets"][task]["myagent"]) for seed in SEEDS)
        mact_correct = sum(correct_count(seed_summaries[seed]["datasets"][task]["mact"]) for seed in SEEDS)
        rows = sum(
            int(seed_summaries[seed]["datasets"][task]["myagent"].get("num_with_gold") or 0)
            for seed in SEEDS
        )
        my_tokens = sum(
            seed_summaries[seed]["datasets"][task]["myagent"]["avg_total_tokens"]
            * int(seed_summaries[seed]["datasets"][task]["myagent"]["num_samples"])
            for seed in SEEDS
        ) / rows
        mact_tokens = sum(
            seed_summaries[seed]["datasets"][task]["mact"]["avg_total_tokens"]
            * int(seed_summaries[seed]["datasets"][task]["mact"]["num_samples"])
            for seed in SEEDS
        ) / rows
        datasets[task] = {
            "rows": rows,
            "myagent_correct": my_correct,
            "mact_correct": mact_correct,
            "delta_correct": my_correct - mact_correct,
            "token_ratio_myagent_to_mact": my_tokens / mact_tokens if mact_tokens else None,
            "myagent_avg_total_tokens": my_tokens,
            "mact_avg_total_tokens": mact_tokens,
            "strictly_above_mact": my_correct > mact_correct,
            "at_least_mact": my_correct >= mact_correct,
        }
    overall_rows = sum(item["rows"] for item in datasets.values())
    overall_my = sum(item["myagent_correct"] for item in datasets.values())
    overall_mact = sum(item["mact_correct"] for item in datasets.values())
    overall_my_tokens = sum(item["myagent_avg_total_tokens"] * item["rows"] for item in datasets.values()) / overall_rows
    overall_mact_tokens = sum(item["mact_avg_total_tokens"] * item["rows"] for item in datasets.values()) / overall_rows
    failed_my = sum(
        int(seed_summaries[seed]["overall"]["myagent"]["num_failed_exec"])
        for seed in SEEDS
    )
    failed_mact = sum(
        int(seed_summaries[seed]["overall"]["mact"]["num_failed_exec"])
        for seed in SEEDS
    )
    missing_my = sum(
        int(seed_summaries[seed]["overall"]["myagent"]["num_missing_answer"])
        for seed in SEEDS
    )
    missing_mact = sum(
        int(seed_summaries[seed]["overall"]["mact"]["num_missing_answer"])
        for seed in SEEDS
    )
    strict_all = all(item["strictly_above_mact"] for item in datasets.values())
    accepted = (
        overall_my >= overall_mact
        and sum(item["at_least_mact"] for item in datasets.values()) >= 2
        and overall_my_tokens / overall_mact_tokens <= 0.75
        and failed_my / max(1, overall_rows) <= 0.02
    )
    return {
        "artifact_name": "e3_s4_paired_mact_combined_summary",
        "run_dir": str(RUN_DIR),
        "candidate_source": str(FRESH_RUN / "summary/e3_boundary_fresh_combined_summary.json"),
        "seeds": {
            seed: {
                "summary_json": str(RUN_DIR / "summary" / f"{seed}_paired_gate50_summary.json"),
                "accepted": seed_summaries[seed]["accepted"],
                "strict_all_dataset_superiority": seed_summaries[seed]["strict_all_dataset_superiority"],
                "overall_myagent_correct": correct_count(seed_summaries[seed]["overall"]["myagent"]),
                "overall_mact_correct": correct_count(seed_summaries[seed]["overall"]["mact"]),
                "overall_rows": int(seed_summaries[seed]["overall"]["myagent"]["num_samples"]),
                "token_ratio_myagent_to_mact": seed_summaries[seed]["token_ratio_myagent_to_mact"],
            }
            for seed in SEEDS
        },
        "datasets": datasets,
        "overall": {
            "rows": overall_rows,
            "myagent_correct": overall_my,
            "mact_correct": overall_mact,
            "delta_correct": overall_my - overall_mact,
            "token_ratio_myagent_to_mact": overall_my_tokens / overall_mact_tokens if overall_mact_tokens else None,
            "myagent_avg_total_tokens": overall_my_tokens,
            "mact_avg_total_tokens": overall_mact_tokens,
            "myagent_failed": failed_my,
            "mact_failed": failed_mact,
            "myagent_missing": missing_my,
            "mact_missing": missing_mact,
        },
        "accepted_existing_paired_criteria": accepted,
        "strict_all_dataset_superiority": strict_all,
        "decision": "s4_paired_pass_strict_all_dataset"
        if strict_all and accepted
        else "s4_paired_pass_existing_criteria_not_strict"
        if accepted
        else "s4_paired_stop_or_inspect",
    }


def render_combined_md(combined: dict[str, Any]) -> None:
    lines = [
        "# E3 S4 Paired MACT Combined Summary",
        "",
        f"Run dir: `{RUN_DIR}`",
        "",
        "| Dataset | MyAgent | MACT | Delta | Token Ratio |",
        "|---|---:|---:|---:|---:|",
    ]
    for task in TASKS:
        item = combined["datasets"][task]
        lines.append(
            f"| {task} | {item['myagent_correct']}/{item['rows']} | {item['mact_correct']}/{item['rows']} | "
            f"{item['delta_correct']:+d} | {item['token_ratio_myagent_to_mact']:.4f} |"
        )
    overall = combined["overall"]
    lines.extend(
        [
            f"| aggregate | {overall['myagent_correct']}/{overall['rows']} | {overall['mact_correct']}/{overall['rows']} | {overall['delta_correct']:+d} | {overall['token_ratio_myagent_to_mact']:.4f} |",
            "",
            f"MyAgent failed/missing: `{overall['myagent_failed']}/{overall['myagent_missing']}`.",
            f"MACT failed/missing: `{overall['mact_failed']}/{overall['mact_missing']}`.",
            f"Accepted existing paired criteria: `{combined['accepted_existing_paired_criteria']}`.",
            f"Strict all-dataset superiority: `{combined['strict_all_dataset_superiority']}`.",
            f"Decision: `{combined['decision']}`.",
            "",
        ]
    )
    (RUN_DIR / "summary/e3_s4_paired_combined_summary.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def main() -> None:
    check_required_rows()
    seed_summaries = {seed: compare_seed(seed) for seed in SEEDS}
    combined = build_combined(seed_summaries)
    out_path = RUN_DIR / "summary/e3_s4_paired_combined_summary.json"
    out_path.write_text(json.dumps(combined, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    render_combined_md(combined)
    print(json.dumps(combined, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
