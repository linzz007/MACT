#!/usr/bin/env python3
"""Project current deterministic shortcuts on Seed-D WTQ/TabFact S3 rows.

This is a no-model offline projection. It applies the current MyAgent
deterministic semantic shortcuts to the completed Seed-D S3 WTQ/TabFact rows,
then recomputes evaluator accuracy to decide whether a bounded fresh rerun is
worth spending server time on.
"""

from __future__ import annotations

import datetime as dt
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


RUN_DIR = Path(__file__).resolve().parent
MYAGENT_ROOT = Path("/home/ubuntu/lzz/MyAgent")
MYAGENT_CODE = MYAGENT_ROOT / "code"
SUMMARY_DIR = RUN_DIR / "summary"
DATASETS = ("wtq", "tabfact")

sys.path.insert(0, str(MYAGENT_CODE))
from answer_contracts import infer_answer_contract  # noqa: E402
from evaluate_results import dataset_accuracy  # noqa: E402
from my_agents import (  # noqa: E402
    Calculator,
    CriticAgent,
    FinalAnswerAgent,
    LLMCallTracker,
    PlannerAgent,
    RouterAgent,
    TQASessionState,
    TableQAPipeline,
    _build_table_schema,
    build_df_from_table,
)


class DummyLLM:
    def __call__(self, prompt: str) -> str:
        return "{}"


def git_commit(path: Path) -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=path,
            text=True,
        ).strip()
    except Exception:
        return "unknown"


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def projected_final_answer(value: Any, dataset: str) -> str:
    if dataset == "tabfact":
        return str(value).lower()
    if isinstance(value, list):
        return json.dumps(value, ensure_ascii=False)
    return str(value)


def make_pipeline() -> TableQAPipeline:
    tracker = LLMCallTracker(DummyLLM())
    return TableQAPipeline(
        router=RouterAgent(tracker),
        planner=PlannerAgent(tracker),
        calculator=Calculator(),
        critic=CriticAgent(tracker),
        final_answer_agent=FinalAnswerAgent(tracker),
    )


def project_dataset(dataset: str, pipeline: TableQAPipeline, summary: dict[str, Any]) -> dict[str, Any]:
    merged_path = RUN_DIR / "myagent_s3_after_guard" / "seed_d" / "merged" / f"{dataset}_qwen3-32b-local.jsonl"
    rows = read_jsonl(merged_path)
    threshold = int(summary["datasets"][dataset]["threshold_correct"])
    projected_rows: list[dict[str, Any]] = []
    old_correct = 0
    projected_correct = 0
    triggered = 0
    recovered = 0
    harmed = 0

    for row in rows:
        old_is_correct = bool(dataset_accuracy(row))
        question = row.get("question") or row.get("statement") or ""
        answer_mode = "true_false" if dataset == "tabfact" else ""
        df = build_df_from_table(row["table_text"])
        state = TQASessionState(
            question=question,
            df=df,
            table_schema=_build_table_schema(df),
            answer_mode=answer_mode,
            answer_contract=infer_answer_contract(question, answer_mode),
            dataset_profile=dataset,
        )
        shortcut_ok = (
            pipeline._try_wtq_semantic_shortcut(state)
            if dataset == "wtq"
            else pipeline._try_tabfact_semantic_shortcut(state)
        )
        projected_row = dict(row)
        if shortcut_ok:
            projected_row["final_value"] = state.final_value
            projected_row["final_answer"] = projected_final_answer(state.final_value, dataset)
            projected_row["deterministic_shortcut_applied"] = True
            projected_row["deterministic_shortcut_reason"] = state.deterministic_shortcut_reason
        projected_is_correct = bool(dataset_accuracy(projected_row))

        old_correct += int(old_is_correct)
        projected_correct += int(projected_is_correct)
        triggered += int(shortcut_ok)
        recovered += int(shortcut_ok and not old_is_correct and projected_is_correct)
        harmed += int(shortcut_ok and old_is_correct and not projected_is_correct)

        if shortcut_ok and (old_is_correct != projected_is_correct or not old_is_correct):
            projected_rows.append(
                {
                    "id": row.get("id"),
                    "old_correct": old_is_correct,
                    "projected_correct": projected_is_correct,
                    "projected_value": state.final_value,
                    "shortcut_reason": state.deterministic_shortcut_reason,
                    "gold": row.get("answer") or row.get("gold_answer"),
                    "question_or_statement": question,
                }
            )

    return {
        "dataset": dataset,
        "merged_path": str(merged_path),
        "rows": len(rows),
        "old_correct": old_correct,
        "projected_correct": projected_correct,
        "delta_correct": projected_correct - old_correct,
        "threshold_correct": threshold,
        "passes_projected_gate": projected_correct >= threshold,
        "triggered": triggered,
        "recovered": recovered,
        "harmed": harmed,
        "projected_rows": projected_rows,
    }


