#!/usr/bin/env python3
"""Build the current formal result ledger from frozen experiment artifacts."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
from pathlib import Path
from typing import Any


PACKAGE_DIR = Path(__file__).resolve().parent
MACT_ROOT = Path("/home/ubuntu/lzz/MACT")
MYAGENT_ROOT = Path("/home/ubuntu/lzz/MyAgent")
FULL200_SUMMARY = Path(
    "/home/ubuntu/lzz/MACT/outputs/server_runs/"
    "qwen3_32b_policy_v6b_all200_acceptance_20260731_132611/"
    "qwen3_policy_v6b_all200_acceptance_summary.json"
)
FULL200_EVIDENCE_MD = Path(
    "/home/ubuntu/lzz/MACT/outputs/server_runs/"
    "qwen3_32b_policy_v6b_all200_acceptance_20260731_132611/"
    "qwen3_policy_v6b_patent_evidence_index.md"
)
P4B_SUMMARY = Path(
    "/home/ubuntu/lzz/MACT/outputs/server_runs/"
    "qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/"
    "p4b_paired_gate50_summary.json"
)
P4B_SUMMARY_MD = Path(
    "/home/ubuntu/lzz/MACT/outputs/server_runs/"
    "qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/"
    "p4b_paired_gate50_summary.md"
)
P4B_WTQ_TARGETED_FRESH_SUMMARY = Path(
    "/home/ubuntu/lzz/MACT/outputs/server_runs/"
    "qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/"
    "p4b_wtq_targeted_fresh_summary.json"
)
P4B_WTQ_TARGETED_FRESH_SUMMARY_MD = Path(
    "/home/ubuntu/lzz/MACT/outputs/server_runs/"
    "qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/"
    "p4b_wtq_targeted_fresh_summary.md"
)
P4B_AFTER_TARGETED_SUMMARY = Path(
    "/home/ubuntu/lzz/MACT/outputs/server_runs/"
    "qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/"
    "p4b_after_wtq_targeted_paired_summary.json"
)
P4B_AFTER_TARGETED_SUMMARY_MD = Path(
    "/home/ubuntu/lzz/MACT/outputs/server_runs/"
    "qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/"
    "p4b_after_wtq_targeted_paired_summary.md"
)
FORMAL_TEMPLATE = PACKAGE_DIR / "formal_result_tables_template_20260801_2252.json"
LATEST_PREFLIGHT = PACKAGE_DIR / "latest_qwen3_runtime_preflight.json"
E3_RUN_DIR = Path(
    "/home/ubuntu/lzz/MACT/outputs/server_runs/"
    "qwen3_32b_policy_v6b_multiseed_gate50_20260801_2231"
)
E3_BOUNDARY_DIAGNOSIS_JSON = E3_RUN_DIR / "summary" / "seed_boundary_error_diagnosis.json"
E3_BOUNDARY_DIAGNOSIS_MD = E3_RUN_DIR / "summary" / "seed_boundary_error_diagnosis.md"
E4_READINESS_JSON = PACKAGE_DIR / "latest_e4_multimodel_gate_readiness_audit.json"
E4_READINESS_MD = PACKAGE_DIR / "latest_e4_multimodel_gate_readiness_audit_zh.md"
CURRENT_PATENT_SECTION_JSON = PACKAGE_DIR / "latest_current_patent_experiment_section.json"
CURRENT_PATENT_SECTION_MD = PACKAGE_DIR / "latest_current_patent_experiment_section_zh.md"
E3_SEEDS = ("seed_c", "seed_d")
TASK_ORDER = ("wtq", "tabfact", "crt")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def count_jsonl(path: str | Path | None) -> int | None:
    if not path:
        return None
    file_path = Path(path)
    if not file_path.exists():
        return None
    return sum(1 for line in file_path.open(encoding="utf-8") if line.strip())


def git_commit(repo: Path) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "--short", "HEAD"],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout.strip()


def correct_count(metrics: dict[str, Any]) -> int:
    if "correct" in metrics:
        return int(metrics["correct"])
    rows = int(metrics.get("num_with_gold") or metrics.get("num_samples") or 0)
    return int(round(float(metrics.get("primary_accuracy") or 0.0) * rows))


def full200_rows(summary: dict[str, Any], *, mact_commit: str, myagent_commit: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for task in TASK_ORDER:
        item = summary["datasets"][task]
        current = item["current"]
        mact = item["mact"]
        eval_rows = int(current.get("rows") or item.get("rows") or 0)
        rows.append(
            {
                "stage": "Qwen3-32B full200 anchor",
                "status": "complete",
                "dataset": task,
                "input_rows": int(item.get("rows") or eval_rows),
                "merged_rows": int(item.get("merged_rows") or count_jsonl(item.get("merged_path")) or eval_rows),
                "eval_rows": eval_rows,
                "myagent_correct": int(current["correct"]),
                "mact_correct_or_reference": int(mact["correct"]),
                "accuracy_delta_correct": int(item["accuracy_delta_correct"]),
                "token_ratio": float(item["token_ratio_current_over_mact"]),
                "avg_total_tokens": float(current["avg_total_tokens"]),
                "avg_elapsed_seconds": float(current["avg_elapsed_seconds"]),
                "num_failed_exec": int(current["num_failed_exec"]),
                "num_missing_answer": int(current["num_missing_answer"]),
                "decision": "complete_full200_dataset_superiority",
                "evidence_json": str(FULL200_SUMMARY),
                "evidence_md": str(FULL200_EVIDENCE_MD),
                "git_commit": {"myagent": myagent_commit, "mact": mact_commit},
            }
        )
    aggregate = summary["aggregate"]
    rows.append(
        {
            "stage": "Qwen3-32B full200 anchor",
            "status": "complete",
            "dataset": "aggregate",
            "input_rows": int(aggregate["rows"]),
            "merged_rows": int(aggregate["rows"]),
            "eval_rows": int(aggregate["rows"]),
            "myagent_correct": int(aggregate["current_correct"]),
            "mact_correct_or_reference": int(aggregate["mact_correct"]),
            "accuracy_delta_correct": int(aggregate["accuracy_delta_correct"]),
            "token_ratio": float(aggregate["token_ratio_current_over_mact"]),
            "avg_total_tokens": float(aggregate["current_avg_total_tokens_weighted"]),
            "avg_elapsed_seconds": float(aggregate["current_avg_elapsed_seconds_weighted"]),
            "num_failed_exec": int(aggregate["current_failures"]),
            "num_missing_answer": int(aggregate["current_missing_answers"]),
            "decision": "complete_full200_all_dataset_superiority",
            "evidence_json": str(FULL200_SUMMARY),
            "evidence_md": str(FULL200_EVIDENCE_MD),
            "git_commit": {"myagent": myagent_commit, "mact": mact_commit},
        }
    )
    return rows


def p4b_rows(
    summary: dict[str, Any],
    *,
    mact_commit: str,
    myagent_commit: str,
    stage: str,
    evidence_json: Path,
    evidence_md: Path,
    row_status: str,
    aggregate_status: str,
    aggregate_decision: str,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for task in TASK_ORDER:
        item = summary["datasets"][task]
        myagent = item["myagent"]
        mact = item["mact"]
        n = int(myagent.get("num_samples") or myagent.get("num_with_gold") or 0)
        myagent_correct = correct_count(myagent)
        mact_correct = correct_count(mact)
        rows.append(
            {
                "stage": stage,
                "status": row_status,
                "dataset": task,
                "input_rows": n,
                "merged_rows": n,
                "eval_rows": n,
                "myagent_correct": myagent_correct,
                "mact_correct_or_reference": mact_correct,
                "accuracy_delta_correct": myagent_correct - mact_correct,
                "token_ratio": float(item["token_ratio_myagent_to_mact"]),
                "avg_total_tokens": float(myagent["avg_total_tokens"]),
                "avg_elapsed_seconds": float(myagent["avg_elapsed_seconds"]),
                "num_failed_exec": int(myagent["num_failed_exec"]),
                "num_missing_answer": int(myagent["num_missing_answer"]),
                "decision": "complete_dataset_superiority" if myagent_correct > mact_correct else "complete_dataset_risk",
                "evidence_json": str(evidence_json),
                "evidence_md": str(evidence_md),
                "git_commit": {"myagent": myagent_commit, "mact": mact_commit},
            }
        )
    overall = summary["overall"]
    myagent = overall["myagent"]
    mact = overall["mact"]
    n = int(myagent.get("num_samples") or myagent.get("num_with_gold") or 0)
    myagent_correct = correct_count(myagent)
    mact_correct = correct_count(mact)
    rows.append(
        {
            "stage": stage,
            "status": aggregate_status,
            "dataset": "aggregate",
            "input_rows": n,
            "merged_rows": n,
            "eval_rows": n,
            "myagent_correct": myagent_correct,
            "mact_correct_or_reference": mact_correct,
            "accuracy_delta_correct": myagent_correct - mact_correct,
            "token_ratio": float(summary["token_ratio_myagent_to_mact"]),
            "avg_total_tokens": float(myagent["avg_total_tokens"]),
            "avg_elapsed_seconds": float(myagent["avg_elapsed_seconds"]),
            "num_failed_exec": int(myagent["num_failed_exec"]),
            "num_missing_answer": int(myagent["num_missing_answer"]),
            "decision": aggregate_decision,
            "evidence_json": str(evidence_json),
            "evidence_md": str(evidence_md),
            "git_commit": {"myagent": myagent_commit, "mact": mact_commit},
        }
    )
    return rows


def targeted_fresh_rows(summary: dict[str, Any], *, mact_commit: str, myagent_commit: str) -> list[dict[str, Any]]:
    coverage = summary["coverage"]
    fresh = summary["fresh"]
    min_correct = int(fresh["min_correct"])
    correct = int(fresh["correct"])
    return [
        {
            "stage": "WTQ targeted fresh affected slice",
            "status": "complete" if summary["decision"] == "pass" else "complete_failed",
            "dataset": "wtq",
            "input_rows": int(coverage["expected_rows"]),
            "merged_rows": int(coverage["merged_rows"]),
            "eval_rows": int(coverage["eval_rows"]),
            "myagent_correct": correct,
            "mact_correct_or_reference": min_correct,
            "accuracy_delta_correct": correct - min_correct,
            "token_ratio": None,
            "avg_total_tokens": float(fresh["avg_total_tokens"]),
            "avg_elapsed_seconds": float(fresh["avg_elapsed_seconds"]),
            "num_failed_exec": int(fresh["num_failed_exec"]),
            "num_missing_answer": int(fresh["num_missing_answer"]),
            "decision": summary["decision"],
            "reference_label": "min_correct_threshold",
            "fresh_wrong_ids": fresh.get("fresh_wrong_ids", []),
            "evidence_json": str(P4B_WTQ_TARGETED_FRESH_SUMMARY),
            "evidence_md": str(P4B_WTQ_TARGETED_FRESH_SUMMARY_MD),
            "git_commit": {"myagent": myagent_commit, "mact": mact_commit},
        }
    ]


def seed_stage_name(seed: str, suffix: str) -> str:
    return f"E3 Seed-{seed.split('_', 1)[1].upper()} {suffix}"


def e3_current_rows(summary: dict[str, Any], *, mact_commit: str, myagent_commit: str) -> list[dict[str, Any]]:
    seed = summary["seed_label"]
    stage = seed_stage_name(seed, "current-only Gate-50")
    rows: list[dict[str, Any]] = []
    failures = 0
    missing = 0
    for task in TASK_ORDER:
        item = summary["datasets"][task]
        failures += int(item["num_failed_exec"])
        missing += int(item["num_missing_answer"])
        rows.append(
            {
                "stage": stage,
                "status": "complete_current_gate_pass"
                if item["passed_current_seed_gate"]
                else "complete_current_gate_inspect",
                "dataset": task,
                "input_rows": int(item["input_rows"]),
                "merged_rows": int(item["merged_rows"]),
                "eval_rows": int(item["eval_rows"]),
                "myagent_correct": int(item["correct"]),
                "mact_correct_or_reference": None,
                "accuracy_delta_correct": None,
                "token_ratio": float(item["token_ratio_to_mact_full200"]),
                "avg_total_tokens": float(item["avg_total_tokens"]),
                "avg_elapsed_seconds": float(item["avg_elapsed_seconds"]),
                "num_failed_exec": int(item["num_failed_exec"]),
                "num_missing_answer": int(item["num_missing_answer"]),
                "decision": "current_seed_gate_pass"
                if item["passed_current_seed_gate"]
                else "current_seed_gate_inspect",
                "reference_label": "current_gate_only_no_same_seed_mact",
                "evidence_json": str(E3_RUN_DIR / "summary" / f"{seed}_myagent_gate50_summary.json"),
                "evidence_md": str(E3_RUN_DIR / "summary" / f"{seed}_myagent_gate50_summary.md"),
                "git_commit": {"myagent": myagent_commit, "mact": mact_commit},
            }
        )
    overall = summary["overall"]
    rows.append(
        {
            "stage": stage,
            "status": "complete_current_only_gate_pass"
            if summary["decision"] == "run_paired_mact"
            else "complete_current_only_stop_or_inspect",
            "dataset": "aggregate",
            "input_rows": int(overall["rows"]),
            "merged_rows": int(overall["rows"]),
            "eval_rows": int(overall["rows"]),
            "myagent_correct": int(overall["correct"]),
            "mact_correct_or_reference": None,
            "accuracy_delta_correct": None,
            "token_ratio": float(overall["token_ratio_to_mact_full200_weighted"]),
            "avg_total_tokens": float(overall["avg_total_tokens_weighted"]),
            "avg_elapsed_seconds": float(overall["avg_elapsed_seconds_weighted"]),
            "num_failed_exec": failures,
            "num_missing_answer": missing,
            "decision": summary["decision"],
            "reference_label": "current_gate_only_no_same_seed_mact",
            "evidence_json": str(E3_RUN_DIR / "summary" / f"{seed}_myagent_gate50_summary.json"),
            "evidence_md": str(E3_RUN_DIR / "summary" / f"{seed}_myagent_gate50_summary.md"),
            "git_commit": {"myagent": myagent_commit, "mact": mact_commit},
        }
    )
    return rows


def e3_current_decisions() -> dict[str, str]:
    decisions: dict[str, str] = {}
    for seed in E3_SEEDS:
        path = E3_RUN_DIR / "summary" / f"{seed}_myagent_gate50_summary.json"
        if path.exists():
            decisions[seed] = read_json(path)["decision"]
    return decisions


def pending_rows(
    template: dict[str, Any],
    *,
    completed_stages: set[str],
    current_seed_decisions: dict[str, str],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in template["pending_experiment_rows"]:
        if item["stage"] in completed_stages:
            continue
        evidence_json = item.get("expected_evidence_json")
        evidence_md = item.get("expected_evidence_md")
        evidence_exists = bool(evidence_json and Path(evidence_json).exists())
        input_rows_observed = count_jsonl(item.get("input_path"))
        if input_rows_observed is None and "Seed-C" in item["stage"]:
            input_rows_observed = sum(
                count_jsonl(E3_RUN_DIR / "input" / "seed_c" / f"{task}_seed_c_gate50.jsonl") or 0
                for task in TASK_ORDER
            )
        if input_rows_observed is None and "Seed-D" in item["stage"]:
            input_rows_observed = sum(
                count_jsonl(E3_RUN_DIR / "input" / "seed_d" / f"{task}_seed_d_gate50.jsonl") or 0
                for task in TASK_ORDER
            )
        status = "needs_ledger_refresh_from_completed_evidence" if evidence_exists else item["status"]
        not_required_reason = None
        for seed in E3_SEEDS:
            if f"Seed-{seed.split('_', 1)[1].upper()} paired" in item["stage"]:
                decision = current_seed_decisions.get(seed)
                if decision and decision != "run_paired_mact":
                    status = "not_required"
                    not_required_reason = f"{seed} current-only decision={decision}"
        row = {
            "stage": item["stage"],
            "status": status,
            "dataset": item["dataset"],
            "input_rows_required": item["input_rows_required"],
            "input_rows_observed": input_rows_observed,
            "pass_condition": item["pass_condition"],
            "runner": item["runner"],
            "expected_evidence_json": evidence_json,
            "expected_evidence_md": evidence_md,
            "evidence_json_exists": evidence_exists,
            "evidence_md_exists": bool(evidence_md and Path(evidence_md).exists()),
            "if_fail": item["if_fail"],
        }
        if not_required_reason:
            row["not_required_reason"] = not_required_reason
        rows.append(row)
    return rows


def completion_summary(completed: list[dict[str, Any]], pending: list[dict[str, Any]]) -> dict[str, Any]:
    unresolved = [
        row["stage"]
        for row in pending
        if row["status"] not in {"complete", "accepted", "not_required"}
    ]
    return {
        "overall_status": "active_not_complete" if unresolved else "complete",
        "completed_result_rows": len(completed),
        "pending_result_rows": len(pending),
        "remaining_required_stages": unresolved,
        "can_write_now": [
            "Qwen3-32B full200 stage: MyAgent beats MACT on WTQ, TabFact, and CRT with lower aggregate tokens.",
            "P4b new-seed Gate-50 supports overall/token evidence but exposes WTQ risk.",
            "WTQ targeted fresh closure has completed, and P4b after-targeted Gate-50 shows all-dataset superiority.",
            "E3 Seed-C current-only Gate-50 is a documented stability boundary: overall 114/150, decision stop_or_inspect.",
            "E3 Seed-D current-only Gate-50 is a second documented stability boundary: overall 98/150, decision stop_or_inspect.",
            "E3 Seed-C/Seed-D offline boundary diagnosis has explained the current-gate boundary as semantic accuracy stability, not runtime/tool failure or token-budget failure.",
            "E4 latest readiness audit has completed with no untested local model path and no API provider profile, so no Gate-10 should be started yet.",
            "The current patent experiment section has been consolidated as draft-ready evidence with explicit unsupported-claim boundaries.",
        ],
        "cannot_write_yet": [
            "A viable additional model gate has completed.",
            "The final experiment package closeout has completed after either an E4 candidate result or explicit acceptance of the no-candidate boundary.",
        ],
    }


def render_number(value: Any, digits: int = 4) -> str:
    if value is None:
        return "n/a"
    if isinstance(value, float):
        return f"{value:.{digits}f}"
    return str(value)


def render_count(value: Any, rows: int) -> str:
    if value is None:
        return "n/a"
    return f"{value}/{rows}"


def render_delta(value: Any) -> str:
    if value is None:
        return "n/a"
    return f"{int(value):+d}"


def render_markdown(ledger: dict[str, Any]) -> str:
    lines = [
        "# Current Formal Result Ledger",
        "",
        f"Generated: `{ledger['generated_at_local']}`",
        "",
        f"Overall status: `{ledger['completion_summary']['overall_status']}`.",
        "",
        "## Completed Result Rows",
        "",
        "| stage | dataset | rows input/merged/eval | MyAgent | MACT/ref | delta | token ratio | avg tokens | avg elapsed s | failed/missing | decision |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in ledger["completed_rows"]:
        lines.append(
            f"| {row['stage']} | {row['dataset']} | "
            f"{row['input_rows']}/{row['merged_rows']}/{row['eval_rows']} | "
            f"{row['myagent_correct']}/{row['eval_rows']} | "
            f"{render_count(row['mact_correct_or_reference'], row['eval_rows'])} | "
            f"{render_delta(row['accuracy_delta_correct'])} | {render_number(row['token_ratio'])} | "
            f"{render_number(row['avg_total_tokens'], 2)} | {render_number(row['avg_elapsed_seconds'], 2)} | "
            f"{row['num_failed_exec']}/{row['num_missing_answer']} | `{row['decision']}` |"
        )
    lines.extend(
        [
            "",
            "## Pending Result Rows",
            "",
            "| stage | status | dataset | required rows | observed input rows | pass condition | evidence exists |",
            "|---|---|---|---:|---:|---|---|",
        ]
    )
    for row in ledger["pending_rows"]:
        lines.append(
            f"| {row['stage']} | `{row['status']}` | {row['dataset']} | "
            f"{row['input_rows_required']} | {row['input_rows_observed']} | "
            f"{row['pass_condition']} | json=`{row['evidence_json_exists']}`, md=`{row['evidence_md_exists']}` |"
        )
    readiness = (ledger.get("latest_runtime_preflight") or {}).get("readiness") or {}
    if readiness:
        lines.extend(
            [
                "",
                "## Runtime Preflight",
                "",
                f"Latest status: `{readiness.get('status')}`.",
                f"Recommendation: {readiness.get('recommendation')}",
            ]
        )
    lines.extend(["", "## Can Write Now", ""])
    lines.extend(f"- {item}" for item in ledger["completion_summary"]["can_write_now"])
    lines.extend(["", "## Claims Not Supported Yet", ""])
    lines.extend(f"- {item}" for item in ledger["completion_summary"]["cannot_write_yet"])
    lines.append("")
    return "\n".join(lines)


def build_ledger() -> dict[str, Any]:
    generated_at = dt.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
    myagent_commit = git_commit(MYAGENT_ROOT)
    mact_commit = git_commit(MACT_ROOT)
    template = read_json(FORMAL_TEMPLATE)
    completed = [
        *full200_rows(read_json(FULL200_SUMMARY), mact_commit=mact_commit, myagent_commit=myagent_commit),
        *p4b_rows(
            read_json(P4B_SUMMARY),
            mact_commit=mact_commit,
            myagent_commit=myagent_commit,
            stage="P4b new-seed paired Gate-50",
            evidence_json=P4B_SUMMARY,
            evidence_md=P4B_SUMMARY_MD,
            row_status="complete_risk_evidence",
            aggregate_status="complete_with_wtq_risk",
            aggregate_decision="accepted_existing_paired_gate_but_not_all_dataset_superiority",
        ),
    ]
    if P4B_WTQ_TARGETED_FRESH_SUMMARY.exists():
        completed.extend(
            targeted_fresh_rows(
                read_json(P4B_WTQ_TARGETED_FRESH_SUMMARY),
                mact_commit=mact_commit,
                myagent_commit=myagent_commit,
            )
        )
    if P4B_AFTER_TARGETED_SUMMARY.exists():
        completed.extend(
            p4b_rows(
                read_json(P4B_AFTER_TARGETED_SUMMARY),
                mact_commit=mact_commit,
                myagent_commit=myagent_commit,
                stage="P4b WTQ after-fix full50",
                evidence_json=P4B_AFTER_TARGETED_SUMMARY,
                evidence_md=P4B_AFTER_TARGETED_SUMMARY_MD,
                row_status="complete_after_targeted_evidence",
                aggregate_status="complete_after_targeted_all_dataset_superiority",
                aggregate_decision="accepted_after_targeted_all_dataset_superiority",
            )
        )
    for seed in E3_SEEDS:
        current_summary = E3_RUN_DIR / "summary" / f"{seed}_myagent_gate50_summary.json"
        if current_summary.exists():
            completed.extend(
                e3_current_rows(
                    read_json(current_summary),
                    mact_commit=mact_commit,
                    myagent_commit=myagent_commit,
                )
            )
    current_seed_decisions = e3_current_decisions()
    pending = pending_rows(
        template,
        completed_stages={row["stage"] for row in completed},
        current_seed_decisions=current_seed_decisions,
    )
    return {
        "artifact_name": "qwen3_32b_current_formal_result_ledger",
        "generated_at_local": generated_at,
        "purpose": "Current machine-readable formal result ledger for patent-facing MyAgent vs MACT evidence.",
        "scope_boundary": "This ledger compiles existing frozen artifacts and pending rows. It does not create new benchmark results.",
        "source_files": {
            "full200_summary": str(FULL200_SUMMARY),
            "p4b_summary": str(P4B_SUMMARY),
            "p4b_wtq_targeted_fresh_summary": str(P4B_WTQ_TARGETED_FRESH_SUMMARY),
            "p4b_after_targeted_summary": str(P4B_AFTER_TARGETED_SUMMARY),
            "e3_current_summaries": {
                seed: str(E3_RUN_DIR / "summary" / f"{seed}_myagent_gate50_summary.json")
                for seed in E3_SEEDS
                if (E3_RUN_DIR / "summary" / f"{seed}_myagent_gate50_summary.json").exists()
            },
            "e3_boundary_diagnosis_json": str(E3_BOUNDARY_DIAGNOSIS_JSON) if E3_BOUNDARY_DIAGNOSIS_JSON.exists() else None,
            "e3_boundary_diagnosis_md": str(E3_BOUNDARY_DIAGNOSIS_MD) if E3_BOUNDARY_DIAGNOSIS_MD.exists() else None,
            "e4_multimodel_readiness_json": str(E4_READINESS_JSON) if E4_READINESS_JSON.exists() else None,
            "e4_multimodel_readiness_md": str(E4_READINESS_MD) if E4_READINESS_MD.exists() else None,
            "current_patent_experiment_section_json": str(CURRENT_PATENT_SECTION_JSON)
            if CURRENT_PATENT_SECTION_JSON.exists()
            else None,
            "current_patent_experiment_section_md": str(CURRENT_PATENT_SECTION_MD)
            if CURRENT_PATENT_SECTION_MD.exists()
            else None,
            "formal_template": str(FORMAL_TEMPLATE),
            "latest_runtime_preflight": str(LATEST_PREFLIGHT),
        },
        "git_commits_at_generation": {
            "myagent": myagent_commit,
            "mact": mact_commit,
        },
        "completed_rows": completed,
        "pending_rows": pending,
        "latest_runtime_preflight": read_json(LATEST_PREFLIGHT) if LATEST_PREFLIGHT.exists() else None,
        "completion_summary": completion_summary(completed, pending),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=PACKAGE_DIR)
    args = parser.parse_args()
    ledger = build_ledger()
    stamp = dt.datetime.now().astimezone().strftime("%Y%m%d_%H%M%S")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    json_path = args.output_dir / f"formal_result_ledger_current_{stamp}.json"
    md_path = args.output_dir / f"formal_result_ledger_current_{stamp}_zh.md"
    latest_json = args.output_dir / "latest_formal_result_ledger_current.json"
    latest_md = args.output_dir / "latest_formal_result_ledger_current_zh.md"
    json_text = json.dumps(ledger, ensure_ascii=False, indent=2) + "\n"
    md_text = render_markdown(ledger)
    json_path.write_text(json_text, encoding="utf-8")
    md_path.write_text(md_text, encoding="utf-8")
    latest_json.write_text(json_text, encoding="utf-8")
    latest_md.write_text(md_text, encoding="utf-8")
    print(
        json.dumps(
            {
                "json": str(json_path),
                "md": str(md_path),
                "overall_status": ledger["completion_summary"]["overall_status"],
                "completed_rows": len(ledger["completed_rows"]),
                "pending_rows": len(ledger["pending_rows"]),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
