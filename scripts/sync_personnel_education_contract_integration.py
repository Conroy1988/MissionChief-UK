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
                "personnel education imports",
                "from patient_contract import build_expected_patient, load_mapping_registry as load_patient_mappings, patient_owned_paths\nfrom personnel_contract import build_expected_personnel, load_mapping_registry as load_personnel_mappings\n",
                "from patient_contract import build_expected_patient, load_mapping_registry as load_patient_mappings, patient_owned_paths\nfrom personnel_contract import build_expected_personnel, load_mapping_registry as load_personnel_mappings\nfrom personnel_education_contract import (\n    build_expected_personnel_educations,\n    load_mapping_registry as load_personnel_education_mappings,\n    owned_paths as personnel_education_owned_paths,\n)\n",
            ),
            (
                "personnel education constants",
                "PRISONER_MAPPINGS = load_prisoner_mappings()\nCONDITIONAL_MAPPINGS = load_conditional_mappings()\nPATIENT_ADDITIONAL_KEYS, PATIENT_CHANCE_KEYS = patient_owned_paths(PATIENT_MAPPINGS)\n",
                "PRISONER_MAPPINGS = load_prisoner_mappings()\nCONDITIONAL_MAPPINGS = load_conditional_mappings()\nPERSONNEL_EDUCATION_MAPPINGS = load_personnel_education_mappings()\nPATIENT_ADDITIONAL_KEYS, PATIENT_CHANCE_KEYS = patient_owned_paths(PATIENT_MAPPINGS)\n",
            ),
            (
                "personnel education owned paths",
                ") = conditional_owned_paths(CONDITIONAL_MAPPINGS)\nSAFE_ADDITIONAL_KEYS = {\n",
                ") = conditional_owned_paths(CONDITIONAL_MAPPINGS)\n(\n    PERSONNEL_EDUCATION_REQUIREMENT_KEYS,\n    PERSONNEL_EDUCATION_PREREQUISITE_KEYS,\n    PERSONNEL_EDUCATION_ADDITIONAL_KEYS,\n    PERSONNEL_EDUCATION_ROLES,\n) = personnel_education_owned_paths(PERSONNEL_EDUCATION_MAPPINGS)\nSAFE_ADDITIONAL_KEYS = {\n",
            ),
            (
                "personnel education safe additional",
                "    *CONDITIONAL_ADDITIONAL_KEYS,\n}\n",
                "    *CONDITIONAL_ADDITIONAL_KEYS,\n    *PERSONNEL_EDUCATION_ADDITIONAL_KEYS,\n}\n",
            ),
            (
                "personnel education delegated keys",
                "                if group == \"chances\" and str(official_key) in CONDITIONAL_CHANCE_KEYS:\n                    continue\n                blockers.append(f\"unmapped {group}.{official_key}\")\n",
                "                if group == \"chances\" and str(official_key) in CONDITIONAL_CHANCE_KEYS:\n                    continue\n                if group == \"requirements\" and str(official_key) in PERSONNEL_EDUCATION_REQUIREMENT_KEYS:\n                    continue\n                if group == \"prerequisites\" and str(official_key) in PERSONNEL_EDUCATION_PREREQUISITE_KEYS:\n                    continue\n                blockers.append(f\"unmapped {group}.{official_key}\")\n",
            ),
            (
                "personnel education operational validation",
                "        try:\n            build_expected_conditionals(record, CONDITIONAL_MAPPINGS)\n        except ValueError as exc:\n            blockers.append(str(exc))\n        unsupported = sorted(set(additional) - SAFE_ADDITIONAL_KEYS)\n",
                "        try:\n            build_expected_conditionals(record, CONDITIONAL_MAPPINGS)\n        except ValueError as exc:\n            blockers.append(str(exc))\n        try:\n            build_expected_personnel_educations(record, PERSONNEL_EDUCATION_MAPPINGS)\n        except ValueError as exc:\n            blockers.append(str(exc))\n        unsupported = sorted(set(additional) - SAFE_ADDITIONAL_KEYS)\n",
            ),
            (
                "personnel education candidate payload",
                "    conditionals = build_expected_conditionals(record, CONDITIONAL_MAPPINGS)\n    if conditionals:\n        output[\"conditional_requirements\"] = conditionals\n    return output\n",
                "    conditionals = build_expected_conditionals(record, CONDITIONAL_MAPPINGS)\n    if conditionals:\n        output[\"conditional_requirements\"] = conditionals\n    personnel_educations = build_expected_personnel_educations(\n        record, PERSONNEL_EDUCATION_MAPPINGS\n    )\n    if personnel_educations:\n        output[\"personnel_educations\"] = personnel_educations\n    return output\n",
            ),
            (
                "personnel education report summary",
                "        \"schema_version\": \"5\",\n        \"official_count\": len(records),\n        \"canonical_count\": len(existing),\n        \"patient_contract_fields\": len(PATIENT_MAPPINGS),\n        \"conditional_resource_contracts\": len(CONDITIONAL_MAPPINGS),\n",
                "        \"schema_version\": \"6\",\n        \"official_count\": len(records),\n        \"canonical_count\": len(existing),\n        \"patient_contract_fields\": len(PATIENT_MAPPINGS),\n        \"conditional_resource_contracts\": len(CONDITIONAL_MAPPINGS),\n        \"personnel_education_roles\": len(PERSONNEL_EDUCATION_MAPPINGS[\"roles\"]),\n",
            ),
            (
                "personnel education CLI summary",
                "        \"conditional_resource_contracts\": result[\"conditional_resource_contracts\"],\n        \"personnel_contract_roles\": result[\"personnel_contract_roles\"],\n",
                "        \"conditional_resource_contracts\": result[\"conditional_resource_contracts\"],\n        \"personnel_education_roles\": result[\"personnel_education_roles\"],\n        \"personnel_contract_roles\": result[\"personnel_contract_roles\"],\n",
            ),
        ]):
            changed.append(candidate.relative_to(ROOT).as_posix())

        generator = ROOT / "scripts" / "generate_ready_canonical_batch.py"
        if patch(generator, [
            (
                "generator personnel education imports",
                "from patient_contract import ROOT, build_expected_patient, load_mapping_registry\nfrom report_canonical_candidates import report as candidate_report\n",
                "from patient_contract import ROOT, build_expected_patient, load_mapping_registry\nfrom personnel_education_contract import (\n    build_expected_personnel_educations,\n    load_mapping_registry as load_personnel_education_mappings,\n    owned_paths as personnel_education_owned_paths,\n)\nfrom report_canonical_candidates import report as candidate_report\n",
            ),
            (
                "generator personnel education constants",
                ") = conditional_owned_paths(CONDITIONAL_MAPPINGS)\n\nGENERATOR_METADATA = {\n",
                ") = conditional_owned_paths(CONDITIONAL_MAPPINGS)\nPERSONNEL_EDUCATION_MAPPINGS = load_personnel_education_mappings()\n(\n    PERSONNEL_EDUCATION_REQUIREMENT_KEYS,\n    PERSONNEL_EDUCATION_PREREQUISITE_KEYS,\n    PERSONNEL_EDUCATION_ADDITIONAL_KEYS,\n    PERSONNEL_EDUCATION_ROLES,\n) = personnel_education_owned_paths(PERSONNEL_EDUCATION_MAPPINGS)\n\nGENERATOR_METADATA = {\n",
            ),
            (
                "generator delegated personnel requirement",
                "        if not isinstance(mapping, dict):\n            if str(official_key) in CONDITIONAL_REQUIREMENT_KEYS:\n                continue\n            raise ValueError(f\"Mission {mission_id} requirement {official_key} is unmapped\")\n",
                "        if not isinstance(mapping, dict):\n            if str(official_key) in CONDITIONAL_REQUIREMENT_KEYS:\n                continue\n            if str(official_key) in PERSONNEL_EDUCATION_REQUIREMENT_KEYS:\n                continue\n            raise ValueError(f\"Mission {mission_id} requirement {official_key} is unmapped\")\n",
            ),
            (
                "generator delegated personnel prerequisite",
                "        mapping = mappings[\"prerequisites\"].get(str(official_key))\n        if not isinstance(mapping, dict):\n            raise ValueError(f\"Mission {mission_id} prerequisite {official_key} is unmapped\")\n",
                "        mapping = mappings[\"prerequisites\"].get(str(official_key))\n        if not isinstance(mapping, dict):\n            if str(official_key) in PERSONNEL_EDUCATION_PREREQUISITE_KEYS:\n                continue\n            raise ValueError(f\"Mission {mission_id} prerequisite {official_key} is unmapped\")\n",
            ),
            (
                "generator personnel education record",
                "    patients = build_expected_patient(official, patient_mappings)\n    if patients:\n        record[\"patients\"] = patients\n    reward = official.get(\"average_credits\")\n",
                "    patients = build_expected_patient(official, patient_mappings)\n    if patients:\n        record[\"patients\"] = patients\n    personnel_educations = build_expected_personnel_educations(\n        official, PERSONNEL_EDUCATION_MAPPINGS\n    )\n    if personnel_educations:\n        record[\"personnel\"] = personnel_educations\n    reward = official.get(\"average_credits\")\n",
            ),
            (
                "generator personnel education decision",
                "            \"strict_conditional_equivalence\": bool(\n                build_expected_conditionals(official, CONDITIONAL_MAPPINGS)\n            ),\n            \"sources\":",
                "            \"strict_conditional_equivalence\": bool(\n                build_expected_conditionals(official, CONDITIONAL_MAPPINGS)\n            ),\n            \"strict_personnel_education_equivalence\": bool(\n                build_expected_personnel_educations(\n                    official, PERSONNEL_EDUCATION_MAPPINGS\n                )\n            ),\n            \"sources\":",
            ),
            (
                "generator personnel education note",
                "                \"Exact resource, prerequisite, patient, conditional-resource and relationship equivalence is required.\",\n",
                "                \"Exact resource, prerequisite, patient, personnel-education, conditional-resource and relationship equivalence is required.\",\n",
            ),
        ]):
            changed.append(generator.relative_to(ROOT).as_posix())

        validator = ROOT / "scripts" / "validate_official_key_mappings.py"
        if patch(validator, [
            (
                "validator personnel education imports",
                "from conditional_resource_contract import (\n    load_mapping_registry as load_conditional_mappings,\n    owned_paths as conditional_owned_paths,\n    validate_promoted_conditionals,\n)\n\nROOT =",
                "from conditional_resource_contract import (\n    load_mapping_registry as load_conditional_mappings,\n    owned_paths as conditional_owned_paths,\n    validate_promoted_conditionals,\n)\nfrom personnel_education_contract import (\n    load_mapping_registry as load_personnel_education_mappings,\n    owned_paths as personnel_education_owned_paths,\n    validate_promoted_personnel_educations,\n)\n\nROOT =",
            ),
            (
                "validator personnel education constants",
                ") = conditional_owned_paths(CONDITIONAL_MAPPINGS)\n\nPROMOTED_STAGES",
                ") = conditional_owned_paths(CONDITIONAL_MAPPINGS)\nPERSONNEL_EDUCATION_MAPPINGS = load_personnel_education_mappings()\n(\n    PERSONNEL_EDUCATION_REQUIREMENT_KEYS,\n    PERSONNEL_EDUCATION_PREREQUISITE_KEYS,\n    PERSONNEL_EDUCATION_ADDITIONAL_KEYS,\n    PERSONNEL_EDUCATION_ROLES,\n) = personnel_education_owned_paths(PERSONNEL_EDUCATION_MAPPINGS)\n\nPROMOTED_STAGES",
            ),
            (
                "validator delegated personnel requirement",
                "        if mapping is None:\n            if str(official_key) in CONDITIONAL_REQUIREMENT_KEYS:\n                continue\n            raise ValueError(f\"Mission {mission_id} is promoted but official key requirements.{official_key} is unmapped\")\n",
                "        if mapping is None:\n            if str(official_key) in CONDITIONAL_REQUIREMENT_KEYS:\n                continue\n            if str(official_key) in PERSONNEL_EDUCATION_REQUIREMENT_KEYS:\n                continue\n            raise ValueError(f\"Mission {mission_id} is promoted but official key requirements.{official_key} is unmapped\")\n",
            ),
            (
                "validator delegated personnel prerequisite",
                "        mapping = mappings[\"prerequisites\"].get(str(official_key))\n        if mapping is None:\n            raise ValueError(f\"Mission {mission_id} is promoted but official key prerequisites.{official_key} is unmapped\")\n",
                "        mapping = mappings[\"prerequisites\"].get(str(official_key))\n        if mapping is None:\n            if str(official_key) in PERSONNEL_EDUCATION_PREREQUISITE_KEYS:\n                continue\n            raise ValueError(f\"Mission {mission_id} is promoted but official key prerequisites.{official_key} is unmapped\")\n",
            ),
            (
                "validator personnel education audit",
                "        validate_promoted_conditionals(\n            key, decision, official, canonical, CONDITIONAL_MAPPINGS\n        )\n        promoted += 1\n",
                "        validate_promoted_conditionals(\n            key, decision, official, canonical, CONDITIONAL_MAPPINGS\n        )\n        validate_promoted_personnel_educations(\n            key, decision, official, canonical, PERSONNEL_EDUCATION_MAPPINGS\n        )\n        promoted += 1\n",
            ),
        ]):
            changed.append(validator.relative_to(ROOT).as_posix())

        backlog = ROOT / "scripts" / "report_key_mapping_backlog.py"
        if patch(backlog, [
            (
                "backlog personnel education imports",
                "from patient_contract import load_mapping_registry, patient_owned_paths\n",
                "from patient_contract import load_mapping_registry, patient_owned_paths\nfrom personnel_education_contract import (\n    build_expected_personnel_educations,\n    load_mapping_registry as load_personnel_education_mappings,\n    owned_paths as personnel_education_owned_paths,\n)\n",
            ),
            (
                "backlog personnel education constants",
                "CONDITIONAL_MAPPINGS = load_conditional_mappings()\nPATIENT_ADDITIONAL_KEYS, PATIENT_CHANCE_KEYS = patient_owned_paths(PATIENT_MAPPINGS)\n",
                "CONDITIONAL_MAPPINGS = load_conditional_mappings()\nPERSONNEL_EDUCATION_MAPPINGS = load_personnel_education_mappings()\nPATIENT_ADDITIONAL_KEYS, PATIENT_CHANCE_KEYS = patient_owned_paths(PATIENT_MAPPINGS)\n",
            ),
            (
                "backlog personnel education owned paths",
                ") = conditional_owned_paths(CONDITIONAL_MAPPINGS)\nSAFE_ADDITIONAL_KEYS = {\n",
                ") = conditional_owned_paths(CONDITIONAL_MAPPINGS)\n(\n    PERSONNEL_EDUCATION_REQUIREMENT_KEYS,\n    PERSONNEL_EDUCATION_PREREQUISITE_KEYS,\n    PERSONNEL_EDUCATION_ADDITIONAL_KEYS,\n    PERSONNEL_EDUCATION_ROLES,\n) = personnel_education_owned_paths(PERSONNEL_EDUCATION_MAPPINGS)\nSAFE_ADDITIONAL_KEYS = {\n",
            ),
            (
                "backlog personnel education safe additional",
                "    *CONDITIONAL_ADDITIONAL_KEYS,\n}\n",
                "    *CONDITIONAL_ADDITIONAL_KEYS,\n    *PERSONNEL_EDUCATION_ADDITIONAL_KEYS,\n}\n",
            ),
            (
                "backlog personnel education mapped keys",
                "    result[\"requirements\"].update(CONDITIONAL_REQUIREMENT_KEYS)\n    result[\"chances\"].update(CONDITIONAL_CHANCE_KEYS)\n    return result\n",
                "    result[\"requirements\"].update(CONDITIONAL_REQUIREMENT_KEYS)\n    result[\"chances\"].update(CONDITIONAL_CHANCE_KEYS)\n    result[\"requirements\"].update(PERSONNEL_EDUCATION_REQUIREMENT_KEYS)\n    result[\"prerequisites\"].update(PERSONNEL_EDUCATION_PREREQUISITE_KEYS)\n    return result\n",
            ),
            (
                "backlog personnel education validation",
                "        try:\n            build_expected_conditionals(record, CONDITIONAL_MAPPINGS)\n        except ValueError as exc:\n            blockers.append(str(exc))\n        unsupported = sorted(set(additional) - SAFE_ADDITIONAL_KEYS)\n",
                "        try:\n            build_expected_conditionals(record, CONDITIONAL_MAPPINGS)\n        except ValueError as exc:\n            blockers.append(str(exc))\n        try:\n            build_expected_personnel_educations(record, PERSONNEL_EDUCATION_MAPPINGS)\n        except ValueError as exc:\n            blockers.append(str(exc))\n        unsupported = sorted(set(additional) - SAFE_ADDITIONAL_KEYS)\n",
            ),
            (
                "backlog personnel education summary",
                "        \"conditional_resource_contracts\": len(CONDITIONAL_MAPPINGS),\n        \"mapped_key_counts\": {group: len(mapped[group]) for group in KEY_GROUPS},\n",
                "        \"conditional_resource_contracts\": len(CONDITIONAL_MAPPINGS),\n        \"personnel_education_roles\": len(PERSONNEL_EDUCATION_MAPPINGS[\"roles\"]),\n        \"mapped_key_counts\": {group: len(mapped[group]) for group in KEY_GROUPS},\n",
            ),
        ]):
            changed.append(backlog.relative_to(ROOT).as_posix())

    except (OSError, ValueError) as exc:
        print(f"Personnel education contract integration failed: {exc}", file=sys.stderr)
        return 1

    print(
        "Personnel education contract integration synchronized: "
        + (", ".join(changed) if changed else "already current")
        + "."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
