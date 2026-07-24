#!/usr/bin/env python3

from pathlib import Path

path = Path("scripts/release_readiness.py")
text = path.read_text(encoding="utf-8")

files_anchor = '''    "scripts/validate_verification_programme_assets.py",
    "tests/python/test_release_integrity.py",'''
files_replacement = '''    "scripts/validate_verification_programme_assets.py",
    "scripts/detect_official_mission_drift.py",
    "tests/test_official_mission_drift.py",
    "tests/python/test_release_integrity.py",'''
if files_anchor in text:
    text = text.replace(files_anchor, files_replacement, 1)

quality_anchor = '''    "tests/python/test_release_integrity.py",
    "docs/quality-assurance.md",'''
quality_replacement = '''    "tests/python/test_release_integrity.py",
    "docs/quality-assurance.md",
    "CATALOGUE_DRIFT.md",'''
if quality_anchor in text:
    text = text.replace(quality_anchor, quality_replacement, 1)

start_marker = '    workflow_text = (ROOT / ".github" / "workflows" / "import-official-uk-missions.yml").read_text(encoding="utf-8")'
end_marker = '    release_workflow = (ROOT / ".github" / "workflows" / "release-v1.yml").read_text(encoding="utf-8")'
start = text.find(start_marker)
end = text.find(end_marker, start)
if start < 0 or end < 0:
    raise SystemExit("Unable to locate catalogue refresh readiness policy anchors")

new_policy = '''    workflow_text = (ROOT / ".github" / "workflows" / "import-official-uk-missions.yml").read_text(encoding="utf-8")
    for marker in (
        "workflow_dispatch",
        "schedule:",
        "CANDIDATE_DIR: ${{ runner.temp }}/official-uk-candidate",
        "detect_official_mission_drift.py",
        "merge_verification_registry_batches.py",
        "steps.drift.outputs.has_drift == 'false'",
        "steps.drift.outputs.has_drift == 'true'",
        "reconcile_official_mission_coverage.py",
        "validate_official_mission_catalogue.py",
        "validate_official_key_mappings.py",
        "validate_official_patient_mappings.py",
        "validate_official_personnel_mappings.py",
        "validate_official_personnel_education_mappings.py",
        "validate_official_prisoner_mappings.py",
        "validate_official_recovery_mappings.py",
        "validate_official_operational_mappings.py",
        "python -m unittest discover -s tests/python",
        "report_canonical_candidates.py",
        "report_key_mapping_backlog.py",
        "generate_mission_verification_status.py",
        "validate_verification_programme_assets.py",
        "release_readiness.py",
        "data/validation/official-catalogue-drift.json",
        "docs/reference/official-catalogue-drift-report.md",
        "automation/official-catalogue-drift-${FINGERPRINT_SHORT}",
        "gh issue create",
        "gh pr create",
        "Fail closed on official drift",
    ):
        require(marker in workflow_text, f"Official catalogue drift workflow is missing control: {marker}")

    for forbidden in (
        "git push origin HEAD:main",
        "gh workflow run deploy-pages.yml --ref main",
        "Deploy refreshed catalogue",
        "git add -f",
        "data/sources/missionchief-uk \\",
        "docs/assets/data/official \\",
        "data/sources/missionchief-uk/mission-verification-status.json",
        "docs/assets/data/official/uk-mission-verification.json",
    ):
        require(
            forbidden not in workflow_text,
            f"Official catalogue drift workflow permits unsafe production mutation: {forbidden}",
        )

'''

text = text[:start] + new_policy + text[end:]
path.write_text(text, encoding="utf-8", newline="\n")
