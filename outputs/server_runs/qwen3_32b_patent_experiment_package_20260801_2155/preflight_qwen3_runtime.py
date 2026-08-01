#!/usr/bin/env python3
"""Record Qwen3 runtime readiness before launching patent-evidence queues."""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parent
DEFAULT_ENDPOINTS = "http://127.0.0.1:8000/v1,http://127.0.0.1:8001/v1"
DEFAULT_GPU_IDS = "6,7"


def run_cmd(command: list[str], timeout: int = 10) -> dict[str, Any]:
    try:
        completed = subprocess.run(
            command,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
        )
        return {
            "command": command,
            "returncode": completed.returncode,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
            "timeout": False,
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "command": command,
            "returncode": None,
            "stdout": exc.stdout or "",
            "stderr": exc.stderr or "",
            "timeout": True,
        }


def parse_gpu_csv(text: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    reader = csv.reader(line for line in text.splitlines() if line.strip())
    for row in reader:
        if len(row) < 5:
            continue
        try:
            rows.append(
                {
                    "index": int(row[0].strip()),
                    "name": row[1].strip(),
                    "memory_used_mib": int(row[2].strip()),
                    "memory_total_mib": int(row[3].strip()),
                    "utilization_gpu_percent": int(row[4].strip()),
                }
            )
        except ValueError:
            continue
    return rows


def parse_compute_apps(text: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    reader = csv.reader(line for line in text.splitlines() if line.strip())
    for row in reader:
        if len(row) < 4:
            continue
        rows.append(
            {
                "gpu_uuid": row[0].strip(),
                "pid": row[1].strip(),
                "process_name": row[2].strip(),
                "used_memory_mib": row[3].strip(),
            }
        )
    return rows


def endpoint_health(endpoint: str, api_key: str) -> dict[str, Any]:
    endpoint = endpoint.rstrip("/")
    result = run_cmd(
        [
            "curl",
            "-sS",
            "--max-time",
            "5",
            "-H",
            f"Authorization: Bearer {api_key}",
            f"{endpoint}/models",
        ],
        timeout=8,
    )
    return {
        "endpoint": endpoint,
        "models_url": f"{endpoint}/models",
        "healthy": result["returncode"] == 0,
        "returncode": result["returncode"],
        "stderr": result["stderr"].strip(),
        "stdout_preview": result["stdout"][:500],
    }


def classify_readiness(
    *,
    endpoints: list[dict[str, Any]],
    gpus: list[dict[str, Any]],
    compute_apps: list[dict[str, Any]],
    target_gpu_ids: set[int],
) -> dict[str, Any]:
    healthy_endpoints = [item for item in endpoints if item["healthy"]]
    target_gpus = [gpu for gpu in gpus if gpu["index"] in target_gpu_ids]
    residual_target_gpus = [
        gpu
        for gpu in target_gpus
        if gpu["memory_used_mib"] >= 20_000 or gpu["utilization_gpu_percent"] >= 20
    ]
    compute_app_pids = [app.get("pid") for app in compute_apps if app.get("pid")]

    if healthy_endpoints:
        status = "ready_existing_endpoint"
        recommendation = "Use the queue script with the healthy endpoint list."
    elif residual_target_gpus and not compute_app_pids:
        status = "blocked_gpu_runtime_residual"
        recommendation = (
            "Do not start Qwen3 on the target GPUs yet. Ask the server owner to "
            "clear/reset the runtime or authorize another clean GPU pair."
        )
    elif residual_target_gpus:
        status = "blocked_visible_gpu_process"
        recommendation = "Inspect listed GPU processes before starting a new vLLM service."
    else:
        status = "start_service_required"
        recommendation = "Start Qwen3 vLLM on the target GPUs, then rerun this preflight."

    return {
        "status": status,
        "ready": status == "ready_existing_endpoint",
        "healthy_endpoint_count": len(healthy_endpoints),
        "target_gpu_ids": sorted(target_gpu_ids),
        "target_gpus": target_gpus,
        "residual_target_gpus": residual_target_gpus,
        "compute_app_pids": compute_app_pids,
        "recommendation": recommendation,
    }


def render_markdown(report: dict[str, Any]) -> str:
    readiness = report["readiness"]
    lines = [
        "# Qwen3 Runtime Preflight",
        "",
        f"Generated: `{report['generated_at_local']}`",
        "",
        "| item | value |",
        "|---|---|",
        f"| status | `{readiness['status']}` |",
        f"| ready | `{readiness['ready']}` |",
        f"| recommendation | {readiness['recommendation']} |",
        f"| endpoints | `{', '.join(item['endpoint'] for item in report['endpoints'])}` |",
        f"| target GPUs | `{', '.join(str(gpu) for gpu in readiness['target_gpu_ids'])}` |",
        "",
        "## Endpoint Health",
        "",
        "| endpoint | healthy | returncode | stderr |",
        "|---|---:|---:|---|",
    ]
    for item in report["endpoints"]:
        stderr = item["stderr"].replace("|", "\\|") or ""
        lines.append(
            f"| `{item['endpoint']}` | `{item['healthy']}` | `{item['returncode']}` | `{stderr}` |"
        )

    lines.extend(
        [
            "",
            "## GPU Snapshot",
            "",
            "| gpu | memory used MiB | memory total MiB | util % | name |",
            "|---:|---:|---:|---:|---|",
        ]
    )
    for gpu in report["gpus"]:
        lines.append(
            f"| {gpu['index']} | {gpu['memory_used_mib']} | {gpu['memory_total_mib']} | "
            f"{gpu['utilization_gpu_percent']} | {gpu['name']} |"
        )

    lines.extend(
        [
            "",
            "## GPU Process Evidence",
            "",
            f"Compute apps listed by `nvidia-smi`: `{len(report['compute_apps'])}`.",
            "",
        ]
    )
    if report["compute_apps"]:
        lines.extend(["| gpu uuid | pid | process | used memory MiB |", "|---|---:|---|---:|"])
        for app in report["compute_apps"]:
            lines.append(
                f"| `{app['gpu_uuid']}` | `{app['pid']}` | `{app['process_name']}` | "
                f"`{app['used_memory_mib']}` |"
            )
    else:
        lines.append("No compute apps were reported.")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument(
        "--endpoints",
        default=os.environ.get("VLLM_ENDPOINTS", DEFAULT_ENDPOINTS),
        help="Comma-separated OpenAI-compatible endpoint list.",
    )
    parser.add_argument(
        "--target-gpus",
        default=os.environ.get("TARGET_QWEN3_GPUS", DEFAULT_GPU_IDS),
        help="Comma-separated GPU ids intended for Qwen3.",
    )
    parser.add_argument("--api-key", default=os.environ.get("LOCAL_VLLM_API_KEY", "local-vllm-key-change-me"))
    parser.add_argument("--fail-if-not-ready", action="store_true")
    args = parser.parse_args()

    generated_at = dt.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
    stamp = dt.datetime.now().astimezone().strftime("%Y%m%d_%H%M%S")
    endpoints = [item.strip() for item in args.endpoints.split(",") if item.strip()]
    target_gpu_ids = {int(item.strip()) for item in args.target_gpus.split(",") if item.strip()}

    endpoint_reports = [endpoint_health(endpoint, args.api_key) for endpoint in endpoints]
    gpu_cmd = run_cmd(
        [
            "nvidia-smi",
            "--query-gpu=index,name,memory.used,memory.total,utilization.gpu",
            "--format=csv,noheader,nounits",
        ],
        timeout=10,
    )
    apps_cmd = run_cmd(
        [
            "nvidia-smi",
            "--query-compute-apps=gpu_uuid,pid,process_name,used_memory",
            "--format=csv,noheader,nounits",
        ],
        timeout=10,
    )
    pmon_cmd = run_cmd(["nvidia-smi", "pmon", "-c", "1"], timeout=10)
    process_cmd = run_cmd(
        [
            "bash",
            "-lc",
            "ps -eo pid,ppid,user,stat,etime,%cpu,%mem,cmd "
            "| rg 'vllm|api_server|run_sharded_tqa|run_mact|run_remaining_qwen3|Qwen3|qwen' || true",
        ],
        timeout=10,
    )

    gpus = parse_gpu_csv(gpu_cmd["stdout"])
    compute_apps = parse_compute_apps(apps_cmd["stdout"])
    readiness = classify_readiness(
        endpoints=endpoint_reports,
        gpus=gpus,
        compute_apps=compute_apps,
        target_gpu_ids=target_gpu_ids,
    )

    report = {
        "generated_at_local": generated_at,
        "package_dir": str(DEFAULT_OUTPUT_DIR),
        "inputs": {
            "endpoints": endpoints,
            "target_gpus": sorted(target_gpu_ids),
        },
        "endpoints": endpoint_reports,
        "gpus": gpus,
        "compute_apps": compute_apps,
        "commands": {
            "gpu_query": gpu_cmd,
            "compute_apps_query": apps_cmd,
            "pmon": pmon_cmd,
            "process_scan": process_cmd,
        },
        "readiness": readiness,
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    json_path = args.output_dir / f"qwen3_runtime_preflight_{stamp}.json"
    md_path = args.output_dir / f"qwen3_runtime_preflight_{stamp}_zh.md"
    latest_json = args.output_dir / "latest_qwen3_runtime_preflight.json"
    latest_md = args.output_dir / "latest_qwen3_runtime_preflight_zh.md"
    json_text = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    md_text = render_markdown(report)
    json_path.write_text(json_text, encoding="utf-8")
    md_path.write_text(md_text, encoding="utf-8")
    latest_json.write_text(json_text, encoding="utf-8")
    latest_md.write_text(md_text, encoding="utf-8")

    print(json.dumps({"json": str(json_path), "md": str(md_path), "readiness": readiness}, ensure_ascii=False, indent=2))
    if args.fail_if_not_ready and not readiness["ready"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
