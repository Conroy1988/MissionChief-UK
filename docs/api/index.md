# MissionChief UK Static Data API

MissionChief UK publishes two read-only public data tiers:

1. a versioned canonical API generated from normalized evidence records; and
2. a separate lossless snapshot of the complete public MissionChief UK mission catalogue, including reconciliation and verification status.

Official internal keys are never silently treated as canonical resources.

## Canonical API base

```text
https://conroy1988.github.io/MissionChief-UK/assets/data/v1/
```

## Current publication

```text
API contract: v1
Data version: 1.1.0
Released: 23 July 2026
Canonical missions: 281
Official UK missions: 1,062
Direct official/canonical ID matches: 264
Fully canonical missions: 223
```

Version 1.1.0 retains the canonical v1 contract, adds the complete official catalogue as a separate surface and exposes a deterministic route to 100% fully canonical coverage.

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
| `uk-missions.json` | Complete lossless official UK catalogue with source provenance |
| `uk-mission-coverage.json` | Reconciliation between official IDs and canonical records |
| `uk-mission-verification.json` | Every official mission’s verification gate, blockers and next action |

The official catalogue contains 1,062 records. It preserves every published field and adds only:

- `official_url`;
- `limited_availability`; and
- normalized `availability.starts_at` and `availability.ends_at` values.

The verification endpoint is generated after merging the base registry with scalable batch registries. A record is never promoted merely because its name exists in both collections.

## Canonical response envelope

```json
{
  "schema_version": "1",
  "data_version": "1.1.0",
  "released_at": "2026-07-23",
  "collection": "missions",
  "count": 281,
  "records": []
}
```

The deployed records are generated during the build.

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
    "canonical_count": 281,
    "direct_canonical_id_matches": 264,
    "fully_canonical_percent": 21.00,
    "remaining_to_fully_canonical": 839
  },
  "records": []
}
```

Each verification record contains:

- official mission ID and exact UK name;
- current verification stage and rank;
- official source URL;
- canonical path where one exists;
- explicit registry decision where promoted;
- blocking reasons; and
- the next required action.

Consumers should use the source SHA-256 to detect catalogue changes, `data_version` for canonical publications and the verification summary for progress toward 100%.

## Versioning policy

- `v1` identifies the API contract generation.
- `data_version` identifies the current validated publication.
- Additive canonical records and optional fields may be published within v1.
- Breaking envelope or field changes require a new path such as `v2`.
- Official records remain under a separate non-canonical path.
- New official fields may appear additively without being normalized automatically.
- Verification-stage changes are additive evidence updates.
- Previous API directories should remain available when practical.

## Availability and caching

All endpoints are static GitHub Pages content with no authentication, write methods, query parameters or server-side filtering.

Consumers should:

- cache responses responsibly;
- use the manifest to detect `data_version` changes;
- use the official SHA-256 to detect source changes;
- use the verification endpoint instead of inferring completeness from catalogue presence;
- avoid unnecessary polling; and
- preserve evidence-tier distinctions.

## Validation contract

Every publication is checked against:

- canonical schemas, identifiers and relationships;
- offline official/canonical coverage reconciliation;
- official catalogue scale, ordering and identity;
- source URL, retrieval time and SHA-256 consistency;
- lossless preservation of every official field;
- requirement, chance and prerequisite inventories;
- merged verification batch registries;
- aggregate promoted-mission identity diagnostics;
- explicit official-key mappings for every promoted mission;
- strict chance-aware key equivalence for fully canonical missions;
- deterministic verification stages, blockers and actions;
- evidence-safe candidate and key-backlog analysis;
- deterministic collections, manifest and FAQ generation;
- strict documentation, link and built-site audits;
- deployed HTTP and data smoke testing; and
- Chromium, Firefox, iPhone WebKit and iPad WebKit acceptance.

## Evidence contract

Consumers must preserve these semantics:

- omitted canonical fields are unknown, not zero;
- verified applies only to populated canonical fields;
- empty requirement arrays may mean dispatch evidence is unavailable;
- alternative groups require a qualifying combination total;
- towing remains separate from emergency resources;
- official presence proves publication, not complete interpretation;
- identity verification does not prove operational completeness; and
- unknown official keys must not be guessed.

## Licence and attribution

Original project data and code are provided under the repository licence. MissionChief names and game-derived terminology remain the property of their respective owners.
