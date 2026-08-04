#!/usr/bin/env python3
"""Build an E3 semantic-boundary repair and validation plan."""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from typing import Any


RUN_DIR = Path(__file__).resolve().parent
SUMMARY_DIR = RUN_DIR / "summary"
MULTISEED_RUN = Path(
    "/home/ubuntu/lzz/MACT/outputs/server_runs/"
    "qwen3_32b_policy_v6b_multiseed_gate50_20260801_2231"
)
BUDGET_PROBE_RUN = Path(
    "/home/ubuntu/lzz/MACT/outputs/server_runs/"
    "qwen3_32b_policy_v6b_e3_boundary_budget_probe_20260804_1035"
)
DIAGNOSIS_JSON = MULTISEED_RUN / "summary" / "seed_boundary_error_diagnosis.json"
BUDGET_PROBE_JSON = BUDGET_PROBE_RUN / "summary" / "e3_boundary_budget_probe_summary.json"

CURRENT_SEED_THRESHOLDS = {"wtq": 35, "tabfact": 45, "crt": 30}


CATEGORY_CONFIG: dict[str, dict[str, Any]] = {
    "wtq_temporal_or_age_lookup_boundary": {
        "mechanism": "WTQ temporal/age lookup contract plus selective max_replan=5 when the answer column is temporal or age-like.",
        "claim_families": ["C1", "C4", "C5", "C6"],
        "code_hook": "WTQ high-risk denotation verifier and answer-contract layer.",
        "validation_gate": "Recover remaining temporal representative rows without changing already-correct direct lookup rows; failed/missing must stay 0.",
        "patent_note": "Useful as adaptive-budget evidence, but partial recovery means it still needs a semantic answer-shape guard.",
    },
    "wtq_entity_lookup_or_row_selection_boundary": {
        "mechanism": "Entity lookup / row-selection guard that validates the selected row against numeric predicates and returns null only after evidence exhaustion.",
        "claim_families": ["C1", "C2", "C4", "C5"],
        "code_hook": "Table compression row recall, simple lookup fallback, and final answer contract.",
        "validation_gate": "Recover at least one probe row and preserve no-harm rows where entity lookup already agrees with gold-free verifier evidence.",
        "patent_note": "Zero recovery under extra budget; treat as semantic guard backlog rather than a replan-budget problem.",
    },
    "wtq_numeric_aggregation_or_difference_boundary": {
        "mechanism": "Numeric aggregation/difference contract that checks count, sum, difference, and comparison operators against parsed table columns.",
        "claim_families": ["C3", "C5"],
        "code_hook": "WTQ deterministic numeric audit before accepting high-risk denotation.",
        "validation_gate": "Use a gold-free affected slice from Seed-C/D wrong rows plus held-out correct aggregation rows; no answer-format regressions.",
        "patent_note": "High-volume unprobed category; should be evaluated before spending paired MACT runtime.",
    },
    "wtq_rank_direction_or_ordinal_boundary": {
        "mechanism": "Rank direction and ordinal phrase guard for highest/lowest, before/after, first/last, and listed-after target columns.",
        "claim_families": ["C3", "C5"],
        "code_hook": "WTQ ordinal/rank answer contract and target-column selector.",
        "validation_gate": "Recover rank-direction rows without using sample IDs or gold answers; existing P4b targeted WTQ fixes must remain green.",
        "patent_note": "Unprobed but visible in Seed-D; likely belongs with deterministic semantic audit rather than budget.",
    },
    "tabfact_temporal_order_boundary": {
        "mechanism": "Temporal order entailment audit with selective extra replan only when date/order evidence is ambiguous.",
        "claim_families": ["C3", "C4", "C6"],
        "code_hook": "TabFact deterministic temporal audit and risk-gated replan budget.",
        "validation_gate": "Keep the 2/2 budget-probe recoveries and verify no harm on temporal true/false no-harm rows.",
        "patent_note": "Strong budget-sensitive evidence; claim selective budget, not blanket extra reasoning.",
    },
    "tabfact_numeric_count_or_comparison_boundary": {
        "mechanism": "Column-value count / numeric comparison audit with selective replan when the deterministic count conflicts with model entailment.",
        "claim_families": ["C3", "C4", "C6"],
        "code_hook": "TabFact column-value counting shortcuts and high-risk verifier override.",
        "validation_gate": "Keep the recovered probe row and run no-harm checks on existing TabFact full200 correct numeric rows.",
        "patent_note": "Useful adaptive-budget and deterministic-audit evidence; sample count is small, so avoid broad claims.",
    },
    "tabfact_false_negative_entailment_boundary": {
        "mechanism": "Multi-entity equality / same-team entailment audit to prevent false negatives when multiple entities share a table relation.",
        "claim_families": ["C3", "C5"],
        "code_hook": "TabFact entity-attribute and same-row/multi-entity deterministic audit.",
        "validation_gate": "Recover the same-team representative row without flipping existing false-positive/negation rows.",
        "patent_note": "Zero recovery under extra budget; requires semantic entailment audit rather than more replan attempts.",
    },
    "tabfact_false_positive_or_negation_boundary": {
        "mechanism": "Negation and contradiction guard that checks whether a table row explicitly falsifies the statement.",
        "claim_families": ["C3", "C5"],
        "code_hook": "TabFact contradiction/negation deterministic audit.",
        "validation_gate": "Use Seed-D false-positive rows plus held-out true statements; no broad negation keyword hardcoding.",
        "patent_note": "Unprobed follow-up category; should be handled as semantic audit if more TabFact stability is needed.",
    },
    "crt_multi_step_numeric_composition_boundary": {
        "mechanism": "CRT multi-step numeric composition guard that validates intermediate quantities, units, averages, and yes/no answer form.",
        "claim_families": ["C3", "C5"],
        "code_hook": "CRT numeric program audit and answer-shape validator before final response selection.",
        "validation_gate": "Recover at least one of two probe rows while keeping CRT current seed gate at >=30/50 and token ratio <1.0.",
        "patent_note": "Zero recovery and high token cost under extra budget; do not blanket-increase max_replan for CRT.",
    },
    "crt_span_or_universal_quantifier_boundary": {
        "mechanism": "Span / universal-quantifier guard that enforces yes/no or scalar answer contracts instead of comparative-span leakage.",
        "claim_families": ["C3", "C5"],
        "code_hook": "CRT answer-contract enforcement and quantifier parser.",
        "validation_gate": "Recover answer-shape failures such as comparative words returned for yes/no questions; no missing-answer regressions.",
        "patent_note": "Zero recovery under budget probe; evidence points to answer-contract semantics, not runtime budget.",
    },
    "crt_table_reasoning_or_entity_boundary": {
        "mechanism": "CRT table entity grounding guard for matching row groups before doing numeric or logical composition.",
        "claim_families": ["C2", "C3", "C5"],
        "code_hook": "CRT row/column grounding and evidence-retention audit.",
        "validation_gate": "Run affected-slice plus no-harm rows where entity grounding is already correct.",
        "patent_note": "High-volume unprobed category; prioritize after the two zero-recovery CRT probe categories.",
    },
    "crt_percentage_complement_or_aggregation_boundary": {
        "mechanism": "Percentage complement and aggregation guard for percent-to-count, complement, and weighted-average questions.",
        "claim_families": ["C3", "C5"],
        "code_hook": "CRT percentage parser and numeric-composition validator.",
        "validation_gate": "No harm on CRT rows already answered through deterministic shortcuts; failed/missing must stay 0.",
        "patent_note": "High-volume unprobed CRT category; belongs in semantic numeric guard work.",
    },
}


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def dataset_from_category(category: str) -> str:
    if category.startswith("wtq_"):
        return "wtq"
    if category.startswith("tabfact_"):
        return "tabfact"
    if category.startswith("crt_"):
        return "crt"
    return "unknown"


