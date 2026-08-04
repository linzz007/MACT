#!/usr/bin/env python3
"""Build a fine-grained mechanism ablation audit from frozen artifacts."""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from typing import Any


RUN_DIR = Path(__file__).resolve().parent
SUMMARY_DIR = RUN_DIR / "summary"
MACT_ROOT = Path("/home/ubuntu/lzz/MACT")

MECHANISM_MATRIX = MACT_ROOT / (
    "outputs/server_runs/qwen3_32b_policy_v6b_patent_mechanism_evidence_20260801_2222/"
    "patent_mechanism_evidence_matrix.json"
)
MECHANISM_MATRIX_MD = MECHANISM_MATRIX.with_suffix(".md")
S2_BASELINE = MACT_ROOT / (
    "outputs/server_runs/qwen3_32b_policy_v6b_e3_guard_validation_current_baseline_20260804_1142/"
    "summary/e3_guard_validation_current_baseline_summary.json"
)
S2_BASELINE_MD = S2_BASELINE.with_suffix(".md")
S2_AFTER_GUARD = MACT_ROOT / (
    "outputs/server_runs/qwen3_32b_policy_v6b_e3_guard_validation_after_guard_20260804_1203/"
    "summary/e3_guard_validation_after_guard_summary.json"
)
S2_AFTER_GUARD_MD = S2_AFTER_GUARD.with_suffix(".md")
S5_REPLAY = MACT_ROOT / (
    "outputs/server_runs/qwen3_32b_policy_v6c_e3_s5_crt_tiebreaker_diag_20260804_2225/"
    "summary/s5_crt_canonicalizer_replay_summary.json"
)
S5_REPLAY_MD = S5_REPLAY.with_suffix(".md")
S5_AFFECTED = MACT_ROOT / (
    "outputs/server_runs/qwen3_32b_policy_v6c_e3_s5_crt_tiebreaker_diag_20260804_2225/"
    "summary/s5_affected_slice_real_rerun_summary.json"
)
S5_AFFECTED_MD = S5_AFFECTED.with_suffix(".md")
S5_FINAL = MACT_ROOT / (
    "outputs/server_runs/qwen3_32b_policy_v6c_e3_s5_crt_tiebreaker_diag_20260804_2225/"
    "summary/e3_s5_final_combined_summary.json"
)
S5_FINAL_MD = S5_FINAL.with_suffix(".md")
E4_READINESS = MACT_ROOT / (
    "outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/"
    "latest_e4_multimodel_gate_readiness_audit.json"
)
E4_READINESS_MD = E4_READINESS.with_name("latest_e4_multimodel_gate_readiness_audit_zh.md")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def ratio(value: float | int | None) -> float | None:
    if value is None:
        return None
    return round(float(value), 4)


def aggregate_guard_delta(
    baseline: dict[str, Any],
    after_guard: dict[str, Any],
) -> dict[str, Any]:
    base = baseline["aggregate"]
    after = after_guard["aggregate"]
    return {
        "rows": after["rows"],
        "baseline_representative_recovered": base["representative_recovered"],
        "after_guard_representative_recovered": after["representative_recovered"],
        "representative_total": after["representative_total"],
        "representative_recovery_delta": after["representative_recovered"]
        - base["representative_recovered"],
        "baseline_no_harm_correct": base["no_harm_correct"],
        "after_guard_no_harm_correct": after["no_harm_correct"],
        "no_harm_total": after["no_harm_total"],
        "no_harm_delta": after["no_harm_correct"] - base["no_harm_correct"],
        "baseline_failed_missing": [base["failed"], base["missing"]],
        "after_guard_failed_missing": [after["failed"], after["missing"]],
        "baseline_token_ratio": base["token_ratio_to_mact_full200_weighted"],
        "after_guard_token_ratio": after["token_ratio_to_mact_full200_weighted"],
        "token_ratio_delta": after["token_ratio_to_mact_full200_weighted"]
        - base["token_ratio_to_mact_full200_weighted"],
        "baseline_avg_total_tokens": base["avg_total_tokens"],
        "after_guard_avg_total_tokens": after["avg_total_tokens"],
        "avg_total_tokens_delta": after["avg_total_tokens"] - base["avg_total_tokens"],
        "baseline_avg_elapsed_seconds": base["avg_elapsed_seconds"],
        "after_guard_avg_elapsed_seconds": after["avg_elapsed_seconds"],
        "avg_elapsed_seconds_delta": after["avg_elapsed_seconds"] - base["avg_elapsed_seconds"],
    }


