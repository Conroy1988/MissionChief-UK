#!/usr/bin/env python3

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def patch(path: Path, replacements: list[tuple[str, str, str]], sentinel: str) -> bool:
    text = path.read_text(encoding="utf-8")
    if sentinel in text:
        return False
    original = text
    for label, old, new in replacements:
        if old not in text:
            raise ValueError(f"{path.relative_to(ROOT)}: unable to locate integration point {label}")
        text = text.replace(old, new, 1)
    path.write_text(text, encoding="utf-8")
    return text != original


def main() -> int:
    try:
        changed: list[str] = []

        generator = ROOT / "scripts" / "generate_ready_canonical_batch.py"
        if patch(
            generator,
            [
                (
                    "generator active import",
                    "from conditional_resource_contract import (\n    build_expected_conditionals,\n",
                    "from conditional_resource_contract import (\n    active_requirement_keys as active_conditional_requirement_keys,\n    build_expected_conditionals,\n",
                ),
                (
                    "generator active set",
                    "    conditionals = build_expected_conditionals(official, CONDITIONAL_MAPPINGS)\n\n    for official_key, raw_quantity in official_requirements.items():\n",
                    "    conditionals = build_expected_conditionals(official, CONDITIONAL_MAPPINGS)\n    conditional_requirement_keys = active_conditional_requirement_keys(\n        official, CONDITIONAL_MAPPINGS\n    )\n\n    for official_key, raw_quantity in official_requirements.items():\n        if str(official_key) in conditional_requirement_keys:\n            continue\n",
                ),
            ],
            "active_requirement_keys as active_conditional_requirement_keys",
        ):
            changed.append(generator.relative_to(ROOT).as_posix())

        validator = ROOT / "scripts" / "validate_official_key_mappings.py"
        if patch(
            validator,
            [
                (
                    "validator active imports",
                    "from conditional_resource_contract import (\n    load_mapping_registry as load_conditional_mappings,\n",
                    "from conditional_resource_contract import (\n    active_chance_keys as active_conditional_chance_keys,\n    active_requirement_keys as active_conditional_requirement_keys,\n    load_mapping_registry as load_conditional_mappings,\n",
                ),
                (
                    "validator active sets",
                    "    expected_guaranteed: dict[str, int] = {}\n    expected_probabilistic: dict[str, tuple[int, float]] = {}\n",
                    "    conditional_requirement_keys = active_conditional_requirement_keys(\n        official, CONDITIONAL_MAPPINGS\n    )\n    conditional_chance_keys = active_conditional_chance_keys(\n        official, CONDITIONAL_MAPPINGS\n    )\n\n    expected_guaranteed: dict[str, int] = {}\n    expected_probabilistic: dict[str, tuple[int, float]] = {}\n",
                ),
                (
                    "validator requirement skip",
                    "    for official_key, value in official_requirements.items():\n        mapping = mappings[\"requirements\"].get(str(official_key))\n",
                    "    for official_key, value in official_requirements.items():\n        if str(official_key) in conditional_requirement_keys:\n            continue\n        mapping = mappings[\"requirements\"].get(str(official_key))\n",
                ),
                (
                    "validator chance skip",
                    "    for official_key, value in official_chances.items():\n        mapping = mappings[\"chances\"].get(str(official_key))\n",
                    "    for official_key, value in official_chances.items():\n        if str(official_key) in conditional_chance_keys:\n            continue\n        mapping = mappings[\"chances\"].get(str(official_key))\n",
                ),
            ],
            "active_requirement_keys as active_conditional_requirement_keys",
        ):
            changed.append(validator.relative_to(ROOT).as_posix())

    except (OSError, ValueError) as exc:
        print(f"Conditional resource mode integration failed: {exc}", file=sys.stderr)
        return 1

    print(
        "Conditional resource mode integration synchronized: "
        + (", ".join(changed) if changed else "already current")
        + "."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
