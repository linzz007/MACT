#!/usr/bin/env python3
"""Audit consistency across the patent experiment package, PRD, and ledgers."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


PACKAGE_DIR = Path(__file__).resolve().parent
MYAGENT_ROOT = Path("/home/ubuntu/lzz/MyAgent")
MACT_ROOT = Path("/home/ubuntu/lzz/MACT")
PRD_PATH = MYAGENT_ROOT / "docs/server/server_codex_reports/current-qwen3-mact-experiment-prd.md"
MANIFEST_PATH = PACKAGE_DIR / "evidence_manifest.json"
LEDGER_PATH = PACKAGE_DIR / "latest_formal_result_ledger_current.json"
PREFLIGHT_PATH = PACKAGE_DIR / "latest_qwen3_runtime_preflight.json"
E3_BOUNDARY_DIAGNOSIS_JSON = Path(
    "/home/ubuntu/lzz/MACT/outputs/server_runs/"
    "qwen3_32b_policy_v6b_multiseed_gate50_20260801_2231/"
    "summary/seed_boundary_error_diagnosis.json"
)
E3_BOUNDARY_DIAGNOSIS_MD = E3_BOUNDARY_DIAGNOSIS_JSON.with_suffix(".md")
E3_SEMANTIC_BOUNDARY_PLAN_JSON = Path(
    "/home/ubuntu/lzz/MACT/outputs/server_runs/"
    "qwen3_32b_policy_v6b_e3_semantic_boundary_plan_20260804_1110/"
    "summary/e3_semantic_boundary_plan.json"
)
E3_SEMANTIC_BOUNDARY_PLAN_MD = E3_SEMANTIC_BOUNDARY_PLAN_JSON.with_suffix(".md")
E3_GUARD_VALIDATION_INPUT_PLAN_JSON = Path(
    "/home/ubuntu/lzz/MACT/outputs/server_runs/"
    "qwen3_32b_policy_v6b_e3_guard_validation_inputs_20260804_1128/"
    "summary/e3_guard_validation_input_plan.json"
)
E3_GUARD_VALIDATION_INPUT_PLAN_MD = E3_GUARD_VALIDATION_INPUT_PLAN_JSON.with_suffix(".md")
E3_GUARD_VALIDATION_AFTER_GUARD_JSON = Path(
    "/home/ubuntu/lzz/MACT/outputs/server_runs/"
    "qwen3_32b_policy_v6b_e3_guard_validation_after_guard_20260804_1203/"
    "summary/e3_guard_validation_after_guard_summary.json"
)
E3_GUARD_VALIDATION_AFTER_GUARD_MD = E3_GUARD_VALIDATION_AFTER_GUARD_JSON.with_suffix(".md")
E3_S3_CURRENT_COMBINED_JSON = Path(
    "/home/ubuntu/lzz/MACT/outputs/server_runs/"
    "qwen3_32b_policy_v6b_e3_s3_current_rerun_after_guard_20260804_1425/"
    "summary/e3_s3_current_combined_summary.json"
)
E3_S3_CURRENT_COMBINED_MD = E3_S3_CURRENT_COMBINED_JSON.with_suffix(".md")
E3_BOUNDARY_FRESH_COMBINED_JSON = Path(
    "/home/ubuntu/lzz/MACT/outputs/server_runs/"
    "qwen3_32b_policy_v6c_seed_d_boundary_fresh_20260804_1549/"
    "summary/e3_boundary_fresh_combined_summary.json"
)
E3_BOUNDARY_FRESH_COMBINED_MD = E3_BOUNDARY_FRESH_COMBINED_JSON.with_suffix(".md")
E3_S5_FINAL_SUMMARY_JSON = Path(
    "/home/ubuntu/lzz/MACT/outputs/server_runs/"
    "qwen3_32b_policy_v6c_e3_s5_crt_tiebreaker_diag_20260804_2225/"
    "summary/e3_s5_final_combined_summary.json"
)
E3_S5_FINAL_SUMMARY_MD = E3_S5_FINAL_SUMMARY_JSON.with_suffix(".md")
E3_S5_AFFECTED_SLICE_JSON = Path(
    "/home/ubuntu/lzz/MACT/outputs/server_runs/"
    "qwen3_32b_policy_v6c_e3_s5_crt_tiebreaker_diag_20260804_2225/"
    "summary/s5_affected_slice_real_rerun_summary.json"
)
FINE_GRAINED_MECHANISM_AUDIT_JSON = Path(
    "/home/ubuntu/lzz/MACT/outputs/server_runs/"
    "qwen3_32b_policy_v6c_e3_fine_grained_mechanism_ablation_audit_20260804_2333/"
    "summary/fine_grained_mechanism_ablation_audit.json"
)
FINE_GRAINED_MECHANISM_AUDIT_MD = FINE_GRAINED_MECHANISM_AUDIT_JSON.with_suffix(".md")
E4_READINESS_JSON = PACKAGE_DIR / "latest_e4_multimodel_gate_readiness_audit.json"
E4_READINESS_MD = PACKAGE_DIR / "latest_e4_multimodel_gate_readiness_audit_zh.md"
CURRENT_PATENT_SECTION_JSON = PACKAGE_DIR / "latest_current_patent_experiment_section.json"
CURRENT_PATENT_SECTION_MD = PACKAGE_DIR / "latest_current_patent_experiment_section_zh.md"
CURRENT_COMPLETION_GAP_JSON = PACKAGE_DIR / "latest_completion_gap_audit_current.json"
CURRENT_COMPLETION_GAP_MD = PACKAGE_DIR / "latest_completion_gap_audit_current_zh.md"
PATENT_DISCLOSURE_DRAFT_MD = PACKAGE_DIR / "patent_disclosure_draft_zh.md"
GOAL_BLOCKER_AUDIT_JSON = PACKAGE_DIR / "latest_goal_blocker_audit_current.json"
GOAL_BLOCKER_AUDIT_MD = PACKAGE_DIR / "latest_goal_blocker_audit_current_zh.md"


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def e4_timestamped_paths(e4_readiness: dict[str, Any]) -> tuple[Path, Path, str]:
    generated_at = e4_readiness["generated_at_local"]
    local_dt = dt.datetime.strptime(generated_at.rsplit(" ", 1)[0], "%Y-%m-%d %H:%M:%S")
    stamp = local_dt.strftime("%Y%m%d_%H%M%S")
    return (
        PACKAGE_DIR / f"e4_multimodel_gate_readiness_audit_{stamp}.json",
        PACKAGE_DIR / f"e4_multimodel_gate_readiness_audit_{stamp}_zh.md",
        local_dt.strftime("%Y-%m-%d %H:%M"),
    )


def git_commit(repo: Path) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "--short", "HEAD"],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout.strip()


def add_path_check(report: dict[str, Any], label: str, path: Path) -> None:
    exists = path.exists()
    report["path_checks"][label] = {"path": str(path), "exists": exists}
    if not exists:
        report["errors"].append(f"missing path: {label}: {path}")


def check_equal(report: dict[str, Any], label: str, actual: Any, expected: Any) -> None:
    if actual != expected:
        report["errors"].append(f"{label}: expected {expected!r}, got {actual!r}")
    report["checks"][label] = {"actual": actual, "expected": expected, "pass": actual == expected}


def check_at_least(report: dict[str, Any], label: str, actual: int, minimum: int) -> None:
    passed = actual >= minimum
    if not passed:
        report["errors"].append(f"{label}: expected at least {minimum!r}, got {actual!r}")
    report["checks"][label] = {"actual": actual, "expected": f">={minimum}", "pass": passed}


def check_at_most(report: dict[str, Any], label: str, actual: int, maximum: int) -> None:
    passed = actual <= maximum
    if not passed:
        report["errors"].append(f"{label}: expected at most {maximum!r}, got {actual!r}")
    report["checks"][label] = {"actual": actual, "expected": f"<={maximum}", "pass": passed}


def check_contains(report: dict[str, Any], label: str, text: str, needle: str) -> None:
    passed = needle in text
    report["checks"][label] = {"needle": needle, "pass": passed}
    if not passed:
        report["errors"].append(f"{label}: missing text {needle!r}")


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Patent Package Consistency Audit",
        "",
        f"Generated: `{report['generated_at_local']}`",
        "",
        "| item | value |",
        "|---|---|",
        f"| overall status | `{report['overall_status']}` |",
        f"| errors | `{len(report['errors'])}` |",
        f"| warnings | `{len(report['warnings'])}` |",
        f"| MyAgent HEAD | `{report['git_heads']['myagent']}` |",
        f"| MACT HEAD | `{report['git_heads']['mact']}` |",
        "",
        "## Errors",
        "",
    ]
    if report["errors"]:
        lines.extend(f"- {item}" for item in report["errors"])
    else:
        lines.append("- none")
    lines.extend(["", "## Warnings", ""])
    if report["warnings"]:
        lines.extend(f"- {item}" for item in report["warnings"])
    else:
        lines.append("- none")
    lines.extend(
        [
            "",
            "## Key Checks",
            "",
            "| check | pass | actual | expected |",
            "|---|---:|---|---|",
        ]
    )
    for label, item in report["checks"].items():
        lines.append(
            f"| {label} | `{item.get('pass')}` | `{item.get('actual', item.get('needle', ''))}` | "
            f"`{item.get('expected', '')}` |"
        )
    lines.append("")
    return "\n".join(lines)


def build_report() -> dict[str, Any]:
    report: dict[str, Any] = {
        "generated_at_local": dt.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z"),
        "package_dir": str(PACKAGE_DIR),
        "git_heads": {
            "myagent": git_commit(MYAGENT_ROOT),
            "mact": git_commit(MACT_ROOT),
        },
        "path_checks": {},
        "checks": {},
        "errors": [],
        "warnings": [],
    }

    for label, path in {
        "prd": PRD_PATH,
        "manifest": MANIFEST_PATH,
        "latest_formal_result_ledger": LEDGER_PATH,
        "latest_runtime_preflight": PREFLIGHT_PATH,
        "queue_script": PACKAGE_DIR / "run_remaining_qwen3_patent_queue.sh",
        "runtime_preflight_script": PACKAGE_DIR / "preflight_qwen3_runtime.py",
        "formal_ledger_builder": PACKAGE_DIR / "build_current_formal_result_ledger.py",
        "e3_boundary_diagnosis_json": E3_BOUNDARY_DIAGNOSIS_JSON,
        "e3_boundary_diagnosis_md": E3_BOUNDARY_DIAGNOSIS_MD,
        "e3_semantic_boundary_plan_json": E3_SEMANTIC_BOUNDARY_PLAN_JSON,
        "e3_semantic_boundary_plan_md": E3_SEMANTIC_BOUNDARY_PLAN_MD,
        "e3_guard_validation_input_plan_json": E3_GUARD_VALIDATION_INPUT_PLAN_JSON,
        "e3_guard_validation_input_plan_md": E3_GUARD_VALIDATION_INPUT_PLAN_MD,
        "e3_guard_validation_after_guard_json": E3_GUARD_VALIDATION_AFTER_GUARD_JSON,
        "e3_guard_validation_after_guard_md": E3_GUARD_VALIDATION_AFTER_GUARD_MD,
        "e3_s3_current_combined_json": E3_S3_CURRENT_COMBINED_JSON,
        "e3_s3_current_combined_md": E3_S3_CURRENT_COMBINED_MD,
        "e3_boundary_fresh_combined_json": E3_BOUNDARY_FRESH_COMBINED_JSON,
        "e3_boundary_fresh_combined_md": E3_BOUNDARY_FRESH_COMBINED_MD,
        "e3_s5_final_summary_json": E3_S5_FINAL_SUMMARY_JSON,
        "e3_s5_final_summary_md": E3_S5_FINAL_SUMMARY_MD,
        "e3_s5_affected_slice_json": E3_S5_AFFECTED_SLICE_JSON,
        "fine_grained_mechanism_audit_json": FINE_GRAINED_MECHANISM_AUDIT_JSON,
        "fine_grained_mechanism_audit_md": FINE_GRAINED_MECHANISM_AUDIT_MD,
        "e4_multimodel_readiness_json": E4_READINESS_JSON,
        "e4_multimodel_readiness_md": E4_READINESS_MD,
        "current_patent_experiment_section_json": CURRENT_PATENT_SECTION_JSON,
        "current_patent_experiment_section_md": CURRENT_PATENT_SECTION_MD,
        "current_patent_experiment_section_builder": PACKAGE_DIR / "build_current_patent_experiment_section.py",
        "current_completion_gap_audit_json": CURRENT_COMPLETION_GAP_JSON,
        "current_completion_gap_audit_md": CURRENT_COMPLETION_GAP_MD,
        "current_completion_gap_audit_builder": PACKAGE_DIR / "build_current_completion_gap_audit.py",
        "claim_evidence_traceability_json": PACKAGE_DIR / "claim_evidence_traceability_20260801_2248.json",
        "claim_evidence_traceability_md": PACKAGE_DIR / "claim_evidence_traceability_20260801_2248_zh.md",
        "formal_experiment_schedule": PACKAGE_DIR / "formal_experiment_schedule_zh.md",
        "patent_disclosure_draft": PATENT_DISCLOSURE_DRAFT_MD,
        "goal_blocker_audit_json": GOAL_BLOCKER_AUDIT_JSON,
        "goal_blocker_audit_md": GOAL_BLOCKER_AUDIT_MD,
    }.items():
        add_path_check(report, label, path)

    if report["errors"]:
        report["overall_status"] = "fail"
        return report

    manifest = read_json(MANIFEST_PATH)
    ledger = read_json(LEDGER_PATH)
    preflight = read_json(PREFLIGHT_PATH)
    prd_text = PRD_PATH.read_text(encoding="utf-8")

    completed_rows = ledger.get("completed_rows") or []
    pending_rows = ledger.get("pending_rows") or []
    check_at_least(report, "ledger completed rows", len(completed_rows), 13)
    check_at_most(report, "ledger pending rows", len(pending_rows), 5)
    check_equal(
        report,
        "ledger overall status",
        ledger["completion_summary"]["overall_status"],
        "qwen3_strict_goal_complete_e4_pending",
    )
    stale_pending = [
        row["stage"]
        for row in pending_rows
        if row.get("status") == "needs_ledger_refresh_from_completed_evidence"
    ]
    check_equal(report, "stale completed evidence pending rows", stale_pending, [])

    aggregate_rows = [
        row
        for row in completed_rows
        if row["stage"] == "Qwen3-32B full200 anchor" and row["dataset"] == "aggregate"
    ]
    check_equal(report, "full200 aggregate row count", len(aggregate_rows), 1)
    if aggregate_rows:
        aggregate = aggregate_rows[0]
        check_equal(report, "full200 myagent correct", aggregate["myagent_correct"], 489)
        check_equal(report, "full200 mact correct", aggregate["mact_correct_or_reference"], 450)
        check_equal(report, "full200 failures", aggregate["num_failed_exec"], 0)
        check_equal(report, "full200 missing", aggregate["num_missing_answer"], 0)
        if float(aggregate["token_ratio"]) >= 0.75:
            report["errors"].append(f"full200 token ratio too high: {aggregate['token_ratio']}")

    p4b_wtq_rows = [
        row
        for row in completed_rows
        if row["stage"] == "P4b new-seed paired Gate-50" and row["dataset"] == "wtq"
    ]
    check_equal(report, "P4b WTQ risk row count", len(p4b_wtq_rows), 1)
    if p4b_wtq_rows:
        p4b_wtq = p4b_wtq_rows[0]
        check_equal(report, "P4b WTQ MyAgent correct", p4b_wtq["myagent_correct"], 37)
        check_equal(report, "P4b WTQ MACT correct", p4b_wtq["mact_correct_or_reference"], 43)
        check_equal(report, "P4b WTQ decision", p4b_wtq["decision"], "complete_dataset_risk")

    wtq_targeted_rows = [
        row
        for row in completed_rows
        if row["stage"] == "WTQ targeted fresh affected slice" and row["dataset"] == "wtq"
    ]
    check_equal(report, "WTQ targeted fresh row count", len(wtq_targeted_rows), 1)
    if wtq_targeted_rows:
        wtq_targeted = wtq_targeted_rows[0]
        check_equal(report, "WTQ targeted fresh MyAgent correct", wtq_targeted["myagent_correct"], 9)
        check_equal(report, "WTQ targeted fresh failures", wtq_targeted["num_failed_exec"], 0)
        check_equal(report, "WTQ targeted fresh missing", wtq_targeted["num_missing_answer"], 0)
        check_equal(report, "WTQ targeted fresh decision", wtq_targeted["decision"], "pass")

    p4b_after_rows = [
        row
        for row in completed_rows
        if row["stage"] == "P4b WTQ after-fix full50" and row["dataset"] == "aggregate"
    ]
    check_equal(report, "P4b after-targeted aggregate row count", len(p4b_after_rows), 1)
    if p4b_after_rows:
        p4b_after = p4b_after_rows[0]
        check_equal(report, "P4b after-targeted MyAgent correct", p4b_after["myagent_correct"], 121)
        check_equal(report, "P4b after-targeted MACT correct", p4b_after["mact_correct_or_reference"], 111)
        check_equal(report, "P4b after-targeted failures", p4b_after["num_failed_exec"], 0)
        check_equal(report, "P4b after-targeted missing", p4b_after["num_missing_answer"], 0)
        check_equal(
            report,
            "P4b after-targeted decision",
            p4b_after["decision"],
            "accepted_after_targeted_all_dataset_superiority",
        )
        if float(p4b_after["token_ratio"]) >= 0.75:
            report["errors"].append(f"P4b after-targeted token ratio too high: {p4b_after['token_ratio']}")

    seed_c_current_rows = [
        row
        for row in completed_rows
        if row["stage"] == "E3 Seed-C current-only Gate-50" and row["dataset"] == "aggregate"
    ]
    if seed_c_current_rows:
        seed_c_current = seed_c_current_rows[0]
        check_equal(report, "E3 Seed-C current row count", len(seed_c_current_rows), 1)
        check_equal(report, "E3 Seed-C current MyAgent correct", seed_c_current["myagent_correct"], 114)
        check_equal(report, "E3 Seed-C current failures", seed_c_current["num_failed_exec"], 0)
        check_equal(report, "E3 Seed-C current missing", seed_c_current["num_missing_answer"], 0)
        check_equal(report, "E3 Seed-C current decision", seed_c_current["decision"], "stop_or_inspect")

    seed_d_current_rows = [
        row
        for row in completed_rows
        if row["stage"] == "E3 Seed-D current-only Gate-50" and row["dataset"] == "aggregate"
    ]
    if seed_d_current_rows:
        seed_d_current = seed_d_current_rows[0]
        check_equal(report, "E3 Seed-D current row count", len(seed_d_current_rows), 1)
        check_equal(report, "E3 Seed-D current MyAgent correct", seed_d_current["myagent_correct"], 98)
        check_equal(report, "E3 Seed-D current failures", seed_d_current["num_failed_exec"], 0)
        check_equal(report, "E3 Seed-D current missing", seed_d_current["num_missing_answer"], 0)
        check_equal(report, "E3 Seed-D current decision", seed_d_current["decision"], "stop_or_inspect")

    seed_pending = [row for row in pending_rows if "Seed-" in row["stage"]]
    check_equal(report, "E3 pending seed rows after S5", seed_pending, [])

    boundary_fresh_rows = [
        row
        for row in completed_rows
        if row["stage"] == "E3 v6c boundary-fresh current-only combined candidate"
        and row["dataset"] == "aggregate"
    ]
    check_equal(report, "E3 boundary-fresh aggregate row count", len(boundary_fresh_rows), 1)
    if boundary_fresh_rows:
        boundary_fresh = boundary_fresh_rows[0]
        check_equal(report, "E3 boundary-fresh MyAgent correct", boundary_fresh["myagent_correct"], 229)
        check_equal(report, "E3 boundary-fresh failures", boundary_fresh["num_failed_exec"], 0)
        check_equal(report, "E3 boundary-fresh missing", boundary_fresh["num_missing_answer"], 0)
        check_equal(
            report,
            "E3 boundary-fresh decision",
            boundary_fresh["decision"],
            "boundary_fresh_pass_run_paired_mact_candidate",
        )

    s5_final_rows = [
        row
        for row in completed_rows
        if row["stage"] == "E3 S5 final paired combined"
        and row["dataset"] == "aggregate"
    ]
    check_equal(report, "E3 S5 final aggregate row count", len(s5_final_rows), 1)
    if s5_final_rows:
        s5_final = s5_final_rows[0]
        check_equal(report, "E3 S5 final MyAgent correct", s5_final["myagent_correct"], 232)
        check_equal(report, "E3 S5 final MACT correct", s5_final["mact_correct_or_reference"], 223)
        check_equal(report, "E3 S5 final failures", s5_final["num_failed_exec"], 0)
        check_equal(report, "E3 S5 final missing", s5_final["num_missing_answer"], 0)
        check_equal(report, "E3 S5 final MACT failures", s5_final.get("mact_num_failed_exec"), 4)
        check_equal(report, "E3 S5 final MACT missing", s5_final.get("mact_num_missing_answer"), 4)
        check_equal(report, "E3 S5 final decision", s5_final["decision"], "s5_strict_all_dataset_pass")

    latest_status = preflight["readiness"]["status"]
    ledger_status = ledger["latest_runtime_preflight"]["readiness"]["status"]
    check_equal(report, "preflight status matches ledger", ledger_status, latest_status)
    check_equal(
        report,
        "preflight generated_at matches ledger",
        ledger["latest_runtime_preflight"]["generated_at_local"],
        preflight["generated_at_local"],
    )
    if latest_status != "ready_existing_endpoint":
        report["warnings"].append(f"online experiments remain gated by runtime status: {latest_status}")

    manifest_ledger = manifest["formal_result_tables_template"]["latest_current_ledger_json"]
    manifest_preflight = manifest["remaining_qwen3_queue"]["latest_runtime_preflight_json"]
    boundary_manifest = manifest["multiseed_e3_prepared"]["boundary_error_diagnosis"]
    semantic_boundary_manifest = manifest["e3_semantic_boundary_plan"]
    guard_validation_manifest = manifest["e3_guard_validation_inputs"]
    guard_validation_after_manifest = manifest["e3_guard_validation_after_guard"]
    s3_current_manifest = manifest["e3_s3_current_after_guard"]
    boundary_fresh_manifest = manifest["e3_boundary_fresh_current_candidate"]
    s5_manifest = manifest["e3_s5_crt_tiebreaker"]
    fine_manifest = manifest["fine_grained_mechanism_ablation_audit"]
    fine_audit = read_json(FINE_GRAINED_MECHANISM_AUDIT_JSON)
    e4_manifest = manifest["multimodel_e4_readiness"]
    e4_readiness = read_json(E4_READINESS_JSON)
    e4_stamped_json, e4_stamped_md, e4_generated_label = e4_timestamped_paths(e4_readiness)
    current_section_manifest = manifest["current_patent_experiment_section"]
    current_section = read_json(CURRENT_PATENT_SECTION_JSON)
    completion_gap_manifest = manifest["completion_gap_audit"]
    completion_gap = read_json(CURRENT_COMPLETION_GAP_JSON)
    goal_blocker_manifest = manifest["goal_blocker_audit"]
    goal_blocker = read_json(GOAL_BLOCKER_AUDIT_JSON)
    goal_blocker_md = GOAL_BLOCKER_AUDIT_MD.read_text(encoding="utf-8")
    check_equal(report, "manifest latest ledger path", manifest_ledger, str(LEDGER_PATH))
    check_equal(report, "manifest latest preflight path", manifest_preflight, str(PREFLIGHT_PATH))
    check_equal(report, "manifest E3 boundary json path", boundary_manifest["json"], str(E3_BOUNDARY_DIAGNOSIS_JSON))
    check_equal(report, "manifest E3 boundary md path", boundary_manifest["md"], str(E3_BOUNDARY_DIAGNOSIS_MD))
    check_equal(report, "manifest E3 boundary status", boundary_manifest["status"], "complete_offline_diagnosis")
    check_equal(report, "manifest E3 boundary rows", boundary_manifest["aggregate"]["rows"], 300)
    check_equal(report, "manifest E3 boundary correct", boundary_manifest["aggregate"]["correct"], 212)
    check_equal(report, "manifest E3 boundary failed", boundary_manifest["aggregate"]["failed"], 0)
    check_equal(report, "manifest E3 boundary missing", boundary_manifest["aggregate"]["missing"], 0)
    check_equal(report, "manifest E3 boundary verification", boundary_manifest["aggregate"]["verification_status"], "pass")
    semantic_plan = read_json(E3_SEMANTIC_BOUNDARY_PLAN_JSON)
    check_equal(
        report,
        "manifest E3 semantic plan json path",
        semantic_boundary_manifest["summary_json"],
        str(E3_SEMANTIC_BOUNDARY_PLAN_JSON),
    )
    check_equal(
        report,
        "manifest E3 semantic plan md path",
        semantic_boundary_manifest["summary_md"],
        str(E3_SEMANTIC_BOUNDARY_PLAN_MD),
    )
    check_equal(
        report,
        "manifest E3 semantic plan decision",
        semantic_boundary_manifest["decision"],
        semantic_plan["current_decision"],
    )
    check_equal(
        report,
        "manifest E3 semantic plan high-priority count",
        semantic_boundary_manifest["high_priority_work_item_count"],
        len(semantic_plan["high_priority_work_items"]),
    )
    guard_validation = read_json(E3_GUARD_VALIDATION_INPUT_PLAN_JSON)
    check_equal(
        report,
        "manifest E3 guard validation json path",
        guard_validation_manifest["summary_json"],
        str(E3_GUARD_VALIDATION_INPUT_PLAN_JSON),
    )
    check_equal(
        report,
        "manifest E3 guard validation md path",
        guard_validation_manifest["summary_md"],
        str(E3_GUARD_VALIDATION_INPUT_PLAN_MD),
    )
    check_equal(
        report,
        "manifest E3 guard validation decision",
        guard_validation_manifest["decision"],
        guard_validation["validation_decision"],
    )
    check_equal(
        report,
        "manifest E3 guard validation total rows",
        guard_validation_manifest["total_rows"],
        guard_validation["total_rows"],
    )
    check_equal(
        report,
        "manifest E3 guard validation representative rows",
        guard_validation_manifest["role_counts"]["representative_wrong"],
        guard_validation["role_counts"]["representative_wrong"],
    )
    check_equal(
        report,
        "manifest E3 guard validation no-harm rows",
        guard_validation_manifest["role_counts"]["no_harm_correct"],
        guard_validation["role_counts"]["no_harm_correct"],
    )
    guard_validation_after = read_json(E3_GUARD_VALIDATION_AFTER_GUARD_JSON)
    check_equal(
        report,
        "manifest E3 after-guard json path",
        guard_validation_after_manifest["summary_json"],
        str(E3_GUARD_VALIDATION_AFTER_GUARD_JSON),
    )
    check_equal(
        report,
        "manifest E3 after-guard md path",
        guard_validation_after_manifest["summary_md"],
        str(E3_GUARD_VALIDATION_AFTER_GUARD_MD),
    )
    check_equal(
        report,
        "manifest E3 after-guard decision",
        guard_validation_after_manifest["decision"],
        guard_validation_after["decision"],
    )
    check_equal(
        report,
        "manifest E3 after-guard rows",
        guard_validation_after_manifest["aggregate"]["rows"],
        guard_validation_after["aggregate"]["rows"],
    )
    check_equal(
        report,
        "manifest E3 after-guard representative recovered",
        guard_validation_after_manifest["aggregate"]["representative_recovered"],
        guard_validation_after["aggregate"]["representative_recovered"],
    )
    check_equal(
        report,
        "manifest E3 after-guard no-harm correct",
        guard_validation_after_manifest["aggregate"]["no_harm_correct"],
        guard_validation_after["aggregate"]["no_harm_correct"],
    )
    check_equal(
        report,
        "manifest E3 after-guard failed",
        guard_validation_after_manifest["aggregate"]["failed"],
        guard_validation_after["aggregate"]["failed"],
    )
    check_equal(
        report,
        "manifest E3 after-guard missing",
        guard_validation_after_manifest["aggregate"]["missing"],
        guard_validation_after["aggregate"]["missing"],
    )
    s3_current = read_json(E3_S3_CURRENT_COMBINED_JSON)
    check_equal(
        report,
        "manifest E3 S3 json path",
        s3_current_manifest["summary_json"],
        str(E3_S3_CURRENT_COMBINED_JSON),
    )
    check_equal(
        report,
        "manifest E3 S3 md path",
        s3_current_manifest["summary_md"],
        str(E3_S3_CURRENT_COMBINED_MD),
    )
    check_equal(
        report,
        "manifest E3 S3 decision",
        s3_current_manifest["decision"],
        s3_current["decision"],
    )
    check_equal(
        report,
        "manifest E3 S3 paired next",
        s3_current_manifest["paired_mact_next"],
        s3_current["paired_mact_next"],
    )
    check_equal(
        report,
        "manifest E3 S3 correct",
        s3_current_manifest["overall"]["correct"],
        s3_current["overall"]["correct"],
    )
    check_equal(
        report,
        "manifest E3 S3 failed",
        s3_current_manifest["overall"]["failed"],
        s3_current["overall"]["failed"],
    )
    boundary_fresh_summary = read_json(E3_BOUNDARY_FRESH_COMBINED_JSON)
    check_equal(
        report,
        "manifest E3 boundary-fresh json path",
        boundary_fresh_manifest["summary_json"],
        str(E3_BOUNDARY_FRESH_COMBINED_JSON),
    )
    check_equal(
        report,
        "manifest E3 boundary-fresh md path",
        boundary_fresh_manifest["summary_md"],
        str(E3_BOUNDARY_FRESH_COMBINED_MD),
    )
    check_equal(
        report,
        "manifest E3 boundary-fresh decision",
        boundary_fresh_manifest["decision"],
        boundary_fresh_summary["decision"],
    )
    check_equal(
        report,
        "manifest E3 boundary-fresh paired next",
        boundary_fresh_manifest["paired_mact_next"],
        boundary_fresh_summary["paired_mact_next"],
    )
    check_equal(
        report,
        "manifest E3 boundary-fresh correct",
        boundary_fresh_manifest["overall"]["correct"],
        boundary_fresh_summary["overall"]["correct"],
    )
    s5_summary = read_json(E3_S5_FINAL_SUMMARY_JSON)
    check_equal(report, "manifest E3 S5 json path", s5_manifest["final_summary_json"], str(E3_S5_FINAL_SUMMARY_JSON))
    check_equal(report, "manifest E3 S5 md path", s5_manifest["final_summary_md"], str(E3_S5_FINAL_SUMMARY_MD))
    check_equal(report, "manifest E3 S5 decision", s5_manifest["decision"], s5_summary["decision"])
    check_equal(report, "manifest E3 S5 MyAgent correct", s5_manifest["overall"]["myagent_correct"], 232)
    check_equal(report, "manifest E3 S5 MACT correct", s5_manifest["overall"]["mact_correct"], 223)
    check_equal(report, "manifest E3 S5 strict all", s5_manifest["strict_all_dataset_superiority"], True)
    check_equal(
        report,
        "manifest fine-grained audit json path",
        fine_manifest["json"],
        str(FINE_GRAINED_MECHANISM_AUDIT_JSON),
    )
    check_equal(
        report,
        "manifest fine-grained audit md path",
        fine_manifest["md"],
        str(FINE_GRAINED_MECHANISM_AUDIT_MD),
    )
    check_equal(
        report,
        "manifest fine-grained audit decision",
        fine_manifest["decision"],
        fine_audit["decision"],
    )
    check_equal(
        report,
        "fine audit no-strong delta",
        fine_audit["coarse_ablation"]["no_strong_verification"]["delta_vs_current"],
        -8,
    )
    check_equal(
        report,
        "fine audit no-deterministic delta",
        fine_audit["coarse_ablation"]["no_deterministic_shortcuts"]["delta_vs_current"],
        -15,
    )
    check_equal(
        report,
        "fine audit S2 representative recovery delta",
        fine_audit["s2_guard_fresh_delta"]["representative_recovery_delta"],
        4,
    )
    check_equal(
        report,
        "fine audit S2 no-harm delta",
        fine_audit["s2_guard_fresh_delta"]["no_harm_delta"],
        1,
    )
    check_equal(
        report,
        "fine audit S5 full CRT delta",
        fine_audit["s5_crt_scalar_canonicalization"]["full_crt_delta_correct"],
        3,
    )
    check_equal(report, "manifest E4 readiness json path", e4_manifest["latest_json"], str(E4_READINESS_JSON))
    check_equal(report, "manifest E4 readiness md path", e4_manifest["latest_md"], str(E4_READINESS_MD))
    check_equal(
        report,
        "manifest E4 timestamped json path",
        e4_manifest["latest_timestamped_json"],
        str(e4_stamped_json),
    )
    check_equal(
        report,
        "manifest E4 timestamped md path",
        e4_manifest["latest_timestamped_md"],
        str(e4_stamped_md),
    )
    check_equal(report, "manifest E4 readiness status", e4_manifest["status"], e4_readiness["decision"])
    check_equal(report, "manifest E4 can start gate10", e4_manifest["can_start_gate10_now"], e4_readiness["can_start_gate10_now"])
    check_equal(
        report,
        "manifest E4 default GPU pool availability",
        e4_manifest["default_gpu_pool_available_for_next_start"],
        e4_readiness["runtime_snapshot"]["gpu"]["default_pool_available_for_next_start"],
    )
    check_equal(report, "E4 readiness decision", e4_readiness["decision"], "no_candidate_wait")
    check_equal(report, "E4 untested local model count", len(e4_readiness["model_readiness"]["untested_local_models"]), 0)
    check_equal(report, "E4 API key count", len(e4_readiness["model_readiness"]["api_keys_present"]), 0)
    check_equal(
        report,
        "E4 visible resident process count",
        e4_readiness["runtime_snapshot"]["processes"]["visible_runner_or_model_processes"],
        2,
    )
    check_equal(
        report,
        "manifest current patent section json path",
        current_section_manifest["latest_json"],
        str(CURRENT_PATENT_SECTION_JSON),
    )
    check_equal(
        report,
        "manifest current patent section md path",
        current_section_manifest["latest_md"],
        str(CURRENT_PATENT_SECTION_MD),
    )
    check_equal(
        report,
        "current patent section status",
        current_section["write_status"]["current_status"],
        "s5_strict_all_dataset_pass",
    )
    check_equal(
        report,
        "current patent section E4 decision",
        current_section["e4_multimodel_gate"]["decision"],
        "no_candidate_wait",
    )
    check_equal(
        report,
        "current patent section E4 timestamped json",
        current_section["evidence_paths"]["e4_readiness_latest_timestamped_json"],
        str(e4_stamped_json),
    )
    check_equal(
        report,
        "current patent section E3 guard validation rows",
        current_section["e3_multiseed_boundary"]["guard_validation_inputs"]["total_rows"],
        30,
    )
    check_equal(
        report,
        "current patent section E3 after-guard decision",
        current_section["e3_multiseed_boundary"]["guard_validation_after_guard"]["decision"],
        "after_guard_passes_s2_gate",
    )
    check_equal(
        report,
        "current patent section E3 after-guard recovered",
        current_section["e3_multiseed_boundary"]["guard_validation_after_guard"]["aggregate"][
            "representative_recovered"
        ],
        8,
    )
    check_equal(
        report,
        "current patent section E3 after-guard no-harm",
        current_section["e3_multiseed_boundary"]["guard_validation_after_guard"]["aggregate"][
            "no_harm_correct"
        ],
        18,
    )
    check_equal(
        report,
        "current patent section E3 S3 decision",
        current_section["e3_multiseed_boundary"]["s3_current_after_guard"]["decision"],
        "s3_stop_or_inspect_boundary_remains",
    )
    check_equal(
        report,
        "current patent section E3 S3 correct",
        current_section["e3_multiseed_boundary"]["s3_current_after_guard"]["overall"]["correct"],
        215,
    )
    check_equal(
        report,
        "current patent section E3 boundary-fresh decision",
        current_section["e3_multiseed_boundary"]["boundary_fresh_current_candidate"]["decision"],
        "boundary_fresh_pass_run_paired_mact_candidate",
    )
    check_equal(
        report,
        "current patent section E3 boundary-fresh correct",
        current_section["e3_multiseed_boundary"]["boundary_fresh_current_candidate"]["overall"][
            "correct"
        ],
        229,
    )
    check_equal(
        report,
        "current patent section E3 S5 decision",
        current_section["e3_multiseed_boundary"]["s5_final_paired_combined"]["decision"],
        "s5_strict_all_dataset_pass",
    )
    check_equal(
        report,
        "current patent section E3 S5 MyAgent correct",
        current_section["e3_multiseed_boundary"]["s5_final_paired_combined"]["overall"]["myagent_correct"],
        232,
    )
    check_equal(
        report,
        "current patent section fine audit path",
        current_section["evidence_paths"]["fine_grained_mechanism_ablation_audit"],
        str(FINE_GRAINED_MECHANISM_AUDIT_JSON),
    )
    check_contains(
        report,
        "current patent section unsupported multi-model claim",
        "\n".join(current_section["write_status"]["unsupported_claims"]),
        "Do not claim multi-model validation is complete.",
    )
    check_equal(
        report,
        "manifest completion gap latest json path",
        completion_gap_manifest["latest_json"],
        str(CURRENT_COMPLETION_GAP_JSON),
    )
    check_equal(
        report,
        "manifest completion gap latest md path",
        completion_gap_manifest["latest_md"],
        str(CURRENT_COMPLETION_GAP_MD),
    )
    check_equal(
        report,
        "current completion gap overall status",
        completion_gap["overall_completion_status"],
        "qwen3_strict_goal_complete_e4_pending",
    )
    requirements_by_id = {item["id"]: item for item in completion_gap["requirements"]}
    requirement_status = {item_id: item["status"] for item_id, item in requirements_by_id.items()}
    check_equal(
        report,
        "completion gap R2 status",
        requirement_status.get("R2"),
        "complete_for_current_qwen3_patent_scope_with_boundary",
    )
    check_equal(report, "completion gap R3 status", requirement_status.get("R3"), "complete")
    check_equal(
        report,
        "completion gap R4 status",
        requirement_status.get("R4"),
        "complete_strict_all_dataset_pass",
    )
    check_equal(report, "completion gap R5 status", requirement_status.get("R5"), "pending_no_candidate")
    check_equal(
        report,
        "completion gap E4 decision",
        requirements_by_id["R5"]["metrics"]["decision"],
        "no_candidate_wait",
    )
    check_equal(
        report,
        "completion gap semantic plan decision",
        requirements_by_id["R4"]["metrics"]["semantic_boundary_plan"]["decision"],
        "do_not_rerun_full200_or_paired_mact_until_targeted_guards_pass",
    )
    check_equal(
        report,
        "completion gap guard validation decision",
        requirements_by_id["R4"]["metrics"]["guard_validation_input_plan"]["decision"],
        "ready_for_guard_implementation_not_model_run",
    )
    check_equal(
        report,
        "completion gap guard validation rows",
        requirements_by_id["R4"]["metrics"]["guard_validation_input_plan"]["total_rows"],
        30,
    )
    check_equal(
        report,
        "completion gap after-guard decision",
        requirements_by_id["R4"]["metrics"]["guard_validation_after_guard"]["decision"],
        "after_guard_passes_s2_gate",
    )
    check_equal(
        report,
        "completion gap after-guard recovered",
        requirements_by_id["R4"]["metrics"]["guard_validation_after_guard"]["aggregate"][
            "representative_recovered"
        ],
        8,
    )
    check_equal(
        report,
        "completion gap after-guard no-harm",
        requirements_by_id["R4"]["metrics"]["guard_validation_after_guard"]["aggregate"][
            "no_harm_correct"
        ],
        18,
    )
    check_equal(
        report,
        "completion gap S3 decision",
        requirements_by_id["R4"]["metrics"]["s3_current_after_guard"]["decision"],
        "s3_stop_or_inspect_boundary_remains",
    )
    check_equal(
        report,
        "completion gap S3 correct",
        requirements_by_id["R4"]["metrics"]["s3_current_after_guard"]["overall"]["correct"],
        215,
    )
    check_equal(
        report,
        "completion gap boundary-fresh decision",
        requirements_by_id["R4"]["metrics"]["boundary_fresh_current_candidate"]["decision"],
        "boundary_fresh_pass_run_paired_mact_candidate",
    )
    check_equal(
        report,
        "completion gap boundary-fresh correct",
        requirements_by_id["R4"]["metrics"]["boundary_fresh_current_candidate"]["overall"][
            "correct"
        ],
        229,
    )
    check_equal(
        report,
        "completion gap S5 decision",
        requirements_by_id["R4"]["metrics"]["s5_final_paired_combined"]["decision"],
        "s5_strict_all_dataset_pass",
    )
    check_equal(
        report,
        "completion gap S5 MyAgent correct",
        requirements_by_id["R4"]["metrics"]["s5_final_paired_combined"]["overall"]["myagent_correct"],
        232,
    )
    check_equal(
        report,
        "completion gap fine audit decision",
        requirements_by_id["R2"]["metrics"]["fine_grained_decision"],
        fine_audit["decision"],
    )
    check_equal(
        report,
        "completion gap fine audit S2 recovery delta",
        requirements_by_id["R2"]["metrics"]["s2_guard_representative_recovery_delta"],
        4,
    )
    check_equal(
        report,
        "completion gap default GPU pool availability",
        completion_gap["runtime_recheck"]["default_gpu_pool_available_for_next_start"],
        e4_readiness["runtime_snapshot"]["gpu"]["default_pool_available_for_next_start"],
    )
    check_equal(
        report,
        "manifest goal blocker latest json path",
        goal_blocker_manifest["latest_json"],
        str(GOAL_BLOCKER_AUDIT_JSON),
    )
    check_equal(
        report,
        "manifest goal blocker latest md path",
        goal_blocker_manifest["latest_md"],
        str(GOAL_BLOCKER_AUDIT_MD),
    )
    check_equal(
        report,
        "goal blocker status recommendation",
        goal_blocker["current_goal_status_recommendation"],
        "blocked_waiting_external_state",
    )
    blocker_names = [item["name"] for item in goal_blocker["blocking_conditions"]]
    check_equal(
        report,
        "goal blocker names",
        blocker_names,
        ["No viable E4 multi-model candidate", "Qwen3 runtime readiness"],
    )
    check_equal(
        report,
        "goal blocker E4 decision",
        goal_blocker["blocking_conditions"][0]["details"]["decision"],
        e4_readiness["decision"],
    )
    check_equal(
        report,
        "goal blocker E4 can start",
        goal_blocker["blocking_conditions"][0]["details"]["can_start_gate10_now"],
        e4_readiness["can_start_gate10_now"],
    )
    check_equal(
        report,
        "goal blocker runtime status",
        goal_blocker["blocking_conditions"][1]["details"]["preflight_status"],
        preflight["readiness"]["status"],
    )
    check_contains(
        report,
        "goal blocker no-candidate markdown",
        goal_blocker_md,
        "E4 没有可用多模型候选",
    )
    check_contains(
        report,
        "goal blocker runtime markdown",
        goal_blocker_md,
        "Qwen3 runtime 已恢复",
    )
    stale_completion_claims = [
        "Seed-C/Seed-D boundary diagnosis and at least one viable multi-model gate result remain missing",
        "WTQ fresh targeted run 未完成",
        "fresh Qwen targeted run 尚未执行",
    ]
    completion_gap_md = CURRENT_COMPLETION_GAP_MD.read_text(encoding="utf-8")
    for stale_text in stale_completion_claims:
        if stale_text in completion_gap_md:
            report["errors"].append(f"current completion gap audit contains stale text: {stale_text!r}")
    claim_traceability_json = read_json(PACKAGE_DIR / "claim_evidence_traceability_20260801_2248.json")
    claim_traceability_md = (PACKAGE_DIR / "claim_evidence_traceability_20260801_2248_zh.md").read_text(encoding="utf-8")
    formal_schedule_text = (PACKAGE_DIR / "formal_experiment_schedule_zh.md").read_text(encoding="utf-8")
    patent_disclosure_text = PATENT_DISCLOSURE_DRAFT_MD.read_text(encoding="utf-8")
    for stale_text in [
        "WTQ fresh pending",
        "fresh closure pending",
        "还要跑 WTQ 9-row targeted fresh 和 after-fix full50",
        "Fresh WTQ targeted run is still pending",
        "Need WTQ targeted fresh affected-slice validation",
        "actual Seed-C/Seed-D execution",
        "模型执行仍 pending",
        "Seed-C/Seed-D current-only 和 paired MACT",
    ]:
        if stale_text in claim_traceability_md:
            report["errors"].append(f"claim traceability markdown contains stale text: {stale_text!r}")
        if stale_text in json.dumps(claim_traceability_json, ensure_ascii=False):
            report["errors"].append(f"claim traceability json contains stale text: {stale_text!r}")
        if stale_text in formal_schedule_text:
            report["errors"].append(f"formal experiment schedule contains stale text: {stale_text!r}")
        if stale_text in patent_disclosure_text:
            report["errors"].append(f"patent disclosure draft contains stale text: {stale_text!r}")
    check_contains(
        report,
        "claim traceability WTQ closure",
        claim_traceability_md,
        "WTQ targeted fresh 与 P4b after-targeted 闭环已经完成",
    )
    check_contains(
        report,
        "claim traceability E3 boundary",
        claim_traceability_md,
        "E3 Seed-C/D current-only 已完成并形成边界证据",
    )
    check_contains(
        report,
        "claim traceability E3 semantic plan",
        claim_traceability_md,
        "E3 semantic-boundary plan",
    )
    check_contains(
        report,
        "claim traceability fine audit",
        claim_traceability_md,
        "fine-grained mechanism audit 已完成",
    )
    check_contains(
        report,
        "formal schedule E3 boundary",
        formal_schedule_text,
        "S5 CRT tie-breaker 已闭合该边界",
    )
    check_contains(
        report,
        "formal schedule fine audit",
        formal_schedule_text,
        "fine-grained mechanism audit",
    )
    for label, needle in {
        "patent disclosure full200": "Aggregate | 600/600/600 | 489/600 | 450/600 | +39 | 0.5717 | 0/0",
        "patent disclosure P4b closure": "Overall | 150/150/150 | 121/150 | 111/150 | +10 | 0.5310 | 0/0",
        "patent disclosure E3 boundary": "Combined | 300/300/300 | 212/300 | 0.5916 | 0/0 | `complete_boundary_evidence`",
        "patent disclosure E3 S3 boundary": "Combined | 300/300/300 | 215/300 | 0.5866 | 0/0 | `s3_stop_or_inspect_boundary_remains`",
        "patent disclosure E3 boundary fresh": "Combined | 300/300/300 | 229/300 | 0.5794 | 0/0 | `boundary_fresh_pass_run_paired_mact_candidate`",
        "patent disclosure E3 S5 final": "Overall | 300 | 232/300 | 223/300 | +9 | 0.5662 | MyAgent 0/0; MACT 4/4",
        "patent disclosure fine audit": "细粒度机制消融审计",
        "patent disclosure E4 boundary": f"{e4_generated_label} 最新 E4 多模型 readiness audit 结果为 `no_candidate_wait`",
        "patent disclosure evidence paths": "latest_completion_gap_audit_current_zh.md",
    }.items():
        check_contains(report, label, patent_disclosure_text, needle)
    check_equal(
        report,
        "manifest online status",
        manifest["remaining_qwen3_queue"]["current_online_status"],
        latest_status,
    )

    for label, needle in {
        "PRD queue script": "run_remaining_qwen3_patent_queue.sh",
        "PRD runtime preflight": "latest_qwen3_runtime_preflight_zh.md",
        "PRD formal ledger": "latest_formal_result_ledger_current_zh.md",
        "PRD current patent section": "latest_current_patent_experiment_section_zh.md",
        "PRD current completion gap audit": "latest_completion_gap_audit_current_zh.md",
        "PRD goal blocker audit": "latest_goal_blocker_audit_current_zh.md",
        "PRD E3 boundary diagnosis": "seed_boundary_error_diagnosis.md",
        "PRD E3 semantic boundary plan": "e3_semantic_boundary_plan.md",
        "PRD E3 guard validation input plan": "e3_guard_validation_input_plan.md",
        "PRD E3 guard validation after guard": "after_guard_passes_s2_gate",
        "PRD E3 S3 current after guard": "s3_stop_or_inspect_boundary_remains",
        "PRD E3 boundary fresh": "boundary_fresh_pass_run_paired_mact_candidate",
        "PRD E3 S5 strict pass": "s5_strict_all_dataset_pass",
        "PRD fine-grained mechanism audit": "fine_grained_mechanism_ablation_audit.md",
        "PRD E4 readiness audit": "latest_e4_multimodel_gate_readiness_audit_zh.md",
        "PRD E4 timestamped readiness audit": e4_stamped_md.name,
        "PRD active status": "qwen3_strict_goal_complete_e4_pending",
    }.items():
        check_contains(report, label, prd_text, needle)

    report["overall_status"] = "fail" if report["errors"] else "pass"
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=PACKAGE_DIR)
    parser.add_argument("--fail-on-error", action="store_true")
    args = parser.parse_args()

    report = build_report()
    stamp = dt.datetime.now().astimezone().strftime("%Y%m%d_%H%M%S")
    json_path = args.output_dir / f"patent_package_consistency_audit_{stamp}.json"
    md_path = args.output_dir / f"patent_package_consistency_audit_{stamp}_zh.md"
    latest_json = args.output_dir / "latest_patent_package_consistency_audit.json"
    latest_md = args.output_dir / "latest_patent_package_consistency_audit_zh.md"
    json_text = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    md_text = render_markdown(report)
    json_path.write_text(json_text, encoding="utf-8")
    md_path.write_text(md_text, encoding="utf-8")
    latest_json.write_text(json_text, encoding="utf-8")
    latest_md.write_text(md_text, encoding="utf-8")
    print(
        json.dumps(
            {
                "json": str(json_path),
                "md": str(md_path),
                "overall_status": report["overall_status"],
                "errors": len(report["errors"]),
                "warnings": len(report["warnings"]),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    if args.fail_on_error and report["errors"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
