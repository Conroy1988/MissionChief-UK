#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BASELINE = ROOT / "data" / "sources" / "missionchief-uk" / "einsaetze.raw.json"
DEFAULT_CANDIDATE = ROOT / "data" / "sources" / "missionchief-uk" / "einsaetze.raw.json"
DEFAULT_CANONICAL = ROOT / "data" / "uk" / "missions"
DEFAULT_REGISTRY = ROOT / "data" / "uk" / "mission-verification-registry.json"

IDENTITY_FIELDS = {"id", "name", "caption", "title"}
CRITICAL_OPERATIONAL_FIELDS = {
    "requirements",
    "chances",
    "prerequisites",
    "patients",
    "additional",
    "duration",
    "duration_min",
    "duration_max",
    "guard_mission",
    "possible_missions",
    "expansion_missions_ids",
    "followup_missions_ids",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Compare a candidate official MissionChief UK mission feed with the "
            "committed production snapshot and generate a deterministic review queue."
        )
    )
    parser.add_argument("--baseline", type=Path, default=DEFAULT_BASELINE)
    parser.add_argument("--candidate", type=Path, default=DEFAULT_CANDIDATE)
    parser.add_argument("--canonical-dir", type=Path, default=DEFAULT_CANONICAL)
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--json-output", type=Path)
    parser.add_argument("--markdown-output", type=Path)
    parser.add_argument("--github-output", type=Path)
    parser.add_argument("--markdown-limit", type=int, default=50)
    parser.add_argument("--fail-on-drift", action="store_true")
    return parser.parse_args()


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"{path}: unable to read JSON: {exc}") from exc


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def stable_id(value: Any) -> tuple[int, int | str]:
    try:
        return (0, int(value))
    except (TypeError, ValueError):
        return (1, str(value))


def mission_name(record: dict[str, Any]) -> str:
    value = record.get("name") or record.get("caption") or record.get("title")
    return str(value).strip() if value is not None else ""


def source_records(path: Path) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    document = read_json(path)
    if not isinstance(document, dict):
        raise ValueError(f"{path}: official source must be a JSON object")
    records = document.get("records")
    if not isinstance(records, list):
        raise ValueError(f"{path}: official source records must be a JSON array")

    by_id: dict[str, dict[str, Any]] = {}
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            raise ValueError(f"{path}: record {index} is not an object")
        mission_id = record.get("id")
        if mission_id is None or str(mission_id).strip() == "":
            raise ValueError(f"{path}: record {index} has no mission id")
        key = str(mission_id)
        if key in by_id:
            raise ValueError(f"{path}: duplicate mission id {key}")
        by_id[key] = record
    return document, by_id


def canonical_ids(directory: Path) -> set[str]:
    result: set[str] = set()
    if not directory.exists():
        return result
    for path in sorted(directory.glob("*.json")):
        record = read_json(path)
        if isinstance(record, dict) and record.get("id") is not None:
            result.add(str(record["id"]))
    return result


def fully_canonical_ids(path: Path) -> set[str]:
    document = read_json(path)
    if not isinstance(document, dict):
        raise ValueError(f"{path}: verification registry must be an object")
    records = document.get("records")
    if not isinstance(records, dict):
        raise ValueError(f"{path}: verification registry records must be an object")
    return {
        str(mission_id)
        for mission_id, decision in records.items()
        if isinstance(decision, dict) and decision.get("stage") == "fully-canonical"
    }


class _Missing:
    pass


_MISSING = _Missing()


def compact_value(value: Any, limit: int = 500) -> Any:
    if value is _MISSING:
        return {"missing": True}
    if value is None or isinstance(value, (bool, int, float, str)):
        if isinstance(value, str) and len(value) > limit:
            return {"type": "string", "length": len(value), "sha256": digest(value)}
        return value
    encoded = canonical_json(value)
    if len(encoded) <= limit:
        return value
    size = len(value) if isinstance(value, (list, dict)) else None
    summary: dict[str, Any] = {
        "type": type(value).__name__,
        "sha256": hashlib.sha256(encoded.encode("utf-8")).hexdigest(),
    }
    if size is not None:
        summary["size"] = size
    return summary


