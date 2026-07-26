#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

DIAGNOSTICS_DIR="${DIAGNOSTICS_DIR:-${RUNNER_TEMP:-/tmp}/missionchief-uk-full-data-audit}"
mkdir -p "$DIAGNOSTICS_DIR"

run_logged() {
  local log_path="$1"
  shift
  echo "## $*" | tee -a "$log_path"
  "$@" 2>&1 | tee -a "$log_path"
  echo | tee -a "$log_path"
}

: > "$DIAGNOSTICS_DIR/root-regressions.log"
run_logged "$DIAGNOSTICS_DIR/root-regressions.log" \
  python -m unittest discover -s tests -p 'test_*.py' -v

: > "$DIAGNOSTICS_DIR/synchronizers.log"
run_logged "$DIAGNOSTICS_DIR/synchronizers.log" python scripts/sync_conditional_resource_contract_integration.py
run_logged "$DIAGNOSTICS_DIR/synchronizers.log" python scripts/sync_conditional_resource_modes_integration.py
run_logged "$DIAGNOSTICS_DIR/synchronizers.log" python scripts/sync_recovery_contract_integration.py
run_logged "$DIAGNOSTICS_DIR/synchronizers.log" python scripts/sync_coastguard_generator_integration.py
run_logged "$DIAGNOSTICS_DIR/synchronizers.log" python scripts/sync_all_official_key_mappings.py
run_logged "$DIAGNOSTICS_DIR/synchronizers.log" python scripts/sync_prisoner_schema.py
run_logged "$DIAGNOSTICS_DIR/synchronizers.log" python scripts/run_ready_canonical_batch_generation.py --limit 200
run_logged "$DIAGNOSTICS_DIR/synchronizers.log" python scripts/sync_canonical_patient_fields.py
run_logged "$DIAGNOSTICS_DIR/synchronizers.log" python scripts/sync_canonical_personnel_fields.py
run_logged "$DIAGNOSTICS_DIR/synchronizers.log" python scripts/sync_canonical_personnel_education_fields.py
run_logged "$DIAGNOSTICS_DIR/synchronizers.log" python scripts/sync_canonical_prisoner_fields.py
run_logged "$DIAGNOSTICS_DIR/synchronizers.log" python scripts/sync_canonical_recovery_fields.py
run_logged "$DIAGNOSTICS_DIR/synchronizers.log" python scripts/sync_canonical_operational_fields.py

git status --porcelain --untracked-files=all > "$DIAGNOSTICS_DIR/synchronizer-status.txt"
git diff HEAD --binary -- . > "$DIAGNOSTICS_DIR/synchronizer.patch"
python scripts/check_validation_worktree.py synchronizer

python scripts/validate_data.py
python scripts/reconcile_official_mission_coverage.py
python scripts/validate_official_mission_catalogue.py
python scripts/merge_verification_registry_batches.py
python scripts/report_promoted_mapping_failures.py
python scripts/validate_official_key_mappings.py
python scripts/validate_official_patient_mappings.py
python scripts/validate_official_personnel_mappings.py
python scripts/validate_official_personnel_education_mappings.py
python scripts/validate_official_prisoner_mappings.py
python scripts/validate_official_recovery_mappings.py
python scripts/validate_official_operational_mappings.py
python scripts/generate_full_canonical_catalogue.py --check
python scripts/validate_vehicle_inventory.py
python scripts/generate_vehicle_field_resolution.py --check
python scripts/generate_vehicle_coverage.py --check
python -m unittest discover -s tests/python -p 'test_*.py' -v

python scripts/report_canonical_candidates.py --limit 200 > canonical-candidates.json
python scripts/report_key_mapping_backlog.py --limit 200 --examples 10 > key-mapping-backlog.json
python scripts/report_patient_field_contract.py
python scripts/report_operational_field_contract.py
python scripts/generate_mission_verification_status.py
python scripts/run_public_verification_sync.py
python scripts/sync_verification_batch_navigation.py
python scripts/validate_verification_programme_assets.py
python scripts/generate_exports.py
python scripts/generate_faq.py
python -m unittest discover -s tests/python -p 'test_release_integrity.py'
python scripts/release_readiness.py 2>&1 | tee "$DIAGNOSTICS_DIR/release-readiness.log"
python scripts/check_validation_worktree.py final-working-tree --allow-validation-generated-outputs

echo "Complete MissionChief UK data and generator audit passed."
