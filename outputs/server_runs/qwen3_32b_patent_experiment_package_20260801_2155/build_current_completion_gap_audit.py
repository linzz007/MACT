#!/usr/bin/env python3
"""Build the current requirement-by-requirement completion gap audit."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
from pathlib import Path
from typing import Any


PACKAGE_DIR = Path(__file__).resolve().parent
MYAGENT_ROOT = Path("/home/ubuntu/lzz/MyAgent")
MACT_ROOT = Path("/home/ubuntu/lzz/MACT")
PRD_PATH = MYAGENT_ROOT / "docs/server/server_codex_reports/current-qwen3-mact-experiment-prd.md"
FULL200_SUMMARY = Path(
    "/home/ubuntu/lzz/MACT/outputs/server_runs/"
    "qwen3_32b_policy_v6b_all200_acceptance_20260731_132611/"
    "qwen3_policy_v6b_all200_acceptance_summary.json"
)
MECHANISM_MATRIX = Path(
    "/home/ubuntu/lzz/MACT/outputs/server_runs/"
    "qwen3_32b_policy_v6b_patent_mechanism_evidence_20260801_2222/"
    "patent_mechanism_evidence_matrix.json"
)
P4B_ORIGINAL_SUMMARY = Path(
    "/home/ubuntu/lzz/MACT/outputs/server_runs/"
    "qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/"
    "p4b_paired_gate50_summary.json"
)
P4B_AFTER_TARGETED_SUMMARY = P4B_ORIGINAL_SUMMARY.with_name(
    "p4b_after_wtq_targeted_paired_summary.json"
)
P4B_TARGETED_FRESH_SUMMARY = P4B_ORIGINAL_SUMMARY.with_name("p4b_wtq_targeted_fresh_summary.json")
E3_BOUNDARY_DIAGNOSIS = Path(
    "/home/ubuntu/lzz/MACT/outputs/server_runs/"
    "qwen3_32b_policy_v6b_multiseed_gate50_20260801_2231/"
    "summary/seed_boundary_error_diagnosis.json"
)
E3_BUDGET_PROBE_SUMMARY = Path(
    "/home/ubuntu/lzz/MACT/outputs/server_runs/"
    "qwen3_32b_policy_v6b_e3_boundary_budget_probe_20260804_1035/"
    "summary/e3_boundary_budget_probe_summary.json"
)
E3_SEMANTIC_BOUNDARY_PLAN = Path(
    "/home/ubuntu/lzz/MACT/outputs/server_runs/"
    "qwen3_32b_policy_v6b_e3_semantic_boundary_plan_20260804_1110/"
    "summary/e3_semantic_boundary_plan.json"
)
E3_GUARD_VALIDATION_INPUT_PLAN = Path(
    "/home/ubuntu/lzz/MACT/outputs/server_runs/"
    "qwen3_32b_policy_v6b_e3_guard_validation_inputs_20260804_1128/"
    "summary/e3_guard_validation_input_plan.json"
)
E4_READINESS = PACKAGE_DIR / "latest_e4_multimodel_gate_readiness_audit.json"
FORMAL_LEDGER = PACKAGE_DIR / "latest_formal_result_ledger_current.json"
CURRENT_PATENT_SECTION = PACKAGE_DIR / "latest_current_patent_experiment_section.json"
CONSISTENCY_AUDIT = PACKAGE_DIR / "latest_patent_package_consistency_audit.json"
TASK_ORDER = ("wtq", "tabfact", "crt")


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


def correct_count(metrics: dict[str, Any]) -> int:
    if "correct" in metrics:
        return int(metrics["correct"])
    rows = int(metrics.get("num_with_gold") or metrics.get("num_samples") or 0)
    return int(round(float(metrics.get("primary_accuracy") or metrics.get("exact_match") or 0.0) * rows))


def full200_metrics(full: dict[str, Any]) -> dict[str, Any]:
    return {
        "aggregate": {
            "myagent": int(full["aggregate"]["current_correct"]),
            "mact": int(full["aggregate"]["mact_correct"]),
            "rows": int(full["aggregate"]["rows"]),
            "token_ratio": float(full["aggregate"]["token_ratio_current_over_mact"]),
            "elapsed_ratio": float(full["aggregate"]["elapsed_ratio_current_over_mact"]),
            "failed": int(full["aggregate"]["current_failures"]),
            "missing": int(full["aggregate"]["current_missing_answers"]),
        },
        "datasets": {
            task: {
                "myagent": int(full["datasets"][task]["current"]["correct"]),
                "mact": int(full["datasets"][task]["mact"]["correct"]),
                "rows": int(full["datasets"][task]["rows"]),
                "token_ratio": float(full["datasets"][task]["token_ratio_current_over_mact"]),
                "failed": int(full["datasets"][task]["current"]["num_failed_exec"]),
                "missing": int(full["datasets"][task]["current"]["num_missing_answer"]),
            }
            for task in TASK_ORDER
        },
    }


def p4b_after_metrics(after: dict[str, Any], targeted: dict[str, Any], original: dict[str, Any]) -> dict[str, Any]:
    datasets = {}
    for task in TASK_ORDER:
        item = after["datasets"][task]
        myagent = item["myagent"]
        mact = item["mact"]
        rows = int(myagent["num_samples"])
        datasets[task] = {
            "myagent": correct_count(myagent),
            "mact": correct_count(mact),
            "rows": rows,
            "token_ratio": float(item["token_ratio_myagent_to_mact"]),
            "failed": int(myagent["num_failed_exec"]),
            "missing": int(myagent["num_missing_answer"]),
        }
    overall = after["overall"]
    return {
        "original_wtq_risk": {
            "myagent": correct_count(original["datasets"]["wtq"]["myagent"]),
            "mact": correct_count(original["datasets"]["wtq"]["mact"]),
            "rows": int(original["datasets"]["wtq"]["myagent"]["num_samples"]),
        },
        "targeted_fresh": {
            "correct": int(targeted["fresh"]["correct"]),
            "rows": int(targeted["fresh"]["rows"]),
            "merged_rows": int(targeted["coverage"]["merged_rows"]),
            "eval_rows": int(targeted["coverage"]["eval_rows"]),
            "failed": int(targeted["fresh"]["num_failed_exec"]),
            "missing": int(targeted["fresh"]["num_missing_answer"]),
            "decision": targeted["decision"],
        },
        "after_targeted": {
            "aggregate": {
                "myagent": correct_count(overall["myagent"]),
                "mact": correct_count(overall["mact"]),
                "rows": int(overall["myagent"]["num_samples"]),
                "token_ratio": float(after["token_ratio_myagent_to_mact"]),
                "failed": int(overall["myagent"]["num_failed_exec"]),
                "missing": int(overall["myagent"]["num_missing_answer"]),
            },
            "datasets": datasets,
        },
    }


def e3_metrics(e3: dict[str, Any]) -> dict[str, Any]:
    seed_reports = {}
    for seed, item in e3["seed_reports"].items():
        seed_reports[seed] = {
            "decision": item["decision"],
            "overall": item["overall"],
            "datasets": item["datasets"],
        }
    return {
        "aggregate": e3["aggregate"],
        "seed_reports": seed_reports,
        "boundary_findings": e3["boundary_findings"],
        "next_actions": e3["next_actions"],
    }


def e3_budget_probe_metrics(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    probe = read_json(path)
    aggregate = probe["aggregate"]
    datasets = {
        dataset: {
            "input_rows": item["input_rows"],
            "merged_rows": item["merged_rows"],
            "eval_num_samples": item["eval_num_samples"],
            "replan5_correct": item["replan5_correct"],
            "recovered": item["recovered"],
            "num_failed_exec": item["num_failed_exec"],
            "num_missing_answer": item["num_missing_answer"],
            "original_avg_total_tokens": item["original_avg_total_tokens"],
            "replan5_avg_total_tokens": item["replan5_avg_total_tokens"],
            "replan5_token_ratio_to_mact_full200": item["replan5_token_ratio_to_mact_full200"],
            "avg_elapsed_seconds": item["avg_elapsed_seconds"],
        }
        for dataset, item in probe["datasets"].items()
    }
    return {
        "decision": probe["decision"],
        "scope": probe["scope"],
        "rows": aggregate["rows"],
        "original_correct": aggregate["original_correct"],
        "replan5_correct": aggregate["replan5_correct"],
        "recovered": aggregate["recovered"],
        "recovery_rate_from_original_wrong": aggregate["recovery_rate_from_original_wrong"],
        "failed": aggregate["failed"],
        "missing": aggregate["missing"],
        "avg_original_total_tokens": aggregate["avg_original_total_tokens"],
        "avg_replan5_total_tokens": aggregate["avg_replan5_total_tokens"],
        "avg_replan5_elapsed_seconds": aggregate["avg_replan5_elapsed_seconds"],
        "category_recovery": aggregate["category_recovery"],
        "datasets": datasets,
    }


def e3_semantic_boundary_plan_metrics(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    plan = read_json(path)
    snapshot = plan["evidence_snapshot"]
    return {
        "decision": plan["current_decision"],
        "scope": plan["scope"],
        "zero_recovery_probe_categories": snapshot["zero_recovery_probe_categories"],
        "budget_sensitive_categories": snapshot["budget_sensitive_categories"],
        "high_priority_work_item_count": len(plan["high_priority_work_items"]),
        "seed_gate_gap": plan["seed_gate_gap"],
        "next_ladder_stages": [
            item["stage"] for item in plan["recommended_next_experiment_ladder"]
        ],
    }


def e3_guard_validation_input_metrics(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    plan = read_json(path)
    return {
        "decision": plan["validation_decision"],
        "scope": plan["scope"],
        "total_rows": plan["total_rows"],
        "dataset_counts": plan["dataset_counts"],
        "role_counts": plan["role_counts"],
        "gate_targets": plan["gate_targets"],
        "representative_wrong_budget_probe_recovered": plan[
            "representative_wrong_budget_probe_recovered"
        ],
        "no_harm_proxy_counts": plan["no_harm_proxy_counts"],
    }


def build_audit() -> dict[str, Any]:
    generated_at = dt.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
    full = read_json(FULL200_SUMMARY)
    mechanism = read_json(MECHANISM_MATRIX)
    p4b_original = read_json(P4B_ORIGINAL_SUMMARY)
    p4b_after = read_json(P4B_AFTER_TARGETED_SUMMARY)
    targeted = read_json(P4B_TARGETED_FRESH_SUMMARY)
    e3 = read_json(E3_BOUNDARY_DIAGNOSIS)
    e4 = read_json(E4_READINESS)
    ledger = read_json(FORMAL_LEDGER)
    current_section = read_json(CURRENT_PATENT_SECTION)
    consistency = read_json(CONSISTENCY_AUDIT) if CONSISTENCY_AUDIT.exists() else None

    completion_summary = ledger["completion_summary"]
    runtime = e4["runtime_snapshot"]
    full_metrics = full200_metrics(full)
    p4b_metrics = p4b_after_metrics(p4b_after, targeted, p4b_original)
    e3_current = e3_metrics(e3)
    e3_probe_current = e3_budget_probe_metrics(E3_BUDGET_PROBE_SUMMARY)
    if e3_probe_current:
        e3_current["budget_probe_max_replan5"] = e3_probe_current
    e3_semantic_plan_current = e3_semantic_boundary_plan_metrics(E3_SEMANTIC_BOUNDARY_PLAN)
    if e3_semantic_plan_current:
        e3_current["semantic_boundary_plan"] = e3_semantic_plan_current
    e3_guard_validation_current = e3_guard_validation_input_metrics(E3_GUARD_VALIDATION_INPUT_PLAN)
    if e3_guard_validation_current:
        e3_current["guard_validation_input_plan"] = e3_guard_validation_current

    requirements = [
        {
            "id": "R1",
            "requirement": "Qwen3-32B full200 anchor evidence shows MyAgent exceeds MACT on WTQ, TabFact, and CRT, with lower token usage and zero failed/missing answers.",
            "status": "complete",
            "evidence": [str(FULL200_SUMMARY), str(FULL200_SUMMARY.with_name("qwen3_policy_v6b_patent_evidence_index.md"))],
            "metrics": full_metrics,
            "gap": "none",
        },
        {
            "id": "R2",
            "requirement": "Mechanism evidence supports selective risk collaboration / persuasion-back rather than sample hardcoding.",
            "status": "substantially_complete",
            "evidence": [
                str(MECHANISM_MATRIX),
                str(MECHANISM_MATRIX.with_suffix(".md")),
                str(
                    Path(
                        "/home/ubuntu/lzz/MACT/outputs/server_runs/"
                        "qwen3_32b_policy_v6b_coarse_ablation_gate50_20260801_0040/"
                        "coarse_ablation_gate50_summary.md"
                    )
                ),
            ],
            "metrics": current_section["coarse_ablation_key_numbers"],
            "gap": "Fine-grained verifier-override/evidence-retention ablations remain optional unless more causal granularity is needed for claim drafting.",
        },
        {
            "id": "R3",
            "requirement": "WTQ P4b new-seed risk is diagnosed and closed with fresh Qwen validation before using after-targeted P4b as positive evidence.",
            "status": "complete",
            "evidence": [
                str(P4B_ORIGINAL_SUMMARY),
                str(P4B_TARGETED_FRESH_SUMMARY),
                str(P4B_AFTER_TARGETED_SUMMARY),
            ],
            "metrics": p4b_metrics,
            "gap": "none",
        },
        {
            "id": "R4",
            "requirement": "Multi-seed work explains whether the effect is stable beyond the frozen full200 and P4b seed.",
            "status": "complete_boundary_not_stability_pass",
            "evidence": [
                str(E3_BOUNDARY_DIAGNOSIS),
                str(E3_BOUNDARY_DIAGNOSIS.with_suffix(".md")),
            ]
            + (
                [
                    str(E3_BUDGET_PROBE_SUMMARY),
                    str(E3_BUDGET_PROBE_SUMMARY.with_suffix(".md")),
                ]
                if e3_probe_current
                else []
            )
            + (
                [
                    str(E3_SEMANTIC_BOUNDARY_PLAN),
                    str(E3_SEMANTIC_BOUNDARY_PLAN.with_suffix(".md")),
                ]
                if e3_semantic_plan_current
                else []
            )
            + (
                [
                    str(E3_GUARD_VALIDATION_INPUT_PLAN),
                    str(E3_GUARD_VALIDATION_INPUT_PLAN.with_suffix(".md")),
                ]
                if e3_guard_validation_current
                else []
            ),
            "metrics": e3_current,
            "gap": "Seed-C/Seed-D are boundary evidence, not multi-seed stable superiority evidence. The max_replan=5 probe recovered a minority of representative wrong rows, the semantic-boundary plan defines targeted guard work, and the S2 guard-validation input package is prepared before any paired MACT runtime.",
        },
        {
            "id": "R5",
            "requirement": "Multi-model gate must test model externality through Gate-10 -> Gate-50 -> Gate-150 -> paired-200 without rerunning known no-go models.",
            "status": "pending_no_candidate",
            "evidence": [
                str(E4_READINESS),
                str(E4_READINESS.with_name("latest_e4_multimodel_gate_readiness_audit_zh.md")),
            ],
            "metrics": {
                "decision": e4["decision"],
                "can_start_gate10_now": e4["can_start_gate10_now"],
                "local_models_discovered": len(e4["model_readiness"]["local_models"]),
                "untested_local_models": len(e4["model_readiness"]["untested_local_models"]),
                "api_keys_present": len(e4["model_readiness"]["api_keys_present"]),
                "api_provider_profiles": len(e4["model_readiness"]["api_provider_profiles"]),
            },
            "gap": "No untested local model path or API provider profile/key exists. Do not start E4 Gate-10 until a new candidate appears.",
        },
        {
            "id": "R6",
            "requirement": "Expert/patent package and Chinese patent disclosure draft must exist, point to auditable evidence, and separate supported claims from boundaries.",
            "status": current_section["write_status"]["current_status"],
            "evidence": [
                str(CURRENT_PATENT_SECTION),
                str(CURRENT_PATENT_SECTION.with_name("latest_current_patent_experiment_section_zh.md")),
                str(PACKAGE_DIR / "patent_disclosure_draft_zh.md"),
                str(FORMAL_LEDGER),
            ],
            "metrics": {
                "supported_positive_claims": current_section["write_status"]["supported_positive_claims"],
                "supported_boundary_claims": current_section["write_status"]["supported_boundary_claims"],
                "unsupported_claims": current_section["write_status"]["unsupported_claims"],
                "formal_ledger_completed_rows": len(ledger["completed_rows"]),
                "formal_ledger_pending_rows": len(ledger["pending_rows"]),
            },
            "gap": "Final closeout still needs an E4 candidate result or explicit acceptance of the no-candidate boundary.",
        },
        {
            "id": "R7",
            "requirement": "Process/result context remains in the single MyAgent PRD and MACT artifacts, with sync to GitHub after each update.",
            "status": "complete_for_prior_pushed_state_this_audit_requires_commit_push",
            "evidence": [
                str(PRD_PATH),
                str(PACKAGE_DIR / "evidence_manifest.json"),
                str(PACKAGE_DIR / "SHA256SUMS"),
            ],
            "metrics": {
                "myagent_head_at_generation": git_commit(MYAGENT_ROOT),
                "mact_head_at_generation": git_commit(MACT_ROOT),
                "consistency_audit_status": None if consistency is None else consistency["overall_status"],
                "consistency_audit_errors": None if consistency is None else len(consistency["errors"]),
                "checksum_records": read_json(PACKAGE_DIR / "latest_patent_package_checksums.json")["record_count"],
            },
            "gap": "This generated audit itself must be committed and pushed after generation; final proof is git local/remote HEAD equality.",
        },
    ]

    return {
        "audit_name": "current_completion_gap_audit",
        "generated_at_local": generated_at,
        "purpose": "Requirement-by-requirement audit for the active patent-facing MyAgent vs MACT experiment goal.",
        "scope_boundary": "This audit compiles current evidence and gaps; it does not create new benchmark results.",
        "repositories": {
            "myagent": {
                "path": str(MYAGENT_ROOT),
                "branch": "codex/selective-risk-collaboration",
                "head_at_generation": git_commit(MYAGENT_ROOT),
            },
            "mact": {
                "path": str(MACT_ROOT),
                "branch": "main",
                "head_at_generation": git_commit(MACT_ROOT),
            },
        },
        "runtime_recheck": {
            "source": str(E4_READINESS),
            "checked_at_local": e4["generated_at_local"],
            "default_gpu_pool": runtime["gpu"]["default_pool"],
            "default_gpu_pool_available_for_next_start": runtime["gpu"][
                "default_pool_available_for_next_start"
            ],
            "gpus": runtime["gpu"]["gpus"],
            "visible_runner_or_model_processes": runtime["processes"][
                "visible_runner_or_model_processes"
            ],
            "interpretation": "GPU 0-3 are the default pool configuration, but this audit records whether that pool is actually clean. No E4 run should start without both a new model/API candidate and a clean GPU pair.",
        },
        "requirements": requirements,
        "current_next_actions": [
            "Do not rerun known no-go models. Wait for a new local model path or API provider profile/key before E4 Gate-10.",
            "Use latest_current_patent_experiment_section_zh.md for current expert/patent discussion, with E3 and E4 boundaries explicitly preserved.",
            "If further Qwen3 optimization is requested, start from the E3 semantic-boundary plan and S2 guard-validation input package: implement P0/P1 gold-free guards, run affected-slice fresh validation, then rerun E3 current-only only if the small gate passes.",
        ],
        "overall_completion_status": completion_summary["overall_status"],
        "reason_not_complete": "Current Qwen3 full200 and P4b after-targeted evidence are positive; E3 is boundary evidence with S2 validation inputs prepared but not freshly run; E4 has no candidate, so model-externality evidence and final closeout remain pending.",
        "can_write_now": completion_summary["can_write_now"],
        "cannot_write_yet": completion_summary["cannot_write_yet"],
    }


def render_count(correct: int, rows: int) -> str:
    return f"{correct}/{rows}"


def render_markdown(report: dict[str, Any]) -> str:
    req_by_id = {item["id"]: item for item in report["requirements"]}
    r1 = req_by_id["R1"]["metrics"]
    r3 = req_by_id["R3"]["metrics"]
    r4 = req_by_id["R4"]["metrics"]
    r5 = req_by_id["R5"]["metrics"]
    r4_probe = r4.get("budget_probe_max_replan5")
    r4_semantic_plan = r4.get("semantic_boundary_plan")
    r4_guard_validation = r4.get("guard_validation_input_plan")
    runtime = report["runtime_recheck"]
    lines = [
        "# 当前专利实验完成度审计",
        "",
        f"生成时间：`{report['generated_at_local']}`",
        "",
        "本文档用于回答：当前距离完整专利实验材料还差什么。它从 current/latest 证据自动汇总，不新增 benchmark 结果。",
        "",
        "## 当前结论",
        "",
        f"当前目标状态：`{report['overall_completion_status']}`。Qwen3-32B full200 和 P4b after-targeted 已是正证据；E3 Seed-C/D 是边界证据，并已补 E3 semantic-boundary plan 和 S2 guard-validation input package；E4 状态为 `pending_no_candidate`，artifact decision 为 `no_candidate_wait`，尚无额外模型/API 候选。",
        "",
        "## 环境复核",
        "",
        "| item | result |",
        "|---|---|",
        f"| source | `{runtime['source']}` |",
        f"| checked at | `{runtime['checked_at_local']}` |",
        f"| default GPU pool | `{runtime['default_gpu_pool']}` |",
        f"| default pool available | `{runtime['default_gpu_pool_available_for_next_start']}` |",
        f"| visible model/runner processes | `{runtime['visible_runner_or_model_processes']}` |",
        "",
        "| GPU | memory MiB | util % |",
        "|---:|---:|---:|",
    ]
    for gpu in runtime["gpus"]:
        lines.append(
            f"| {gpu['index']} | {gpu['memory_used_mib']} | {gpu['utilization_gpu_percent']} |"
        )
    lines.extend(
        [
            "",
            "## 要求逐项审计",
            "",
            "| ID | 要求 | 当前状态 | 关键证据 | 缺口 |",
            "|---|---|---|---|---|",
        ]
    )
    for item in report["requirements"]:
        evidence = "<br>".join(f"`{path}`" for path in item["evidence"])
        lines.append(
            f"| {item['id']} | {item['requirement']} | `{item['status']}` | {evidence} | {item['gap']} |"
        )
    lines.extend(
        [
            "",
            "## 关键数字",
            "",
            "| scope | result |",
            "|---|---|",
            f"| full200 aggregate | MyAgent `{render_count(r1['aggregate']['myagent'], r1['aggregate']['rows'])}` vs MACT `{render_count(r1['aggregate']['mact'], r1['aggregate']['rows'])}`, token ratio `{r1['aggregate']['token_ratio']:.4f}`, elapsed ratio `{r1['aggregate']['elapsed_ratio']:.4f}`, failed/missing `{r1['aggregate']['failed']}/{r1['aggregate']['missing']}` |",
            f"| P4b original WTQ risk | MyAgent `{render_count(r3['original_wtq_risk']['myagent'], r3['original_wtq_risk']['rows'])}` vs MACT `{render_count(r3['original_wtq_risk']['mact'], r3['original_wtq_risk']['rows'])}` |",
            f"| WTQ targeted fresh | `{render_count(r3['targeted_fresh']['correct'], r3['targeted_fresh']['rows'])}`, merged/eval `{r3['targeted_fresh']['merged_rows']}/{r3['targeted_fresh']['eval_rows']}`, failed/missing `{r3['targeted_fresh']['failed']}/{r3['targeted_fresh']['missing']}`, decision `{r3['targeted_fresh']['decision']}` |",
            f"| P4b after-targeted aggregate | MyAgent `{render_count(r3['after_targeted']['aggregate']['myagent'], r3['after_targeted']['aggregate']['rows'])}` vs MACT `{render_count(r3['after_targeted']['aggregate']['mact'], r3['after_targeted']['aggregate']['rows'])}`, token ratio `{r3['after_targeted']['aggregate']['token_ratio']:.4f}`, failed/missing `{r3['after_targeted']['aggregate']['failed']}/{r3['after_targeted']['aggregate']['missing']}` |",
            f"| E3 Seed-C/D boundary aggregate | `{r4['aggregate']['correct']}/{r4['aggregate']['rows']}`, wrong `{r4['aggregate']['wrong']}`, weighted token ratio `{r4['aggregate']['weighted_token_ratio_to_mact_full200_reference']:.4f}`, failed/missing `{r4['aggregate']['failed']}/{r4['aggregate']['missing']}`, verification `{r4['aggregate']['verification_status']}` |",
        ]
    )
    if r4_probe:
        lines.append(
            f"| E3 max_replan=5 boundary probe | recovered `{r4_probe['recovered']}/{r4_probe['rows']}` original wrong rows, decision `{r4_probe['decision']}`, failed/missing `{r4_probe['failed']}/{r4_probe['missing']}`, avg tokens `{r4_probe['avg_original_total_tokens']:.1f}->{r4_probe['avg_replan5_total_tokens']:.1f}` |"
        )
    if r4_semantic_plan:
        lines.append(
            f"| E3 semantic-boundary plan | decision `{r4_semantic_plan['decision']}`, high-priority work items `{r4_semantic_plan['high_priority_work_item_count']}`, zero-recovery categories `{len(r4_semantic_plan['zero_recovery_probe_categories'])}`, next ladder `{', '.join(r4_semantic_plan['next_ladder_stages'])}` |"
        )
    if r4_guard_validation:
        lines.append(
            f"| E3 S2 guard-validation input package | decision `{r4_guard_validation['decision']}`, rows `{r4_guard_validation['total_rows']}`, dataset counts `{r4_guard_validation['dataset_counts']}`, role counts `{r4_guard_validation['role_counts']}`, future gate recover `{r4_guard_validation['gate_targets']['representative_wrong_recovery_min']}/12` and no-harm `{r4_guard_validation['gate_targets']['no_harm_correct_min']}/18` |"
        )
    lines.extend(
        [
            f"| E4 readiness | decision `{r5['decision']}`; can_start_gate10_now `{r5['can_start_gate10_now']}`, local models `{r5['local_models_discovered']}`, untested local models `{r5['untested_local_models']}`, API keys/profiles `{r5['api_keys_present']}/{r5['api_provider_profiles']}` |",
            "",
            "## 下一步",
            "",
        ]
    )
    lines.extend(f"- {item}" for item in report["current_next_actions"])
    lines.extend(
        [
            "",
            "## 当前可写",
            "",
        ]
    )
    lines.extend(f"- {item}" for item in report["can_write_now"])
    lines.extend(
        [
            "",
            "## 当前不能写",
            "",
        ]
    )
    lines.extend(f"- {item}" for item in report["cannot_write_yet"])
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=PACKAGE_DIR)
    args = parser.parse_args()
    report = build_audit()
    stamp = dt.datetime.now().astimezone().strftime("%Y%m%d_%H%M%S")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    json_path = args.output_dir / f"completion_gap_audit_current_{stamp}.json"
    md_path = args.output_dir / f"completion_gap_audit_current_{stamp}_zh.md"
    latest_json = args.output_dir / "latest_completion_gap_audit_current.json"
    latest_md = args.output_dir / "latest_completion_gap_audit_current_zh.md"
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
                "latest_json": str(latest_json),
                "latest_md": str(latest_md),
                "overall_completion_status": report["overall_completion_status"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
