#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIELDS = (
    "cost",
    "staffing",
    "training",
    "training_requirements",
    "building_requirements",
    "resource_class",
    "transport_capacity",
    "towing",
    "deployment",
)


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise RuntimeError(f"{path.relative_to(ROOT)}: patch anchor not found")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def main() -> int:
    inventory = ROOT / "scripts" / "vehicle_inventory.py"
    replace_once(
        inventory,
        "def build_vehicle_coverage(\n    inventory_document: dict[str, Any],\n    inventory_records: list[dict[str, Any]],\n    canonical_records: dict[str, dict[str, Any]],\n) -> dict[str, Any]:\n",
        "def build_vehicle_coverage(\n    inventory_document: dict[str, Any],\n    inventory_records: list[dict[str, Any]],\n    canonical_records: dict[str, dict[str, Any]],\n    field_resolution_document: dict[str, Any] | None = None,\n) -> dict[str, Any]:\n",
    )
    replace_once(
        inventory,
        "    field_resolution = load_field_resolution()\n",
        "    field_resolution = field_resolution_document or load_field_resolution()\n",
    )

    test_path = ROOT / "tests" / "python" / "test_vehicle_inventory.py"
    helper = '''\n\ndef field_resolution_document(total: int) -> dict:\n    fields = (\n        "cost",\n        "staffing",\n        "training",\n        "training_requirements",\n        "building_requirements",\n        "resource_class",\n        "transport_capacity",\n        "towing",\n        "deployment",\n    )\n    return {\n        "collection": "uk-vehicle-field-resolution",\n        "summary": {\n            "canonical_records": total,\n            "tracked_fields": len(fields),\n            "total_decisions": total * len(fields),\n            "resolved_decisions": total * len(fields),\n            "unresolved_decisions": 0,\n            "resolution_percent": 100.0,\n        },\n        "field_summary": {\n            field: {\n                "resolved": total,\n                "total": total,\n                "percent": 100.0,\n                "status_counts": {"documented": total},\n            }\n            for field in fields\n        },\n    }\n'''
    replace_once(
        test_path,
        "def inventory_record(type_id: int, name: str, canonical_id: str | None) -> list:\n    return [type_id, name, canonical_id, \"fire\", \"vehicle\", \"candidate\", [\"example\"], []]\n",
        "def inventory_record(type_id: int, name: str, canonical_id: str | None) -> list:\n    return [type_id, name, canonical_id, \"fire\", \"vehicle\", \"candidate\", [\"example\"], []]\n" + helper,
    )
    replace_once(
        test_path,
        "        report = build_vehicle_coverage(document, records, canonical)\n",
        "        report = build_vehicle_coverage(document, records, canonical, field_resolution_document(len(canonical)))\n",
    )
    replace_once(
        test_path,
        "        report = build_vehicle_coverage(document, records, {})\n",
        "        report = build_vehicle_coverage(document, records, {}, field_resolution_document(0))\n",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
