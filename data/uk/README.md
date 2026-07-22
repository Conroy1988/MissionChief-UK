# MissionChief UK Structured Dataset

This directory contains the production machine-readable records used by the MissionChief UK knowledgebase.

## Current inventory

### Missions

Twenty-one verified mission records:

- `0` — Bin fire
- `1` — Container fire
- `2` — Burning car
- `6` — Garden shed fire
- `143` — Stuck Climber
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
- `753-helicopter-overlay` — Belay Failure Whilst Abseiling helicopter overlay
- `755-hart-overlay` — Fall Whilst Fell Running HART overlay
- `756` — Overdue Hikers
- `760` — Amateur Explorers Trapped in Abandoned Mineshaft
- `762` — Palliative Care Visit
- `797` — Person in large enclosure

### Vehicles and deployable resources

Twenty-one verified canonical records:

- `fire_engine` — Fire engine
- `aerial_appliance_truck` — Aerial Appliance Truck
- `rescue_support_vehicle` — Rescue Support Vehicle
- `rapid_response_vehicle` — Rapid Response Vehicle
- `specialist_paramedic_rrv` — Specialist Paramedic RRV
- `atv_carrier` — ATV Carrier
- `prv` — PRV
- `srv` — SRV
- `welfare_vehicle` — Welfare Vehicle
- `police_car` — Police car
- `coastguard_rescue_vehicle` — CRV
- `coastguard_mud_rescue_unit` — Coastguard Mud Rescue Unit
- `mud_decontamination_unit` — Mud Decontamination Unit
- `coastguard_rescue_helicopter` — Coastguard Rescue Helicopter
- `inland_rescue_boat_trailer` — Inland Rescue Boat (Trailer)
- `inshore_lifeboat` — ILB
- `all_weather_lifeboat` — ALB
- `mountain_rescue_4x4` — Mountain Rescue 4x4
- `sar_4x4` — SAR 4x4
- `control_van` — Control Van
- `search_dog_unit` — Search Dog Unit

## Service coverage

The production dataset now contains records across:

- Fire and Rescue;
- Ambulance and HART support;
- Police;
- Coastguard;
- Lifeboat and Ocean Rescue;
- Mountain Rescue and land search.

Airfield Operations, Recovery, Bomb Disposal, Railway Police and other specialist services remain future controlled population batches.

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

## Variant modelling

Stage 16 introduces explicit mission variants. Additive overlays use a unique string dataset ID while retaining the official numeric mission ID:

```json
{
  "id": "753-helicopter-overlay",
  "variant": {
    "source_mission_id": 753,
    "kind": "additive-overlay",
    "key": "coastguard-helicopter"
  }
}
```

This prevents HART, helicopter or future drone requirements from being incorrectly applied to the base mission.

## Mountain Rescue modelling

The Stage 16 schema supports:

- Mountain Rescue Station preconditions;
- Search and Rescue HQ and active-drone preconditions for future SAR records;
- Mountain Rescue 4x4 or SAR 4x4 alternative groups;
- probability-based personnel requirements;
- Control Vans, Search Dog Units, Rescue Support Vehicles and ATV Carriers;
- cave-rescue personnel availability and incident requirements;
- custom spawn areas and structured patient mechanics.

## Evidence policy

A record marked `verified` applies that status only to the populated fields. Missing values are intentional when the current UK game has not yet been reproduced or evidenced for that attribute.

Temporary event multipliers are not stored as base rewards unless explicitly identified as observations rather than canonical values.

Official abbreviations such as PRV and SRV remain unexpanded when the primary source does not provide an authoritative expanded name.
