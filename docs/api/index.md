# MissionChief UK Static Data API

MissionChief UK publishes two read-only public data tiers:

1. a versioned canonical API generated from the project’s normalized evidence records; and
2. a separate lossless snapshot of the complete public MissionChief UK mission catalogue, including reconciliation and verification-programme status.

The separation is deliberate. Official internal keys are not silently treated as verified canonical resources.

## Canonical API base

```text
https://conroy1988.github.io/MissionChief-UK/assets/data/v1/
```

## Current publication

```text
API contract: v1
Data version: 1.1.0
Released: 23 July 2026
Canonical missions: 69
Official UK missions: 1,062
Direct official/canonical ID matches: 52
Fully canonical missions: 11
```

Version 1.1.0 retains the canonical v1 contract, adds the complete official catalogue as a separate public data surface and exposes a deterministic route to 100% fully canonical mission coverage.

## Canonical endpoints

| Endpoint | Purpose |
|---|---|
| `manifest.json` | Version, status and canonical collection counts |
| `missions.json` | Canonical normalized mission records |
| `vehicles.json` | Canonical deployable-resource records |
| `infrastructure.json` | Canonical building and extension records |
| `training.json` | Canonical qualification and course records |
| `search-index.json` | Lightweight canonical cross-collection search index |
| `faq.json` | Generated FAQ entries |
| `openapi.json` | OpenAPI 3.1 contract for the canonical API |

## Official UK mission endpoints

Base:

```text
https://conroy1988.github.io/MissionChief-UK/assets/data/official/
```

| Endpoint | Purpose |
|---|---|
| `uk-missions.json` | Complete lossless official UK mission catalogue with source provenance |
| `uk-mission-coverage.json` | Reconciliation between official IDs and canonical mission records |
| `uk-mission-verification.json` | Every official mission’s current verification gate, blockers and next action |

The official catalogue currently contains 1,062 records. It preserves every field published by the UK mission feed and adds only:

- `official_url`;
- `limited_availability`; and
- normalized `availability.starts_at` and `availability.ends_at` values.

The verification endpoint is generated from the official catalogue, canonical records, explicit promotion registry and verified official-key mappings. It does not promote a record merely because its name exists in both collections.

## Canonical response envelope

Canonical collection endpoints use:

```json
{
  "schema_version": "1",
  "data_version": "1.1.0",
  "released_at": "2026-07-23",
  "collection": "missions",
  "count": 0,
  "records": []
}
```

The deployed count and records are generated during the build.

## Official catalogue envelope

```json
{
  "schema_version": "1",
  "collection": "official-uk-missions",
  "source": {
    "authority": "MissionChief UK",
    "url": "https://www.missionchief.co.uk/einsaetze.json",
    "fetched_at": "2026-07-22T21:40:36Z",
    "sha256": "..."
  },
  "count": 1062,
  "records": []
}
```

## Verification envelope

```json
{
  "schema_version": "1",
  "collection": "official-uk-mission-verification",
  "target_stage": "fully-canonical",
  "summary": {
    "official_count": 1062,
    "canonical_count": 69,
    "direct_canonical_id_matches": 52,
    "fully_canonical_percent": 1.04,
    "remaining_to_fully_canonical": 1051
  },
  "records": []
}
```

Each verification record contains:

- official mission ID and exact UK name;
- current verification stage and rank;
- official source URL;
- canonical file path where one exists;
- explicit registry decision where promoted;
- blocking reasons; and
- the next required verification action.

Consumers should use the source SHA-256 to detect an official-catalogue change, `data_version` to detect a canonical publication change and the verification summary to track progress toward 100% fully canonical coverage.

## Versioning policy

- The canonical URL segment `v1` identifies the API contract generation.
- Canonical `data_version` identifies the current validated publication.
- Additive canonical records and optional fields may be published within v1.
- Breaking canonical envelope or field changes require a new path such as `v2`.
- Official catalogue records follow the public upstream object and are therefore published under a separate non-canonical path.
- New official fields may appear additively without being normalized into canonical resources.
- Verification-stage changes are additive evidence updates and do not redefine the lossless official source record.
- Previous API directories should remain available when practical so integrations can migrate deliberately.

## Availability and caching

All endpoints are static GitHub Pages content. They have no authentication, write methods, query parameters or server-side filtering.

Consumers should:

- cache responses responsibly;
- use the canonical manifest to detect `data_version` changes;
- use the official catalogue SHA-256 to detect source changes;
- use the verification endpoint rather than inferring completeness from catalogue presence;
- avoid polling more frequently than needed; and
- preserve the distinction between official source fields and canonical mapped evidence.

## Validation contract

Every publication is checked against:

- canonical schema, ID and cross-record validation;
- offline official/canonical coverage reconciliation;
- official catalogue IDs, names, deterministic ordering and minimum scale;
- source URL, retrieval time and SHA-256 consistency;
- lossless preservation of every official source field;
- official/canonical reconciliation arithmetic;
- requirement, chance and prerequisite inventories;
- explicit official-to-canonical key mappings for every promoted mission;
- strict key equivalence where a mission is declared fully canonical;
- deterministic verification-stage, blocker and next-action generation;
- deterministic canonical collection and manifest generation;
- strict documentation, link and built-site audits;
- deployed HTTP, canonical API and official-data smoke testing; and
- Chromium, Firefox, iPhone WebKit and iPad WebKit acceptance.

## Evidence contract

Consumers must preserve the repository’s evidence semantics:

- omitted canonical fields are unknown, not zero;
- verified applies only to populated canonical fields;
- empty canonical mission requirement arrays may indicate unavailable response-table evidence;
- canonical alternative groups require a total from any qualifying combination;
- towing remains separate from dispatched emergency resources;
- official catalogue presence proves publication, not complete canonical interpretation;
- identity verification does not prove requirement or operational completeness; and
- unknown official requirement keys must not be guessed into vehicle or personnel mappings.

## Licence and attribution

Original project data and code are provided under the repository licence. MissionChief names and game-derived terminology remain the property of their respective owners.
