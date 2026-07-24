#!/usr/bin/env bash
set -Eeuo pipefail
DIAG="$RUNNER_TEMP/canonical-apply-diagnostic.log"
exec > >(tee -a "$DIAG") 2>&1
stage() { printf '\n=== %s ===\n' "$1"; }

stage 'verify seed'
seed_b64="$RUNNER_TEMP/canonical-100-seed.b64"
seed_archive="$RUNNER_TEMP/canonical-100-seed.tar.xz"
seed_manifest="$RUNNER_TEMP/canonical-100-seed-manifest.txt"
cat .handoff/canonical-100-seed.part.* > "$seed_b64"
echo "b7858115ff81d68f258d59520b1382634000cc5574ba851f0e5830eb3d73eab0  $seed_b64" | sha256sum --check --strict
base64 --decode "$seed_b64" > "$seed_archive"
echo "6317a49f3dc77c6fa32c1dfcfdeaf0c6b5f605a4c8291df22b7df5657103b1b2  $seed_archive" | sha256sum --check --strict
xz --test "$seed_archive"
tar -tJf "$seed_archive" > "$seed_manifest"
if grep -Eq '(^|/)\.git(/|$)|(^|/)\.agent(/|$)|(^|/)\.handoff(/|$)|(^|/)\.github/workflows/agent-' "$seed_manifest"; then
  echo 'The seed archive contains a forbidden control or transport path.' >&2
  exit 1
fi
cp data/uk/mission-verification-registry.json "$RUNNER_TEMP/base-mission-verification-registry.json"
python - <<'PY'
import json
from pathlib import Path
payload=json.loads(Path('data/uk/mission-verification-registry.json').read_text(encoding='utf-8'))
records=payload.get('records')
if not isinstance(records, dict) or len(records) != 21:
    raise SystemExit(f"Expected the 21-record keyed base registry; found {len(records) if isinstance(records, dict) else 'invalid'}")
PY
tar -xJf "$seed_archive" -C .

stage 'generate catalogue'
python scripts/generate_full_canonical_catalogue.py --checked-at 2026-07-24
python scripts/sync_conditional_resource_contract_integration.py
python scripts/sync_conditional_resource_modes_integration.py
python scripts/sync_recovery_contract_integration.py
python scripts/sync_coastguard_generator_integration.py
python scripts/sync_all_official_key_mappings.py
python scripts/sync_prisoner_schema.py
python scripts/run_ready_canonical_batch_generation.py --limit 200
python scripts/sync_canonical_patient_fields.py
python scripts/sync_canonical_personnel_fields.py
python scripts/sync_canonical_personnel_education_fields.py
python scripts/sync_canonical_prisoner_fields.py
python scripts/sync_canonical_recovery_fields.py
python scripts/sync_canonical_operational_fields.py

stage 'strict equivalence'
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

stage 'zero backlog'
candidate_report="$RUNNER_TEMP/canonical-candidates.json"
backlog_report="$RUNNER_TEMP/key-mapping-backlog.json"
python scripts/report_canonical_candidates.py --limit 1200 > "$candidate_report"
python scripts/report_key_mapping_backlog.py --limit 500 --examples 25 > "$backlog_report"
python - "$candidate_report" "$backlog_report" <<'PY'
import json, sys
from pathlib import Path
c=json.loads(Path(sys.argv[1]).read_text())
b=json.loads(Path(sys.argv[2]).read_text())
expected={'official_count':1062,'canonical_count':1079,'direct_canonical_count':1062,'fully_canonical_count':1062,'remaining_to_fully_canonical_count':0,'ready_count':0,'blocked_count':0}
for k,v in expected.items():
    if c.get(k) != v: raise SystemExit(f'Candidate report {k}: expected {v}, found {c.get(k)!r}')
for k in ('official_only_count','canonical_unpromoted_count','catalogue_unmapped_key_count','catalogue_unmapped_occurrence_count'):
    if b.get(k) != 0: raise SystemExit(f'Backlog report {k}: expected 0, found {b.get(k)!r}')
if b.get('official_count') != 1062 or b.get('fully_canonical_count') != 1062:
    raise SystemExit('Backlog report does not prove complete 1,062-mission coverage')
PY

stage 'publication validation'
python -m unittest discover -s tests -p 'test_*.py' -v
python -m unittest discover -s tests/python -p 'test_catalogue_reporting.py'
python scripts/generate_mission_verification_status.py --require-complete
python scripts/run_public_verification_sync.py
python scripts/sync_verification_batch_navigation.py
python scripts/validate_verification_programme_assets.py
python scripts/generate_exports.py
python scripts/generate_faq.py
python -m unittest discover -s tests/python -p 'test_release_integrity.py'
python scripts/release_readiness.py
python scripts/audit_links.py
python -m mkdocs build --strict --site-dir site
python scripts/release_readiness.py --site-dir site

stage 'restore durable registry model'
cp "$RUNNER_TEMP/base-mission-verification-registry.json" data/uk/mission-verification-registry.json
python scripts/generate_full_canonical_catalogue.py --check
python scripts/validate_data.py
python scripts/release_readiness.py

stage 'prepare commit'
rm -rf .handoff .agent site
rm -f scripts/agent_apply_canonical_coverage.sh
find . -type d -name __pycache__ -prune -exec rm -rf {} +
git config user.name 'github-actions[bot]'
git config user.email '41898282+github-actions[bot]@users.noreply.github.com'
git add -A
git clean -fd
git clean -fdX
if git diff --cached --diff-filter=AM --name-only | grep -Eq '(^|/)(\.agent|\.handoff)(/|$)|agent-apply-canonical-coverage|agent_apply_canonical_coverage|__pycache__|(^|/)site(/|$)'; then
  echo 'A temporary transport or validation path would be committed.' >&2
  git diff --cached --name-status
  exit 1
fi
git diff --cached --check
test -n "$(git diff --cached --name-only)"
echo "staged_files=$(git diff --cached --name-only | wc -l)"
git status --short
git commit -m 'Complete canonical coverage for all UK missions'

stage 'push commit'
git push origin HEAD:agent/canonical-coverage-100
