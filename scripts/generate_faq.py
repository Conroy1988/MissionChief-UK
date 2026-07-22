#!/usr/bin/env python3

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = ROOT / "data" / "uk"
DOC_PATH = ROOT / "docs" / "reference" / "generated-faq.md"
JSON_PATH = ROOT / "docs" / "assets" / "data" / "v1" / "faq.json"
VERSION_PATH = ROOT / "data" / "version.json"

COLLECTIONS = {
    "missions": DATA_ROOT / "missions",
    "vehicles": DATA_ROOT / "vehicles",
    "infrastructure": DATA_ROOT / "infrastructure",
    "training": DATA_ROOT / "training",
}


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def count_records(directory: Path) -> int:
    return len(list(directory.glob("*.json"))) if directory.exists() else 0


def mission_services() -> Counter[str]:
    services: Counter[str] = Counter()
    for path in sorted(COLLECTIONS["missions"].glob("*.json")):
        record = read_json(path)
        service = record.get("service")
        if isinstance(service, str):
            services[service] += 1
    return services


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def main() -> int:
    version = read_json(VERSION_PATH)
    counts = {name: count_records(directory) for name, directory in COLLECTIONS.items()}
    services = mission_services()
    service_summary = ", ".join(f"{name.replace('_', ' ')} ({count})" for name, count in services.most_common())

    entries = [
        {
            "question": "How much verified data is currently published?",
            "answer": f"Version {version['version']} contains {counts['missions']} mission records, {counts['vehicles']} deployable-resource records, {counts['infrastructure']} infrastructure records and {counts['training']} qualification records.",
        },
        {
            "question": "What does verified mean?",
            "answer": "Verified applies only to populated fields that were reproduced in the current UK game or supported by a suitable primary source. It does not automatically verify omitted prices, staffing, training or response details.",
        },
        {
            "question": "Why do some missions have no published vehicle requirements?",
            "answer": "For some missions the official directory verifies the ID, reward, POI and generation preconditions, while the individual response table is unavailable. Empty arrays preserve that evidence boundary and do not mean that no response is required.",
        },
        {
            "question": "How are alternative resources interpreted?",
            "answer": "An alternative group requires the stated total from any combination of the listed qualifying resources. It never means the full quantity of every resource in the group.",
        },
        {
            "question": "How are conditional and probabilistic requirements different?",
            "answer": "Probabilistic requirements may appear at a verified probability. Conditional requirements apply only when an explicit condition is true; a conditional requirement may also carry a probability when both facts are shown.",
        },
        {
            "question": "Is towing treated as a dispatched vehicle requirement?",
            "answer": "No. Official recovery pages list towing as an outcome under Other information. Towing assets are stored separately from emergency resources and infrastructure generation requirements.",
        },
        {
            "question": "Can I use this data programmatically?",
            "answer": "Yes. Versioned read-only JSON exports are published under assets/data/v1 and documented in the API section.",
        },
        {
            "question": "Which mission service groups are represented?",
            "answer": service_summary or "No mission service groups are currently available.",
        },
    ]

    lines = [
        "# Generated FAQ",
        "",
        f"This page is generated from MissionChief UK data version **{version['version']}** released **{version['released_at']}**.",
        "",
        "!!! info \"Generated content\"",
        "    Counts and service coverage are regenerated during validation and Pages deployment. Evidence-policy answers are maintained in the generator so the page cannot drift from the publication model.",
        "",
    ]
    for entry in entries:
        lines.extend([f"## {entry['question']}", "", entry["answer"], ""])
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8", newline="\n")

    write_json(
        JSON_PATH,
        {
            "schema_version": "1",
            "data_version": version["version"],
            "released_at": version["released_at"],
            "count": len(entries),
            "entries": entries,
        },
    )
    print(f"Generated {len(entries)} FAQ entries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
