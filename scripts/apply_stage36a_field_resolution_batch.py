#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def write_json(path: str, value: object) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def replace_once(path: str, old: str, new: str) -> None:
    target = ROOT / path
    text = target.read_text(encoding="utf-8")
    if old not in text:
        raise RuntimeError(f"{path}: expected patch anchor not found: {old[:100]!r}")
    target.write_text(text.replace(old, new, 1), encoding="utf-8")


def main() -> int:
    foam_source = "https://xyrality.helpshift.com/hc/en/23-mission-chief/faq/1708-which-vehicles-can-carry-foam/"
    write_json(
        "data/uk/vehicles/water-ladder-with-cafs.json",
        {
            "id": "water_ladder_with_cafs",
            "name": "Water Ladder with CAFS",
            "aliases": ["Water Ladder CAFS"],
            "service": "fire_and_rescue",
            "category": "Foam firefighting appliance",
            "cost": {"credits": 17300, "coins": 10},
            "staffing": {"minimum": 2, "maximum": 9},
            "building_requirements": ["Fire Station with Fire Support"],
            "resource_class": "vehicle",
            "capabilities": ["firefighting", "foam_response", "compressed_air_foam_system"],
            "notes": [
                "Official UK foam guidance publishes the Water Ladder with CAFS as a distinct foam-capable appliance."
            ],
            "verification": {
                "status": "verified",
                "checked_at": "2026-07-25",
                "sources": [foam_source],
            },
        },
    )

    generator = ROOT / "scripts/generate_vehicle_field_resolution.py"
    generator_text = generator.read_text(encoding="utf-8")
    generator_text = generator_text.replace("from datetime import date\n", "")
    generator_text = generator_text.replace(
        "    checked_at = date.today().isoformat()\n",
        "    checked_dates = [\n"
        "        str(record.get('verification', {}).get('checked_at', ''))\n"
        "        for record in records\n"
        "        if isinstance(record.get('verification'), dict)\n"
        "        and record.get('verification', {}).get('checked_at')\n"
        "    ]\n"
        "    checked_at = max(checked_dates) if checked_dates else '1970-01-01'\n",
    )
    generator.write_text(generator_text, encoding="utf-8")

    replace_once(
        "scripts/vehicle_inventory.py",
        'VEHICLE_ROOT = ROOT / "data" / "uk" / "vehicles"\n',
        'VEHICLE_ROOT = ROOT / "data" / "uk" / "vehicles"\nFIELD_RESOLUTION_PATH = ROOT / "data" / "uk" / "vehicle-field-resolution.json"\n',
    )
    replace_once(
        "scripts/vehicle_inventory.py",
        "\n\ndef build_vehicle_coverage(\n",
        '''\n\ndef load_field_resolution(path: Path = FIELD_RESOLUTION_PATH) -> dict[str, Any]:
    document = read_json(path)
    require(isinstance(document, dict), "Vehicle field-resolution registry must be an object")
    require(document.get("collection") == "uk-vehicle-field-resolution", "Vehicle field-resolution collection is invalid")
    summary = document.get("summary")
    field_summary = document.get("field_summary")
    require(isinstance(summary, dict), "Vehicle field-resolution summary must be an object")
    require(isinstance(field_summary, dict), "Vehicle field-resolution field_summary must be an object")
    require(summary.get("unresolved_decisions") == 0, "Vehicle field-resolution registry contains unresolved decisions")
    require(summary.get("resolution_percent") == 100.0, "Vehicle field-resolution registry must report 100 percent decision coverage")
    return document


def build_vehicle_coverage(
''',
    )
    replace_once(
        "scripts/vehicle_inventory.py",
        "    inventory_count = len(inventory_records)\n",
        '    field_resolution = load_field_resolution()\n    require(field_resolution["summary"].get("canonical_records") == canonical_total, "Vehicle field-resolution registry record count is stale")\n\n    inventory_count = len(inventory_records)\n',
    )
    replace_once(
        "scripts/vehicle_inventory.py",
        '        "field_completeness": field_completeness,\n',
        '        "field_completeness": field_completeness,\n        "field_resolution": field_resolution["summary"],\n        "field_resolution_by_field": field_resolution["field_summary"],\n',
    )

    replace_once(
        "scripts/generate_vehicle_coverage.py",
        '    unresolved_rows = "\\n".join(\n',
        '''    resolution = report["field_resolution"]
    resolution_rows = "\\n".join(
        f"| {field.replace('_', ' ').title()} | {values['resolved']:,} / {values['total']:,} | {values['percent']:.2f}% |"
        for field, values in report["field_resolution_by_field"].items()
    )
    unresolved_rows = "\\n".join(
''',
    )
    replace_once(
        "scripts/generate_vehicle_coverage.py",
        "An omitted value is unknown, not zero. Field completeness is reported separately from identity coverage so partial records cannot be mistaken for complete economics or staffing data.\n\n## Source-ledger entries awaiting canonical mapping",
        '''An omitted value is unknown, not zero. Field completeness is reported separately from identity coverage so partial records cannot be mistaken for complete economics or staffing data.

## Field decision coverage

| Metric | Value |
|---|---:|
| Resolved field decisions | **{resolution['resolved_decisions']:,} / {resolution['total_decisions']:,}** |
| Unresolved field decisions | **{resolution['unresolved_decisions']:,}** |
| Decision coverage | **{resolution['resolution_percent']:.2f}%** |

| Field | Resolved | Coverage |
|---|---:|---:|
{resolution_rows}

Decision coverage distinguishes documented values, fields that are not applicable, and values that are not published by a reproducible current UK source. It does not convert unknown values into zeroes or guesses.

## Source-ledger entries awaiting canonical mapping''',
    )

    workflow = ROOT / ".github/workflows/vehicle-inventory-validation.yml"
    workflow_text = workflow.read_text(encoding="utf-8")
    workflow_text = workflow_text.replace(
        "      - tests/python/test_vehicle_inventory.py\n",
        "      - tests/python/test_vehicle_inventory.py\n      - tests/python/test_vehicle_field_resolution.py\n      - scripts/generate_vehicle_field_resolution.py\n      - data/schema/vehicle-field-resolution.schema.json\n      - data/uk/vehicle-field-resolution.json\n      - docs/assets/data/official/uk-vehicle-field-resolution.json\n      - docs/reference/vehicle-field-resolution.md\n",
        2,
    )
    workflow_text = workflow_text.replace(
        "      - name: Check deterministic vehicle coverage outputs\n        run: python scripts/generate_vehicle_coverage.py --check\n",
        "      - name: Check deterministic vehicle field-resolution outputs\n        run: python scripts/generate_vehicle_field_resolution.py --check\n\n      - name: Check deterministic vehicle coverage outputs\n        run: python scripts/generate_vehicle_coverage.py --check\n",
        1,
    )
    workflow_text = workflow_text.replace(
        "      - name: Run vehicle inventory regressions\n        run: python -m unittest tests/python/test_vehicle_inventory.py -v\n",
        "      - name: Run vehicle inventory regressions\n        run: python -m unittest tests/python/test_vehicle_inventory.py tests/python/test_vehicle_field_resolution.py -v\n",
        1,
    )
    workflow_text = workflow_text.replace(
        "            docs/reference/vehicle-coverage-status.md\n",
        "            docs/reference/vehicle-coverage-status.md\n            data/uk/vehicle-field-resolution.json\n            docs/reference/vehicle-field-resolution.md\n",
        1,
    )
    workflow.write_text(workflow_text, encoding="utf-8")

    replace_once(
        "scripts/release_readiness.py",
        '    "reference/vehicle-coverage-status.md",\n',
        '    "reference/vehicle-coverage-status.md",\n    "reference/vehicle-field-resolution.md",\n',
    )
    replace_once(
        "scripts/release_readiness.py",
        '    "docs/reference/vehicle-coverage-status.md",\n',
        '    "docs/reference/vehicle-coverage-status.md",\n    "scripts/generate_vehicle_field_resolution.py",\n    "data/schema/vehicle-field-resolution.schema.json",\n    "data/uk/vehicle-field-resolution.json",\n    "docs/assets/data/official/uk-vehicle-field-resolution.json",\n    "docs/reference/vehicle-field-resolution.md",\n    "tests/python/test_vehicle_field_resolution.py",\n',
    )

    replace_once(
        "mkdocs.yml",
        "          - Vehicle Coverage Status: reference/vehicle-coverage-status.md\n",
        "          - Vehicle Coverage Status: reference/vehicle-coverage-status.md\n          - Vehicle Field Resolution — 100%: reference/vehicle-field-resolution.md\n          - Field Resolution Batch 5: reference/verified-vehicle-field-resolution-batch-5.md\n",
    )

    release_test = ROOT / "tests/python/test_release_integrity.py"
    release_text = release_test.read_text(encoding="utf-8")
    release_text = release_text.replace('metrics["vehicles"], 103', 'metrics["vehicles"], 104')
    release_text = release_text.replace('metrics["search_entities"], 1214', 'metrics["search_entities"], 1215')
    release_text = release_text.replace('data-mcuk-collection="vehicles">103<', 'data-mcuk-collection="vehicles">104<')
    release_test.write_text(release_text, encoding="utf-8")

    evidence = """# Stage 36A — Field Resolution and Final Foam Appliance

This batch closes every tracked vehicle-data field with an explicit evidence outcome while preserving the distinction between published values and unavailable data.

## Delivered

- Water Ladder with CAFS, using the current official UK foam-vehicle contract;
- deterministic field-resolution registry for every canonical resource;
- nine tracked operational fields per resource;
- explicit `documented`, `not_applicable`, `not_published` or `review_required` outcomes;
- 100% decision coverage with zero unresolved field decisions;
- public JSON, generated documentation, CI and release-readiness enforcement.

## Integrity rule

A `not_published` decision is not a zero value. It means no reproducible current UK source publishes the field and the guide refuses to infer it.
"""
    (ROOT / "docs/reference/verified-vehicle-field-resolution-batch-5.md").write_text(evidence, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
