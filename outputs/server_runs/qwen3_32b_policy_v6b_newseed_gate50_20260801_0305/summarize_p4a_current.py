#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

RUN_DIR = Path(__file__).resolve().parent
MODEL = "qwen3-32b-local"
DATASETS = ["wtq", "tabfact", "crt"]
MACT_AVG = {"wtq": 10508.03, "tabfact": 10830.825, "crt": 12809.985}
THRESHOLDS = {"wtq": 35, "tabfact": 45, "crt": 30}

def count_jsonl(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(1 for line in path.open(encoding="utf-8") if line.strip())

def load_json(path: Path):
    with path.open(encoding="utf-8") as f:
        return json.load(f)

rows = {}
overall_correct = 0
overall_eval_rows = 0
overall_tokens_num = 0.0
overall_tokens_den = 0.0
overall_elapsed_num = 0.0
for dataset in DATASETS:
    input_path = RUN_DIR / "input" / f"{dataset}_newseed_gate50.jsonl"
    merged_path = RUN_DIR / "myagent_current" / "merged" / f"{dataset}_{MODEL}.jsonl"
    eval_path = RUN_DIR / "myagent_current" / "eval" / f"{dataset}_{MODEL}_eval.json"
    item = {
        "input_rows": count_jsonl(input_path),
        "merged_rows": count_jsonl(merged_path),
        "eval_path": str(eval_path),
        "merged_path": str(merged_path),
    }
    if eval_path.exists():
        ev = load_json(eval_path)
        eval_rows = int(ev.get("num_samples") or 0)
        with_gold = int(ev.get("num_with_gold") or eval_rows or 0)
        correct = round(float(ev.get("primary_accuracy") or 0.0) * with_gold)
        avg_tokens = float(ev.get("avg_total_tokens") or 0.0)
        avg_elapsed = float(ev.get("avg_elapsed_seconds") or 0.0)
        token_ratio = avg_tokens / MACT_AVG[dataset] if MACT_AVG[dataset] else None
        item.update({
            "eval_rows": eval_rows,
            "num_with_gold": with_gold,
            "correct": correct,
            "accuracy": float(ev.get("primary_accuracy") or 0.0),
            "avg_total_tokens": avg_tokens,
            "mact_avg_tokens_reference": MACT_AVG[dataset],
            "token_ratio_to_mact_full200": token_ratio,
            "avg_elapsed_seconds": avg_elapsed,
            "num_failed_exec": int(ev.get("num_failed_exec") or 0),
            "num_missing_answer": int(ev.get("num_missing_answer") or 0),
            "num_em_mismatch": int(ev.get("num_em_mismatch") or 0),
        })
        item["passed_p4a_dataset_gate"] = all([
            item["input_rows"] == 50,
            item["merged_rows"] == 50,
            item["eval_rows"] == 50,
            item["num_failed_exec"] == 0,
            item["num_missing_answer"] == 0,
            token_ratio is not None and token_ratio < 1.0,
            correct >= THRESHOLDS[dataset],
        ])
        overall_correct += correct
        overall_eval_rows += with_gold
        overall_tokens_num += avg_tokens * eval_rows
        overall_tokens_den += MACT_AVG[dataset] * eval_rows
        overall_elapsed_num += avg_elapsed * eval_rows
    else:
        item.update({
            "eval_rows": 0,
            "correct": 0,
            "accuracy": 0.0,
            "avg_total_tokens": 0.0,
            "token_ratio_to_mact_full200": None,
            "avg_elapsed_seconds": 0.0,
            "num_failed_exec": None,
            "num_missing_answer": None,
            "passed_p4a_dataset_gate": False,
        })
    rows[dataset] = item

summary = {
    "run_dir": str(RUN_DIR),
    "stage": "P4a current new-seed Gate-50",
    "model": MODEL,
    "datasets": rows,
    "overall": {
        "correct": overall_correct,
        "rows": overall_eval_rows,
        "accuracy": overall_correct / overall_eval_rows if overall_eval_rows else 0.0,
        "avg_total_tokens_weighted": overall_tokens_num / overall_eval_rows if overall_eval_rows else 0.0,
        "token_ratio_to_mact_full200_weighted": overall_tokens_num / overall_tokens_den if overall_tokens_den else None,
        "avg_elapsed_seconds_weighted": overall_elapsed_num / overall_eval_rows if overall_eval_rows else 0.0,
    },
    "decision": "p4b_candidate" if all(rows[d]["passed_p4a_dataset_gate"] for d in DATASETS) else "stop_or_inspect",
}
json_path = RUN_DIR / "p4a_current_gate50_summary.json"
json_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

lines = [
    "# P4a Current New-Seed Gate-50 Summary",
    "",
    f"Run dir: `{RUN_DIR}`",
    "",
    "| Dataset | Rows input/merged/eval | Correct | Accuracy | Token Ratio vs MACT full200 | Avg Tokens | Avg Elapsed s | Failed | Missing | Gate |",
    "|---|---:|---:|---:|---:|---:|---:|---:|---:|---|",
]
for dataset in DATASETS:
    r = rows[dataset]
    ratio = r.get("token_ratio_to_mact_full200")
    lines.append(
        f"| {dataset} | {r['input_rows']}/{r['merged_rows']}/{r.get('eval_rows', 0)} | "
        f"{r.get('correct', 0)}/50 | {r.get('accuracy', 0.0):.4f} | "
        f"{ratio:.4f} | {r.get('avg_total_tokens', 0.0):.1f} | "
        f"{r.get('avg_elapsed_seconds', 0.0):.2f} | {r.get('num_failed_exec')} | "
        f"{r.get('num_missing_answer')} | {'pass' if r.get('passed_p4a_dataset_gate') else 'inspect'} |"
        if ratio is not None else
        f"| {dataset} | {r['input_rows']}/{r['merged_rows']}/{r.get('eval_rows', 0)} | 0/50 | 0.0000 | n/a | 0.0 | 0.00 | n/a | n/a | inspect |"
    )
lines += [
    "",
    f"Decision: `{summary['decision']}`",
    "",
    "P4a is a current-only stability gate. It does not prove new-seed superiority over MACT until P4b paired MACT is run on the same IDs.",
]
(RUN_DIR / "p4a_current_gate50_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print(json.dumps(summary, ensure_ascii=False, indent=2))
