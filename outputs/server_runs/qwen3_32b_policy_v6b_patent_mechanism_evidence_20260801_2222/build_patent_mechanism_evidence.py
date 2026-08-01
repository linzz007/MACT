#!/usr/bin/env python3
"""Build patent-facing mechanism evidence from frozen ablation artifacts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


OUT_DIR = Path(__file__).resolve().parent
COARSE_PATH = Path(
    "/home/ubuntu/lzz/MACT/outputs/server_runs/"
    "qwen3_32b_policy_v6b_coarse_ablation_gate50_20260801_0040/"
    "coarse_ablation_gate50_summary.json"
)
ATTR_PATH = Path(
    "/home/ubuntu/lzz/MACT/outputs/server_runs/"
    "qwen3_32b_policy_v6b_mechanism_attribution_20260801_0033/"
    "mechanism_attribution_summary.json"
)
FULL200_PATH = Path(
    "/home/ubuntu/lzz/MACT/outputs/server_runs/"
    "qwen3_32b_policy_v6b_all200_acceptance_20260731_132611/"
    "qwen3_policy_v6b_all200_acceptance_summary.json"
)


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(path)
    return json.loads(path.read_text(encoding="utf-8"))


def _weighted(items: list[dict[str, Any]], key: str) -> float:
    rows = sum(int(item["rows"]) for item in items)
    return sum(float(item[key]) * int(item["rows"]) for item in items) / rows


def summarize_variant(name: str, variant: dict[str, Any]) -> dict[str, Any]:
    per_dataset: dict[str, dict[str, Any]] = {}
    rows = correct = current_correct = mact_correct = 0
    token_items: list[dict[str, Any]] = []
    for dataset in ("wtq", "tabfact", "crt"):
        item = variant["datasets"][dataset]
        var = item["variant"]
        cur = item["current_reference"]
        mact = item["mact_reference"]
        dataset_rows = int(var["rows"])
        rows += dataset_rows
        correct += int(var["correct"])
        current_correct += int(cur["correct"])
        mact_correct += int(mact["correct"])
        token_items.append(
            {
                "rows": dataset_rows,
                "variant_tokens": float(var["avg_total_tokens"]),
                "current_tokens": float(cur["avg_total_tokens"]),
                "mact_tokens": float(mact["avg_total_tokens"]),
            }
        )
        per_dataset[dataset] = {
            "rows": dataset_rows,
            "variant_correct": int(var["correct"]),
            "current_correct": int(cur["correct"]),
            "mact_correct": int(mact["correct"]),
            "delta_vs_current": int(item["delta_vs_current"]),
            "delta_vs_mact": int(item["delta_vs_mact"]),
            "token_ratio_vs_current": float(item["token_ratio_vs_current"]),
            "token_ratio_vs_mact": float(item["token_ratio_vs_mact"]),
            "failed": int(var.get("num_failed_exec") or 0),
            "missing": int(var.get("num_missing_answer") or 0),
        }
    variant_tokens = _weighted(token_items, "variant_tokens")
    current_tokens = _weighted(token_items, "current_tokens")
    mact_tokens = _weighted(token_items, "mact_tokens")
    return {
        "variant": name,
        "rows": rows,
        "correct": correct,
        "current_reference_correct": current_correct,
        "mact_reference_correct": mact_correct,
        "delta_vs_current": correct - current_correct,
        "delta_vs_mact": correct - mact_correct,
        "avg_total_tokens": variant_tokens,
        "token_ratio_vs_current": variant_tokens / current_tokens,
        "token_ratio_vs_mact": variant_tokens / mact_tokens,
        "per_dataset": per_dataset,
    }


def attribution_slice(dataset_item: dict[str, Any]) -> dict[str, Any]:
    groups = dataset_item["groups"]
    return {
        "current_correct": dataset_item["current_correct"],
        "old_correct": dataset_item["old_correct"],
        "mact_correct": dataset_item["mact_correct"],
        "net_gain_vs_old": dataset_item["net_gain_vs_old"],
        "net_gain_vs_mact": dataset_item["net_gain_vs_mact"],
        "gain_vs_old": {
            "count": groups["gain_vs_old"]["count"],
            "family_counts": groups["gain_vs_old"].get("family_counts", {}),
            "top_tags": dict(list(groups["gain_vs_old"].get("tag_counts", {}).items())[:8]),
        },
        "harm_vs_old": {
            "count": groups["harm_vs_old"]["count"],
            "family_counts": groups["harm_vs_old"].get("family_counts", {}),
        },
        "current_only_vs_mact": {
            "count": groups["current_only_vs_mact"]["count"],
            "family_counts": groups["current_only_vs_mact"].get("family_counts", {}),
        },
        "mact_only": {
            "count": groups["mact_only"]["count"],
            "family_counts": groups["mact_only"].get("family_counts", {}),
        },
    }


def build_summary() -> dict[str, Any]:
    coarse = read_json(COARSE_PATH)
    attr = read_json(ATTR_PATH)
    full200 = read_json(FULL200_PATH)
    variants = {
        name: summarize_variant(name, value)
        for name, value in coarse["variants"].items()
    }
    datasets = {
        dataset: attribution_slice(item)
        for dataset, item in attr["datasets"].items()
    }
    result = {
        "title": "Qwen3-32B patent-facing mechanism evidence matrix",
        "created_at_local": "2026-08-01 22:22 CST",
        "scope": "Combine frozen full200, run-based coarse Gate-50 ablations, and offline attribution for patent/expert evidence.",
        "source_paths": {
            "full200": str(FULL200_PATH),
            "coarse_ablation": str(COARSE_PATH),
            "mechanism_attribution": str(ATTR_PATH),
        },
        "full200_anchor": full200["aggregate"],
        "coarse_ablation": {
            "note": coarse["note"],
            "variants": variants,
        },
        "offline_attribution": {
            "method": attr["method"],
            "datasets": datasets,
        },
        "patent_mechanism_evidence": {
            "risk_collaboration_and_persuasion_back": {
                "primary_evidence": [
                    "coarse_ablation.no_strong_verification: overall -8/150 vs current reference",
                    "coarse_ablation.no_strong_verification.wtq: -7/50 vs current reference",
                    "offline_attribution.wtq.gain_vs_old: 24/25 gain rows tagged strong_verification and 16/25 tagged evidence_retention",
                ],
                "boundary": "The coarse slice is diagnostic and disagreement-enriched; it supports mechanism contribution, not a random-seed generalization estimate.",
            },
            "deterministic_audit": {
                "primary_evidence": [
                    "coarse_ablation.no_deterministic_shortcuts: overall -15/150 vs current reference",
                    "coarse_ablation.no_deterministic_shortcuts.tabfact: -9/50 vs current reference and 1.4487x current tokens",
                    "coarse_ablation.no_deterministic_shortcuts.crt: -7/50 vs current reference",
                    "offline_attribution.tabfact.gain_vs_old: 8/9 gain rows tagged deterministic_audit",
                ],
                "boundary": "WTQ deterministic shortcuts are mixed on this coarse slice; the strongest deterministic-audit evidence is TabFact and CRT.",
            },
            "evidence_retention": {
                "primary_evidence": [
                    "offline_attribution.wtq.gain_vs_old: 16/25 gain rows tagged evidence_retention",
                    "offline_attribution.tabfact.gain_vs_old: 9/9 gain rows tagged evidence_retention",
                    "offline_attribution.crt.current_only_vs_mact: 37/40 current-only rows tagged evidence_retention",
                ],
                "boundary": "Evidence-retention attribution is associative unless followed by a fine-grained no_evidence_retention ablation.",
            },
            "budget_control": {
                "primary_evidence": [
                    "full200 aggregate token ratio current/MACT = 0.5717",
                    "full200 aggregate elapsed ratio current/MACT = 0.1337",
                    "coarse deterministic audit on TabFact improves accuracy while avoiding the high token path",
                ],
                "boundary": "CRT token savings are weaker than WTQ/TabFact; formal claims should use overall token reduction and per-dataset ratios.",
            },
        },
        "remaining_e2_work": [
            "Run WTQ targeted fresh validation on Qwen3-32B.",
            "Run WTQ after-targeted P4b full50 only if targeted fresh passes.",
            "Add fine-grained no_evidence_retention or no_wtq_verifier_override ablation only if fresh WTQ remains ambiguous.",
        ],
    }
    assert result["full200_anchor"]["current_correct"] == 489
    assert variants["no_strong_verification"]["delta_vs_current"] == -8
    assert variants["no_deterministic_shortcuts"]["delta_vs_current"] == -15
    assert datasets["wtq"]["gain_vs_old"]["family_counts"]["strong_verification"] == 24
    assert datasets["tabfact"]["gain_vs_old"]["family_counts"]["deterministic_audit"] == 8
    return result


def render_markdown(summary: dict[str, Any]) -> str:
    anchor = summary["full200_anchor"]
    lines = [
        "# Patent-Facing Mechanism Evidence Matrix",
        "",
        f"Created: {summary['created_at_local']}",
        "",
        "This document combines frozen full200 results, run-based coarse Gate-50 ablations, and offline attribution. It is written for patent/expert evidence, not as a replacement for future fresh validation.",
        "",
        "## Full200 Anchor",
        "",
        "| metric | value |",
        "|---|---:|",
        f"| MyAgent correct | {anchor['current_correct']}/{anchor['rows']} |",
        f"| MACT correct | {anchor['mact_correct']}/{anchor['rows']} |",
        f"| delta | {anchor['accuracy_delta_correct']:+d} |",
        f"| token ratio | {anchor['token_ratio_current_over_mact']:.4f} |",
        f"| elapsed ratio | {anchor['elapsed_ratio_current_over_mact']:.4f} |",
        f"| MyAgent failures / missing | {anchor['current_failures']} / {anchor['current_missing_answers']} |",
        "",
        "## Run-Based Coarse Ablation",
        "",
        "Diagnostic Gate-50 is disagreement-enriched. It supports mechanism contribution, not random-seed generalization.",
        "",
        "| variant | correct | current ref | delta vs current | token/current | token/MACT |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for name, item in summary["coarse_ablation"]["variants"].items():
        lines.append(
            f"| {name} | {item['correct']}/{item['rows']} | "
            f"{item['current_reference_correct']}/{item['rows']} | "
            f"{item['delta_vs_current']:+d} | "
            f"{item['token_ratio_vs_current']:.4f} | {item['token_ratio_vs_mact']:.4f} |"
        )
    lines.extend(["", "Per-dataset deltas:", "", "| variant | WTQ | TabFact | CRT |", "|---|---:|---:|---:|"])
    for name, item in summary["coarse_ablation"]["variants"].items():
        per = item["per_dataset"]
        lines.append(
            f"| {name} | {per['wtq']['delta_vs_current']:+d}/50 | "
            f"{per['tabfact']['delta_vs_current']:+d}/50 | {per['crt']['delta_vs_current']:+d}/50 |"
        )
    lines.extend(["", "## Offline Attribution", ""])
    lines.extend(
        [
            "| dataset | current | old | MACT | net vs old | net vs MACT | gain vs old | harm vs old |",
            "|---|---:|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for dataset, item in summary["offline_attribution"]["datasets"].items():
        lines.append(
            f"| {dataset} | {item['current_correct']}/200 | {item['old_correct']}/200 | "
            f"{item['mact_correct']}/200 | {item['net_gain_vs_old']:+d} | "
            f"{item['net_gain_vs_mact']:+d} | {item['gain_vs_old']['count']} | {item['harm_vs_old']['count']} |"
        )
    lines.extend(["", "Gain family counts:", ""])
    for dataset, item in summary["offline_attribution"]["datasets"].items():
        families = ", ".join(
            f"{name}={count}"
            for name, count in item["gain_vs_old"]["family_counts"].items()
        )
        lines.append(f"- {dataset}: {families}")
    lines.extend(["", "## Patent Mechanism Evidence", ""])
    for mechanism, item in summary["patent_mechanism_evidence"].items():
        lines.append(f"### {mechanism}")
        lines.append("")
        for evidence in item["primary_evidence"]:
            lines.append(f"- {evidence}")
        lines.append(f"- Boundary: {item['boundary']}")
        lines.append("")
    lines.extend(["## Remaining E2 Work", ""])
    for item in summary["remaining_e2_work"]:
        lines.append(f"- {item}")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    summary = build_summary()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    json_path = OUT_DIR / "patent_mechanism_evidence_matrix.json"
    md_path = OUT_DIR / "patent_mechanism_evidence_matrix.md"
    json_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(summary), encoding="utf-8")
    print(json.dumps({"json": str(json_path), "md": str(md_path)}, indent=2))


if __name__ == "__main__":
    main()
