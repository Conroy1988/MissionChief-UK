# Search and Rescue HQ

Search and Rescue HQ operations provide the structured land-search and drone-enabled response layer used by the verified missing-person missions.

!!! success "Verified Stage 17 baseline"
    The current production records verify the populated fields for High Risk Missing Person and Very High Risk Missing Person. Purchase prices, vehicle staffing, training durations and HQ capacity remain unpublished until reproduced from the current UK interfaces.

## Service model

The verified missions require:

- 2 Search and Rescue HQs;
- 1 active Drone;
- Search Advisors and SAR Commanders available before generation;
- Control Van command support;
- one qualifying operational-support resource;
- one Police Helicopter or Drone;
- two qualifying 4x4 vehicles;
- an average minimum of 10 Search Technicians.

The active-Drone precondition and the incident aerial-search requirement are separate concepts. A mission can require an active Drone before generation while still allowing a Police Helicopter to satisfy the response requirement.

## Canonical resources

### Control Van

The Control Van is the guaranteed command resource on both verified missing-person missions.

### Operational-support alternatives

One of the following satisfies the operational-support requirement:

- Operational Support Van;
- Operational Support Trailer;
- Personal SAR Vehicle.

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

The Operational Support Trailer is explicitly recorded as a trailer. Compatible towing vehicles are not yet published.

### Aerial-search alternatives

One of the following satisfies the aerial-search requirement:

- Police Helicopter;
- Drone.

An active Drone precondition does not force the dispatched aerial resource to be a Drone.

### 4x4 alternatives

Two qualifying vehicles are required in total:

- Mountain Rescue 4x4;
- SAR 4x4.

Any valid combination can satisfy the group where the game permits both resource types.

## Personnel model

### Available before generation

- 2 Search Advisors;
- 4 SAR Commanders.

### Required at the incident

- 1 Search Advisor;
- 2 SAR Commanders.

### Average minimum

- 10 Search Technicians.

The Search Technician figure is stored as `average_minimum`. It must not be presented as an exact guaranteed incident headcount.

## Verified missions

| ID | Mission | Police Cars | Average reward |
|---:|---|---:|---:|
| `635` | High Risk Missing Person | 3 | 15,275 |
| `636` | Very High Risk Missing Person | 5 | 18,750 |

Both missions also require one Control Van, one operational-support alternative, one aerial-search alternative and two qualifying 4x4s.

## Patient behaviour

Both verified missions contain exactly one patient with:

- 40% transport probability;
- 5% critical-care probability;
- General Internal specialisation;
- possible codes C-1, C-2 and C-3.

## Common modelling errors

Avoid these mistakes:

1. requiring an Operational Support Van, Trailer and Personal SAR Vehicle simultaneously;
2. requiring both a Police Helicopter and Drone;
3. treating an active Drone precondition as the dispatched vehicle;
4. requiring two Mountain Rescue 4x4s plus two SAR 4x4s instead of two qualifying vehicles total;
5. treating the average-minimum Search Technician value as an exact guaranteed count;
6. replacing the base reward with a temporary live multiplier.

## Machine-readable records

```text
data/uk/missions/
├── high-risk-missing-person.json
└── very-high-risk-missing-person.json

data/uk/vehicles/
├── drone.json
├── operational-support-trailer.json
├── operational-support-van.json
├── personal-sar-vehicle.json
└── police-helicopter.json
```

## Primary evidence

- [High Risk Missing Person](https://www.missionchief.co.uk/einsaetze/635)
- [Very High Risk Missing Person](https://www.missionchief.co.uk/einsaetze/636)
