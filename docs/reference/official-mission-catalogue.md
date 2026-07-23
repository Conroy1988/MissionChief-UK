# Official UK Mission Catalogue

MissionChief UK publishes a complete searchable snapshot of the public United Kingdom mission catalogue alongside the project’s smaller, higher-trust canonical mission collection and an explicit programme to reach 100% fully canonical coverage.

## Three evidence states

| State | Purpose | Operational meaning |
|---|---|---|
| **Official catalogue** | Lossless snapshot of the public MissionChief UK mission feed | Confirms that a mission and its published official fields exist. Internal keys are retained verbatim and are not automatically treated as verified vehicle mappings. |
| **Canonical mapped** | Normalized records under `data/uk/missions/` | Resource IDs, alternatives, probabilities, patients, personnel and preconditions are represented only where the project has reproduced or suitably verified them. |
| **Fully canonical** | Canonical records promoted through the verification registry | Identity, every published key, operational mechanics and final evidence completeness have passed the enforced audit gates. |

Mission Lookup and the verification dashboard expose these states separately. A mission may therefore be fully searchable before every internal requirement key has been mapped into the canonical resource model.

## Current programme position

```text
1,062 official UK missions captured
69 canonical mission records
52 direct official/canonical ID matches
11 fully canonical missions
1,010 official missions awaiting direct canonical records
17 canonical-only overlays or derived records
```

The first fully canonical batch covers mission IDs `0`, `1`, `2`, `3`, `4`, `6`, `7`, `8`, `9`, `10` and `11`.

## Official source

The automated importer retrieves:

```text
https://www.missionchief.co.uk/einsaetze.json
```

Every successful refresh records:

- the official source URL;
- retrieval time;
- SHA-256 source digest;
- complete official record count;
- reconciliation against canonical mission IDs;
- distinct requirement, chance and prerequisite keys; and
- regenerated verification-stage status for every mission.

The importer rejects invalid JSON, duplicate IDs, missing names and implausibly small responses.

## Published browser data

The live site exposes:

```text
assets/data/official/uk-missions.json
assets/data/official/uk-mission-coverage.json
assets/data/official/uk-mission-verification.json
```

`uk-missions.json` preserves every official mission field and adds only three derived navigation fields:

- `official_url`;
- `limited_availability`;
- normalized `availability` start and end values.

`uk-mission-coverage.json` reconciles official IDs against current canonical records.

`uk-mission-verification.json` identifies each mission’s current gate, canonical path, blockers, explicit registry decision and next action.

The complete source snapshot, key inventories and generated verification source remain under:

```text
data/sources/missionchief-uk/
```

## Captured fields

The catalogue preserves the full official object rather than a fixed allow-list. Current UK records include fields such as:

- mission ID and name;
- generating service or filter;
- average credits;
- POIs and categories;
- guaranteed requirement keys;
- probability fields;
- generation prerequisites;
- patient ranges, specialisations and UK patient codes;
- transport and critical-care probabilities;
- required personnel and qualifications;
- mission duration;
- follow-up, expansion and subsequent missions;
- base mission IDs, overlays, additive overlays and variants;
- seasonal availability windows;
- any new top-level or `additional` field introduced by the game.

Mission Lookup presents common fields directly, provides a structured expandable table for additional values and retains the complete official JSON record on demand.

## Verification gates

Every official mission progresses through:

1. **Captured** — retained losslessly from the official feed.
2. **Identity verified** — official ID and exact UK name match a canonical record.
3. **Requirements mapped** — every requirement, chance and prerequisite key is explicitly verified or narrowly classified as non-operational.
4. **Operationally verified** — conditional mechanics, probabilities, patients, personnel, relationships and variants have reproducible evidence.
5. **Fully canonical** — final evidence-completeness audit passed.

A mission cannot be promoted merely because its name appears in both collections. Promotion requires an explicit registry decision and evidence sources.

## Official-key mappings

Verified mappings are stored in:

```text
data/uk/official-key-mappings.json
```

The first mappings establish:

- `requirements.firetrucks` → canonical `fire_engine` guaranteed quantity;
- `prerequisites.fire_stations` → canonical `fire_stations` minimum building count; and
- `prerequisites.main_building` as non-operational only while its official value is exactly `0`.

Any promoted mission containing an unmapped key fails validation. A non-operational classification must define a narrow allowed-value list; an unexpected upstream value also fails validation.

## Refresh and deployment

The dedicated refresh workflow checks the official source daily and may also be run manually. It is content-addressed: unchanged source and generated verification state produce no commit.

When the source or canonical state changes, the workflows:

1. download and validate the official feed when required;
2. reconcile the retained official records against current canonical IDs;
3. validate official-to-canonical key mappings;
4. regenerate mission verification status and blockers;
5. republish compact browser assets;
6. run deterministic catalogue and release audits;
7. commit only changed generated assets; and
8. dispatch the full Pages deployment and cross-browser acceptance suite.

## Local validation

```bash
python scripts/reconcile_official_mission_coverage.py
python scripts/validate_official_mission_catalogue.py
python scripts/validate_official_key_mappings.py
python scripts/generate_mission_verification_status.py
```

The audits independently check record counts, ordering, duplicate IDs, field preservation, source metadata, file-size limits, canonical reconciliation, key inventories, promoted-mission equivalence, verification stages and public/source equality.

## Accuracy boundary

Official catalogue values are reproduced as published. They are not silently converted into canonical vehicles, personnel or building requirements where the internal key has not been verified. The raw official key remains visible so later mapping work is auditable and reversible.

A **fully canonical** label applies only after the corresponding official record, canonical record, mapped keys, operational evidence and registry decision all pass the enforced programme checks.
