#!/usr/bin/env python3
"""Build an E4 multi-model gate readiness audit for the patent package."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


PACKAGE_DIR = Path(__file__).resolve().parent
MYAGENT_ROOT = Path("/home/ubuntu/lzz/MyAgent")
MACT_ROOT = Path("/home/ubuntu/lzz/MACT")
READINESS_JSON = (
    MACT_ROOT
    / "outputs/server_runs/qwen3_32b_blind200_mact_full200_20260723/latest_experiment_readiness_audit.json"
)
READINESS_MD = (
    MACT_ROOT
    / "outputs/server_runs/qwen3_32b_blind200_mact_full200_20260723/latest_expert_evidence_summary.md"
)
MODEL_ROOTS = (
    Path("/home/ubuntu/models"),
    Path("/home/ubuntu/.cache/huggingface"),
    Path("/data"),
    Path("/mnt"),
)

sys.path.insert(0, str(MYAGENT_ROOT / "scripts/server"))
from audit_qwen3_experiment_state import build_audit, default_env_files  # noqa: E402


def run_command(args: list[str]) -> dict[str, Any]:
    result = subprocess.run(
        args,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return {
        "args": args,
        "returncode": result.returncode,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
    }


def gpu_snapshot() -> dict[str, Any]:
    query = run_command(
        [
            "nvidia-smi",
            "--query-gpu=index,memory.used,utilization.gpu",
            "--format=csv,noheader,nounits",
        ]
    )
    gpus = []
    if query["returncode"] == 0:
        for line in query["stdout"].splitlines():
            parts = [part.strip() for part in line.split(",")]
            if len(parts) != 3:
                continue
            index, memory_used, utilization = parts
            try:
                gpus.append(
                    {
                        "index": int(index),
                        "memory_used_mib": int(memory_used),
                        "utilization_gpu_percent": int(utilization),
                    }
                )
            except ValueError:
                continue
    default_pool = [gpu for gpu in gpus if gpu["index"] in {0, 1, 2, 3}]
    default_pool_available = bool(default_pool) and all(
        gpu["memory_used_mib"] <= 1024 and gpu["utilization_gpu_percent"] <= 5
        for gpu in default_pool
    )
    return {
        "query": query,
        "gpus": gpus,
        "default_pool": "0,1 -> 8000; 2,3 -> 8001",
        "default_pool_available_for_next_start": default_pool_available,
        "availability_rule": "All GPU 0-3 memory_used_mib <= 1024 and utilization <= 5.",
    }


def process_snapshot() -> dict[str, Any]:
    pattern = "[v]llm|[a]pi_server|[r]un_mact_one_by_one|[t]qa.py|[r]un_sharded_tqa|[r]un_seed_"
    result = run_command(["pgrep", "-af", pattern])
    matches = [line for line in result["stdout"].splitlines() if line.strip()]
    return {
        "pattern": pattern,
        "matches": matches,
        "visible_runner_or_model_processes": len(matches),
        "pgrep_returncode": result["returncode"],
    }


def build_report() -> dict[str, Any]:
    generated_at = dt.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
    audit = build_audit(
        myagent_root=MYAGENT_ROOT,
        mact_root=MACT_ROOT,
        model_roots=MODEL_ROOTS,
        env=os.environ,
        env_files=default_env_files(MYAGENT_ROOT),
    )
    readiness = audit["model_readiness"]
    has_candidate = bool(
        readiness.get("untested_local_model_paths")
        or readiness.get("api_provider_profiles")
        or readiness.get("api_keys_present")
    )
    decision = "candidate_available_prepare_gate" if has_candidate else "no_candidate_wait"
    return {
        "artifact_name": "e4_multimodel_gate_readiness_audit",
        "generated_at_local": generated_at,
        "purpose": "Decide whether E4 multi-model Gate-10/Gate-50 can start without rerunning known no-go models.",
        "source_readiness_audit_json": str(READINESS_JSON),
        "source_readiness_summary_md": str(READINESS_MD),
        "model_roots": [str(path) for path in MODEL_ROOTS],
        "decision": decision,
        "can_start_gate10_now": has_candidate,
        "model_readiness": readiness,
        "runtime_snapshot": {
            "gpu": gpu_snapshot(),
            "processes": process_snapshot(),
        },
        "policy": {
            "do_not_rerun_known_no_go_models": True,
            "known_tested_local_models": readiness.get("known_tested_local_models", []),
            "gate_funnel": "Gate-10 -> Gate-50 -> Gate-150 -> paired-200 only for candidates that pass each stage.",
        },
        "next_actions": [
            "If untested_local_model_paths becomes non-empty, run prepare_model_gate_run.py --readiness-audit <latest audit> and start Gate-10.",
            "If an API key appears, generate an API gate run with prepare_model_gate_run.py --backend api and run healthcheck_services.sh before Gate-10.",
            "If no candidates are present, keep E4 pending/no-candidate and do not consume GPU time on known no-go models.",
        ],
    }


def render_markdown(report: dict[str, Any]) -> str:
    readiness = report["model_readiness"]
    gpu = report["runtime_snapshot"]["gpu"]
    processes = report["runtime_snapshot"]["processes"]
    lines = [
        "# E4 Multi-Model Gate Readiness Audit",
        "",
        f"Generated: `{report['generated_at_local']}`",
        "",
        f"Decision: `{report['decision']}`.",
        "",
        "| item | value |",
        "|---|---|",
        f"| can start Gate-10 now | `{report['can_start_gate10_now']}` |",
        f"| local models discovered | `{len(readiness.get('local_models', []))}` |",
        f"| untested local models | `{len(readiness.get('untested_local_models', []))}` |",
        f"| API keys present | `{len(readiness.get('api_keys_present', []))}` |",
        f"| API provider profiles | `{len(readiness.get('api_provider_profiles', {}))}` |",
        f"| default GPU pool available | `{gpu['default_pool_available_for_next_start']}` |",
        f"| visible model/runner processes | `{processes['visible_runner_or_model_processes']}` |",
        "",
        "## Local Models",
        "",
        "| model | paths | status |",
        "|---|---|---|",
    ]
    untested = set(readiness.get("untested_local_models", []))
    local_model_paths = readiness.get("local_model_paths", {})
    for model in readiness.get("local_models", []):
        status = "untested_candidate" if model in untested else "known_tested_or_no_go"
        paths = "<br>".join(f"`{path}`" for path in local_model_paths.get(model, []))
        lines.append(f"| {model} | {paths} | `{status}` |")
    if not readiness.get("local_models"):
        lines.append("| none | n/a | `none` |")

    lines.extend(
        [
            "",
            "## API Readiness",
            "",
            f"- API keys present: `{readiness.get('api_keys_present', [])}`",
            f"- API provider profiles: `{sorted((readiness.get('api_provider_profiles') or {}).keys())}`",
            "",
            "## Runtime Snapshot",
            "",
            "| GPU | memory MiB | util % |",
            "|---:|---:|---:|",
        ]
    )
    for item in gpu["gpus"]:
        lines.append(
            f"| {item['index']} | {item['memory_used_mib']} | {item['utilization_gpu_percent']} |"
        )
    lines.extend(
        [
            "",
            f"Visible model/runner processes: `{processes['visible_runner_or_model_processes']}`.",
            "",
            "## Conclusion",
            "",
        ]
    )
    if report["can_start_gate10_now"]:
        lines.append("A new candidate is available. Prepare a Gate run before starting model services.")
    else:
        lines.append(
            "No E4 Gate-10 should start now: no untested local model path and no API provider profile are available. "
            "Keep E4 pending/no-candidate and avoid rerunning known no-go models."
        )
    lines.extend(["", "## Next Actions", ""])
    lines.extend(f"- {item}" for item in report["next_actions"])
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=PACKAGE_DIR)
    args = parser.parse_args()

    report = build_report()
    stamp = dt.datetime.now().astimezone().strftime("%Y%m%d_%H%M%S")
    json_path = args.output_dir / f"e4_multimodel_gate_readiness_audit_{stamp}.json"
    md_path = args.output_dir / f"e4_multimodel_gate_readiness_audit_{stamp}_zh.md"
    latest_json = args.output_dir / "latest_e4_multimodel_gate_readiness_audit.json"
    latest_md = args.output_dir / "latest_e4_multimodel_gate_readiness_audit_zh.md"
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
                "decision": report["decision"],
                "can_start_gate10_now": report["can_start_gate10_now"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
