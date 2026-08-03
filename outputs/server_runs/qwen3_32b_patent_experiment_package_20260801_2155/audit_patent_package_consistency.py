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
    check_equal(report, "manifest latest ledger path", manifest_ledger, str(LEDGER_PATH))
    check_equal(report, "manifest latest preflight path", manifest_preflight, str(PREFLIGHT_PATH))
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