def classify_category(total_wrong: int, probe: dict[str, Any] | None) -> tuple[str, str]:
    if probe is None:
        if total_wrong >= 7:
            return "P1", "unprobed_semantic_guard_candidate"
        return "P2", "unprobed_followup"
    recovered = int(probe.get("recovered") or 0)
    total = int(probe.get("total") or 0)
    if total > 0 and recovered == total:
        return "P2", "adaptive_budget_candidate"
    if recovered > 0:
        return "P1", "mixed_budget_and_semantic_guard"
    return "P0", "semantic_guard_required_after_budget_failed"


def build_plan() -> dict[str, Any]:
    generated_at = dt.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
    diagnosis = read_json(DIAGNOSIS_JSON)
    budget = read_json(BUDGET_PROBE_JSON)

    wrong_counts: dict[str, int] = {
        str(k): int(v)
        for k, v in (diagnosis.get("aggregate", {}).get("wrong_category_top") or {}).items()
    }
    probe_categories: dict[str, dict[str, Any]] = {
        str(k): dict(v)
        for k, v in (budget.get("aggregate", {}).get("category_recovery") or {}).items()
    }
    rows_by_category: dict[str, list[dict[str, Any]]] = {}
    for row in budget.get("rows", []):
        rows_by_category.setdefault(str(row.get("category") or ""), []).append(row)

    categories: list[dict[str, Any]] = []
    for category in sorted(set(wrong_counts) | set(probe_categories)):
        probe = probe_categories.get(category)
        priority, track = classify_category(wrong_counts.get(category, 0), probe)
        cfg = CATEGORY_CONFIG.get(
            category,
            {
                "mechanism": "Gold-free semantic guard to be specified after row inspection.",
                "claim_families": ["C3", "C5"],
                "code_hook": "Dataset-specific verifier or answer-contract layer.",
                "validation_gate": "Affected-slice fresh run with no-harm rows and failed/missing fixed at 0.",
                "patent_note": "Do not claim until a targeted fresh run validates the guard.",
            },
        )
        probe_total = int(probe.get("total") or 0) if probe else 0
        probe_recovered = int(probe.get("recovered") or 0) if probe else 0
        categories.append(
            {
                "category": category,
                "dataset": dataset_from_category(category),
                "priority": priority,
                "track": track,
                "e3_wrong_rows": wrong_counts.get(category, 0),
                "budget_probe_rows": probe_total,
                "budget_probe_recovered": probe_recovered,
                "budget_probe_recovery_rate": (probe_recovered / probe_total) if probe_total else None,
                "representative_probe_ids": [
                    f"{row.get('seed')}/{row.get('dataset')}/{row.get('id')}"
                    for row in rows_by_category.get(category, [])
                ],
                **cfg,
            }
        )

    priority_order = {"P0": 0, "P1": 1, "P2": 2}
    categories.sort(
        key=lambda item: (
            priority_order.get(item["priority"], 9),
            -int(item["e3_wrong_rows"]),
            item["dataset"],
            item["category"],
        )
    )

    seed_reports = diagnosis.get("seed_reports", {})
    seed_gap = {}
    for seed, report in seed_reports.items():
        seed_gap[seed] = {}
        for dataset, item in (report.get("datasets") or {}).items():
            correct = int(item.get("summary", {}).get("correct") or 0)
            threshold = CURRENT_SEED_THRESHOLDS[dataset]
            seed_gap[seed][dataset] = {
                "correct": correct,
                "threshold": threshold,
                "needed_to_pass": max(0, threshold - correct),
                "passed_current_seed_gate": bool(item.get("summary", {}).get("passed_current_seed_gate")),
            }

    high_priority = [item for item in categories if item["priority"] in {"P0", "P1"}]
    zero_recovery = [
        item["category"]
        for item in categories
        if item["budget_probe_rows"] > 0 and item["budget_probe_recovered"] == 0
    ]
    budget_sensitive = [
        item["category"]
        for item in categories
        if item["budget_probe_rows"] > 0 and item["budget_probe_recovered"] > 0
    ]

    return {
        "artifact_name": "e3_semantic_boundary_plan",
        "generated_at_local": generated_at,
        "run_dir": str(RUN_DIR),
        "source_diagnosis_json": str(DIAGNOSIS_JSON),
        "source_budget_probe_json": str(BUDGET_PROBE_JSON),
        "scope": "Planning artifact only. It uses completed E3 Seed-C/D diagnosis and max_replan=5 probe; it does not run models or change benchmark results.",
        "current_decision": "do_not_rerun_full200_or_paired_mact_until_targeted_guards_pass",
        "evidence_snapshot": {
            "e3_rows": diagnosis.get("aggregate", {}).get("rows"),
            "e3_correct": diagnosis.get("aggregate", {}).get("correct"),
            "e3_wrong": diagnosis.get("aggregate", {}).get("wrong"),
            "e3_weighted_token_ratio": diagnosis.get("aggregate", {}).get(
                "weighted_token_ratio_to_mact_full200_reference"
            ),
            "e3_failed": diagnosis.get("aggregate", {}).get("failed"),
            "e3_missing": diagnosis.get("aggregate", {}).get("missing"),
            "budget_probe_rows": budget.get("aggregate", {}).get("rows"),
            "budget_probe_recovered": budget.get("aggregate", {}).get("recovered"),
            "budget_probe_decision": budget.get("decision"),
            "zero_recovery_probe_categories": zero_recovery,
            "budget_sensitive_categories": budget_sensitive,
        },
        "seed_gate_gap": seed_gap,
        "category_plan": categories,
        "recommended_next_experiment_ladder": [
            {
                "stage": "S1_design_and_unit",
                "action": "Implement or specify gold-free semantic guards for P0 categories first; keep adaptive max_replan restricted to budget-sensitive categories.",
                "entry_condition": "No sample ID or gold-answer logic; existing full200/P4b artifacts remain frozen.",
                "exit_gate": "Code/unit/offline checks pass and guard trigger evidence is logged per row.",
            },
            {
                "stage": "S2_affected_slice_fresh",
                "action": "Run a small affected slice using current Qwen endpoints: all 12 budget-probe representative rows plus no-harm rows from each touched category.",
                "entry_condition": "S1 passes and services 8000/8001 are healthy.",
                "exit_gate": "Recover >=3 of the 7 zero-recovery probe rows, keep the 4 already-recovered budget rows correct, failed/missing 0/0, and avoid blanket CRT replan token growth.",
            },
            {
                "stage": "S3_e3_current_only_rerun",
                "action": "Only after S2 passes, rerun E3 Seed-C/D current-only Gate-50 rather than paired MACT.",
                "entry_condition": "Affected-slice gate passes with no-harm evidence.",
                "exit_gate": "For every seed/dataset: rows 50/50/50, failed/missing 0/0, token ratio <1.0, WTQ >=35/50, TabFact >=45/50, CRT >=30/50.",
            },
            {
                "stage": "S4_paired_mact_or_boundary_closeout",
                "action": "Run paired MACT only if both Seed-C and Seed-D pass current-only gates; otherwise update the patent package as an explicit applicability boundary.",
                "entry_condition": "S3 decision becomes run_paired_mact for both seeds.",
                "exit_gate": "Paired MACT summary is generated and committed, or the boundary is explicitly accepted in the patent package.",
            },
        ],
        "high_priority_work_items": high_priority,
        "patent_writing_boundary": {
            "can_write": [
                "Adaptive replan budget helps selected TabFact temporal/numeric and one WTQ temporal representative row.",
                "E3 remaining failures are semantic-boundary failures with failed/missing 0/0 and token still below MACT full200 reference overall.",
                "Future optimization should be framed as semantic audit and answer-contract expansion, not as benchmark reruns.",
            ],
            "cannot_write": [
                "Blanket max_replan=5 closes E3 stability.",
                "CRT representative errors are budget-sensitive.",
                "Multi-seed stable superiority is complete.",
                "Multi-model validation is complete.",
            ],
        },
    }


