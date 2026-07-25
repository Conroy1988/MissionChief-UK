#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parents[1]
VERSION = "1.3.0"
RELEASE_DATE = "2026-07-25"
HUMAN_DATE = "25 July 2026"
STAGE = 36


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8", newline="\n")


def replace_once(
    text: str,
    pattern: str,
    replacement: str | Callable[[re.Match[str]], str],
    label: str,
    *,
    flags: int = 0,
) -> str:
    updated, count = re.subn(pattern, replacement, text, count=1, flags=flags)
    if count != 1:
        raise RuntimeError(f"Expected one {label}; found {count}")
    return updated


def update_version_files() -> None:
    version = {
        "version": VERSION,
        "released_at": RELEASE_DATE,
        "stage": STAGE,
        "status": "production",
        "release_snapshot": {
            "official_missions": 1062,
            "canonical_missions": 1079,
            "direct_matches": 1062,
            "fully_canonical": 1062,
            "vehicles": 104,
            "infrastructure": 20,
            "training": 12,
        },
    }
    write("data/version.json", json.dumps(version, indent=2) + "\n")

    package = json.loads(read("package.json"))
    package["version"] = VERSION
    write("package.json", json.dumps(package, indent=2) + "\n")


def update_changelog() -> None:
    text = read("CHANGELOG.md")
    section = """## [1.3.0] — 2026-07-25

### Complete deployable-resource intelligence

- Expanded the canonical deployable-resource estate from 59 to 104 vehicles, aircraft, vessels, trailers, containers and specialist equipment.
- Mapped all 73 observed MissionChief UK vehicle type IDs with zero unresolved identities and 100% identity coverage.
- Added the complete official UK container fleet, Container Extension and verified bidirectional carrier relationships.
- Added official economics, staffing, training-duration, building-compatibility, resource-class, capacity, towing and deployment contracts where reproducible.
- Added Water Ladder with CAFS with verified official cost, crew and Fire Support building compatibility.
- Resolved all nine tracked operational fields for every canonical resource: 936 / 936 explicit evidence-safe decisions and zero unresolved decisions.
- Added deterministic field-resolution schemas, registries, public JSON endpoints, evidence pages, regression tests and permanent CI enforcement.
- Preserved raw documented-value completeness separately from decision coverage; unpublished values remain unknown rather than being converted into zeroes or guesses.

### Release and publication integrity

- Advanced the production programme to Stage 36 and the compatible Static Data API publication to v1.3.0.
- Reconciled README, roadmap, Command Centre, API documentation, generated FAQ, OpenAPI metadata and release artefacts with the completed Stage 36A baseline.
- Extended built-site release validation to cover the vehicle-coverage and field-resolution evidence endpoints.
- Retained the canonical API v1 contract and all existing mission, infrastructure and qualification identifiers.

"""
    text = replace_once(
        text,
        r"## \[Unreleased\]\n\nNo unreleased changes are currently recorded\.\n\n",
        "## [Unreleased]\n\nNo unreleased changes are currently recorded.\n\n" + section,
        "v1.3.0 changelog insertion",
    )
    write("CHANGELOG.md", text)


