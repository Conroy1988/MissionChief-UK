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

        candidate = ROOT / "scripts" / "report_canonical_candidates.py"
        if patch(
            candidate,
            [
                (
                    "candidate recovery import",
                    "from prisoner_contract import build_expected_prisoners, load_mapping_registry as load_prisoner_mappings, owned_additional_keys\n",
                    "from prisoner_contract import build_expected_prisoners, load_mapping_registry as load_prisoner_mappings, owned_additional_keys\nfrom recovery_contract import (\n    build_expected_recovery,\n    load_mapping_registry as load_recovery_mappings,\n    owned_additional_keys as recovery_owned_additional_keys,\n)\n",
                ),
                (
                    "candidate recovery constants",
                    "PERSONNEL_EDUCATION_MAPPINGS = load_personnel_education_mappings()\nPATIENT_ADDITIONAL_KEYS, PATIENT_CHANCE_KEYS = patient_owned_paths(PATIENT_MAPPINGS)\n",
                    "PERSONNEL_EDUCATION_MAPPINGS = load_personnel_education_mappings()\nRECOVERY_MAPPINGS = load_recovery_mappings()\nRECOVERY_ADDITIONAL_KEYS = recovery_owned_additional_keys(RECOVERY_MAPPINGS)\nPATIENT_ADDITIONAL_KEYS, PATIENT_CHANCE_KEYS = patient_owned_paths(PATIENT_MAPPINGS)\n",
                ),
                (
                    "candidate recovery safe keys",
                    "    *PERSONNEL_EDUCATION_ADDITIONAL_KEYS,\n}\nSAFE_GENERATOR_FAMILIES = {\"firehouse_missions\", \"police_station_missions\", \"ambulance_station_missions\"}\n",
                    "    *PERSONNEL_EDUCATION_ADDITIONAL_KEYS,\n    *RECOVERY_ADDITIONAL_KEYS,\n}\nSAFE_GENERATOR_FAMILIES = {\n    \"firehouse_missions\",\n    \"police_station_missions\",\n    \"ambulance_station_missions\",\n    \"tow_trucks_missions\",\n}\n",
                ),
                (
                    "candidate recovery validation",
                    "        try:\n            build_expected_personnel_educations(record, PERSONNEL_EDUCATION_MAPPINGS)\n        except ValueError as exc:\n            blockers.append(str(exc))\n        unsupported = sorted(set(additional) - SAFE_ADDITIONAL_KEYS)\n",
                    "        try:\n            build_expected_personnel_educations(record, PERSONNEL_EDUCATION_MAPPINGS)\n        except ValueError as exc:\n            blockers.append(str(exc))\n        try:\n            build_expected_recovery(record, RECOVERY_MAPPINGS)\n        except ValueError as exc:\n            blockers.append(str(exc))\n        unsupported = sorted(set(additional) - SAFE_ADDITIONAL_KEYS)\n",
                ),
                (
                    "candidate recovery payload",
                    "    if personnel_educations:\n        output[\"personnel_educations\"] = personnel_educations\n    return output\n",
                    "    if personnel_educations:\n        output[\"personnel_educations\"] = personnel_educations\n    recovery = build_expected_recovery(record, RECOVERY_MAPPINGS)\n    if recovery:\n        output[\"recovery\"] = recovery\n    return output\n",
                ),
                (
                    "candidate recovery summary",
                    "        \"schema_version\": \"6\",\n        \"official_count\": len(records),\n",
                    "        \"schema_version\": \"7\",\n        \"official_count\": len(records),\n",
                ),
                (
                    "candidate recovery contract count",
                    "        \"personnel_education_roles\": len(PERSONNEL_EDUCATION_MAPPINGS[\"roles\"]),\n        \"personnel_contract_roles\": len(PERSONNEL_MAPPINGS),\n",
                    "        \"personnel_education_roles\": len(PERSONNEL_EDUCATION_MAPPINGS[\"roles\"]),\n        \"recovery_asset_contracts\": len(RECOVERY_MAPPINGS),\n        \"personnel_contract_roles\": len(PERSONNEL_MAPPINGS),\n",
                ),
                (
                    "candidate recovery CLI count",
                    "        \"personnel_education_roles\": result[\"personnel_education_roles\"],\n        \"personnel_contract_roles\": result[\"personnel_contract_roles\"],\n",
                    "        \"personnel_education_roles\": result[\"personnel_education_roles\"],\n        \"recovery_asset_contracts\": result[\"recovery_asset_contracts\"],\n        \"personnel_contract_roles\": result[\"personnel_contract_roles\"],\n",
                ),
            ],
            "RECOVERY_MAPPINGS = load_recovery_mappings()",
        ):
            changed.append(candidate.relative_to(ROOT).as_posix())

        generator = ROOT / "scripts" / "generate_ready_canonical_batch.py"
        if patch(
            generator,
            [
                (
                    "generator recovery import",
                    "from report_canonical_candidates import report as candidate_report\n",
                    "from recovery_contract import build_expected_recovery, load_mapping_registry as load_recovery_mappings\nfrom report_canonical_candidates import report as candidate_report\n",
                ),
                (
                    "generator recovery constants",
                    ") = personnel_education_owned_paths(PERSONNEL_EDUCATION_MAPPINGS)\n\nGENERATOR_METADATA = {\n",
                    ") = personnel_education_owned_paths(PERSONNEL_EDUCATION_MAPPINGS)\nRECOVERY_MAPPINGS = load_recovery_mappings()\n\nGENERATOR_METADATA = {\n",
                ),
                (
                    "generator recovery metadata",
                    "    \"ambulance_station_missions\": (\"ambulance\", [\"Ambulance Missions\"]),\n}\n",
                    "    \"ambulance_station_missions\": (\"ambulance\", [\"Ambulance Missions\"]),\n    \"tow_trucks_missions\": (\"recovery\", [\"Recovery Vehicle Missions\"]),\n}\n",
                ),
                (
                    "generator recovery record",
                    "    if personnel_educations:\n        record[\"personnel\"] = personnel_educations\n    reward = official.get(\"average_credits\")\n",
                    "    if personnel_educations:\n        record[\"personnel\"] = personnel_educations\n    recovery = build_expected_recovery(official, RECOVERY_MAPPINGS)\n    if recovery:\n        record[\"recovery\"] = recovery\n    reward = official.get(\"average_credits\")\n",
                ),
                (
                    "generator recovery decision",
                    "            \"strict_personnel_education_equivalence\": bool(\n                build_expected_personnel_educations(\n                    official, PERSONNEL_EDUCATION_MAPPINGS\n                )\n            ),\n            \"sources\":",
                    "            \"strict_personnel_education_equivalence\": bool(\n                build_expected_personnel_educations(\n                    official, PERSONNEL_EDUCATION_MAPPINGS\n                )\n            ),\n            \"strict_recovery_equivalence\": bool(\n                build_expected_recovery(official, RECOVERY_MAPPINGS)\n            ),\n            \"sources\":",
                ),
                (
                    "generator recovery note",
                    "                \"Exact resource, prerequisite, patient, personnel-education, conditional-resource and relationship equivalence is required.\",\n",
                    "                \"Exact resource, prerequisite, patient, personnel-education, conditional-resource, recovery-outcome and relationship equivalence is required.\",\n",
                ),
            ],
            "RECOVERY_MAPPINGS = load_recovery_mappings()",
        ):
            changed.append(generator.relative_to(ROOT).as_posix())

        backlog = ROOT / "scripts" / "report_key_mapping_backlog.py"
        if patch(
            backlog,
            [
                (
                    "backlog recovery import",
                    "from patient_contract import load_mapping_registry, patient_owned_paths\n",
                    "from patient_contract import load_mapping_registry, patient_owned_paths\nfrom recovery_contract import (\n    build_expected_recovery,\n    load_mapping_registry as load_recovery_mappings,\n    owned_additional_keys as recovery_owned_additional_keys,\n)\n",
                ),
                (
                    "backlog recovery constants",
                    "PERSONNEL_EDUCATION_MAPPINGS = load_personnel_education_mappings()\nPATIENT_ADDITIONAL_KEYS, PATIENT_CHANCE_KEYS = patient_owned_paths(PATIENT_MAPPINGS)\n",
                    "PERSONNEL_EDUCATION_MAPPINGS = load_personnel_education_mappings()\nRECOVERY_MAPPINGS = load_recovery_mappings()\nRECOVERY_ADDITIONAL_KEYS = recovery_owned_additional_keys(RECOVERY_MAPPINGS)\nPATIENT_ADDITIONAL_KEYS, PATIENT_CHANCE_KEYS = patient_owned_paths(PATIENT_MAPPINGS)\n",
                ),
                (
                    "backlog recovery safe keys",
                    "    *PERSONNEL_EDUCATION_ADDITIONAL_KEYS,\n}\nSAFE_GENERATOR_FAMILIES = {\"firehouse_missions\", \"police_station_missions\", \"ambulance_station_missions\"}\n",
                    "    *PERSONNEL_EDUCATION_ADDITIONAL_KEYS,\n    *RECOVERY_ADDITIONAL_KEYS,\n}\nSAFE_GENERATOR_FAMILIES = {\n    \"firehouse_missions\",\n    \"police_station_missions\",\n    \"ambulance_station_missions\",\n    \"tow_trucks_missions\",\n}\n",
                ),
                (
                    "backlog recovery validation",
                    "        try:\n            build_expected_personnel_educations(record, PERSONNEL_EDUCATION_MAPPINGS)\n        except ValueError as exc:\n            blockers.append(str(exc))\n        unsupported = sorted(set(additional) - SAFE_ADDITIONAL_KEYS)\n",
                    "        try:\n            build_expected_personnel_educations(record, PERSONNEL_EDUCATION_MAPPINGS)\n        except ValueError as exc:\n            blockers.append(str(exc))\n        try:\n            build_expected_recovery(record, RECOVERY_MAPPINGS)\n        except ValueError as exc:\n            blockers.append(str(exc))\n        unsupported = sorted(set(additional) - SAFE_ADDITIONAL_KEYS)\n",
                ),
                (
                    "backlog recovery summary",
                    "        \"personnel_education_roles\": len(PERSONNEL_EDUCATION_MAPPINGS[\"roles\"]),\n        \"mapped_key_counts\": {group: len(mapped[group]) for group in KEY_GROUPS},\n",
                    "        \"personnel_education_roles\": len(PERSONNEL_EDUCATION_MAPPINGS[\"roles\"]),\n        \"recovery_asset_contracts\": len(RECOVERY_MAPPINGS),\n        \"mapped_key_counts\": {group: len(mapped[group]) for group in KEY_GROUPS},\n",
                ),
            ],
            "RECOVERY_MAPPINGS = load_recovery_mappings()",
        ):
            changed.append(backlog.relative_to(ROOT).as_posix())

    except (OSError, ValueError) as exc:
        print(f"Recovery contract integration failed: {exc}", file=sys.stderr)
        return 1

    print(
        "Recovery contract integration synchronized: "
        + (", ".join(changed) if changed else "already current")
        + "."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
