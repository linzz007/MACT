#!/usr/bin/env python3
"""Diagnose WTQ P4b MyAgent-vs-MACT discordant rows.

This script is intentionally stored inside the run directory so the generated
diagnosis can be reproduced from the exact frozen artifacts used for P4b.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any


RUN_DIR = Path(__file__).resolve().parent


DIAGNOSES: dict[str, dict[str, str]] = {
    "nu-3537": {
        "category": "conflict_gate_and_cell_semantics",
        "cause": "Code counted `Champion (no playoff)` as a playoff row. The thinking verifier found the correct count, but the conflict gate did not let that candidate take over.",
        "next_action": "Add a generic WTQ playoff/no-playoff cell audit and allow high-confidence verifier override when a parenthetical negator contradicts the code path.",
    },
    "nu-1108": {
        "category": "entity_surface_contract",
        "cause": "MyAgent selected the right person but returned the table cell with military title prefix `MG`; WTQ gold expects the mentioned person surface `William A. Mann`.",
        "next_action": "Add requested-entity surface canonicalization for rank/title prefixes when the question names the candidate entity without the prefix.",
    },
    "nu-2825": {
        "category": "count_semantics",
        "cause": "Question asks the number of winners in a division. MyAgent interpreted this as distinct/non-empty winners and returned 7, while gold counts the 8 non-empty Community Division entries.",
        "next_action": "Add a count-intent audit that separates row/cell occurrence count from distinct-value count for `number of winners in <column>` questions.",
    },
    "nu-3905": {
        "category": "entity_surface_contract",
        "cause": "MyAgent identified the correct row but returned `Ludwig Wolf Germany (GER)` instead of the requested person name only.",
        "next_action": "Add medal/person column answer cleanup that strips adjacent country suffixes when the question asks `who/person` rather than full medal cell text.",
    },
    "nu-3317": {
        "category": "count_semantics",
        "cause": "MyAgent summed filled cells across sponsor columns and returned 21. Gold expects the main sponsor occurrence count used by WTQ for this table, 13.",
        "next_action": "Add sponsor-count disambiguation: for open `total number of sponsors` questions prefer the primary sponsor column/row occurrence unless the question names multiple sponsor columns.",
    },
    "nu-3990": {
        "category": "answer_target_column",
        "cause": "MyAgent found the previous row before Felix but returned the previous row nickname `Pop`; the question asks for the experiment number, `009`.",
        "next_action": "Strengthen answer-contract target-column detection for `which <column> number` questions before accepting row-neighbor shortcuts.",
    },
    "nu-1478": {
        "category": "domain_marker_parsing",
        "cause": "MyAgent treated overtime as tied final scores and returned 0. The table explicitly marks overtime with `(OT)` in the Result column.",
        "next_action": "Add a generic sports-score marker audit for overtime/extra-time tokens such as `(OT)` before score-equality heuristics.",
    },
    "nu-3320": {
        "category": "ordinal_phrase_matching",
        "cause": "MyAgent looked for literal `3 attempts` and missed `third attempt`; it then chose a different athlete.",
        "next_action": "Normalize ordinal phrases (`third attempt`, `3rd attempt`, `three attempts`) in WTQ event/performance matching.",
    },
    "nu-1825": {
        "category": "listed_after_shortcut_targeting",
        "cause": "The row-major listed-after shortcut returned the current row Capacity value `48712` instead of the next row Stadium value.",
        "next_action": "Fix listed-after shortcut column targeting: when the question asks for a column/entity after a named item, return the same requested column from the next row.",
    },
    "nu-4296": {
        "category": "myagent_strength_semantic_disambiguation",
        "cause": "MyAgent used Notes semantics to distinguish acquired/ordered vessels and returned 2001; MACT took the minimum Date value, 1998, from a row that is not an acquisition answer under the gold label.",
        "next_action": "Preserve this behavior as evidence that verifier/thinking fallback can correct naive min-date execution.",
    },
    "nu-2441": {
        "category": "myagent_strength_answer_contract",
        "cause": "MyAgent returned the compact WTQ denotation `No`; MACT returned a full explanatory sentence that is semantically right but fails strict WTQ denotation matching.",
        "next_action": "Use this as patent evidence for answer-shape checking and concise denotation enforcement.",
    },
    "nu-3246": {
        "category": "myagent_strength_temporal_neighbor",
        "cause": "MyAgent selected the immediately next designed building after Hvittrask Studio and Home; MACT selected a later building.",
        "next_action": "Use this as evidence for row-neighbor temporal evidence retention under compressed routing.",
    },
    "nu-2572": {
        "category": "both_wrong_numeric_range_parsing",
        "cause": "Both systems mishandled speed thresholds/ranges such as `85 km/h-105 km/h`; MyAgent undercounted and MACT overcounted.",
        "next_action": "Add range-aware numeric parsing for threshold count questions if WTQ stability remains a priority.",
    },
    "nu-1104": {
        "category": "both_wrong_location_alias",
        "cause": "Both systems disagreed with gold on United States location matching; table contains United States plus city/state aliases such as Michigan and New Jersey.",
        "next_action": "Treat country aliases and US state/city cells explicitly before country-count audits.",
    },
    "nu-66": {
        "category": "both_wrong_same_row_next_field",
        "cause": "Both systems returned the next row premiere date. Gold expects the next listed date after June 14, 2010 in row-major order, the same row's following finale date December 6, 2010.",
        "next_action": "Clarify `next listed after` semantics: scan row-major cells after the matched cell, not only the next row.",
    },
    "nu-1775": {
        "category": "both_wrong_multi_answer_contract",
        "cause": "MyAgent omitted one competition and MACT emitted a comma-delimited sentence rather than a structured WTQ answer list.",
        "next_action": "Strengthen list-answer arity enforcement and pre-event filtering for multi-answer temporal questions.",
    },
}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def load_eval_functions(myagent_root: Path) -> tuple[Any, Any, Any]:
    sys.path.insert(0, str(myagent_root / "code"))
    from evaluate_results import dataset_accuracy, gold_for_em, prediction_for_em

    return dataset_accuracy, gold_for_em, prediction_for_em


def short(value: Any, limit: int = 180) -> str:
    text = "" if value is None else str(value)
    text = text.replace("\n", " ")
    if len(text) > limit:
        return text[: limit - 3] + "..."
    return text


def md_escape(value: Any) -> str:
    return short(value).replace("|", "\\|")


def token_total(row: dict[str, Any]) -> float:
    api = row.get("api_metrics") or {}
    if api.get("total_tokens") is not None:
        return float(api["total_tokens"])
    llm = row.get("llm_metrics") or {}
    return float(llm.get("total_tokens_est") or 0.0)


def candidate_summary(row: dict[str, Any]) -> str:
    pieces = []
    for candidate in row.get("candidate_answers") or []:
        pieces.append(f"{candidate.get('name')}={candidate.get('raw_answer')!r}")
    return "; ".join(pieces)


def build_report(myagent_root: Path) -> dict[str, Any]:
    dataset_accuracy, gold_for_em, prediction_for_em = load_eval_functions(myagent_root)
    my_rows = read_jsonl(RUN_DIR / "myagent_current/merged/wtq_qwen3-32b-local.jsonl")
    mact_rows = read_jsonl(RUN_DIR / "mact/wtq_mact_newseed_gate50.jsonl")
    mact_by_id = {row["id"]: row for row in mact_rows}
    if len(my_rows) != 50 or len(mact_rows) != 50:
        raise RuntimeError(f"Expected 50/50 rows, got {len(my_rows)}/{len(mact_rows)}")

    records: list[dict[str, Any]] = []
    confusion = Counter()
    categories = Counter()
    by_group_categories: dict[str, Counter[str]] = {
        "mact_only": Counter(),
        "myagent_only": Counter(),
        "both_wrong": Counter(),
    }

    for my_row in my_rows:
        row_id = my_row["id"]
        mact_row = mact_by_id[row_id]
        my_correct = bool(dataset_accuracy(my_row))
        mact_correct = bool(dataset_accuracy(mact_row))
        if my_correct and mact_correct:
            group = "both_correct"
        elif my_correct:
            group = "myagent_only"
        elif mact_correct:
            group = "mact_only"
        else:
            group = "both_wrong"
        confusion[group] += 1
        if group == "both_correct":
            continue

        diagnosis = DIAGNOSES.get(row_id)
        if not diagnosis:
            raise RuntimeError(f"Missing manual diagnosis for {row_id}")
        categories[diagnosis["category"]] += 1
        by_group_categories[group][diagnosis["category"]] += 1
        compression = my_row.get("compression_info") or {}
        selected = (my_row.get("agreement_decision") or {}).get("selected") or {}
        records.append(
            {
                "id": row_id,
                "group": group,
                "question": my_row.get("question"),
                "gold": gold_for_em(my_row),
                "answer_canonical": my_row.get("answer_canonical"),
                "myagent_prediction": prediction_for_em(my_row),
                "mact_prediction": prediction_for_em(mact_row),
                "myagent_correct": my_correct,
                "mact_correct": mact_correct,
                "category": diagnosis["category"],
                "cause": diagnosis["cause"],
                "next_action": diagnosis["next_action"],
                "problem_tags": my_row.get("problem_tags") or [],
                "risk_level": my_row.get("risk_level"),
                "strong_verification_reason": my_row.get("strong_verification_reason"),
                "deterministic_shortcut_applied": bool(my_row.get("deterministic_shortcut_applied")),
                "deterministic_shortcut_reason": my_row.get("deterministic_shortcut_reason") or "",
                "selected_candidate": {
                    "name": selected.get("name"),
                    "raw_answer": selected.get("raw_answer"),
                },
                "candidate_summary": candidate_summary(my_row),
                "compression": {
                    "original_rows": compression.get("original_rows"),
                    "compressed_rows": compression.get("compressed_rows"),
                    "original_cols": compression.get("original_cols"),
                    "compressed_cols": compression.get("compressed_cols"),
                    "compression_ratio": compression.get("compression_ratio"),
                },
                "tokens": {
                    "myagent_total": token_total(my_row),
                    "mact_total": token_total(mact_row),
                },
            }
        )

    mact_only = [record for record in records if record["group"] == "mact_only"]
    avg_mact_only_compression = sum(
        float((record["compression"] or {}).get("compression_ratio") or 0.0)
        for record in mact_only
    ) / len(mact_only)
    full_context_mact_only = sum(
        1
        for record in mact_only
        if float((record["compression"] or {}).get("compression_ratio") or 0.0) >= 0.999
    )

    return {
        "run_dir": str(RUN_DIR),
        "method": {
            "myagent_rows": str(RUN_DIR / "myagent_current/merged/wtq_qwen3-32b-local.jsonl"),
            "mact_rows": str(RUN_DIR / "mact/wtq_mact_newseed_gate50.jsonl"),
            "eval_module": str(myagent_root / "code/evaluate_results.py"),
            "note": "Correctness is recomputed with the same WTQ denotation function used by experiment eval.",
        },
        "confusion": dict(confusion),
        "categories": dict(categories),
        "categories_by_group": {
            group: dict(counter) for group, counter in by_group_categories.items()
        },
        "mact_only_compression": {
            "count": len(mact_only),
            "avg_compression_ratio": avg_mact_only_compression,
            "full_context_count": full_context_mact_only,
        },
        "records": records,
        "conclusion": {
            "primary_finding": "WTQ P4b loss is mainly semantic/answer-contract risk, not execution failure. All 9 MACT-only rows used high-risk MyAgent routing with strong verification, but several wrong answers came from target-column selection, surface normalization, count semantics, or conflict-gate rejection of a better candidate.",
            "patent_implication": "This supports the patent framing that selective risk collaboration needs a bounded repel/override layer plus deterministic semantic audits. The next evidence should be targeted WTQ diagnostics and fine-grained ablation, not blind Gate-100/full200 expansion.",
            "next_priority": "Run or implement targeted WTQ checks for listed-after target columns, experiment-number target selection, overtime marker parsing, entity surface cleanup, and verifier override on parenthetical negators.",
        },
    }


def write_markdown(report: dict[str, Any], path: Path) -> None:
    lines = [
        "# P4b WTQ Discordant Diagnosis",
        "",
        f"Run dir: `{report['run_dir']}`",
        "",
        "This report diagnoses the WTQ new-seed Gate-50 paired comparison where MyAgent scored `37/50` and MACT scored `43/50`.",
        "It is generated from frozen P4b artifacts without starting a model.",
        "",
        "## Method",
        "",
        f"- MyAgent rows: `{report['method']['myagent_rows']}`",
        f"- MACT rows: `{report['method']['mact_rows']}`",
        f"- Evaluation module: `{report['method']['eval_module']}`",
        "- Correctness: recomputed with the same WTQ denotation metric used by `evaluate_results.py`.",
        "",
        "## Pair Confusion",
        "",
        "| bucket | count |",
        "|---|---:|",
    ]
    for key in ("both_correct", "myagent_only", "mact_only", "both_wrong"):
        lines.append(f"| {key} | {report['confusion'].get(key, 0)} |")

    lines += [
        "",
        "## Root-Cause Buckets",
        "",
        "| category | count |",
        "|---|---:|",
    ]
    for category, count in sorted(report["categories"].items()):
        lines.append(f"| {category} | {count} |")

    comp = report["mact_only_compression"]
    lines += [
        "",
        "## Diagnosis",
        "",
        report["conclusion"]["primary_finding"],
        "",
        f"For the 9 MACT-only rows, average MyAgent compression ratio was `{comp['avg_compression_ratio']:.4f}` and `{comp['full_context_count']}/9` rows used effectively full-row context. This means the main WTQ gap is not a simple case of missing table rows.",
        "",
        "The most actionable MACT-only causes are answer target/surface contract errors, deterministic row-neighbor shortcut targeting, explicit marker parsing, count semantics, and conflict-gate behavior when a verifier candidate is better than the code candidate.",
        "",
        "## Discordant Rows",
        "",
        "| group | id | category | question | gold | MyAgent | MACT | cause | next action |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    group_order = {"mact_only": 0, "myagent_only": 1, "both_wrong": 2}
    records = sorted(report["records"], key=lambda item: (group_order.get(item["group"], 9), item["id"]))
    for record in records:
        lines.append(
            "| "
            + " | ".join(
                [
                    md_escape(record["group"]),
                    md_escape(record["id"]),
                    md_escape(record["category"]),
                    md_escape(record["question"]),
                    md_escape(record["gold"]),
                    md_escape(record["myagent_prediction"]),
                    md_escape(record["mact_prediction"]),
                    md_escape(record["cause"]),
                    md_escape(record["next_action"]),
                ]
            )
            + " |"
        )

    lines += [
        "",
        "## Patent Implication",
        "",
        report["conclusion"]["patent_implication"],
        "",
        "## Next Priority",
        "",
        report["conclusion"]["next_priority"],
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--myagent-root", default="/home/ubuntu/lzz/MyAgent")
    args = parser.parse_args()
    report = build_report(Path(args.myagent_root))
    json_path = RUN_DIR / "p4b_wtq_discordant_diagnosis.json"
    md_path = RUN_DIR / "p4b_wtq_discordant_diagnosis.md"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_markdown(report, md_path)
    print(f"wrote {json_path}")
    print(f"wrote {md_path}")


if __name__ == "__main__":
    main()
