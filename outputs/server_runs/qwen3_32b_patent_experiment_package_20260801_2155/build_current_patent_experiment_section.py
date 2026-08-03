#!/usr/bin/env python3
"""Build a current patent-facing experiment section from frozen evidence."""

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
FULL200_SUMMARY = Path(
    "/home/ubuntu/lzz/MACT/outputs/server_runs/"
    "qwen3_32b_policy_v6b_all200_acceptance_20260731_132611/"
    "qwen3_policy_v6b_all200_acceptance_summary.json"
)
FULL200_EVIDENCE_MD = FULL200_SUMMARY.with_name("qwen3_policy_v6b_patent_evidence_index.md")
P4B_ORIGINAL_SUMMARY = Path(
    "/home/ubuntu/lzz/MACT/outputs/server_runs/"
    "qwen3_32b_policy_v6b_newseed_gate50_20260801_0305/"
    "p4b_paired_gate50_summary.json"
)
P4B_ORIGINAL_SUMMARY_MD = P4B_ORIGINAL_SUMMARY.with_suffix(".md")
P4B_TARGETED_FRESH_SUMMARY = P4B_ORIGINAL_SUMMARY.with_name("p4b_wtq_targeted_fresh_summary.json")
P4B_TARGETED_FRESH_SUMMARY_MD = P4B_TARGETED_FRESH_SUMMARY.with_suffix(".md")
P4B_AFTER_TARGETED_SUMMARY = P4B_ORIGINAL_SUMMARY.with_name(
    "p4b_after_wtq_targeted_paired_summary.json"
)
P4B_AFTER_TARGETED_SUMMARY_MD = P4B_AFTER_TARGETED_SUMMARY.with_suffix(".md")
MECHANISM_MATRIX = Path(
    "/home/ubuntu/lzz/MACT/outputs/server_runs/"
    "qwen3_32b_policy_v6b_patent_mechanism_evidence_20260801_2222/"
    "patent_mechanism_evidence_matrix.json"
)
MECHANISM_MATRIX_MD = MECHANISM_MATRIX.with_suffix(".md")
E3_RUN_DIR = Path(
    "/home/ubuntu/lzz/MACT/outputs/server_runs/"
    "qwen3_32b_policy_v6b_multiseed_gate50_20260801_2231"
)
E3_BOUNDARY_DIAGNOSIS = E3_RUN_DIR / "summary" / "seed_boundary_error_diagnosis.json"
E3_BOUNDARY_DIAGNOSIS_MD = E3_BOUNDARY_DIAGNOSIS.with_suffix(".md")
E4_READINESS = PACKAGE_DIR / "latest_e4_multimodel_gate_readiness_audit.json"
E4_READINESS_MD = PACKAGE_DIR / "latest_e4_multimodel_gate_readiness_audit_zh.md"
FORMAL_LEDGER = PACKAGE_DIR / "latest_formal_result_ledger_current.json"
FORMAL_LEDGER_MD = PACKAGE_DIR / "latest_formal_result_ledger_current_zh.md"
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


def pct(value: float) -> str:
    return f"{value * 100:.2f}%"