def changed_paths(before: Any, after: Any, path: tuple[str, ...] = ()) -> list[dict[str, Any]]:
    if type(before) is not type(after):
        return [
            {
                "path": ".".join(path) or "$",
                "before": compact_value(before),
                "after": compact_value(after),
            }
        ]

    if isinstance(before, dict):
        changes: list[dict[str, Any]] = []
        for key in sorted(set(before) | set(after), key=str):
            changes.extend(
                changed_paths(
                    before.get(key, _MISSING),
                    after.get(key, _MISSING),
                    (*path, str(key)),
                )
            )
        return changes

    # Array order can be operationally meaningful. Retain the complete array as
    # one change rather than generating noisy index-by-index differences.
    if isinstance(before, list):
        if canonical_json(before) == canonical_json(after):
            return []
        return [
            {
                "path": ".".join(path) or "$",
                "before": compact_value(before),
                "after": compact_value(after),
            }
        ]

    if before == after:
        return []
    return [
        {
            "path": ".".join(path) or "$",
            "before": compact_value(before),
            "after": compact_value(after),
        }
    ]


def change_groups(changes: Iterable[dict[str, Any]]) -> list[str]:
    groups: set[str] = set()
    for change in changes:
        path = str(change.get("path", "$"))
        top_level = path.split(".", 1)[0]
        if top_level in IDENTITY_FIELDS:
            groups.add("identity")
        elif top_level in CRITICAL_OPERATIONAL_FIELDS:
            groups.add(top_level)
        else:
            groups.add("other")
    return sorted(groups)


def change_severity(groups: Iterable[str]) -> str:
    group_set = set(groups)
    if "identity" in group_set or group_set & CRITICAL_OPERATIONAL_FIELDS:
        return "critical"
    return "high"


def record_reference(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": record.get("id"),
        "name": mission_name(record),
        "record_sha256": digest(record),
    }


