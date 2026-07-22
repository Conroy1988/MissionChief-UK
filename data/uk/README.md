# MissionChief UK Structured Dataset

This directory contains the production machine-readable records used by the MissionChief UK knowledgebase.

## Current inventory

```text
27 verified mission records
26 canonical vehicle-resource records
2 canonical infrastructure records
8 represented operational service groups
7 published mission-data batches
```

### Stage 18 mission records

- `829` — Unexploded WW2 Ordnance in Countryside
- `830` — Unexploded WW2 Ordnance on Quiet Beach
- `832` — Unexploded WW2 Ordnance in Harbour
- `839` — Unexploded WW2 Bomb Located at Building Site (Large)

### Stage 18 infrastructure records

- `bomb_disposal_hq` — Bomb Disposal HQ
- `bomb_disposal_marine_unit_extension` — Bomb Disposal Marine Unit Extension

The full vehicle and mission inventories remain available through the public reference pages and the JSON files under this directory.

## Service coverage

The production dataset now contains records across:

- Fire and Rescue;
- Ambulance and HART support;
- Police;
- Coastguard;
- Lifeboat and Ocean Rescue;
- Mountain Rescue and land search;
- Search and Rescue HQ and drone-enabled operations;
- Bomb Disposal and EOD mission generation.

Airfield Operations, Recovery, Railway Police and other specialist services remain future controlled population batches.

## Validation guarantees

The repository validator checks:

1. valid JSON syntax;
2. conformance with the applicable Draft 2020-12 schema;
3. unique identifiers within each record type;
4. valid date formats;
5. guaranteed and probabilistic mission resources against canonical resource IDs;
6. every resource inside every alternative requirement group;
7. that patient minimums do not exceed patient maximums;
8. Bomb Disposal infrastructure preconditions against canonical infrastructure records.

A mission fails validation when it references an unknown vehicle resource or a Bomb Disposal infrastructure entity that does not exist under `data/uk/infrastructure/`.

## Stage 18 infrastructure modelling

Stage 18 introduces production records for buildings and extensions through `infrastructure.schema.json`.

```text
Bomb Disposal HQ
Bomb Disposal Marine Unit Extension
```

The mission fields `bomb_disposal_hqs` and `bomb_disposal_marine_unit_extensions` are validated against these records.

## Evidence boundary

The official mission directory exposed mission IDs, names, POIs, rewards and preconditions. Individual response tables were not consistently retrievable during Stage 18 verification.

Vehicle and personnel requirement arrays are therefore empty for the first Bomb Disposal batch. Empty fields are deliberate and must not be interpreted as proof that no specialist response is required.

Temporary event multipliers are not stored as base rewards unless explicitly identified as observations rather than canonical values.