def update_readme() -> None:
    text = read("README.md")
    replacements = {
        r"RELEASE-v1\.2\.0": "RELEASE-v1.3.0",
        r"\]\(docs/releases/v1\.2\.0\.md\)": "](docs/releases/v1.3.0.md)",
        r"PROGRAMME-STAGE_35_COMPLETE": "PROGRAMME-STAGE_36_COMPLETE",
        r"STATIC_API-v1\.2\.0": "STATIC_API-v1.3.0",
        r"\[\*\*v1\.2\.0 Notes\*\*\]\(docs/releases/v1\.2\.0\.md\)": "[**v1.3.0 Notes**](docs/releases/v1.3.0.md)",
        r"The numbered core programme is complete through \*\*Stage 35\*\*\. Version \*\*1\.2\.0\*\* completes direct canonical coverage and strict evidence-controlled verification for every official UK mission\.": (
            "The numbered programme is complete through **Stage 36**. Version **1.3.0** combines complete canonical mission coverage with evidence-safe identity and field-decision coverage for the current UK deployable-resource estate."
        ),
        r"\| \*\*Public interface\*\* \| \*\*Static API v1\.2\.0\*\* \|": "| **Public interface** | **Static API v1.3.0** |",
    }
    for pattern, replacement in replacements.items():
        text, count = re.subn(pattern, replacement, text)
        if count < 1:
            raise RuntimeError(f"README replacement failed: {pattern}")

    insertion = """# 🚒 Stage 36 Resource Intelligence

The completed Stage 36A programme treats resource identity and operational-field evidence as separate contracts.

| Resource gate | Current position |
|---|---:|
| Observed UK vehicle type IDs mapped | **73 / 73 — 100.00%** |
| Canonical deployable resources | **104** |
| Tracked operational fields per resource | **9** |
| Field decisions resolved | **936 / 936 — 100.00%** |
| Unresolved field decisions | **0** |

Each field is classified as `documented`, `not_applicable`, `not_published` or `review_required`. A `not_published` decision means no reproducible current UK source publishes the value; it never means zero, free, unrestricted or untrained.

[Review vehicle coverage →](https://conroy1988.github.io/MissionChief-UK/reference/vehicle-coverage-status/) · [Audit field resolution →](https://conroy1988.github.io/MissionChief-UK/reference/vehicle-field-resolution/)

---

"""
    text = replace_once(
        text,
        r"(# 💯 Mission Verification Programme\n)",
        insertion + r"\1",
        "Stage 36 README section",
    )
    write("README.md", text)


def update_home() -> None:
    text = read("docs/index.md")
    text = text.replace('data-mcuk-metric="version">v1.2.0', 'data-mcuk-metric="version">v1.3.0')
    text = text.replace('data-mcuk-metric="stage">Stage 35', 'data-mcuk-metric="stage">Stage 36')
    text = text.replace("Released 24 July 2026", "Released 25 July 2026")
    text = text.replace(
        "A complete UK mission catalogue with every official mission directly mapped, fully canonical, searchable and protected by strict source-equivalence validation.",
        "A complete UK mission catalogue and deployable-resource intelligence platform with 100% canonical mission coverage, 73/73 observed vehicle identities mapped and 936/936 resource-field decisions resolved.",
    )
    text = text.replace(
        "[Track 100% verification](reference/mission-verification-status.md){ .md-button }",
        "[Track mission verification](reference/mission-verification-status.md){ .md-button }\n[Audit resource resolution](reference/vehicle-field-resolution.md){ .md-button }",
    )
    text = text.replace(
        "<h3>Complete official coverage and 100% fully canonical intelligence</h3>",
        "<h3>Complete mission coverage and evidence-safe Stage 36 resource intelligence</h3>",
    )
    vehicle_card = """
<a class="mcuk-command-card mcuk-command-card--red" href="reference/vehicle-field-resolution/">
  <span class="mcuk-command-icon">08</span>
  <small>STAGE 36 RESOURCE EVIDENCE</small>
  <strong>Vehicle Field Resolution</strong>
  <p>Audit 936 explicit decisions across 104 resources without converting unpublished values into zeroes or guesses.</p>
  <em>Inspect resolution →</em>
</a>
"""
    text = replace_once(text, r"(</a>\n\n</div>\n\n## Live intelligence estate)", r"</a>\n" + vehicle_card + r"\n</div>\n\n## Live intelligence estate", "home resource card")
    write("docs/index.md", text)