def generated_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def build_report(
    baseline_path: Path,
    candidate_path: Path,
    canonical_dir: Path,
    registry_path: Path,
    *,
    generated_at: str | None = None,
) -> dict[str, Any]:
    baseline_document, baseline = source_records(baseline_path)
    candidate_document, candidate = source_records(candidate_path)
    canonical = canonical_ids(canonical_dir)
    fully_canonical = fully_canonical_ids(registry_path)

    baseline_ids = set(baseline)
    candidate_ids = set(candidate)
    added_ids = sorted(candidate_ids - baseline_ids, key=stable_id)
    removed_ids = sorted(baseline_ids - candidate_ids, key=stable_id)

    modified: list[dict[str, Any]] = []
    for mission_id in sorted(baseline_ids & candidate_ids, key=stable_id):
        before = baseline[mission_id]
        after = candidate[mission_id]
        if canonical_json(before) == canonical_json(after):
            continue
        paths = changed_paths(before, after)
        groups = change_groups(paths)
        modified.append(
            {
                "id": after.get("id"),
                "baseline_name": mission_name(before),
                "candidate_name": mission_name(after),
                "baseline_record_sha256": digest(before),
                "candidate_record_sha256": digest(after),
                "severity": change_severity(groups),
                "groups": groups,
                "changed_paths": paths,
            }
        )

    added = [record_reference(candidate[mission_id]) for mission_id in added_ids]
    removed = [record_reference(baseline[mission_id]) for mission_id in removed_ids]
    modified_ids = {str(item["id"]) for item in modified}
    impacted_existing = modified_ids | set(removed_ids)

    invalidated = sorted(fully_canonical & impacted_existing, key=stable_id)
    canonical_impacted = sorted(canonical & impacted_existing, key=stable_id)
    new_uncovered = sorted(set(added_ids) - canonical, key=stable_id)
    review_required = sorted(set(added_ids) | impacted_existing, key=stable_id)

    projected_verified = (fully_canonical & candidate_ids) - modified_ids
    candidate_count = len(candidate)
    projected_percent = (
        round(len(projected_verified) / candidate_count * 100, 2)
        if candidate_count
        else 0.0
    )

    stable_change_payload = {
        "added": added,
        "removed": removed,
        "modified": modified,
        "baseline_source_sha256": baseline_document.get("source_sha256"),
        "candidate_source_sha256": candidate_document.get("source_sha256"),
    }
    fingerprint = digest(stable_change_payload)
    has_drift = bool(added or removed or modified)

    return {
        "schema_version": "1",
        "generated_at": generated_at or generated_timestamp(),
        "status": "review-required" if has_drift else "clean",
        "has_drift": has_drift,
        "fingerprint": fingerprint,
        "source": {
            "baseline": {
                "path": str(baseline_path),
                "count": len(baseline),
                "source_sha256": baseline_document.get("source_sha256"),
                "fetched_at": baseline_document.get("fetched_at"),
            },
            "candidate": {
                "path": str(candidate_path),
                "count": len(candidate),
                "source_sha256": candidate_document.get("source_sha256"),
                "fetched_at": candidate_document.get("fetched_at"),
            },
        },
        "summary": {
            "added_count": len(added),
            "removed_count": len(removed),
            "modified_count": len(modified),
            "review_required_count": len(review_required),
            "invalidated_fully_canonical_count": len(invalidated),
            "new_uncovered_count": len(new_uncovered),
        },
        "impact": {
            "review_required_ids": review_required,
            "new_uncovered_ids": new_uncovered,
            "invalidated_fully_canonical_ids": invalidated,
            "impacted_canonical_ids": canonical_impacted,
            "current_fully_canonical_count": len(fully_canonical & baseline_ids),
            "projected_fully_canonical_count": len(projected_verified),
            "candidate_official_count": candidate_count,
            "projected_fully_canonical_percent": projected_percent,
            "coverage_regression": bool(new_uncovered or invalidated),
        },
        "changes": {
            "added": added,
            "removed": removed,
            "modified": modified,
        },
    }


def markdown_list(values: list[str], limit: int) -> str:
    if not values:
        return "_None._"
    shown = values[:limit]
    lines = [f"- `{value}`" for value in shown]
    if len(values) > limit:
        lines.append(f"- …and {len(values) - limit} more (see the JSON report).")
    return "\n".join(lines)


