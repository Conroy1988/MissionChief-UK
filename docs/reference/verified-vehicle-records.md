# Verified Vehicle Records

This page exposes the canonical deployable-resource records currently available in the MissionChief UK dataset.

Each record verifies only its populated attributes. Purchase prices, crew limits, training and station restrictions remain absent until reproduced from the current UK interfaces.

!!! success "Evidence boundary"
    A verified resource record does not mean every attribute has been verified. Empty or omitted fields are preferable to unsupported values.

## Current records

| Canonical ID | UK requirement label | Service | Category |
|---|---|---|---|
| `fire_engine` | Fire engine | Fire and Rescue | Response |
| `aerial_appliance_truck` | Aerial Appliance Truck | Fire and Rescue | Specialist |
| `rescue_support_vehicle` | Rescue Support Vehicle | Fire and Rescue | Specialist support |
| `rapid_response_vehicle` | Rapid Response Vehicle | Ambulance | Response |
| `specialist_paramedic_rrv` | Specialist Paramedic RRV | Ambulance | Specialist response |
| `atv_carrier` | ATV Carrier | Ambulance/HART | Specialist support |
| `prv` | PRV | Ambulance | Specialist response |
| `srv` | SRV | Ambulance | Specialist response |
| `welfare_vehicle` | Welfare Vehicle | Ambulance | Support |
| `police_car` | Police car | Police | Response |
| `police_helicopter` | Police Helicopter | Police | Air support |
| `drone` | Drone | Shared | Aerial search and reconnaissance |
| `coastguard_rescue_vehicle` | CRV | Coastguard | Response |
| `coastguard_mud_rescue_unit` | Coastguard Mud Rescue Unit | Coastguard | Specialist rescue |
| `mud_decontamination_unit` | Mud Decontamination Unit | Coastguard | Specialist support |
| `coastguard_rescue_helicopter` | Coastguard Rescue Helicopter | Coastguard | Air rescue |
| `inland_rescue_boat_trailer` | Inland Rescue Boat (Trailer) | Lifeboat | Water-rescue trailer |
| `inshore_lifeboat` | ILB | Lifeboat | Ocean-rescue boat |
| `all_weather_lifeboat` | ALB | Lifeboat | Ocean-rescue boat |
| `mountain_rescue_4x4` | Mountain Rescue 4x4 | Mountain Rescue | Response |
| `sar_4x4` | SAR 4x4 | Search and Rescue | Response |
| `control_van` | Control Van | Search and Rescue | Command |
| `search_dog_unit` | Search Dog Unit | Search and Rescue | Specialist search |
| `operational_support_van` | Operational Support Van | Search and Rescue | Operational support |
| `operational_support_trailer` | Operational Support Trailer | Search and Rescue | Operational support trailer |
| `personal_sar_vehicle` | Personal SAR Vehicle | Search and Rescue | Personnel transport and support |

All records shown above were checked on 22 July 2026.

## Search and Rescue HQ resources

### Operational Support Van, Trailer and Personal SAR Vehicle

The official High Risk Missing Person and Very High Risk Missing Person pages group these resources as alternatives:

```json
{
  "resources": [
    "operational_support_van",
    "operational_support_trailer",
    "personal_sar_vehicle"
  ],
  "quantity": 1
}
```

One qualifying resource satisfies the requirement. The Operational Support Trailer is explicitly recorded as a trailer, but compatible towing vehicles remain unverified.

### Police Helicopter and Drone

The official SAR pages allow one Police Helicopter or one Drone to satisfy the aerial-search requirement.

The active-Drone generation precondition is separate from the response requirement. It does not mean a Drone must be dispatched when a Police Helicopter can satisfy the mission.

### Control Van

The Control Van is the guaranteed command resource on both verified missing-person missions. It is also used by Stage 16 Mountain Rescue records.

## Mountain Rescue and land-search resources

### Mountain Rescue 4x4 and SAR 4x4

Official UK Mountain Rescue and SAR pages present these as alternatives. Mission records therefore use an alternative group rather than requiring one of each.

```json
{
  "resources": [
    "mountain_rescue_4x4",
    "sar_4x4"
  ],
  "quantity": 2
}
```

The quantity represents the total number of qualifying 4x4s.

### Search Dog Unit

The Search Dog Unit is a distinct search resource and must not be confused with a Police Dog Support Unit. It is verified on Overdue Hikers and the abandoned-mineshaft rescue.

### Rescue Support Vehicle

The Rescue Support Vehicle is retained as the exact official requirement label. The dataset does not infer a fixed crew, training course or station dependency from the mission requirement alone.

### ATV Carrier

The ATV Carrier is currently verified through the HART additive overlay for Fall Whilst Fell Running. Its requirement belongs to the overlay and must not be added to the base mission.

### PRV and SRV

The official abandoned-mineshaft mission page uses the abbreviations **PRV** and **SRV**. The records preserve those labels without inventing expanded names.

### Welfare Vehicle

The Welfare Vehicle is verified as prolonged-incident support on the abandoned-mineshaft rescue.

## Maritime resources

### CRV

The official maritime mission pages use the abbreviation **CRV**. Coastguard Rescue Vehicle remains a searchable alias.

### Inland Rescue Boat (Trailer)

The official requirement label identifies this resource as a trailer. The record sets `is_trailer` to `true` but does not guess compatible towing vehicles.

### ILB and ALB

The abbreviations **ILB** and **ALB** remain canonical. Inshore Lifeboat and All-weather Lifeboat are searchable aliases. An `ILB or ALB` requirement is stored as an alternative group.

## Ambulance alternatives

Rapid Response Vehicle and Specialist Paramedic RRV can satisfy the same alternative requirement on the verified HCP Home Visit and Palliative Care Visit missions. The dataset does not treat both as simultaneously required.

## Machine-readable records

```text
data/uk/vehicles/
├── aerial-appliance-truck.json
├── all-weather-lifeboat.json
├── atv-carrier.json
├── coastguard-mud-rescue-unit.json
├── coastguard-rescue-helicopter.json
├── coastguard-rescue-vehicle.json
├── control-van.json
├── drone.json
├── fire-engine.json
├── inland-rescue-boat-trailer.json
├── inshore-lifeboat.json
├── mountain-rescue-4x4.json
├── mud-decontamination-unit.json
├── operational-support-trailer.json
├── operational-support-van.json
├── personal-sar-vehicle.json
├── police-car.json
├── police-helicopter.json
├── prv.json
├── rapid-response-vehicle.json
├── rescue-support-vehicle.json
├── sar-4x4.json
├── search-dog-unit.json
├── specialist-paramedic-rrv.json
├── srv.json
└── welfare-vehicle.json
```

Repository validation fails when a guaranteed, probabilistic or alternative mission requirement references an unknown canonical resource.

## Still awaiting verification

The next attribute-level pass should reproduce:

1. credit and coin purchase prices;
2. minimum and maximum vehicle staffing;
3. exact training requirements and durations;
4. building and extension dependencies;
5. purchase limits and unlock conditions;
6. trailer towing or carrier relationships;
7. patient, prisoner and transport capabilities.