def update_roadmap() -> None:
    write(
        "docs/ROADMAP.md",
        """# Project Roadmap

MissionChief UK is maintained as an evidence-led information system rather than a one-off collection of articles.

## Core programme status

**Stages 1–36 are delivered.**

```text
1,079 canonical mission records
1,062 / 1,062 official missions fully canonical
104 deployable-resource records
20 infrastructure records
12 qualification records
73 / 73 observed vehicle type IDs mapped
936 / 936 vehicle field decisions resolved
Static Data API v1.3.0
```

## Delivered foundation — Stages 1–12

- [x] project identity and information architecture
- [x] player journey and service-guide framework
- [x] vehicle, mission, building, personnel and training models
- [x] planning-tool architecture
- [x] evidence and verification standards
- [x] contribution controls and templates
- [x] Draft 2020-12 schemas and recursive validation
- [x] GitHub Pages delivery through Actions

## Delivered operational data — Stages 13–20

- [x] Fire and Rescue baseline and resource integrity
- [x] Ambulance and Police alternatives, patients and personnel
- [x] Coastguard, Lifeboat, trailer and ocean-rescue modelling
- [x] Mountain Rescue resources and explicit mission variants
- [x] Search and Rescue HQ, active Drone and missing-person operations
- [x] Bomb Disposal infrastructure and initial mission sequence
- [x] Airfield Operations, airport infrastructure and Code C/F incidents
- [x] Recovery Centres, HGV extensions and structured towing outcomes

## Delivered completion programme — Stages 21–35

- [x] Stage 21 — Railway response
- [x] Stage 22 — Specialist infrastructure
- [x] Stage 23 — Qualifications
- [x] Stage 24 — Vehicle economics and staffing
- [x] Stage 25 — Bomb Disposal enrichment
- [x] Stage 26 — Airfield enrichment
- [x] Stage 27 — Recovery enrichment
- [x] Stage 28 — Deterministic generated exports
- [x] Stage 29 — Complete browser-side mission lookup
- [x] Stage 30 — Resource and qualification comparison
- [x] Stage 31 — Concurrent fleet planning
- [x] Stage 32 — Deterministic query catalogue
- [x] Stage 33 — Generated FAQ
- [x] Stage 34 — Static Data API v1
- [x] Stage 35 — Complete canonical coverage for all 1,062 official UK missions

## Stage 36A — Complete deployable-resource coverage

**Status: complete.**

- [x] establish an evidence-tiered UK vehicle type ledger
- [x] compare source identities with canonical deployable-resource records
- [x] publish identity and raw field-completeness coverage separately
- [x] block duplicate IDs, dangling mappings and stale generated reports in CI
- [x] map every observed current UK vehicle type ID
- [x] create or reconcile every missing canonical resource identity
- [x] add official economics, staffing, training, building, towing, capacity and deployment contracts where reproducible
- [x] classify every tracked field as documented, not applicable, not published or review required
- [x] reach 73 / 73 observed identities with zero unresolved mappings
- [x] resolve 936 / 936 field decisions across 104 canonical resources
- [x] publish permanent schemas, JSON endpoints, evidence pages and regression enforcement
- [x] preserve unpublished values as unknown rather than zero

### Completion result

```text
104 canonical deployable resources
73 / 73 observed vehicle type IDs mapped
0 unresolved observed identities
9 tracked operational fields per resource
936 / 936 explicit field decisions resolved
0 unresolved field decisions
100% identity coverage
100% field-decision coverage
```

Canonical-only resources without an observed type-ID entry are explicit overlays or equipment records and do not represent an unresolved observed identity.

## Ongoing evidence maintenance

The numbered completion programmes are delivered. Remaining work is continuous source monitoring and evidence enrichment:

- reproduce additional published prices, staffing and training durations when suitable evidence appears;
- directly reproduce community-candidate type IDs in the current authenticated UK interface;
- verify currently unavailable EOD and Recovery response tables;
- add new UK missions, vehicles and game changes through fail-closed drift review;
- test overlapping alternative-resource dispatch allocation;
- enrich infrastructure cost, capacity and parent-building data;
- maintain API compatibility and publish future versioned releases;
- improve tools only when new verified fields support transparent calculations.

## Definition of complete

A subject is complete only when:

1. terminology and aliases are searchable;
2. exact values are verified and dated where they are published;
3. dependencies, alternatives, conditions and overlays are explicit;
4. unpublished and not-applicable fields have explicit decisions;
5. evidence boundaries are stated;
6. related documentation and structured records are linked;
7. validation covers the relevant relationships; and
8. a player can act without relying on an unexplained assumption.
""",
    )