def full200_table(summary: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for task in TASK_ORDER:
        item = summary["datasets"][task]
        current = item["current"]
        mact = item["mact"]
        rows.append(
            {
                "dataset": task,
                "input_rows": int(item["rows"]),
                "merged_rows": int(item["merged_rows"]),
                "eval_rows": int(current["rows"]),
                "myagent_correct": int(current["correct"]),
                "mact_correct": int(mact["correct"]),
                "delta_correct": int(item["accuracy_delta_correct"]),
                "token_ratio": float(item["token_ratio_current_over_mact"]),
                "elapsed_ratio": float(item["elapsed_ratio_current_over_mact"]),
                "myagent_avg_tokens": float(current["avg_total_tokens"]),
                "myagent_avg_elapsed_seconds": float(current["avg_elapsed_seconds"]),
                "num_failed_exec": int(current["num_failed_exec"]),
                "num_missing_answer": int(current["num_missing_answer"]),
            }
        )
    aggregate = summary["aggregate"]
    rows.append(
        {
            "dataset": "aggregate",
            "input_rows": int(aggregate["rows"]),
            "merged_rows": int(aggregate["rows"]),
            "eval_rows": int(aggregate["rows"]),
            "myagent_correct": int(aggregate["current_correct"]),
            "mact_correct": int(aggregate["mact_correct"]),
            "delta_correct": int(aggregate["accuracy_delta_correct"]),
            "token_ratio": float(aggregate["token_ratio_current_over_mact"]),
            "elapsed_ratio": float(aggregate["elapsed_ratio_current_over_mact"]),
            "myagent_avg_tokens": float(aggregate["current_avg_total_tokens_weighted"]),
            "myagent_avg_elapsed_seconds": float(aggregate["current_avg_elapsed_seconds_weighted"]),
            "num_failed_exec": int(aggregate["current_failures"]),
            "num_missing_answer": int(aggregate["current_missing_answers"]),
        }
    )
    return rows


def paired_gate_table(summary: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for task in TASK_ORDER:
        item = summary["datasets"][task]
        myagent = item["myagent"]
        mact = item["mact"]
        eval_rows = int(myagent.get("num_with_gold") or myagent.get("num_samples") or 0)
        myagent_correct = correct_count(myagent)
        mact_correct = correct_count(mact)
        rows.append(
            {
                "dataset": task,
                "input_rows": int(myagent["num_samples"]),
                "merged_rows": int(myagent["num_samples"]),
                "eval_rows": eval_rows,
                "myagent_correct": myagent_correct,
                "mact_correct": mact_correct,
                "delta_correct": myagent_correct - mact_correct,
                "token_ratio": float(item["token_ratio_myagent_to_mact"]),
                "elapsed_ratio": None,
                "myagent_avg_tokens": float(myagent["avg_total_tokens"]),
                "myagent_avg_elapsed_seconds": float(myagent["avg_elapsed_seconds"]),
                "num_failed_exec": int(myagent["num_failed_exec"]),
                "num_missing_answer": int(myagent["num_missing_answer"]),
            }
        )
    overall = summary["overall"]
    myagent = overall["myagent"]
    mact = overall["mact"]
    eval_rows = int(myagent.get("num_with_gold") or myagent.get("num_samples") or 0)
    myagent_correct = correct_count(myagent)
    mact_correct = correct_count(mact)
    rows.append(
        {
            "dataset": "aggregate",
            "input_rows": int(myagent["num_samples"]),
            "merged_rows": int(myagent["num_samples"]),
            "eval_rows": eval_rows,
            "myagent_correct": myagent_correct,
            "mact_correct": mact_correct,
            "delta_correct": myagent_correct - mact_correct,
            "token_ratio": float(summary["token_ratio_myagent_to_mact"]),
            "elapsed_ratio": None,
            "myagent_avg_tokens": float(myagent["avg_total_tokens"]),
            "myagent_avg_elapsed_seconds": float(myagent["avg_elapsed_seconds"]),
            "num_failed_exec": int(myagent["num_failed_exec"]),
            "num_missing_answer": int(myagent["num_missing_answer"]),
        }
    )
    return rows


def e3_seed_table(seed_summary: dict[str, Any]) -> dict[str, Any]:
    datasets: list[dict[str, Any]] = []
    failures = 0
    missing = 0
    for task in TASK_ORDER:
        item = seed_summary["datasets"][task]
        failures += int(item["num_failed_exec"])
        missing += int(item["num_missing_answer"])
        datasets.append(
            {
                "dataset": task,
                "input_rows": int(item["input_rows"]),
                "merged_rows": int(item["merged_rows"]),
                "eval_rows": int(item["eval_rows"]),
                "myagent_correct": int(item["correct"]),
                "mact_correct": None,
                "delta_correct": None,
                "token_ratio_to_mact_full200_reference": float(item["token_ratio_to_mact_full200"]),
                "myagent_avg_tokens": float(item["avg_total_tokens"]),
                "myagent_avg_elapsed_seconds": float(item["avg_elapsed_seconds"]),
                "num_failed_exec": int(item["num_failed_exec"]),
                "num_missing_answer": int(item["num_missing_answer"]),
                "passed_current_seed_gate": bool(item["passed_current_seed_gate"]),
            }
        )
    overall = seed_summary["overall"]
    aggregate = {
        "dataset": "aggregate",
        "input_rows": int(overall["rows"]),
        "merged_rows": int(overall["rows"]),
        "eval_rows": int(overall["rows"]),
        "myagent_correct": int(overall["correct"]),
        "mact_correct": None,
        "delta_correct": None,
        "token_ratio_to_mact_full200_reference": float(overall["token_ratio_to_mact_full200_weighted"]),
        "myagent_avg_tokens": float(overall["avg_total_tokens_weighted"]),
        "myagent_avg_elapsed_seconds": float(overall["avg_elapsed_seconds_weighted"]),
        "num_failed_exec": failures,
        "num_missing_answer": missing,
        "passed_current_seed_gate": seed_summary["decision"] == "run_paired_mact",
    }
    return {
        "seed_label": seed_summary["seed_label"],
        "decision": seed_summary["decision"],
        "datasets": datasets,
        "aggregate": aggregate,
    }


def build_section() -> dict[str, Any]:
    generated_at = dt.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
    full = read_json(FULL200_SUMMARY)
    p4b_original = read_json(P4B_ORIGINAL_SUMMARY)
    p4b_after = read_json(P4B_AFTER_TARGETED_SUMMARY)
    targeted = read_json(P4B_TARGETED_FRESH_SUMMARY)
    mechanism = read_json(MECHANISM_MATRIX)
    e3_boundary = read_json(E3_BOUNDARY_DIAGNOSIS)
    e4 = read_json(E4_READINESS)
    e3_seeds = [
        e3_seed_table(read_json(E3_RUN_DIR / "summary" / f"{seed}_myagent_gate50_summary.json"))
        for seed in ("seed_c", "seed_d")
    ]

    return {
        "artifact_name": "current_patent_experiment_section",
        "generated_at_local": generated_at,
        "purpose": "Current patent/expert-facing experiment section with explicit supported claims and boundaries.",
        "scope_boundary": "This artifact synthesizes existing frozen evidence. It does not create new benchmark results and must not be read as final full official benchmark completion.",
        "git_commits_at_generation": {
            "myagent": git_commit(MYAGENT_ROOT),
            "mact": git_commit(MACT_ROOT),
        },
        "evidence_paths": {
            "full200_summary": str(FULL200_SUMMARY),
            "full200_evidence_md": str(FULL200_EVIDENCE_MD),
            "p4b_original_summary": str(P4B_ORIGINAL_SUMMARY),
            "p4b_original_summary_md": str(P4B_ORIGINAL_SUMMARY_MD),
            "p4b_targeted_fresh_summary": str(P4B_TARGETED_FRESH_SUMMARY),
            "p4b_targeted_fresh_summary_md": str(P4B_TARGETED_FRESH_SUMMARY_MD),
            "p4b_after_targeted_summary": str(P4B_AFTER_TARGETED_SUMMARY),
            "p4b_after_targeted_summary_md": str(P4B_AFTER_TARGETED_SUMMARY_MD),
            "mechanism_matrix": str(MECHANISM_MATRIX),
            "mechanism_matrix_md": str(MECHANISM_MATRIX_MD),
            "e3_boundary_diagnosis": str(E3_BOUNDARY_DIAGNOSIS),
            "e3_boundary_diagnosis_md": str(E3_BOUNDARY_DIAGNOSIS_MD),
            "e4_readiness": str(E4_READINESS),
            "e4_readiness_md": str(E4_READINESS_MD),
            "formal_ledger": str(FORMAL_LEDGER),
            "formal_ledger_md": str(FORMAL_LEDGER_MD),
        },
        "write_status": {
            "current_status": "stage_patent_draft_ready_with_boundaries",
            "supported_positive_claims": [
                "On Qwen3-32B full200, MyAgent beats MACT on WTQ, TabFact, and CRT, with aggregate token ratio 0.5717 and zero MyAgent failures/missing answers.",
                "After WTQ targeted fresh validation, P4b after-targeted Gate-50 beats MACT on all three datasets and aggregate, with aggregate token ratio 0.5310 and zero MyAgent failures/missing answers.",
                "Mechanism evidence supports risk-stratified collaboration, controlled verifier override, deterministic semantic audit, evidence retention, and budget control as patent-facing mechanisms.",
            ],
            "supported_boundary_claims": [
                "P4b original new-seed Gate-50 exposed WTQ risk: MyAgent 37/50 vs MACT 43/50 before targeted fixes.",
                "E3 Seed-C/Seed-D current-only Gate-50 are boundary evidence, not stable multi-seed superiority evidence; no same-seed paired MACT baseline was run because current-only gate decided stop_or_inspect.",
                "E4 multi-model gate is blocked by no candidate: no untested local model path and no API provider profile/key are available.",
            ],
            "unsupported_claims": [
                "Do not claim multi-model validation is complete.",
                "Do not claim multi-seed stable superiority over MACT is complete.",
                "Do not claim full official dataset completion beyond the frozen full200/gate scopes.",
            ],
        },
        "full200_anchor": {
            "decision": "accepted_qwen3_full200_all_dataset_superiority",
            "aggregate_accuracy": {
                "myagent": full["aggregate"]["current_accuracy"],
                "mact": full["aggregate"]["mact_accuracy"],
                "delta": full["aggregate"]["accuracy_delta"],
            },
            "aggregate_token_ratio": full["aggregate"]["token_ratio_current_over_mact"],
            "aggregate_elapsed_ratio": full["aggregate"]["elapsed_ratio_current_over_mact"],
            "rows": full200_table(full),
        },
        "p4b_new_seed": {
            "original_decision": "accepted_overall_but_wtq_risk",
            "original_wtq": {
                "myagent_correct": correct_count(p4b_original["datasets"]["wtq"]["myagent"]),
                "mact_correct": correct_count(p4b_original["datasets"]["wtq"]["mact"]),
                "rows": int(p4b_original["datasets"]["wtq"]["myagent"]["num_samples"]),
            },
            "targeted_fresh": {
                "decision": targeted["decision"],
                "correct": int(targeted["fresh"]["correct"]),
                "rows": int(targeted["fresh"]["rows"]),
                "merged_rows": int(targeted["coverage"]["merged_rows"]),
                "eval_rows": int(targeted["coverage"]["eval_rows"]),
                "num_failed_exec": int(targeted["fresh"]["num_failed_exec"]),
                "num_missing_answer": int(targeted["fresh"]["num_missing_answer"]),
                "avg_total_tokens": float(targeted["fresh"]["avg_total_tokens"]),
                "avg_elapsed_seconds": float(targeted["fresh"]["avg_elapsed_seconds"]),
            },
            "after_targeted_decision": "accepted_after_targeted_all_dataset_superiority",
            "after_targeted_rows": paired_gate_table(p4b_after),
        },
        "mechanism_evidence": mechanism["patent_mechanism_evidence"],
        "coarse_ablation_key_numbers": {
            "no_strong_verification_delta_vs_current": mechanism["coarse_ablation"]["variants"][
                "no_strong_verification"
            ]["delta_vs_current"],
            "no_strong_verification_wtq_delta_vs_current": mechanism["coarse_ablation"]["variants"][
                "no_strong_verification"
            ]["per_dataset"]["wtq"]["delta_vs_current"],
            "no_deterministic_shortcuts_delta_vs_current": mechanism["coarse_ablation"]["variants"][
                "no_deterministic_shortcuts"
            ]["delta_vs_current"],
            "no_deterministic_shortcuts_tabfact_delta_vs_current": mechanism["coarse_ablation"]["variants"][
                "no_deterministic_shortcuts"
            ]["per_dataset"]["tabfact"]["delta_vs_current"],
            "no_deterministic_shortcuts_crt_delta_vs_current": mechanism["coarse_ablation"]["variants"][
                "no_deterministic_shortcuts"
            ]["per_dataset"]["crt"]["delta_vs_current"],
            "no_deterministic_shortcuts_tabfact_token_ratio_vs_current": mechanism["coarse_ablation"]["variants"][
                "no_deterministic_shortcuts"
            ]["per_dataset"]["tabfact"]["token_ratio_vs_current"],
        },
        "e3_multiseed_boundary": {
            "decision": "boundary_not_stable_superiority",
            "seed_runs": e3_seeds,
            "aggregate_diagnosis": e3_boundary["aggregate"],
            "boundary_findings": e3_boundary["boundary_findings"],
            "next_actions": e3_boundary["next_actions"],
        },
        "e4_multimodel_gate": {
            "decision": e4["decision"],
            "can_start_gate10_now": e4["can_start_gate10_now"],
            "local_models_discovered": e4["model_readiness"]["local_models"],
            "untested_local_models": e4["model_readiness"]["untested_local_models"],
            "api_keys_present": e4["model_readiness"]["api_keys_present"],
            "api_provider_profiles": e4["model_readiness"]["api_provider_profiles"],
            "default_gpu_pool": e4["runtime_snapshot"]["gpu"]["default_pool"],
            "default_gpu_pool_available_for_next_start": e4["runtime_snapshot"]["gpu"][
                "default_pool_available_for_next_start"
            ],
            "visible_runner_or_model_processes": e4["runtime_snapshot"]["processes"][
                "visible_runner_or_model_processes"
            ],
        },
        "formal_experiment_status": [
            {
                "stage": "E0 full200 anchor",
                "status": "complete",
                "patent_use": "main positive evidence",
            },
            {
                "stage": "E1 WTQ P4b risk diagnosis",
                "status": "complete",
                "patent_use": "risk and boundary diagnosis",
            },
            {
                "stage": "E2 WTQ targeted fresh and after-targeted full50",
                "status": "complete",
                "patent_use": "targeted mechanism repair evidence",
            },
            {
                "stage": "E3 multi-seed current-only boundary diagnosis",
                "status": "complete_boundary_evidence",
                "patent_use": "applicability boundary, not stability proof",
            },
            {
                "stage": "E4 multi-model gate",
                "status": "pending_no_candidate",
                "patent_use": "future external validity evidence after new model/API appears",
            },
            {
                "stage": "E5/E6 patent experiment section and disclosure draft",
                "status": "current_section_consolidated",
                "patent_use": "draft-ready with explicit unsupported claims",
            },
            {
                "stage": "E7 final experiment package closeout",
                "status": "pending",
                "patent_use": "requires at least E4 candidate or explicit acceptance of no-candidate boundary",
            },
        ],
        "next_trigger_rules": [
            "If GPUs 0-3 remain free and a new candidate model/API appears, start Gate-10 on 0,1 and 2,3 through prepare_model_gate_run.py; do not consume 4-7 unless explicitly reassigned.",
            "If no new model/API exists, do not rerun known no-go models; continue drafting with E4 marked pending/no-candidate.",
            "If more Qwen optimization is requested, target E3 boundary categories instead of re-optimizing already-passing full200/P4b-after-targeted rows.",
        ],
    }


def render_result_table(rows: list[dict[str, Any]], *, token_key: str = "token_ratio") -> list[str]:
    lines = [
        "| dataset | rows input/merged/eval | MyAgent | MACT/ref | delta | token ratio | avg tokens | avg elapsed s | failed/missing |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        token_value = row.get(token_key, row.get("token_ratio"))
        token_text = "n/a" if token_value is None else f"{float(token_value):.4f}"
        mact = row.get("mact_correct")
        mact_text = "n/a" if mact is None else f"{mact}/{row['eval_rows']}"
        delta = row.get("delta_correct")
        delta_text = "n/a" if delta is None else f"{int(delta):+d}"
        lines.append(
            f"| {row['dataset']} | {row['input_rows']}/{row['merged_rows']}/{row['eval_rows']} | "
            f"{row['myagent_correct']}/{row['eval_rows']} | {mact_text} | {delta_text} | "
            f"{token_text} | {row['myagent_avg_tokens']:.2f} | {row['myagent_avg_elapsed_seconds']:.2f} | "
            f"{row['num_failed_exec']}/{row['num_missing_answer']} |"
        )
    return lines


def render_markdown(report: dict[str, Any]) -> str:
    full = report["full200_anchor"]
    p4b = report["p4b_new_seed"]
    e3 = report["e3_multiseed_boundary"]
    e4 = report["e4_multimodel_gate"]
    coarse = report["coarse_ablation_key_numbers"]
    lines = [
        "# 当前专利实验章节收口稿",
        "",
        f"生成时间：`{report['generated_at_local']}`",
        "",
        "本文档用于回答：当前哪些实验结果可以写进专家/专利材料，哪些结论必须保留边界。它只汇总已有 frozen 证据，不新增 benchmark 结果。",
        "",
        "## 1. 当前总判断",
        "",
        f"- Qwen3-32B full200：MyAgent `489/600`，MACT `450/600`，delta `+39`，整体 token ratio `{full['aggregate_token_ratio']:.4f}`，整体耗时 ratio `{full['aggregate_elapsed_ratio']:.4f}`。",
        f"- P4b after-targeted Gate-50：MyAgent `121/150`，MACT `111/150`，三数据集单项均超过 MACT，整体 token ratio `{p4b['after_targeted_rows'][-1]['token_ratio']:.4f}`。",
        f"- E3 Seed-C/D：current-only 合计 `212/300`，token ratio `{e3['aggregate_diagnosis']['weighted_token_ratio_to_mact_full200_reference']:.4f}`，failed/missing `0/0`，但 decision 仍是 boundary，不是多 seed 稳定性达标。",
        f"- E4 多模型 gate：`{e4['decision']}`，无 untested local model、无 API provider profile/key；0-3 卡作为默认下一次启动池 `{e4['default_gpu_pool']}`。",
        "",
        "## 2. 可以写入的正证据",
        "",
        "### Qwen3-32B Full200 主结果",
        "",
        *render_result_table(full["rows"]),
        "",
        "### P4b After-Targeted Gate-50",
        "",
        f"P4b 原始 WTQ 风险为 MyAgent `{p4b['original_wtq']['myagent_correct']}/{p4b['original_wtq']['rows']}` vs MACT `{p4b['original_wtq']['mact_correct']}/{p4b['original_wtq']['rows']}`。WTQ affected-slice fresh 验证为 `{p4b['targeted_fresh']['correct']}/{p4b['targeted_fresh']['rows']}`，merged/eval `{p4b['targeted_fresh']['merged_rows']}/{p4b['targeted_fresh']['eval_rows']}`，failed/missing `{p4b['targeted_fresh']['num_failed_exec']}/{p4b['targeted_fresh']['num_missing_answer']}`。",
        "",
        *render_result_table(p4b["after_targeted_rows"]),
        "",
        "## 3. 机制证据",
        "",
        f"- strong verification / 劝返：关闭 no_strong_verification 后 overall 相对 current `{coarse['no_strong_verification_delta_vs_current']}/150`，WTQ 相对 current `{coarse['no_strong_verification_wtq_delta_vs_current']}/50`。",
        f"- deterministic audit：关闭 deterministic shortcuts 后 overall 相对 current `{coarse['no_deterministic_shortcuts_delta_vs_current']}/150`，TabFact `{coarse['no_deterministic_shortcuts_tabfact_delta_vs_current']}/50`，CRT `{coarse['no_deterministic_shortcuts_crt_delta_vs_current']}/50`。",
        f"- TabFact deterministic audit 同时节省预算：no_deterministic_shortcuts 的 TabFact token 为 current 的 `{coarse['no_deterministic_shortcuts_tabfact_token_ratio_vs_current']:.4f}x`。",
        f"- 机制矩阵：`{report['evidence_paths']['mechanism_matrix_md']}`。",
        "",
        "## 4. 必须保留的边界",
        "",
        "- P4b 原始结果不能写成新 seed 三数据集全部超过 MACT；WTQ 原始结果低于 MACT，after-targeted 结果才恢复单项优势。",
        "- E3 Seed-C/D current-only 不能写成多 seed 稳定超过 MACT；它们没有同 seed paired MACT，且 decision 为 `stop_or_inspect`。",
        "- E4 不能写成多模型已验证；当前只是 readiness audit，结论是没有可启动候选。",
        "- 不能把 full200/gate 结果写成全量官方测试集完成。",
        "",
        "### E3 Boundary 表",
        "",
    ]
    for seed in e3["seed_runs"]:
        seed_name = seed["seed_label"].replace("_", "-")
        lines.extend(
            [
                f"#### {seed_name}",
                "",
                *render_result_table(seed["datasets"] + [seed["aggregate"]], token_key="token_ratio_to_mact_full200_reference"),
                "",
                f"decision: `{seed['decision']}`。",
                "",
            ]
        )
    lines.extend(
        [
            "E3 诊断结论：",
            "",
            *[f"- {item}" for item in e3["boundary_findings"]],
            "",
            "## 5. 正式实验表状态",
            "",
            "| stage | status | patent use |",
            "|---|---|---|",
        ]
    )
    for item in report["formal_experiment_status"]:
        lines.append(f"| {item['stage']} | `{item['status']}` | {item['patent_use']} |")
    lines.extend(
        [
            "",
            "## 6. 下一步触发规则",
            "",
            *[f"- {item}" for item in report["next_trigger_rules"]],
            "",
            "## 7. 关键证据路径",
            "",
            *[f"- `{key}`: `{value}`" for key, value in report["evidence_paths"].items()],
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=PACKAGE_DIR)
    args = parser.parse_args()
    report = build_section()
    stamp = dt.datetime.now().astimezone().strftime("%Y%m%d_%H%M%S")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    json_path = args.output_dir / f"current_patent_experiment_section_{stamp}.json"
    md_path = args.output_dir / f"current_patent_experiment_section_{stamp}_zh.md"
    latest_json = args.output_dir / "latest_current_patent_experiment_section.json"
    latest_md = args.output_dir / "latest_current_patent_experiment_section_zh.md"
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
                "status": report["write_status"]["current_status"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
