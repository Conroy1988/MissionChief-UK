# MissionChief UK Structured Dataset

This directory contains the production machine-readable records used by the MissionChief UK knowledgebase.

## Current inventory

### Missions

Eleven verified mission records:

- `0` — Bin fire
- `1` — Container fire
- `2` — Burning car
- `6` — Garden shed fire
- `208` — Domestic smoke alarm activation
- `521` — Community Engagement (Fire)
- `522` — Community Engagement (Ambulance)
- `622` — Group Throwing Flares
- `693` — HCP Home Visit
- `762` — Palliative Care Visit
- `797` — Person in large enclosure

### Vehicles

Five verified resource records:

- `fire_engine` — Fire engine
- `aerial_appliance_truck` — Aerial Appliance Truck
- `rapid_response_vehicle` — Rapid Response Vehicle
- `specialist_paramedic_rrv` — Specialist Paramedic RRV
- `police_car` — Police car

## Service coverage

The production dataset now contains records across:

- Fire and Rescue;
- Ambulance;
- Police.

Maritime, Coastguard, Search and Rescue and other specialist services remain future controlled population batches.

## Validation guarantees

The repository validator checks:

1. valid JSON syntax;
2. conformance with the applicable Draft 2020-12 schema;
3. unique identifiers within each record type;
4. valid date formats;
5. guaranteed and probabilistic mission resources against canonical vehicle IDs;
6. every resource inside an alternative requirement group;
7. that patient minimums do not exceed patient maximums.

A mission file fails validation when it references a resource that does not exist under `data/uk/vehicles/`.

## Evidence policy

A record marked `verified` applies that status only to the populated fields. Missing values are intentional when the current UK game has not yet been reproduced or evidenced for that attribute.

Temporary event multipliers are not stored as base rewards unless explicitly identified as observations rather than canonical values.

When the official mission directory exposes only a mission name, POI, reward and station precondition, those values may be recorded while unavailable vehicle or patient fields remain empty.