def update_api() -> None:
    write(
        "docs/api/index.md",
        """# MissionChief UK Static Data API

MissionChief UK publishes three read-only evidence surfaces:

1. a versioned canonical API generated from normalized records;
2. a lossless snapshot and verification status for the complete official UK mission catalogue; and
3. deterministic UK vehicle identity, completeness and field-resolution evidence.

Official internal keys and unpublished resource values are never silently treated as verified canonical data.

## Canonical API base

```text
https://conroy1988.github.io/MissionChief-UK/assets/data/v1/
```

## Current publication

```text
API contract: v1
Data version: 1.3.0
Released: 25 July 2026
Programme stage: 36
Canonical missions: 1,079
Official UK missions: 1,062
Direct official/canonical ID matches: 1,062
Fully canonical missions: 1,062
Canonical deployable resources: 104
Observed vehicle IDs mapped: 73 / 73
Vehicle field decisions resolved: 936 / 936
```

Version 1.3.0 retains the canonical v1 contract. It adds Stage 36 resource records and evidence endpoints without changing existing envelope or identifier semantics.

## Canonical endpoints

| Endpoint | Purpose |
|---|---|
| `manifest.json` | Version, status, programme stage and canonical collection counts |
| `missions.json` | Canonical normalized mission records |
| `vehicles.json` | Canonical deployable-resource records |
| `infrastructure.json` | Canonical building and extension records |
| `training.json` | Canonical qualification and course records |
| `search-index.json` | Lightweight canonical cross-collection search index |
| `faq.json` | Generated FAQ entries |
| `openapi.json` | OpenAPI 3.1 contract for the canonical API |

## Official and evidence endpoints

Base:

```text
https://conroy1988.github.io/MissionChief-UK/assets/data/official/
```

| Endpoint | Purpose |
|---|---|
| `uk-missions.json` | Complete lossless official UK mission catalogue with source provenance |
| `uk-mission-coverage.json` | Reconciliation between official mission IDs and canonical records |
| `uk-mission-verification.json` | Every official mission’s verification gate, blockers and next action |
| `uk-vehicle-coverage.json` | Observed vehicle-ID reconciliation and raw documented-field completeness |
| `uk-vehicle-field-resolution.json` | Explicit decision for nine tracked operational fields across every canonical resource |

## Canonical response envelope

```json
{
  "schema_version": "1",
  "data_version": "1.3.0",
  "released_at": "2026-07-25",
  "collection": "missions",
  "count": 1079,
  "records": []
}
```

## Vehicle field-resolution envelope

```json
{
  "schema_version": "1",
  "collection": "uk-vehicle-field-resolution",
  "status": "complete",
  "summary": {
    "canonical_records": 104,
    "tracked_fields": 9,
    "total_decisions": 936,
    "resolved_decisions": 936,
    "unresolved_decisions": 0,
    "resolution_percent": 100.0
  },
  "records": []
}
```

Each resource-field decision uses one of four statuses:

| Status | Meaning |
|---|---|
| `documented` | A reproducible current UK source publishes the value or contract |
| `not_applicable` | The field does not apply to the resource under the verified model |
| `not_published` | No retained reproducible current UK source publishes the value |
| `review_required` | Evidence is incomplete or contradictory and requires renewed review |

`not_published` never means zero, free, unrestricted or untrained.

## Mission verification envelope

```json
{
  "schema_version": "1",
  "collection": "official-uk-mission-verification",
  "target_stage": "fully-canonical",
  "summary": {
    "official_count": 1062,
    "canonical_count": 1079,
    "direct_canonical_id_matches": 1062,
    "fully_canonical_percent": 100.00,
    "remaining_to_fully_canonical": 0
  },
  "records": []
}
```

## Versioning policy

- `v1` identifies the API contract generation.
- `data_version` identifies the current validated publication.
- Additive canonical records, evidence endpoints and optional fields may be published within v1.
- Breaking envelope or field changes require a new path such as `v2`.
- Official records and evidence ledgers remain under separate non-canonical paths.
- New official fields may appear additively without being normalized automatically.
- Previous API directories should remain available when practical.

## Availability and caching

All endpoints are static GitHub Pages content with no authentication, write methods, query parameters or server-side filtering.

Consumers should cache responsibly, use the manifest to detect `data_version` changes, use official source hashes for mission drift and preserve evidence-tier distinctions.

## Validation contract

Every publication is checked against:

- canonical schemas, identifiers and relationships;
- official mission losslessness, identity and strict equivalence;
- complete mission verification and zero unmapped-key backlog;
- vehicle-ledger uniqueness, mapping integrity and identity coverage;
- deterministic vehicle field-resolution schemas and 936 / 936 decision coverage;
- deterministic collections, manifest, OpenAPI and FAQ generation;
- strict documentation, link and built-site audits;
- deployed HTTP and data smoke testing; and
- Chromium, Firefox, iPhone WebKit and iPad WebKit acceptance.

## Evidence contract

Consumers must preserve these semantics:

- omitted canonical fields are unknown, not zero;
- verified applies only to populated canonical fields;
- a resolved field decision does not imply a published numeric value;
- empty mission requirement arrays may mean dispatch evidence is unavailable;
- alternative groups require a qualifying combination total;
- towing remains separate from emergency resources;
- official presence proves publication, not complete interpretation; and
- unknown official keys must not be guessed.

## Licence and attribution

Original project data and code are provided under the repository licence. MissionChief names and game-derived terminology remain the property of their respective owners.
""",
    )


