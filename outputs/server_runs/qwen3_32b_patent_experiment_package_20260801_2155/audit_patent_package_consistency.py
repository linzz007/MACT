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
E4_READINESS_JSON = PACKAGE_DIR / "latest_e4_multimodel_gate_readiness_audit.json"
E4_READINESS_MD = PACKAGE_DIR / "latest_e4_multimodel_gate_readiness_audit_zh.md"
CURRENT_PATENT_SECTION_JSON = PACKAGE_DIR / "latest_current_patent_experiment_section.json"
CURRENT_PATENT_SECTION_MD = PACKAGE_DIR / "latest_current_patent_experiment_section_zh.md"
CURRENT_COMPLETION_GAP_JSON = PACKAGE_DIR / "latest_completion_gap_audit_current.json"
CURRENT_COMPLETION_GAP_MD = PACKAGE_DIR / "latest_completion_gap_audit_current_zh.md"
PATENT_DISCLOSURE_DRAFT_MD = PACKAGE_DIR / "patent_disclosure_draft_zh.md"


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


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
    check_equal(report, "ledger overall status", ledger["completion_summary"]["overall_status"], "active_not_complete")
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

    seed_pending = [
        row for row in pending_rows if "Seed-" in row["stage"]
    ]
    check_at_least(report, "E3 pending row count lower bound", len(seed_pending), 2)
    check_at_most(report, "E3 pending row count upper bound", len(seed_pending), 4)
    for row in seed_pending:
        if row.get("input_rows_observed") != 150:
            report["errors"].append(
                f"{row['stage']} observed input rows expected 150, got {row.get('input_rows_observed')!r}"
            )

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
    e4_manifest = manifest["multimodel_e4_readiness"]
    e4_readiness = read_json(E4_READINESS_JSON)
    current_section_manifest = manifest["current_patent_experiment_section"]
    current_section = read_json(CURRENT_PATENT_SECTION_JSON)
    completion_gap_manifest = manifest["completion_gap_audit"]
    completion_gap = read_json(CURRENT_COMPLETION_GAP_JSON)
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
    check_equal(report, "manifest E4 readiness json path", e4_manifest["latest_json"], str(E4_READINESS_JSON))
    check_equal(report, "manifest E4 readiness md path", e4_manifest["latest_md"], str(E4_READINESS_MD))
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
        "stage_patent_draft_ready_with_boundaries",
    )
    check_equal(
        report,
        "current patent section E4 decision",
        current_section["e4_multimodel_gate"]["decision"],
        "no_candidate_wait",
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
        "active_not_complete",
    )
    requirements_by_id = {item["id"]: item for item in completion_gap["requirements"]}
    requirement_status = {item_id: item["status"] for item_id, item in requirements_by_id.items()}
    check_equal(report, "completion gap R3 status", requirement_status.get("R3"), "complete")
    check_equal(
        report,
        "completion gap R4 status",
        requirement_status.get("R4"),
        "complete_boundary_not_stability_pass",
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
        "completion gap default GPU pool availability",
        completion_gap["runtime_recheck"]["default_gpu_pool_available_for_next_start"],
        e4_readiness["runtime_snapshot"]["gpu"]["default_pool_available_for_next_start"],
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
        "formal schedule E3 boundary",
        formal_schedule_text,
        "E3 已经完成，但它是适用边界证据",
    )
    for label, needle in {
        "patent disclosure full200": "Aggregate | 600/600/600 | 489/600 | 450/600 | +39 | 0.5717 | 0/0",
        "patent disclosure P4b closure": "Overall | 150/150/150 | 121/150 | 111/150 | +10 | 0.5310 | 0/0",
        "patent disclosure E3 boundary": "Combined | 300/300/300 | 212/300 | 0.5916 | 0/0 | `complete_boundary_evidence`",
        "patent disclosure E4 boundary": "E4 多模型 readiness audit 结果为 `no_candidate_wait`",
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
        "PRD E3 boundary diagnosis": "seed_boundary_error_diagnosis.md",
        "PRD E4 readiness audit": "latest_e4_multimodel_gate_readiness_audit_zh.md",
        "PRD active status": "active_not_complete",
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
