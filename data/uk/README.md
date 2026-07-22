# MissionChief UK Structured Dataset

This directory contains the production machine-readable records used by the MissionChief UK knowledgebase.

## Current inventory

### Missions

Sixteen verified mission records:

- `0` — Bin fire
- `1` — Container fire
- `2` — Burning car
- `6` — Garden shed fire
- `208` — Domestic smoke alarm activation
- `521` — Community Engagement (Fire)
- `522` — Community Engagement (Ambulance)
- `546` — Mud Rescue
- `561` — Broken Down Boat
- `562` — Medivac from vessel
- `567` — Rescue Boat Assist Coastguard Mud Rescue
- `569` — Rescue Boat Assist Coastguard, Persons Cut off by Tide
- `622` — Group Throwing Flares
- `693` — HCP Home Visit
- `762` — Palliative Care Visit
- `797` — Person in large enclosure

### Vehicles

Twelve verified resource records:

- `fire_engine` — Fire engine
- `aerial_appliance_truck` — Aerial Appliance Truck
- `rapid_response_vehicle` — Rapid Response Vehicle
- `specialist_paramedic_rrv` — Specialist Paramedic RRV
- `police_car` — Police car
- `coastguard_rescue_vehicle` — CRV
- `coastguard_mud_rescue_unit` — Coastguard Mud Rescue Unit
- `mud_decontamination_unit` — Mud Decontamination Unit
- `coastguard_rescue_helicopter` — Coastguard Rescue Helicopter
- `inland_rescue_boat_trailer` — Inland Rescue Boat (Trailer)
- `inshore_lifeboat` — ILB
- `all_weather_lifeboat` — ALB

## Service coverage

The production dataset now contains records across:

- Fire and Rescue;
- Ambulance;
- Police;
- Coastguard;
- Lifeboat and Ocean Rescue.

Mountain Rescue, Airfield Operations, HART, Recovery, Bomb Disposal and other specialist services remain future controlled population batches.

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

## Maritime modelling

The Stage 15 schema supports:

- Coastguard Rescue Station and Lifeboat Station preconditions;
- Helicopter Hangars and specialist maritime extensions;
- trailers and operating environments;
- ocean-only vehicle restrictions;
- custom mission spawn areas;
- patient and prisoner hand-off destinations;
- ILB-or-ALB alternative requirements.

## Evidence policy

A record marked `verified` applies that status only to the populated fields. Missing values are intentional when the current UK game has not yet been reproduced or evidenced for that attribute.

Temporary event multipliers are not stored as base rewards unless explicitly identified as observations rather than canonical values.

When the official mission directory exposes only a mission name, POI, reward and station precondition, those values may be recorded while unavailable vehicle or patient fields remain empty.