def create_release_notes() -> None:
    write(
        "docs/releases/v1.3.0.md",
        """# MissionChief UK v1.3.0

**Released:** 25 July 2026<br>
**Release type:** Complete Stage 36 deployable-resource intelligence<br>
**Static Data API:** v1.3.0, backwards compatible with the v1 contract

MissionChief UK v1.3.0 publishes the completed Stage 36A resource programme while retaining complete canonical coverage for every official UK mission.

## Production result

```text
1,062 official UK mission records
1,079 canonical mission records
1,062 direct official/canonical ID matches
1,062 fully canonical mission records
0 official records awaiting direct canonical records
17 canonical overlay or derived records without standalone official IDs
104 canonical deployable-resource records
20 canonical infrastructure records
12 qualification records
73 / 73 observed UK vehicle type IDs mapped
936 / 936 vehicle field decisions resolved
Static Data API v1.3.0
```

## Stage 36A identity result

- all **73 / 73** observed UK vehicle type IDs map to canonical resource identities;
- **0** observed identities remain unresolved;
- identity coverage is **100%**;
- canonical-only equipment, containers and overlays remain explicit rather than being misclassified as missing observed IDs.

## Field-resolution contract

Nine operational fields are tracked for each of the 104 canonical resources:

1. cost;
2. staffing;
3. training label;
4. structured training requirements;
5. building requirements;
6. resource class;
7. transport capacity;
8. towing; and
9. deployment.

The release contains **936 / 936** explicit decisions and **0** unresolved decisions. Each decision is classified as `documented`, `not_applicable`, `not_published` or `review_required`.

A `not_published` decision does not mean zero, free, unrestricted or untrained. Raw documented-value completeness remains separately visible.

## Resource expansion

Stage 36A expands and enriches the resource estate through five evidence-controlled batches:

- Public Order and specialist Police vehicles;
- complete observed type-ID reconciliation;
- official Coastguard, Lifeboat, technical rescue, foam and drone contracts;
- Academy course durations, HART and specialist-building compatibility;
- Container Vehicle, ten official UK container pods and Container Extension; and
- Water Ladder with CAFS plus the final field-resolution registry.

## Public evidence surfaces

The release adds or formalizes:

- `uk-vehicle-coverage.json`;
- `uk-vehicle-field-resolution.json`;
- vehicle identity and field-resolution reference pages;
- Draft 2020-12 field-resolution schema;
- deterministic generation and stale-output checks;
- dedicated vehicle inventory and field-resolution regressions; and
- permanent GitHub Actions enforcement.

## Validation

The release pipeline requires:

- complete canonical and official mission validation;
- 73 / 73 vehicle identity mapping with zero dangling mappings;
- 936 / 936 field decisions and zero unresolved decisions;
- deterministic field-resolution, coverage, API and FAQ generation;
- release-integrity and verification-programme regressions;
- link and anchor auditing;
- strict MkDocs build and built-site equality checks;
- exact-SHA GitHub Pages deployment; and
- desktop, iPhone and iPad browser acceptance.

## Compatibility

The public API remains on contract path `v1`. Existing mission, vehicle, infrastructure and training envelopes and identifiers remain compatible. Version metadata advances to `1.3.0` to identify the new validated publication.

## Independence

MissionChief UK is an independent community project maintained by Conroy1988. It is not operated by, endorsed by or affiliated with SHPlay GmbH or the official MissionChief team.
""",
    )