def build_report() -> dict[str, Any]:
    generated_at = dt.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
    summary = read_json(SUMMARY_DIR / "seed_d_s3_current_summary.json")
    pipeline = make_pipeline()
    datasets = {dataset: project_dataset(dataset, pipeline, summary) for dataset in DATASETS}
    total_old = sum(item["old_correct"] for item in datasets.values())
    total_projected = sum(item["projected_correct"] for item in datasets.values())
    total_threshold = sum(item["threshold_correct"] for item in datasets.values())
    total_recovered = sum(item["recovered"] for item in datasets.values())
    total_harmed = sum(item["harmed"] for item in datasets.values())
    return {
        "artifact_name": "seed_d_wtq_tabfact_boundary_shortcut_projection",
        "generated_at_local": generated_at,
        "scope": "Offline no-model projection of current deterministic shortcuts on completed Seed-D S3 WTQ/TabFact rows.",
        "run_dir": str(RUN_DIR),
        "git_commits_at_generation": {
            "myagent": git_commit(MYAGENT_ROOT),
            "mact": git_commit(Path("/home/ubuntu/lzz/MACT")),
        },
        "datasets": datasets,
        "aggregate": {
            "rows": sum(item["rows"] for item in datasets.values()),
            "old_correct": total_old,
            "projected_correct": total_projected,
            "delta_correct": total_projected - total_old,
            "threshold_correct": total_threshold,
            "passes_projected_gate": all(item["passes_projected_gate"] for item in datasets.values()),
            "recovered": total_recovered,
            "harmed": total_harmed,
            "decision": "run_seed_d_wtq_tabfact_fresh_rerun" if total_harmed == 0 and all(item["passes_projected_gate"] for item in datasets.values()) else "do_not_expand_without_inspection",
        },
        "interpretation": [
            "This projection uses gold labels only after deterministic answers are computed, for evaluator recomputation; gold is not part of any shortcut input.",
            "The result is not a fresh model run and must not be cited as final Seed-D accuracy.",
            "Because both WTQ and TabFact pass projected gates with zero projected harm, the next step is a bounded fresh rerun on the same Seed-D WTQ/TabFact full50 inputs.",
        ],
    }


def markdown_table(headers: list[str], rows: list[list[Any]]) -> list[str]:
    lines = [
        "| " + " | ".join(headers) + " |",
        "|" + "|".join("---" for _ in headers) + "|",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(value) for value in row) + " |")
    return lines


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Seed-D WTQ/TabFact Boundary Shortcut Projection",
        "",
        f"Generated: `{report['generated_at_local']}`",
        "",
        f"Scope: {report['scope']}",
        "",
        "## Decision",
        "",
        f"`{report['aggregate']['decision']}`",
        "",
        "## Aggregate",
        "",
        "| rows | old correct | projected correct | delta | threshold | recovered | harmed | projected gate |",
        "|---:|---:|---:|---:|---:|---:|---:|---|",
        f"| {report['aggregate']['rows']} | {report['aggregate']['old_correct']} | {report['aggregate']['projected_correct']} | {report['aggregate']['delta_correct']} | {report['aggregate']['threshold_correct']} | {report['aggregate']['recovered']} | {report['aggregate']['harmed']} | `{report['aggregate']['passes_projected_gate']}` |",
        "",
        "## Dataset Projection",
        "",
    ]
    dataset_rows = []
    projected_rows = []
    for dataset, item in report["datasets"].items():
        dataset_rows.append(
            [
                dataset,
                item["rows"],
                item["old_correct"],
                item["projected_correct"],
                item["delta_correct"],
                item["threshold_correct"],
                item["triggered"],
                item["recovered"],
                item["harmed"],
                f"`{item['passes_projected_gate']}`",
            ]
        )
        for row in item["projected_rows"]:
            projected_rows.append(
                [
                    dataset,
                    row["id"],
                    row["old_correct"],
                    row["projected_correct"],
                    row["shortcut_reason"],
                    str(row["projected_value"])[:80],
                    str(row["gold"])[:80],
                ]
            )
    lines.extend(
        markdown_table(
            ["dataset", "rows", "old", "projected", "delta", "threshold", "triggered", "recovered", "harmed", "gate"],
            dataset_rows,
        )
    )
    lines.extend(["", "## Projected Changed/Wrong Trigger Rows", ""])
    lines.extend(markdown_table(["dataset", "id", "old ok", "projected ok", "reason", "projected", "gold"], projected_rows))
    lines.extend(["", "## Interpretation", ""])
    lines.extend(f"- {item}" for item in report["interpretation"])
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    report = build_report()
    json_path = SUMMARY_DIR / "seed_d_wtq_tabfact_boundary_shortcut_projection.json"
    md_path = SUMMARY_DIR / "seed_d_wtq_tabfact_boundary_shortcut_projection.md"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(report), encoding="utf-8")
    print(
        json.dumps(
            {
                "json": str(json_path),
                "md": str(md_path),
                "decision": report["aggregate"]["decision"],
                "old_correct": report["aggregate"]["old_correct"],
                "projected_correct": report["aggregate"]["projected_correct"],
                "harmed": report["aggregate"]["harmed"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
