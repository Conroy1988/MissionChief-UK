# MissionChief UK Static Data API

MissionChief UK publishes three read-only evidence surfaces:

1. a versioned canonical API generated from normalised records;
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
Data version: 1.4.0
Released: 28 July 2026
Programme stage: 42
Canonical missions: 1,079
Official UK missions: 1,062
Direct official/canonical ID matches: 1,062
Fully canonical missions: 1,062
Canonical deployable resources: 104
Infrastructure records: 20
Training and role records: 12
Observed vehicle IDs mapped: 73 / 73
Vehicle field decisions resolved: 936 / 936
```

Version 1.4.0 retains the canonical v1 contract. It adds completed operational guidance, cross-service strategy and browser planning capabilities without changing existing collection-envelope, identifier or populated-field semantics.

## Canonical endpoints

| Endpoint | Purpose |
|---|---|
| `manifest.json` | Version, status, programme stage and canonical collection counts |
| `missions.json` | Canonical normalised mission records |
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
  "data_version": "1.4.0",
  "released_at": "2026-07-28",
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

## Browser-planning relationship

Public browser tools read these static endpoints directly:

- Mission Lookup consumes canonical missions and the separate official catalogue;
- Resource Comparison consumes vehicles and training records;
- Fleet Planner consumes canonical guaranteed and alternative mission rows;
- Query Catalogue consumes the canonical search index; and
- Account Readiness consumes canonical missions and vehicles plus user-entered browser-local inventory.

No browser tool writes to the API or authenticates against MissionChief.

## Versioning policy

- `v1` identifies the API contract generation.
- `data_version` identifies the current validated publication.
- Additive canonical records, evidence endpoints, optional fields and compatible tools may be published within v1.
- Breaking envelope or field changes require a new path such as `v2`.
- Official records and evidence ledgers remain under separate non-canonical paths.
- New official fields may appear additively without being normalised automatically.
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
- release metadata and matching release-note consistency;
- strict documentation, link and built-site audits;
- deployed HTTP and data smoke testing; and
- Chromium desktop, iPhone WebKit and iPad WebKit programme-route acceptance.

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
