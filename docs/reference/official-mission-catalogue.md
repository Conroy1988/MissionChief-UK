# Official UK Mission Catalogue

MissionChief UK publishes a complete searchable snapshot of the public United Kingdom mission catalogue alongside the project’s smaller, higher-trust canonical mission collection.

## Two evidence tiers

| Tier | Purpose | Operational meaning |
|---|---|---|
| **Canonical mapped** | Normalized records under `data/uk/missions/` | Resource IDs, alternatives, probabilities, patients, personnel and preconditions are represented only where the project has reproduced or suitably verified them. |
| **Official catalogue** | Lossless snapshot of the public MissionChief UK mission feed | Confirms that a mission and its published official fields exist. Internal keys are retained verbatim and are not automatically treated as verified vehicle mappings. |

The Mission Lookup labels these tiers separately. A mission may therefore be fully searchable before every internal requirement key has been mapped into the canonical resource model.

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
- distinct requirement, chance and prerequisite keys.

The importer rejects invalid JSON, duplicate IDs, missing names and implausibly small responses.

## Published browser data

The live site exposes:

```text
assets/data/official/uk-missions.json
assets/data/official/uk-mission-coverage.json
```

`uk-missions.json` preserves every official mission field and adds only three derived navigation fields:

- `official_url`;
- `limited_availability`;
- normalized `availability` start and end values.

The complete source snapshot and key inventories remain under:

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

## Refresh and deployment

The dedicated refresh workflow checks the official source daily and may also be run manually. It is content-addressed: an unchanged SHA-256 produces no commit.

When the source changes, the workflow:

1. downloads and validates the official feed;
2. reconciles it against canonical mission IDs;
3. republishes compact browser assets;
4. runs the deterministic catalogue audit;
5. commits only changed source assets; and
6. dispatches the full Pages deployment and cross-browser acceptance suite.

## Local validation

```bash
python scripts/validate_official_mission_catalogue.py
```

The audit independently checks record counts, ordering, duplicate IDs, field preservation, source metadata, file-size limits, canonical reconciliation, key inventories and public/source equality.

## Accuracy boundary

Official catalogue values are reproduced as published. They are not silently converted into canonical vehicles, personnel or building requirements where the internal key has not been verified. The raw official key remains visible so later mapping work is auditable and reversible.
