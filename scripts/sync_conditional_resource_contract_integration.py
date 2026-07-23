#!/usr/bin/env python3

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def patch(path: Path, replacements: list[tuple[str, str, str]]) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text
    for label, old, new in replacements:
        if new in text:
            continue
        if old not in text:
            raise ValueError(f"{path.relative_to(ROOT)}: unable to locate integration point {label}")
        text = text.replace(old, new, 1)
    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> int:
    try:
        changed: list[str] = []

        candidate = ROOT / "scripts" / "report_canonical_candidates.py"
        if patch(candidate, [
            (
                "conditional imports",
                "from patient_contract import build_expected_patient, load_mapping_registry as load_patient_mappings, patient_owned_paths\nfrom personnel_contract import build_expected_personnel, load_mapping_registry as load_personnel_mappings\nfrom prisoner_contract import build_expected_prisoners, load_mapping_registry as load_prisoner_mappings, owned_additional_keys\n",
                "from conditional_resource_contract import (\n    build_expected_conditionals,\n    load_mapping_registry as load_conditional_mappings,\n    owned_paths as conditional_owned_paths,\n)\nfrom patient_contract import build_expected_patient, load_mapping_registry as load_patient_mappings, patient_owned_paths\nfrom personnel_contract import build_expected_personnel, load_mapping_registry as load_personnel_mappings\nfrom prisoner_contract import build_expected_prisoners, load_mapping_registry as load_prisoner_mappings, owned_additional_keys\n",
            ),
            (
                "conditional constants",
                "PRISONER_MAPPINGS = load_prisoner_mappings()\nPATIENT_ADDITIONAL_KEYS, PATIENT_CHANCE_KEYS = patient_owned_paths(PATIENT_MAPPINGS)\nPRISONER_ADDITIONAL_KEYS = owned_additional_keys(PRISONER_MAPPINGS)\nSAFE_ADDITIONAL_KEYS = {\n    \"filter_id\",\n    *RELATIONSHIP_KEYS,\n    *PATIENT_ADDITIONAL_KEYS,\n    *PRISONER_ADDITIONAL_KEYS,\n}\n",
                "PRISONER_MAPPINGS = load_prisoner_mappings()\nCONDITIONAL_MAPPINGS = load_conditional_mappings()\nPATIENT_ADDITIONAL_KEYS, PATIENT_CHANCE_KEYS = patient_owned_paths(PATIENT_MAPPINGS)\nPRISONER_ADDITIONAL_KEYS = owned_additional_keys(PRISONER_MAPPINGS)\n(\n    CONDITIONAL_REQUIREMENT_KEYS,\n    CONDITIONAL_CHANCE_KEYS,\n    CONDITIONAL_ADDITIONAL_KEYS,\n    CONDITIONAL_RESOURCES,\n) = conditional_owned_paths(CONDITIONAL_MAPPINGS)\nSAFE_ADDITIONAL_KEYS = {\n    \"filter_id\",\n    *RELATIONSHIP_KEYS,\n    *PATIENT_ADDITIONAL_KEYS,\n    *PRISONER_ADDITIONAL_KEYS,\n    *CONDITIONAL_ADDITIONAL_KEYS,\n}\n",
            ),
            (
                "conditional key ownership",
                "            mapping = mappings[group].get(str(official_key))\n            if mapping is None:\n                blockers.append(f\"unmapped {group}.{official_key}\")\n                continue\n",
                "            mapping = mappings[group].get(str(official_key))\n            if mapping is None:\n                if group == \"requirements\" and str(official_key) in CONDITIONAL_REQUIREMENT_KEYS:\n                    continue\n                if group == \"chances\" and str(official_key) in CONDITIONAL_CHANCE_KEYS:\n                    continue\n                blockers.append(f\"unmapped {group}.{official_key}\")\n                continue\n",
            ),
            (
                "conditional operational validation",
                "    else:\n        unsupported = sorted(set(additional) - SAFE_ADDITIONAL_KEYS)\n",
                "    else:\n        try:\n            build_expected_conditionals(record, CONDITIONAL_MAPPINGS)\n        except ValueError as exc:\n            blockers.append(str(exc))\n        unsupported = sorted(set(additional) - SAFE_ADDITIONAL_KEYS)\n",
            ),
            (
                "conditional candidate payload",
                "    prisoners = build_expected_prisoners(record, PRISONER_MAPPINGS)\n    if prisoners:\n        output[\"prisoners\"] = prisoners\n    return output\n",
                "    prisoners = build_expected_prisoners(record, PRISONER_MAPPINGS)\n    if prisoners:\n        output[\"prisoners\"] = prisoners\n    conditionals = build_expected_conditionals(record, CONDITIONAL_MAPPINGS)\n    if conditionals:\n        output[\"conditional_requirements\"] = conditionals\n    return output\n",
            ),
            (
                "candidate schema and summary",
                "        \"schema_version\": \"4\",\n        \"official_count\": len(records),\n        \"canonical_count\": len(existing),\n        \"patient_contract_fields\": len(PATIENT_MAPPINGS),\n",
                "        \"schema_version\": \"5\",\n        \"official_count\": len(records),\n        \"canonical_count\": len(existing),\n        \"patient_contract_fields\": len(PATIENT_MAPPINGS),\n        \"conditional_resource_contracts\": len(CONDITIONAL_MAPPINGS),\n",
            ),
            (
                "candidate CLI summary",
                "        \"patient_contract_fields\": result[\"patient_contract_fields\"],\n        \"personnel_contract_roles\": result[\"personnel_contract_roles\"],\n",
                "        \"patient_contract_fields\": result[\"patient_contract_fields\"],\n        \"conditional_resource_contracts\": result[\"conditional_resource_contracts\"],\n        \"personnel_contract_roles\": result[\"personnel_contract_roles\"],\n",
            ),
        ]):
            changed.append(candidate.relative_to(ROOT).as_posix())

        generator = ROOT / "scripts" / "generate_ready_canonical_batch.py"
        if patch(generator, [
            (
                "generator conditional imports",
                "from patient_contract import ROOT, build_expected_patient, load_mapping_registry\nfrom report_canonical_candidates import report as candidate_report\n",
                "from conditional_resource_contract import (\n    build_expected_conditionals,\n    load_mapping_registry as load_conditional_mappings,\n    owned_paths as conditional_owned_paths,\n)\nfrom patient_contract import ROOT, build_expected_patient, load_mapping_registry\nfrom report_canonical_candidates import report as candidate_report\n",
            ),
            (
                "generator conditional constants",
                "CHECKED_AT = \"2026-07-23\"\nBATCH_PATTERN = re.compile(r\"fully-canonical-fire-batch-(\\d+)\\.json$\")\n",
                "CHECKED_AT = \"2026-07-23\"\nBATCH_PATTERN = re.compile(r\"fully-canonical-fire-batch-(\\d+)\\.json$\")\nCONDITIONAL_MAPPINGS = load_conditional_mappings()\n(\n    CONDITIONAL_REQUIREMENT_KEYS,\n    CONDITIONAL_CHANCE_KEYS,\n    CONDITIONAL_ADDITIONAL_KEYS,\n    CONDITIONAL_RESOURCES,\n) = conditional_owned_paths(CONDITIONAL_MAPPINGS)\n",
            ),
            (
                "generator conditional translation",
                "    guaranteed: dict[str, int] = {}\n    probabilistic: dict[str, tuple[int, float]] = {}\n    alternatives: dict[tuple[str, ...], tuple[list[str], int]] = {}\n",
                "    guaranteed: dict[str, int] = {}\n    probabilistic: dict[str, tuple[int, float]] = {}\n    alternatives: dict[tuple[str, ...], tuple[list[str], int]] = {}\n    conditionals = build_expected_conditionals(official, CONDITIONAL_MAPPINGS)\n",
            ),
            (
                "generator delegated requirement",
                "        mapping = mappings[\"requirements\"].get(str(official_key))\n        if not isinstance(mapping, dict):\n            raise ValueError(f\"Mission {mission_id} requirement {official_key} is unmapped\")\n",
                "        mapping = mappings[\"requirements\"].get(str(official_key))\n        if not isinstance(mapping, dict):\n            if str(official_key) in CONDITIONAL_REQUIREMENT_KEYS:\n                continue\n            raise ValueError(f\"Mission {mission_id} requirement {official_key} is unmapped\")\n",
            ),
            (
                "generator conditional output",
                "    if alternatives:\n        output[\"alternatives\"] = [\n            {\n                \"resources\": resources,\n                \"quantity\": quantity,\n                \"notes\": [\"Any listed qualifying resource may satisfy this official alternative group.\"],\n            }\n            for _, (resources, quantity) in sorted(alternatives.items())\n        ]\n    return output\n",
                "    if alternatives:\n        output[\"alternatives\"] = [\n            {\n                \"resources\": resources,\n                \"quantity\": quantity,\n                \"notes\": [\"Any listed qualifying resource may satisfy this official alternative group.\"],\n            }\n            for _, (resources, quantity) in sorted(alternatives.items())\n        ]\n    if conditionals:\n        output[\"conditional\"] = conditionals\n    return output\n",
            ),
            (
                "generator conditional decision",
                "            \"strict_key_equivalence\": True,\n            \"strict_patient_equivalence\": True,\n",
                "            \"strict_key_equivalence\": True,\n            \"strict_patient_equivalence\": True,\n            \"strict_conditional_equivalence\": bool(\n                build_expected_conditionals(official, CONDITIONAL_MAPPINGS)\n            ),\n",
            ),
            (
                "generator conditional note",
                "                \"Exact resource, prerequisite, patient and relationship equivalence is required.\",\n",
                "                \"Exact resource, prerequisite, patient, conditional-resource and relationship equivalence is required.\",\n",
            ),
        ]):
            changed.append(generator.relative_to(ROOT).as_posix())

        validator = ROOT / "scripts" / "validate_official_key_mappings.py"
        if patch(validator, [
            (
                "validator conditional imports",
                "from typing import Any\n\nROOT = Path(__file__).resolve().parents[1]\n",
                "from typing import Any\n\nfrom conditional_resource_contract import (\n    load_mapping_registry as load_conditional_mappings,\n    owned_paths as conditional_owned_paths,\n    validate_promoted_conditionals,\n)\n\nROOT = Path(__file__).resolve().parents[1]\n",
            ),
            (
                "validator conditional constants",
                "KEY_MAPPING_PATH = ROOT / \"data\" / \"uk\" / \"official-key-mappings.json\"\n\nPROMOTED_STAGES",
                "KEY_MAPPING_PATH = ROOT / \"data\" / \"uk\" / \"official-key-mappings.json\"\nCONDITIONAL_MAPPINGS = load_conditional_mappings()\n(\n    CONDITIONAL_REQUIREMENT_KEYS,\n    CONDITIONAL_CHANCE_KEYS,\n    CONDITIONAL_ADDITIONAL_KEYS,\n    CONDITIONAL_RESOURCES,\n) = conditional_owned_paths(CONDITIONAL_MAPPINGS)\n\nPROMOTED_STAGES",
            ),
            (
                "validator delegated requirement",
                "        mapping = mappings[\"requirements\"].get(str(official_key))\n        if mapping is None:\n            raise ValueError(f\"Mission {mission_id} is promoted but official key requirements.{official_key} is unmapped\")\n",
                "        mapping = mappings[\"requirements\"].get(str(official_key))\n        if mapping is None:\n            if str(official_key) in CONDITIONAL_REQUIREMENT_KEYS:\n                continue\n            raise ValueError(f\"Mission {mission_id} is promoted but official key requirements.{official_key} is unmapped\")\n",
            ),
            (
                "validator delegated chance",
                "        mapping = mappings[\"chances\"].get(str(official_key))\n        if mapping is None:\n            raise ValueError(f\"Mission {mission_id} is promoted but official key chances.{official_key} is unmapped\")\n",
                "        mapping = mappings[\"chances\"].get(str(official_key))\n        if mapping is None:\n            if str(official_key) in CONDITIONAL_CHANCE_KEYS:\n                continue\n            raise ValueError(f\"Mission {mission_id} is promoted but official key chances.{official_key} is unmapped\")\n",
            ),
            (
                "validator conditional audit",
                "        audit_promoted_mission(key, decision, official, canonical, mappings)\n        promoted += 1\n",
                "        audit_promoted_mission(key, decision, official, canonical, mappings)\n        validate_promoted_conditionals(\n            key, decision, official, canonical, CONDITIONAL_MAPPINGS\n        )\n        promoted += 1\n",
            ),
        ]):
            changed.append(validator.relative_to(ROOT).as_posix())

        backlog = ROOT / "scripts" / "report_key_mapping_backlog.py"
        if patch(backlog, [
            (
                "backlog conditional imports",
                "from patient_contract import load_mapping_registry, patient_owned_paths\n",
                "from conditional_resource_contract import (\n    build_expected_conditionals,\n    load_mapping_registry as load_conditional_mappings,\n    owned_paths as conditional_owned_paths,\n)\nfrom patient_contract import load_mapping_registry, patient_owned_paths\n",
            ),
            (
                "backlog conditional constants",
                "PATIENT_MAPPINGS = load_mapping_registry()\nPATIENT_ADDITIONAL_KEYS, PATIENT_CHANCE_KEYS = patient_owned_paths(PATIENT_MAPPINGS)\nSAFE_ADDITIONAL_KEYS = {\"filter_id\", *RELATIONSHIP_KEYS, *PATIENT_ADDITIONAL_KEYS}\n",
                "PATIENT_MAPPINGS = load_mapping_registry()\nCONDITIONAL_MAPPINGS = load_conditional_mappings()\nPATIENT_ADDITIONAL_KEYS, PATIENT_CHANCE_KEYS = patient_owned_paths(PATIENT_MAPPINGS)\n(\n    CONDITIONAL_REQUIREMENT_KEYS,\n    CONDITIONAL_CHANCE_KEYS,\n    CONDITIONAL_ADDITIONAL_KEYS,\n    CONDITIONAL_RESOURCES,\n) = conditional_owned_paths(CONDITIONAL_MAPPINGS)\nSAFE_ADDITIONAL_KEYS = {\n    \"filter_id\",\n    *RELATIONSHIP_KEYS,\n    *PATIENT_ADDITIONAL_KEYS,\n    *CONDITIONAL_ADDITIONAL_KEYS,\n}\n",
            ),
            (
                "backlog mapped conditional keys",
                "        result[group] = {str(key) for key in values}\n    return result\n",
                "        result[group] = {str(key) for key in values}\n    result[\"requirements\"].update(CONDITIONAL_REQUIREMENT_KEYS)\n    result[\"chances\"].update(CONDITIONAL_CHANCE_KEYS)\n    return result\n",
            ),
            (
                "backlog conditional complexity",
                "    if isinstance(additional, dict):\n        unsupported = sorted(set(additional) - SAFE_ADDITIONAL_KEYS)\n",
                "    if isinstance(additional, dict):\n        try:\n            build_expected_conditionals(record, CONDITIONAL_MAPPINGS)\n        except ValueError as exc:\n            blockers.append(str(exc))\n        unsupported = sorted(set(additional) - SAFE_ADDITIONAL_KEYS)\n",
            ),
            (
                "backlog contract summary",
                "        \"patient_contract_fields\": len(PATIENT_MAPPINGS),\n        \"mapped_key_counts\": {group: len(mapped[group]) for group in KEY_GROUPS},\n",
                "        \"patient_contract_fields\": len(PATIENT_MAPPINGS),\n        \"conditional_resource_contracts\": len(CONDITIONAL_MAPPINGS),\n        \"mapped_key_counts\": {group: len(mapped[group]) for group in KEY_GROUPS},\n",
            ),
        ]):
            changed.append(backlog.relative_to(ROOT).as_posix())

    except (OSError, ValueError) as exc:
        print(f"Conditional resource contract integration failed: {exc}", file=sys.stderr)
        return 1

    print(
        "Conditional resource contract integration synchronized: "
        + (", ".join(changed) if changed else "already current")
        + "."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