def update_mkdocs() -> None:
    text = read("mkdocs.yml")
    text = replace_once(
        text,
        r"(  - Project:\n      - Quality Assurance: quality-assurance\.md\n)",
        r"\1      - v1.3.0 Release Notes: releases/v1.3.0.md\n",
        "MkDocs v1.3.0 navigation",
    )
    write("mkdocs.yml", text)


def update_hero() -> None:
    text = read("assets/readme/mission-control-hero.svg")
    text = text.replace("v1.2.0", "v1.3.0")
    text = text.replace("STAGE 35 COMPLETE", "STAGE 36 COMPLETE")
    text = text.replace(">1,169<", ">1,215<")
    text = text.replace(
        "Every official UK mission mapped · Every operational contract verified · Read-only data published",
        "Every official UK mission mapped · Every resource field explicitly resolved · Read-only data published",
    )
    write("assets/readme/mission-control-hero.svg", text)


def update_release_readiness() -> None:
    text = read("scripts/release_readiness.py")
    text = replace_once(
        text,
        r'require\(release\.get\("stage"\) == 35, "The v1\.2 release must identify Stage 35"\)',
        'stage = release.get("stage")\n    require(\n        isinstance(stage, int) and not isinstance(stage, bool) and stage >= 35,\n        "Release metadata must identify Stage 35 or later",\n    )',
        "generic release stage validation",
    )
    text = replace_once(
        text,
        r'require\(\n        "stage_35_complete" in readme_lower or "stage 35 complete" in readme_words,\n        "README stage badge is not synchronized to Stage 35",\n    \)',
        'stage = int(release["stage"])\n    require(\n        f"stage_{stage}_complete" in readme_lower or f"stage {stage} complete" in readme_words,\n        f"README stage badge is not synchronized to Stage {stage}",\n    )',
        "dynamic README stage audit",
    )
    text = text.replace(
        '        "reference/generated-faq/index.html",\n',
        '        "reference/generated-faq/index.html",\n        "reference/vehicle-coverage-status/index.html",\n        "reference/vehicle-field-resolution/index.html",\n',
    )
    text = text.replace(
        '        "assets/data/official/uk-mission-verification.json",\n',
        '        "assets/data/official/uk-mission-verification.json",\n        "assets/data/official/uk-vehicle-coverage.json",\n        "assets/data/official/uk-vehicle-field-resolution.json",\n',
    )
    text = replace_once(
        text,
        r'for filename in \("uk-missions\.json", "uk-mission-coverage\.json", "uk-mission-verification\.json"\):',
        'for filename in (\n        "uk-missions.json",\n        "uk-mission-coverage.json",\n        "uk-mission-verification.json",\n        "uk-vehicle-coverage.json",\n        "uk-vehicle-field-resolution.json",\n    ):',
        "built official evidence equality loop",
    )
    write("scripts/release_readiness.py", text)