def render_markdown(report: dict[str, Any], limit: int = 50) -> str:
    summary = report["summary"]
    impact = report["impact"]
    source = report["source"]
    changes = report["changes"]
    lines = [
        "# Official UK mission catalogue drift report",
        "",
        f"**Status:** `{report['status']}`  ",
        f"**Fingerprint:** `{report['fingerprint']}`  ",
        f"**Generated:** `{report['generated_at']}`",
        "",
        "## Source comparison",
        "",
        "| Snapshot | Missions | Source SHA-256 |",
        "|---|---:|---|",
        f"| Baseline | {source['baseline']['count']} | `{source['baseline'].get('source_sha256')}` |",
        f"| Candidate | {source['candidate']['count']} | `{source['candidate'].get('source_sha256')}` |",
        "",
        "## Impact",
        "",
        "| Metric | Result |",
        "|---|---:|",
        f"| Added official missions | {summary['added_count']} |",
        f"| Removed official missions | {summary['removed_count']} |",
        f"| Modified official missions | {summary['modified_count']} |",
        f"| Review-required identities | {summary['review_required_count']} |",
        f"| Fully canonical identities invalidated | {summary['invalidated_fully_canonical_count']} |",
        f"| New uncovered identities | {summary['new_uncovered_count']} |",
        f"| Projected verified coverage | {impact['projected_fully_canonical_count']} / {impact['candidate_official_count']} ({impact['projected_fully_canonical_percent']}%) |",
        "",
    ]
    if not report["has_drift"]:
        lines.extend(
            [
                "The candidate feed is semantically identical to the committed production snapshot.",
                "",
            ]
        )
        return "\n".join(lines)

    lines.extend(
        [
            "> **Fail-closed:** production data must not be refreshed or deployed until every identity below has been reconciled and revalidated.",
            "",
            "## Added missions",
            "",
        ]
    )
    if changes["added"]:
        for item in changes["added"][:limit]:
            lines.append(f"- `#{item['id']}` — {item['name']}")
        if len(changes["added"]) > limit:
            lines.append(f"- …and {len(changes['added']) - limit} more.")
    else:
        lines.append("_None._")

    lines.extend(["", "## Removed missions", ""])
    if changes["removed"]:
        for item in changes["removed"][:limit]:
            lines.append(f"- `#{item['id']}` — {item['name']}")
        if len(changes["removed"]) > limit:
            lines.append(f"- …and {len(changes['removed']) - limit} more.")
    else:
        lines.append("_None._")

    lines.extend(["", "## Modified missions", ""])
    if changes["modified"]:
        for item in changes["modified"][:limit]:
            paths = ", ".join(f"`{change['path']}`" for change in item["changed_paths"][:8])
            if len(item["changed_paths"]) > 8:
                paths += f", …and {len(item['changed_paths']) - 8} more"
            lines.append(
                f"- `#{item['id']}` — {item['candidate_name']} "
                f"(**{item['severity']}**; {paths})"
            )
        if len(changes["modified"]) > limit:
            lines.append(f"- …and {len(changes['modified']) - limit} more.")
    else:
        lines.append("_None._")

    lines.extend(
        [
            "",
            "## Invalidated fully canonical identities",
            "",
            markdown_list([str(value) for value in impact["invalidated_fully_canonical_ids"]], limit),
            "",
            "## Required response",
            "",
            "1. Review the exact field-level changes in the JSON report.",
            "2. Re-establish official evidence and update the owned mapping contracts.",
            "3. Regenerate or amend affected canonical records without guessing semantics.",
            "4. Restore strict equivalence and 100% verified coverage.",
            "5. Merge the review branch only after exact-head validation and deployed-site checks pass.",
            "",
        ]
    )
    return "\n".join(lines)


def write_text(path: Path | None, content: str) -> None:
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def write_json(path: Path | None, value: Any) -> None:
    if path is None:
        return
    write_text(path, json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


def write_github_output(path: Path | None, report: dict[str, Any]) -> None:
    if path is None:
        return
    summary = report["summary"]
    impact = report["impact"]
    values = {
        "has_drift": str(report["has_drift"]).lower(),
        "status": report["status"],
        "fingerprint": report["fingerprint"],
        "fingerprint_short": report["fingerprint"][:16],
        "added_count": summary["added_count"],
        "removed_count": summary["removed_count"],
        "modified_count": summary["modified_count"],
        "review_required_count": summary["review_required_count"],
        "invalidated_count": summary["invalidated_fully_canonical_count"],
        "projected_coverage_percent": impact["projected_fully_canonical_percent"],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        for key, value in values.items():
            handle.write(f"{key}={value}\n")


def main() -> int:
    args = parse_args()
    report = build_report(
        args.baseline,
        args.candidate,
        args.canonical_dir,
        args.registry,
    )
    write_json(args.json_output, report)
    markdown = render_markdown(report, max(1, args.markdown_limit))
    write_text(args.markdown_output, markdown)
    write_github_output(args.github_output, report)
    print(markdown)
    if args.fail_on_drift and report["has_drift"]:
        return 2
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError) as exc:
        print(f"Official mission drift detection failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
