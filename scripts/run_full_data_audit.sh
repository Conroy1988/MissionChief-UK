#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

DIAGNOSTICS_DIR="${DIAGNOSTICS_DIR:-${RUNNER_TEMP:-/tmp}/full-data-audit}"
mkdir -p "$DIAGNOSTICS_DIR"
LOG_PATH="$DIAGNOSTICS_DIR/full-data-audit.log"
: > "$LOG_PATH"

run_check() {
  local label="$1"
  shift
  echo "[full-audit] $label"
  {
    echo "## $label"
    printf 'Command:'
    printf ' %q' "$@"
    echo
    "$@"
    echo
  } >> "$LOG_PATH" 2>&1 || {
    local code=$?
    echo "::error title=Full data audit failed::$label exited with status $code"
    echo "--- retained log tail ---"
    tail -80 "$LOG_PATH"
    return "$code"
  }
}

echo "[full-audit] root regressions"
run_check "root regressions" python -m unittest discover -s tests -p 'test_*.py' -v

echo "[full-audit] canonical synchronizers"
run_check "conditional resource contract sync" python scripts/sync_conditional_resource_contract_integration.py
run_check "conditional resource modes sync" python scripts/sync_conditional_resource_modes_integration.py
run_check "recovery contract sync" python scripts/sync_recovery_contract_integration.py
run_check "coastguard generator sync" python scripts/sync_coastguard_generator_integration.py
run_check "official key mapping sync" python scripts/sync_all_official_key_mappings.py
run_check "prisoner schema sync" python scripts/sync_prisoner_schema.py
run_check "ready canonical batch generation" python scripts/run_ready_canonical_batch_generation.py --limit 200
run_check "canonical patient sync" python scripts/sync_canonical_patient_fields.py
run_check "canonical personnel sync" python scripts/sync_canonical_personnel_fields.py
run_check "canonical personnel education sync" python scripts/sync_canonical_personnel_education_fields.py
run_check "canonical prisoner sync" python scripts/sync_canonical_prisoner_fields.py
run_check "canonical recovery sync" python scripts/sync_canonical_recovery_fields.py
run_check "canonical operational sync" python scripts/sync_canonical_operational_fields.py

git status --porcelain --untracked-files=all > "$DIAGNOSTICS_DIR/synchronizer-status.txt"
git diff HEAD --binary -- . > "$DIAGNOSTICS_DIR/synchronizer.patch"
run_check "synchronizer worktree contract" python scripts/check_validation_worktree.py synchronizer

echo "[full-audit] complete data and evidence validation"
run_check "canonical data" python scripts/validate_data.py
run_check "coverage reconciliation" python scripts/reconcile_official_mission_coverage.py
run_check "official mission catalogue" python scripts/validate_official_mission_catalogue.py
run_check "verification registry merge" python scripts/merge_verification_registry_batches.py
run_check "promoted mapping report" python scripts/report_promoted_mapping_failures.py
run_check "official key equivalence" python scripts/validate_official_key_mappings.py
run_check "official patient equivalence" python scripts/validate_official_patient_mappings.py
run_check "official personnel equivalence" python scripts/validate_official_personnel_mappings.py
run_check "official education equivalence" python scripts/validate_official_personnel_education_mappings.py
run_check "official prisoner equivalence" python scripts/validate_official_prisoner_mappings.py
run_check "official recovery equivalence" python scripts/validate_official_recovery_mappings.py
run_check "official operational equivalence" python scripts/validate_official_operational_mappings.py
run_check "complete canonical catalogue" python scripts/generate_full_canonical_catalogue.py --check
run_check "vehicle inventory" python scripts/validate_vehicle_inventory.py
run_check "vehicle field resolution" python scripts/generate_vehicle_field_resolution.py --check
run_check "vehicle coverage" python scripts/generate_vehicle_coverage.py --check
run_check "Python regression suite" python -m unittest discover -s tests/python -p 'test_*.py' -v

echo "[full-audit] publication and release integrity"
run_check "canonical candidate report" sh -c 'python scripts/report_canonical_candidates.py --limit 200 > canonical-candidates.json'
run_check "key mapping backlog" sh -c 'python scripts/report_key_mapping_backlog.py --limit 200 --examples 10 > key-mapping-backlog.json'
run_check "patient field contract" python scripts/report_patient_field_contract.py
run_check "operational field contract" python scripts/report_operational_field_contract.py
run_check "mission verification status" python scripts/generate_mission_verification_status.py
run_check "public verification sync" python scripts/run_public_verification_sync.py
run_check "batch navigation sync" python scripts/sync_verification_batch_navigation.py
run_check "verification programme assets" python scripts/validate_verification_programme_assets.py
run_check "public exports" python scripts/generate_exports.py
run_check "generated FAQ" python scripts/generate_faq.py
run_check "release integrity regressions" python -m unittest discover -s tests/python -p 'test_release_integrity.py'
run_check "release readiness" python scripts/release_readiness.py
run_check "final working tree contract" python scripts/check_validation_worktree.py final-working-tree --allow-validation-generated-outputs

echo "Complete MissionChief UK data and generator audit passed."