def update_public_sync() -> None:
    text = read("scripts/sync_public_verification_metrics.py")
    text = text.replace(
        'RELEASE_PATH = ROOT / "docs" / "releases" / "v1.2.0.md"',
        'VERSION_PATH = ROOT / "data" / "version.json"',
    )
    replacement = '''def sync_release(text: str, metrics: dict[str, int | float], batches: dict[int, list[str]]) -> str:
    del metrics, batches
    snapshot = release_snapshot_counts()
    awaiting = snapshot["official_missions"] - snapshot["direct_matches"]
    overlays = snapshot["canonical_missions"] - snapshot["direct_matches"]
    baseline_values = (
        (r"[\\d,]+ official UK mission records", f"{format_number(snapshot['official_missions'])} official UK mission records", "release official baseline"),
        (r"[\\d,]+ canonical mission records", f"{format_number(snapshot['canonical_missions'])} canonical mission records", "release canonical baseline"),
        (r"[\\d,]+ direct official/canonical ID matches", f"{format_number(snapshot['direct_matches'])} direct official/canonical ID matches", "release direct baseline"),
        (r"[\\d,]+ fully canonical mission records", f"{format_number(snapshot['fully_canonical'])} fully canonical mission records", "release fully baseline"),
        (r"[\\d,]+ official records awaiting direct canonical records", f"{format_number(awaiting)} official records awaiting direct canonical records", "release awaiting baseline"),
        (r"[\\d,]+ canonical overlay or derived records without standalone official IDs", f"{format_number(overlays)} canonical overlay or derived records without standalone official IDs", "release overlay baseline"),
        (r"[\\d,]+ canonical deployable-resource records", f"{format_number(snapshot['vehicles'])} canonical deployable-resource records", "release resource baseline"),
        (r"[\\d,]+ canonical infrastructure records", f"{format_number(snapshot['infrastructure'])} canonical infrastructure records", "release infrastructure baseline"),
        (r"[\\d,]+ qualification records", f"{format_number(snapshot['training'])} qualification records", "release qualification baseline"),
    )
    for pattern, replacement_value, label in baseline_values:
        text = replace_once(text, pattern, replacement_value, label)
    return text


def sync_changelog'''
    text = replace_once(
        text,
        r"def sync_release\(.*?\ndef sync_changelog",
        replacement,
        "generic release synchronization",
        flags=re.DOTALL,
    )
    text = replace_once(
        text,
        r"updates = \{\n            README_PATH:",
        'release_document = read_json(VERSION_PATH)\n        if not isinstance(release_document, dict) or not isinstance(release_document.get("version"), str):\n            raise SyncFailure("Release metadata version is invalid")\n        release_path = ROOT / "docs" / "releases" / f"v{release_document[\'version\']}.md"\n        updates = {\n            README_PATH:',
        "dynamic release path initialization",
    )
    text = text.replace(
        "            RELEASE_PATH: sync_release(RELEASE_PATH.read_text(encoding=\"utf-8\"), metrics, batches),",
        "            release_path: sync_release(release_path.read_text(encoding=\"utf-8\"), metrics, batches),",
    )
    write("scripts/sync_public_verification_metrics.py", text)


def update_workflow_contracts() -> None:
    text = read(".github/workflows/branch-validation-report.yml")
    text = replace_once(
        text,
        r"          publication_paths=\(\n",
        '''          release_version="$(python - <<'PY'\nimport json\nfrom pathlib import Path\nprint(json.loads(Path("data/version.json").read_text(encoding="utf-8"))["version"])\nPY\n          )"\n          publication_paths=(\n''',
        "dynamic validation release version",
    )
    text = text.replace("            docs/releases/v1.2.0.md", '            "docs/releases/v${release_version}.md"')
    write(".github/workflows/branch-validation-report.yml", text)

    text = read("scripts/validate_verification_programme_assets.py")
    text = text.replace(
        '        "docs/releases/v1.2.0.md",',
        '        "data/version.json",\n        \'docs/releases/v${release_version}.md\',',
    )
    write("scripts/validate_verification_programme_assets.py", text)