def dataset_guard_deltas(
    baseline: dict[str, Any],
    after_guard: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    for dataset, base in baseline["datasets"].items():
        after = after_guard["datasets"][dataset]
        rows[dataset] = {
            "rows": after["input_rows"],
            "baseline_representative_recovered": base["representative_recovered"],
            "after_guard_representative_recovered": after["representative_recovered"],
            "representative_total": after["representative_total"],
            "representative_recovery_delta": after["representative_recovered"]
            - base["representative_recovered"],
            "baseline_no_harm_correct": base["no_harm_correct"],
            "after_guard_no_harm_correct": after["no_harm_correct"],
            "no_harm_total": after["no_harm_total"],
            "no_harm_delta": after["no_harm_correct"] - base["no_harm_correct"],
            "baseline_token_ratio": base["token_ratio_to_mact_full200"],
            "after_guard_token_ratio": after["token_ratio_to_mact_full200"],
            "token_ratio_delta": after["token_ratio_to_mact_full200"]
            - base["token_ratio_to_mact_full200"],
        }
    return rows


def category_guard_deltas(
    baseline: dict[str, Any],
    after_guard: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    categories: dict[str, dict[str, Any]] = {}
    for category, after in after_guard["category_results"].items():
        base = baseline["category_results"].get(category, {})
        categories[category] = {
            "rows": after["rows"],
            "baseline_correct": base.get("correct"),
            "after_guard_correct": after["correct"],
            "correct_delta": after["correct"] - int(base.get("correct", 0)),
            "baseline_representative_recovered": base.get("representative_recovered"),
            "after_guard_representative_recovered": after["representative_recovered"],
            "representative_recovery_delta": after["representative_recovered"]
            - int(base.get("representative_recovered", 0)),
            "baseline_no_harm_retained": base.get("no_harm_retained"),
            "after_guard_no_harm_retained": after["no_harm_retained"],
            "no_harm_delta": after["no_harm_retained"] - int(base.get("no_harm_retained", 0)),
        }
    return categories


def coarse_summary(matrix: dict[str, Any]) -> dict[str, dict[str, Any]]:
    variants = matrix["coarse_ablation"]["variants"]
    compact: dict[str, dict[str, Any]] = {}
    for name, item in variants.items():
        per_dataset = {}
        for dataset, ds in item["per_dataset"].items():
            per_dataset[dataset] = {
                "variant_correct": ds["variant_correct"],
                "current_correct": ds["current_correct"],
                "delta_vs_current": ds["delta_vs_current"],
                "token_ratio_vs_current": ds["token_ratio_vs_current"],
                "failed": ds["failed"],
                "missing": ds["missing"],
            }
        compact[name] = {
            "rows": item["rows"],
            "variant_correct": item["correct"],
            "current_reference_correct": item["current_reference_correct"],
            "delta_vs_current": item["delta_vs_current"],
            "token_ratio_vs_current": item["token_ratio_vs_current"],
            "token_ratio_vs_mact": item["token_ratio_vs_mact"],
            "per_dataset": per_dataset,
        }
    return compact


def s5_canonicalization_summary(
    replay: dict[str, Any],
    affected: dict[str, Any],
    final: dict[str, Any],
) -> dict[str, Any]:
    flips = replay["overall"]["flips"]
    correct_to_wrong = sum(1 for row in flips if row["original_correct"] and not row["patched_correct"])
    wrong_to_correct = sum(1 for row in flips if not row["original_correct"] and row["patched_correct"])
    old = affected["systems"]["old_myagent"]
    new = affected["systems"]["new_myagent_s5"]
    mact = affected["systems"]["mact"]
    crt = final["datasets"]["crt"]
    return {
        "replay_rows": replay["overall"]["rows"],
        "replay_myagent_correct": replay["overall"]["myagent_correct"],
        "replay_mact_correct": replay["overall"]["mact_correct"],
        "replay_delta_correct": replay["overall"]["delta_correct"],
        "replay_flip_count": len(flips),
        "replay_wrong_to_correct": wrong_to_correct,
        "replay_correct_to_wrong": correct_to_wrong,
        "affected_slice_rows": new["rows"],
        "affected_old_myagent_correct": old["correct"],
        "affected_new_myagent_correct": new["correct"],
        "affected_mact_correct": mact["correct"],
        "affected_delta_vs_old": new["correct"] - old["correct"],
        "affected_delta_vs_mact": new["correct"] - mact["correct"],
        "affected_failed_missing": [new["num_failed_exec"], new["num_missing_answer"]],
        "full_crt_rows": crt["rows"],
        "full_crt_myagent_correct": crt["myagent_correct"],
        "full_crt_mact_correct": crt["mact_correct"],
        "full_crt_delta_correct": crt["delta_correct"],
        "full_crt_token_ratio": crt["token_ratio_myagent_to_mact"],
        "full_crt_failed_missing": [crt["myagent_failed"], crt["myagent_missing"]],
    }


def build_report() -> dict[str, Any]:
    matrix = read_json(MECHANISM_MATRIX)
    baseline = read_json(S2_BASELINE)
    after_guard = read_json(S2_AFTER_GUARD)
    s5_replay = read_json(S5_REPLAY)
    s5_affected = read_json(S5_AFFECTED)
    s5_final = read_json(S5_FINAL)
    e4 = read_json(E4_READINESS)
    coarse = coarse_summary(matrix)
    guard_delta = aggregate_guard_delta(baseline, after_guard)
    s5 = s5_canonicalization_summary(s5_replay, s5_affected, s5_final)
    offline = matrix["offline_attribution"]["datasets"]
    decision = (
        "fine_grained_mechanism_evidence_ready_for_qwen3_patent_scope_"
        "with_evidence_retention_boundary_and_e4_pending"
    )
    return {
        "artifact_name": "fine_grained_mechanism_ablation_audit",
        "generated_at_local": dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S CST"),
        "run_dir": str(RUN_DIR),
        "scope": (
            "Frozen-artifact audit that consolidates run-based coarse ablations, "
            "fresh S2 guard before/after evidence, and S5 CRT canonicalizer replay. "
            "No model run is started by this artifact."
        ),
        "decision": decision,
        "source_paths": {
            "mechanism_matrix_json": str(MECHANISM_MATRIX),
            "mechanism_matrix_md": str(MECHANISM_MATRIX_MD),
            "s2_baseline_json": str(S2_BASELINE),
            "s2_baseline_md": str(S2_BASELINE_MD),
            "s2_after_guard_json": str(S2_AFTER_GUARD),
            "s2_after_guard_md": str(S2_AFTER_GUARD_MD),
            "s5_replay_json": str(S5_REPLAY),
            "s5_replay_md": str(S5_REPLAY_MD),
            "s5_affected_json": str(S5_AFFECTED),
            "s5_affected_md": str(S5_AFFECTED_MD),
            "s5_final_json": str(S5_FINAL),
            "s5_final_md": str(S5_FINAL_MD),
            "e4_readiness_json": str(E4_READINESS),
            "e4_readiness_md": str(E4_READINESS_MD),
        },
        "full200_anchor": matrix["full200_anchor"],
        "coarse_ablation": coarse,
        "s2_guard_fresh_delta": guard_delta,
        "s2_guard_dataset_deltas": dataset_guard_deltas(baseline, after_guard),
        "s2_guard_category_deltas": category_guard_deltas(baseline, after_guard),
        "s5_crt_scalar_canonicalization": s5,
        "mechanism_claim_readiness": {
            "risk_collaboration_and_persuasion_back": {
                "status": "run_based_and_fresh_supported",
                "evidence": [
                    "no_strong_verification drops the diagnostic Gate-50 slice by 8/150 vs current.",
                    "WTQ accounts for 7/8 of that coarse loss on the diagnostic slice.",
                    "WTQ offline attribution tags 24/25 gain-vs-old rows with strong_verification.",
                    "S2 fresh semantic guards improve representative recovery from 4/12 to 8/12 while no-harm improves from 17/18 to 18/18.",
                ],
                "boundary": (
                    "The coarse no_strong_verification and legacy variants are identical on this slice, "
                    "so this supports module-level persuasion-back/risk-collaboration contribution, "
                    "not each individual verifier rule independently."
                ),
            },
            "deterministic_audit": {
                "status": "run_based_strong",
                "evidence": [
                    "no_deterministic_shortcuts drops the diagnostic Gate-50 slice by 15/150 vs current.",
                    "TabFact drops by 9/50 and CRT drops by 7/50 without deterministic shortcuts.",
                    "TabFact no_deterministic_shortcuts token usage is 1.4487x current on the diagnostic slice.",
                    "S2 after-guard validates targeted deterministic/semantic guards on a fresh 30-row affected/no-harm slice.",
                ],
                "boundary": "WTQ deterministic shortcuts are mixed in the coarse slice; strongest evidence is TabFact and CRT.",
            },
            "evidence_retention": {
                "status": "associative_plus_fresh_guard_supported",
                "evidence": [
                    f"WTQ gain-vs-old attribution tags {offline['wtq']['gain_vs_old']['family_counts'].get('evidence_retention', 0)}/{offline['wtq']['gain_vs_old']['count']} rows with evidence_retention.",
                    f"TabFact gain-vs-old attribution tags {offline['tabfact']['gain_vs_old']['family_counts'].get('evidence_retention', 0)}/{offline['tabfact']['gain_vs_old']['count']} rows with evidence_retention.",
                    f"CRT current-only-vs-MACT attribution tags {offline['crt']['current_only_vs_mact']['family_counts'].get('evidence_retention', 0)}/{offline['crt']['current_only_vs_mact']['count']} rows with evidence_retention.",
                    "S2 no-harm improves from 17/18 to 18/18 after targeted guards, indicating selective retention/guard changes did not harm the matched control rows.",
                ],
                "boundary": (
                    "There is no standalone no_evidence_retention run-based ablation yet. "
                    "Use this as supporting evidence, not as a sole causal proof if claims need narrow evidence-retention isolation."
                ),
            },
            "crt_scalar_output_canonicalization": {
                "status": "patch_replay_and_fresh_supported",
                "evidence": [
                    "S5 replay changes 3 CRT outputs, with 2 wrong-to-correct and 0 correct-to-wrong.",
                    "S5 affected-slice fresh rerun improves new MyAgent to 16/25 vs old MyAgent 12/25 and MACT 12/25.",
                    "S5 full CRT100 fresh closes the strict boundary at 65/100 vs MACT 62/100.",
                ],
                "boundary": "This is output normalization/scalar canonicalization, not a new broad reasoning module.",
            },
            "budget_control": {
                "status": "supported",
                "evidence": [
                    f"Frozen full200 token ratio current/MACT is {matrix['full200_anchor']['token_ratio_current_over_mact']:.4f}.",
                    f"S5 paired multi-seed overall token ratio is {s5_final['overall']['token_ratio_myagent_to_mact']:.4f}.",
                    "S2 after-guard reduces weighted token ratio from 0.6975 to 0.6104 while improving recovery/no-harm.",
                ],
                "boundary": "CRT token savings are weaker than WTQ/TabFact; use aggregate and per-dataset ratios explicitly.",
            },
        },
        "remaining_boundaries": {
            "e4_multimodel_gate": {
                "decision": e4.get("decision"),
                "can_start_gate10_now": e4.get("can_start_gate10_now"),
                "untested_local_models": e4.get("untested_local_models", []),
                "api_keys_present": e4.get("api_keys_present", []),
                "boundary": "No new model/API candidate exists, so Gate-10 should not start.",
            },
            "fine_grained_evidence_retention_ablation": (
                "Optional only if claim drafting requires standalone isolation of evidence retention. "
                "Current evidence is associative plus fresh no-harm/guard support."
            ),
        },
    }


def write_markdown(report: dict[str, Any]) -> str:
    coarse = report["coarse_ablation"]
    guard = report["s2_guard_fresh_delta"]
    s5 = report["s5_crt_scalar_canonicalization"]
    lines: list[str] = []
    lines.append("# Fine-grained Mechanism Ablation Audit")
    lines.append("")
    lines.append(f"Generated: `{report['generated_at_local']}`")
    lines.append("")
    lines.append(f"Decision: `{report['decision']}`")
    lines.append("")
    lines.append(report["scope"])
    lines.append("")
    lines.append("## Key Conclusion")
    lines.append("")
    lines.append(
        "The Qwen3 patent-scope mechanism evidence is strong enough to draft around "
        "selective risk collaboration / persuasion-back, deterministic audit, CRT scalar "
        "canonicalization, and budget control. Evidence-retention can be cited as supporting "
        "evidence with an explicit boundary because a standalone no-evidence-retention "
        "causal ablation has not been run."
    )
    lines.append("")
    lines.append("## Run-based Coarse Ablation")
    lines.append("")
    lines.append("| variant | correct | current ref | delta vs current | token/current | WTQ delta | TabFact delta | CRT delta |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|")
    for name in ("legacy", "no_strong_verification", "no_deterministic_shortcuts"):
        item = coarse[name]
        lines.append(
            "| {name} | {correct}/{rows} | {current}/{rows} | {delta:+d} | {token:.4f} | {wtq:+d} | {tabfact:+d} | {crt:+d} |".format(
                name=name,
                correct=item["variant_correct"],
                rows=item["rows"],
                current=item["current_reference_correct"],
                delta=item["delta_vs_current"],
                token=item["token_ratio_vs_current"],
                wtq=item["per_dataset"]["wtq"]["delta_vs_current"],
                tabfact=item["per_dataset"]["tabfact"]["delta_vs_current"],
                crt=item["per_dataset"]["crt"]["delta_vs_current"],
            )
        )
    lines.append("")
    lines.append("Interpretation:")
    lines.append("")
    lines.append("- `no_strong_verification` loses `8/150`, concentrated in WTQ `-7/50`; this is the cleanest run-based evidence for risk collaboration / persuasion-back.")
    lines.append("- `no_deterministic_shortcuts` loses `15/150`, with TabFact `-9/50` and CRT `-7/50`; TabFact token/current rises to `1.4487` in the source artifact.")
    lines.append("- These ablations are disagreement-enriched diagnostic slices, so they support mechanism contribution rather than random-seed generalization by themselves.")
    lines.append("")
    lines.append("## Fresh S2 Guard Before/After")
    lines.append("")
    lines.append("| metric | baseline | after guard | delta |")
    lines.append("|---|---:|---:|---:|")
    lines.append(
        f"| representative recovered | {guard['baseline_representative_recovered']}/{guard['representative_total']} | "
        f"{guard['after_guard_representative_recovered']}/{guard['representative_total']} | "
        f"{guard['representative_recovery_delta']:+d} |"
    )
    lines.append(
        f"| no-harm correct | {guard['baseline_no_harm_correct']}/{guard['no_harm_total']} | "
        f"{guard['after_guard_no_harm_correct']}/{guard['no_harm_total']} | {guard['no_harm_delta']:+d} |"
    )
    lines.append(
        f"| failed/missing | {guard['baseline_failed_missing'][0]}/{guard['baseline_failed_missing'][1]} | "
        f"{guard['after_guard_failed_missing'][0]}/{guard['after_guard_failed_missing'][1]} | 0 |"
    )
    lines.append(
        f"| weighted token ratio | {guard['baseline_token_ratio']:.4f} | "
        f"{guard['after_guard_token_ratio']:.4f} | {guard['token_ratio_delta']:.4f} |"
    )
    lines.append(
        f"| avg elapsed seconds | {guard['baseline_avg_elapsed_seconds']:.2f} | "
        f"{guard['after_guard_avg_elapsed_seconds']:.2f} | {guard['avg_elapsed_seconds_delta']:.2f} |"
    )
    lines.append("")
    lines.append("| dataset | representative delta | no-harm delta | token ratio baseline -> after |")
    lines.append("|---|---:|---:|---:|")
    for dataset, item in report["s2_guard_dataset_deltas"].items():
        lines.append(
            f"| {dataset} | {item['representative_recovery_delta']:+d} | {item['no_harm_delta']:+d} | "
            f"{item['baseline_token_ratio']:.4f} -> {item['after_guard_token_ratio']:.4f} |"
        )
    lines.append("")
    lines.append("## S5 CRT Scalar Canonicalization")
    lines.append("")
    lines.append("| evidence | result |")
    lines.append("|---|---:|")
    lines.append(f"| replay rows | {s5['replay_rows']} |")
    lines.append(
        f"| replay MyAgent vs MACT | {s5['replay_myagent_correct']}/{s5['replay_rows']} vs "
        f"{s5['replay_mact_correct']}/{s5['replay_rows']} |"
    )
    lines.append(f"| replay flips | {s5['replay_flip_count']} total; {s5['replay_wrong_to_correct']} wrong-to-correct; {s5['replay_correct_to_wrong']} correct-to-wrong |")
    lines.append(
        f"| affected-slice fresh | new {s5['affected_new_myagent_correct']}/{s5['affected_slice_rows']} vs "
        f"old {s5['affected_old_myagent_correct']}/{s5['affected_slice_rows']} vs MACT {s5['affected_mact_correct']}/{s5['affected_slice_rows']} |"
    )
    lines.append(
        f"| full CRT100 fresh | MyAgent {s5['full_crt_myagent_correct']}/{s5['full_crt_rows']} vs "
        f"MACT {s5['full_crt_mact_correct']}/{s5['full_crt_rows']}; token ratio {s5['full_crt_token_ratio']:.4f} |"
    )
    lines.append("")
    lines.append("## Claim Readiness")
    lines.append("")
    lines.append("| mechanism | status | patent-use boundary |")
    lines.append("|---|---|---|")
    for name, item in report["mechanism_claim_readiness"].items():
        lines.append(f"| {name} | `{item['status']}` | {item['boundary']} |")
    lines.append("")
    lines.append("## Remaining Boundaries")
    lines.append("")
    e4 = report["remaining_boundaries"]["e4_multimodel_gate"]
    lines.append(
        f"- E4 multi-model gate remains `{e4['decision']}`; can_start_gate10_now=`{e4['can_start_gate10_now']}`, "
        f"untested_local_models=`{len(e4['untested_local_models'])}`, api_keys_present=`{len(e4['api_keys_present'])}`."
    )
    lines.append(f"- {report['remaining_boundaries']['fine_grained_evidence_retention_ablation']}")
    lines.append("")
    lines.append("## Source Artifacts")
    lines.append("")
    for key, path in report["source_paths"].items():
        lines.append(f"- `{key}`: `{path}`")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    SUMMARY_DIR.mkdir(parents=True, exist_ok=True)
    report = build_report()
    (SUMMARY_DIR / "fine_grained_mechanism_ablation_audit.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (SUMMARY_DIR / "fine_grained_mechanism_ablation_audit.md").write_text(
        write_markdown(report),
        encoding="utf-8",
    )
    print(json.dumps({"decision": report["decision"], "run_dir": str(RUN_DIR)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
