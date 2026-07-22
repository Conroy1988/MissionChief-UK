# MissionChief UK Structured Dataset

This directory contains the production machine-readable records used by the MissionChief UK knowledgebase.

## Current inventory

### Missions

Seven verified mission records:

- `0` — Bin fire
- `1` — Container fire
- `2` — Burning car
- `6` — Garden shed fire
- `208` — Domestic smoke alarm activation
- `521` — Community Engagement (Fire)
- `797` — Person in large enclosure

### Vehicles

Three verified resource records:

- `fire_engine` — Fire engine
- `police_car` — Police car
- `aerial_appliance_truck` — Aerial Appliance Truck

## Validation guarantees

The repository validator checks:

1. valid JSON syntax;
2. conformance with the applicable Draft 2020-12 schema;
3. unique identifiers within each record type;
4. valid date formats;
5. mission resource references against canonical vehicle IDs.

A mission file will fail validation when it references a resource that does not exist under `data/uk/vehicles/`.

## Evidence policy

A record marked `verified` applies that status only to the populated fields. Missing values are intentional when the current UK game has not yet been reproduced or evidenced for that attribute.

Temporary event multipliers are not stored as base rewards unless they are explicitly identified as observations rather than canonical values.