def update_vehicle_completion_contract() -> None:
    text = read("scripts/vehicle_inventory.py")
    text = replace_once(
        text,
        r'"status": "complete"\n        if not unresolved and not dangling and not canonical_only\n        else "in-progress",',
        '"status": "complete"\n        if (\n            not unresolved\n            and not dangling\n            and field_resolution["summary"].get("unresolved_decisions") == 0\n            and field_resolution["summary"].get("resolution_percent") == 100.0\n        )\n        else "in-progress",',
        "vehicle completion semantics",
    )
    write("scripts/vehicle_inventory.py", text)

    text = read("scripts/generate_vehicle_coverage.py")
    text = text.replace("## Canonical records awaiting source-ledger mapping", "## Canonical records without an observed source-ledger ID")
    text = text.replace(
        "Decision coverage distinguishes documented values, fields that are not applicable, and values that are not published by a reproducible current UK source. It does not convert unknown values into zeroes or guesses.",
        "Decision coverage distinguishes documented values, fields that are not applicable, and values that are not published by a reproducible current UK source. It does not convert unknown values into zeroes or guesses. Canonical-only equipment and overlay records do not block completion when every observed ledger identity is mapped and every tracked field has an explicit decision.",
    )
    write("scripts/generate_vehicle_coverage.py", text)

    text = read("tests/python/test_vehicle_inventory.py")
    insertion = '''\n    def test_canonical_only_records_do_not_block_complete_programme(self) -> None:\n        document = self.document([inventory_record(1, "Mapped", "mapped")])\n        records = validate_inventory_document(document)\n        canonical = {\n            "mapped": {\n                "id": "mapped",\n                "name": "Mapped",\n                "service": "fire",\n                "verification": {"status": "verified", "checked_at": "2026-07-25", "sources": ["https://example.test"]},\n            },\n            "canonical_only": {\n                "id": "canonical_only",\n                "name": "Canonical only",\n                "service": "police",\n                "verification": {"status": "verified", "checked_at": "2026-07-25", "sources": ["https://example.test"]},\n            },\n        }\n\n        report = build_vehicle_coverage(document, records, canonical, field_resolution_document(len(canonical)))\n\n        self.assertEqual(report["status"], "complete")\n        self.assertEqual(report["summary"]["unresolved_inventory_entries"], 0)\n        self.assertEqual(report["summary"]["canonical_records_without_inventory_entry"], 1)\n        self.assertEqual(report["field_resolution"]["resolution_percent"], 100.0)\n'''
    text = replace_once(
        text,
        r"\n    def test_dangling_mapping_is_reported",
        insertion + "\n    def test_dangling_mapping_is_reported",
        "canonical-only completion regression",
    )
    write("tests/python/test_vehicle_inventory.py", text)


def update_faq_generator() -> None:
    text = read("scripts/generate_faq.py")
    marker = '''        {\n            "question": "Can I use this data programmatically?",'''
    addition = '''        {\n            "question": "Does 100% vehicle field resolution mean every value is published?",\n            "answer": "No. It means each of nine tracked fields for every canonical resource has an explicit evidence decision: documented, not applicable, not published or review required. A not-published decision never means zero, free, unrestricted or untrained.",\n        },\n'''
    if marker not in text:
        raise RuntimeError("FAQ insertion marker missing")
    text = text.replace(marker, addition + marker, 1)
    write("scripts/generate_faq.py", text)


def main() -> int:
    update_version_files()
    update_changelog()
    update_readme()
    update_home()
    update_roadmap()
    update_api()
    create_release_notes()
    update_mkdocs()
    update_hero()
    update_release_readiness()
    update_public_sync()
    update_workflow_contracts()
    update_vehicle_completion_contract()
    update_faq_generator()
    print("Prepared MissionChief UK v1.3.0 source release alignment.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