def format_rate(value: Any) -> str:
    return "n/a" if value is None else f"{float(value):.4f}"


def render_markdown(plan: dict[str, Any]) -> str:
    snap = plan["evidence_snapshot"]
    lines = [
        "# E3 Semantic Boundary Repair Plan",
        "",
        f"Generated: `{plan['generated_at_local']}`",
        "",
        "## Scope",
        "",
        plan["scope"],
        "",
        f"Current decision: `{plan['current_decision']}`.",
        "",
        "## Evidence Snapshot",
        "",
        "| item | value |",
        "|---|---:|",
        f"| E3 rows | {snap['e3_rows']} |",
        f"| E3 correct/wrong | {snap['e3_correct']}/{snap['e3_wrong']} |",
        f"| E3 weighted token ratio | {float(snap['e3_weighted_token_ratio']):.4f} |",
        f"| E3 failed/missing | {snap['e3_failed']}/{snap['e3_missing']} |",
        f"| budget probe rows | {snap['budget_probe_rows']} |",
        f"| budget probe recovered | {snap['budget_probe_recovered']} |",
        "",
        f"Budget probe decision: `{snap['budget_probe_decision']}`.",
        "",
        "Zero-recovery probe categories:",
        "",
    ]
    lines.extend(f"- `{item}`" for item in snap["zero_recovery_probe_categories"])
    lines.extend(["", "Budget-sensitive categories:", ""])
    lines.extend(f"- `{item}`" for item in snap["budget_sensitive_categories"])
    lines.extend(
        [
            "",
            "## Seed Gate Gap",
            "",
            "| seed | dataset | current | threshold | needed | pass |",
            "|---|---|---:|---:|---:|---|",
        ]
    )
    for seed, datasets in plan["seed_gate_gap"].items():
        for dataset, item in datasets.items():
            lines.append(
                f"| {seed} | {dataset} | {item['correct']}/50 | {item['threshold']}/50 | "
                f"{item['needed_to_pass']} | `{item['passed_current_seed_gate']}` |"
            )
    lines.extend(
        [
            "",
            "## Category Plan",
            "",
            "| priority | dataset | category | E3 wrong | probe recovered/rows | track | claim families |",
            "|---|---|---|---:|---:|---|---|",
        ]
    )
    for item in plan["category_plan"]:
        probe = "n/a" if item["budget_probe_rows"] == 0 else f"{item['budget_probe_recovered']}/{item['budget_probe_rows']}"
        lines.append(
            f"| {item['priority']} | {item['dataset']} | `{item['category']}` | "
            f"{item['e3_wrong_rows']} | {probe} | `{item['track']}` | "
            f"{', '.join(item['claim_families'])} |"
        )
    lines.extend(["", "## High Priority Work Items", ""])
    for item in plan["high_priority_work_items"]:
        ids = ", ".join(item["representative_probe_ids"]) or "no representative probe row"
        lines.extend(
            [
                f"### {item['priority']} `{item['category']}`",
                "",
                f"- E3 wrong rows: `{item['e3_wrong_rows']}`; budget probe: `{item['budget_probe_recovered']}/{item['budget_probe_rows'] or 0}`.",
                f"- Mechanism: {item['mechanism']}",
                f"- Code hook: {item['code_hook']}",
                f"- Validation gate: {item['validation_gate']}",
                f"- Probe IDs: {ids}",
                f"- Patent note: {item['patent_note']}",
                "",
            ]
        )
    lines.extend(
        [
            "## Next Experiment Ladder",
            "",
            "| stage | action | entry condition | exit gate |",
            "|---|---|---|---|",
        ]
    )
    for item in plan["recommended_next_experiment_ladder"]:
        lines.append(
            f"| `{item['stage']}` | {item['action']} | {item['entry_condition']} | {item['exit_gate']} |"
        )
    boundary = plan["patent_writing_boundary"]
    lines.extend(["", "## Patent Writing Boundary", "", "Can write:", ""])
    lines.extend(f"- {item}" for item in boundary["can_write"])
    lines.extend(["", "Cannot write:", ""])
    lines.extend(f"- {item}" for item in boundary["cannot_write"])
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    SUMMARY_DIR.mkdir(parents=True, exist_ok=True)
    plan = build_plan()
    json_text = json.dumps(plan, ensure_ascii=False, indent=2) + "\n"
    md_text = render_markdown(plan)
    (SUMMARY_DIR / "e3_semantic_boundary_plan.json").write_text(json_text, encoding="utf-8")
    (SUMMARY_DIR / "e3_semantic_boundary_plan.md").write_text(md_text, encoding="utf-8")
    print(
        json.dumps(
            {
                "summary_json": str(SUMMARY_DIR / "e3_semantic_boundary_plan.json"),
                "summary_md": str(SUMMARY_DIR / "e3_semantic_boundary_plan.md"),
                "high_priority_items": len(plan["high_priority_work_items"]),
                "decision": plan["current_decision"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
