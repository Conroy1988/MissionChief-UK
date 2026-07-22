# Verified Vehicle Records

This page exposes the canonical vehicle-resource records currently available in the MissionChief UK dataset.

Each record verifies only the populated attributes. Purchase prices, crew limits, training and station restrictions remain intentionally absent until those values are reproduced from the current UK vehicle market.

!!! success "Evidence boundary"
    A verified vehicle record does not mean every vehicle attribute has been verified. Empty or omitted fields are preferable to unsupported values.

## Current records

| Canonical ID | UK requirement label | Service | Category | Evidence status |
|---|---|---|---|---|
| `fire_engine` | Fire engine | Fire and Rescue | Response | Verified 22 July 2026 |
| `aerial_appliance_truck` | Aerial Appliance Truck | Fire and Rescue | Specialist | Verified 22 July 2026 |
| `rapid_response_vehicle` | Rapid Response Vehicle | Ambulance | Response | Verified 22 July 2026 |
| `specialist_paramedic_rrv` | Specialist Paramedic RRV | Ambulance | Specialist response | Verified 22 July 2026 |
| `police_car` | Police car | Police | Response | Verified 22 July 2026 |
| `coastguard_rescue_vehicle` | CRV | Coastguard | Response | Verified 22 July 2026 |
| `coastguard_mud_rescue_unit` | Coastguard Mud Rescue Unit | Coastguard | Specialist rescue | Verified 22 July 2026 |
| `mud_decontamination_unit` | Mud Decontamination Unit | Coastguard | Specialist support | Verified 22 July 2026 |
| `coastguard_rescue_helicopter` | Coastguard Rescue Helicopter | Coastguard | Air rescue | Verified 22 July 2026 |
| `inland_rescue_boat_trailer` | Inland Rescue Boat (Trailer) | Lifeboat | Water-rescue trailer | Verified 22 July 2026 |
| `inshore_lifeboat` | ILB | Lifeboat | Ocean-rescue boat | Verified 22 July 2026 |
| `all_weather_lifeboat` | ALB | Lifeboat | Ocean-rescue boat | Verified 22 July 2026 |

## Fire engine

The Fire engine is the first canonical response resource in the dataset. Official UK mission pages repeatedly identify it as a guaranteed requirement, including Bin fire, Garden shed fire and Community Engagement (Fire).

**Not yet published:** purchase cost, maximum crew, station unlocks and training dependencies.

## Aerial Appliance Truck

The Aerial Appliance Truck record establishes the canonical specialist-resource identifier used by conditional mission requirements.

**Not yet published:** purchase cost, staffing, training and station restrictions.

## Rapid Response Vehicle

The Rapid Response Vehicle establishes the canonical `rapid_response_vehicle` identifier and the searchable alias `RRV`.

Official UK mission pages identify an RRV as one valid response option for HCP Home Visit and Palliative Care Visit.

**Not yet published:** purchase cost, staffing, training, patient capability limits and station restrictions.

## Specialist Paramedic RRV

The Specialist Paramedic RRV establishes a separate canonical specialist-response resource. It appears as an alternative to the standard RRV on verified UK ambulance mission pages.

The dataset preserves that relationship as an alternative resource group rather than treating both vehicles as simultaneously required.

**Not yet published:** purchase cost, staffing, training and station or extension dependencies.

## Police car

The Police car record establishes the canonical identifier used by mission requirements. Official UK mission records identify Police Cars as required or conditional policing resources.

**Not yet published:** purchase cost, crew model, custody behaviour and station restrictions.

## Coastguard Rescue Vehicle

The official maritime mission pages use the abbreviation **CRV**. The expanded term **Coastguard Rescue Vehicle** is retained as a searchable alias.

Verified mission usage includes two CRVs for Rescue Boat Assist Coastguard, Persons Cut off by Tide.

## Coastguard Mud Rescue Unit

This specialist Coastguard resource is verified on Mud Rescue and Rescue Boat Assist Coastguard Mud Rescue.

The mission data separately stores the number of trained Mud Rescue Operators available and required; it does not infer a fixed vehicle crew.

## Mud Decontamination Unit

The Mud Decontamination Unit is recorded as specialist Coastguard support. It appears alongside Coastguard Mud Rescue Units in the first verified mud-rescue mission set.

## Coastguard Rescue Helicopter

The Coastguard Rescue Helicopter is the first maritime air-resource record. Medivac from vessel applies a verified 50% requirement probability to it.

**Not yet published:** purchase cost, crew, training and hangar restrictions beyond mission preconditions.

## Inland Rescue Boat (Trailer)

The official requirement label explicitly identifies this resource as a trailer. The record therefore sets `is_trailer` to `true` but does not guess which towing vehicles are compatible.

This resource appears in inland and coastal support missions and is distinct from ILB and ALB ocean-rescue boats.

## ILB and ALB

Official UK ocean-rescue mission pages use the abbreviations **ILB** and **ALB**. The dataset preserves those labels as canonical names and stores **Inshore Lifeboat** and **All-weather Lifeboat** as searchable aliases.

Where the game states `ILBs or ALBs`, the mission record uses an alternative group. One qualifying lifeboat satisfies the requirement.

## Machine-readable records

```text
data/uk/vehicles/
├── aerial-appliance-truck.json
├── all-weather-lifeboat.json
├── coastguard-mud-rescue-unit.json
├── coastguard-rescue-helicopter.json
├── coastguard-rescue-vehicle.json
├── fire-engine.json
├── inland-rescue-boat-trailer.json
├── inshore-lifeboat.json
├── mud-decontamination-unit.json
├── police-car.json
├── rapid-response-vehicle.json
└── specialist-paramedic-rrv.json
```

Mission records reference these resources through their canonical IDs. Repository validation fails when a guaranteed, probabilistic or alternative requirement names a resource without a corresponding vehicle record.

## Next verification target

The next vehicle-data pass should reproduce current values directly from the UK vehicle market and station purchase interfaces, including:

1. price in credits and coins where applicable;
2. minimum and maximum personnel;
3. training requirements;
4. building and extension dependencies;
5. purchase limits and unlock conditions;
6. exact trailer towing or carrier relationships;
7. patient, prisoner and transport capabilities.
