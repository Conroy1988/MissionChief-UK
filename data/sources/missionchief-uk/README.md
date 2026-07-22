# Official MissionChief UK Mission Catalogue

This directory contains an automated, lossless snapshot of the official public MissionChief UK mission feed:

```text
https://www.missionchief.co.uk/einsaetze.json
```

## Trust model

The official feed is authoritative for the mission catalogue and the raw game fields it publishes. It is not automatically treated as a complete canonical dispatch model.

The production records under `data/uk/missions/` remain the highest-trust, schema-normalized collection used for verified operational guidance. Fields are promoted from this source snapshot only when their UK meaning and resource mappings are reproducible.

## Generated files

```text
einsaetze.raw.json          Complete official response with source metadata
mission-coverage.json       Reconciliation against canonical mission IDs
official-key-inventory.json Distinct requirement, chance and prerequisite keys
```

The browser catalogue is generated at:

```text
docs/assets/data/official/uk-missions.json
docs/assets/data/official/uk-mission-coverage.json
```

Both the raw source and browser catalogue retain every official mission field. The two largest files are stored as compact JSON to remain within repository content limits without removing information.

## Refresh process

Run:

```bash
python scripts/import_official_uk_missions.py
python scripts/publish_official_mission_catalogue.py
python scripts/compact_official_mission_catalogue.py
```

The dedicated GitHub Actions workflow refreshes this snapshot on the feature branch. It validates duplicate IDs, missing names, suspiciously small responses, record counts and reconciliation totals before committing generated data.

## Accuracy boundaries

- Official raw values are preserved verbatim.
- Internal requirement keys are not guessed into canonical vehicle IDs.
- Time-limited missions remain in the complete catalogue and retain their official availability dates.
- Mission variations, overlays and base mission relationships remain separate official records.
- Canonical verification status is never inferred merely because a mission exists in the official feed.
