#!/usr/bin/env python3
"""Build SHA256 checksums for patent-package files and referenced evidence."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable


WORKSPACE_ROOT = Path("/home/ubuntu/lzz")
PACKAGE_DIR = Path(__file__).resolve().parent
MANIFEST_PATH = PACKAGE_DIR / "evidence_manifest.json"
EXCLUDED_PACKAGE_PREFIXES = (
    "SHA256SUMS",
    "patent_package_checksums_",
    "latest_patent_package_checksums",
)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def workspace_relative(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(WORKSPACE_ROOT.resolve()))
    except ValueError:
        return str(path.resolve())


def iter_manifest_strings(value: Any, prefix: str = "") -> Iterable[tuple[str, str]]:
    if isinstance(value, dict):
        for key, item in value.items():
            yield from iter_manifest_strings(item, f"{prefix}.{key}" if prefix else str(key))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from iter_manifest_strings(item, f"{prefix}[{index}]")
    elif isinstance(value, str):
        yield prefix, value


def is_candidate_path(value: str) -> bool:
    return value.startswith(str(WORKSPACE_ROOT)) or value.startswith("/home/ubuntu/lzz/")


def is_package_checksum_file(path: Path) -> bool:
    name = path.name
    return any(name.startswith(prefix) for prefix in EXCLUDED_PACKAGE_PREFIXES)


def collect_package_files() -> list[Path]:
    files: list[Path] = []
    for path in PACKAGE_DIR.rglob("*"):
        if not path.is_file():
            continue
        if "__pycache__" in path.parts:
            continue
        if is_package_checksum_file(path):
            continue
        files.append(path)
    return sorted(files)


def collect_manifest_references(manifest: dict[str, Any]) -> tuple[list[Path], list[dict[str, Any]]]:
    files: set[Path] = set()
    missing: list[dict[str, Any]] = []
    for key, value in iter_manifest_strings(manifest):
        if not is_candidate_path(value):
            continue
        path = Path(value)
        if path.parent == PACKAGE_DIR and is_package_checksum_file(path):
            continue
        if path.is_file():
            files.add(path)
        elif path.exists():
            continue
        else:
            missing.append({"key": key, "path": value, "status": "missing_or_pending"})
    return sorted(files), missing


def build_checksums() -> dict[str, Any]:
    generated_at = dt.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
    manifest = read_json(MANIFEST_PATH)
    package_files = collect_package_files()
    referenced_files, missing_refs = collect_manifest_references(manifest)
    all_files = sorted(set(package_files) | set(referenced_files), key=lambda item: workspace_relative(item))

    records = []
    for path in all_files:
        records.append(
            {
                "sha256": sha256_file(path),
                "bytes": path.stat().st_size,
                "path": str(path),
                "workspace_relative_path": workspace_relative(path),
                "source": "package" if path in package_files else "manifest_reference",
            }
        )

    return {
        "artifact_name": "qwen3_32b_patent_package_checksums",
        "generated_at_local": generated_at,
        "package_dir": str(PACKAGE_DIR),
        "workspace_root": str(WORKSPACE_ROOT),
        "scope_boundary": "Checksums cover package files plus existing manifest-referenced files. Pending future evidence paths are reported separately and are not checksum failures.",
        "record_count": len(records),
        "package_file_count": len(package_files),
        "manifest_reference_file_count": len(referenced_files),
        "missing_or_pending_reference_count": len(missing_refs),
        "records": records,
        "missing_or_pending_references": missing_refs,
    }


def render_sha256sums(report: dict[str, Any]) -> str:
    return "".join(
        f"{record['sha256']}  {record['workspace_relative_path']}\n"
        for record in sorted(report["records"], key=lambda item: item["workspace_relative_path"])
    )


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Patent Package Checksums",
        "",
        f"Generated: `{report['generated_at_local']}`",
        "",
        "| item | value |",
        "|---|---:|",
        f"| checksum records | {report['record_count']} |",
        f"| package files | {report['package_file_count']} |",
        f"| manifest reference files | {report['manifest_reference_file_count']} |",
        f"| missing or pending references | {report['missing_or_pending_reference_count']} |",
        "",
        "Verify from workspace root:",
        "",
        "```bash",
        "cd /home/ubuntu/lzz",
        "sha256sum -c MACT/outputs/server_runs/qwen3_32b_patent_experiment_package_20260801_2155/SHA256SUMS",
        "```",
        "",
        "Missing or pending references are not checksum failures. They are expected only for explicitly future evidence such as E4 model/API gate results or optional follow-up seed-boundary work.",
        "",
        "## Missing Or Pending References",
        "",
    ]
    if report["missing_or_pending_references"]:
        lines.extend(
            f"- `{item['key']}` -> `{item['path']}`"
            for item in report["missing_or_pending_references"]
        )
    else:
        lines.append("- none")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=PACKAGE_DIR)
    args = parser.parse_args()

    report = build_checksums()
    stamp = dt.datetime.now().astimezone().strftime("%Y%m%d_%H%M%S")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    json_path = args.output_dir / f"patent_package_checksums_{stamp}.json"
    md_path = args.output_dir / f"patent_package_checksums_{stamp}_zh.md"
    latest_json = args.output_dir / "latest_patent_package_checksums.json"
    latest_md = args.output_dir / "latest_patent_package_checksums_zh.md"
    sha_path = args.output_dir / "SHA256SUMS"
    json_text = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    md_text = render_markdown(report)
    sha_text = render_sha256sums(report)
    json_path.write_text(json_text, encoding="utf-8")
    md_path.write_text(md_text, encoding="utf-8")
    latest_json.write_text(json_text, encoding="utf-8")
    latest_md.write_text(md_text, encoding="utf-8")
    sha_path.write_text(sha_text, encoding="utf-8")
    print(
        json.dumps(
            {
                "sha256sums": str(sha_path),
                "json": str(json_path),
                "md": str(md_path),
                "record_count": report["record_count"],
                "missing_or_pending_reference_count": report["missing_or_pending_reference_count"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
