# Verified Mission Batch 6 — Search and Rescue HQ

Stage 17 establishes the first verified Search and Rescue HQ mission model, including active-drone preconditions, SAR command personnel, operational-support alternatives and aerial-search alternatives.

!!! success "Verification boundary"
    Verification applies only to populated fields. Vehicle prices, crew limits, training durations and HQ capacity are not implied by these mission records.

## Batch summary

| ID | Mission | Police Cars | Control Van | Average credits |
|---:|---|---:|---:|---:|
| `635` | High Risk Missing Person | 3 | 1 | 15,275 |
| `636` | Very High Risk Missing Person | 5 | 1 | 18,750 |

## Shared SAR response model

Both missions require:

- 3 Rescue Stations;
- 2 Search and Rescue HQs;
- 1 active Drone;
- 1 Control Van;
- 1 Operational Support Van, Operational Support Trailer **or** Personal SAR Vehicle;
- 1 Police Helicopter **or** Drone;
- 2 Mountain Rescue 4x4s or SAR 4x4s in any qualifying combination.

### Operational-support group

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

One qualifying resource satisfies this group. The requirement does not ask for one of each.

### Aerial-search group

```json
{
  "resources": [
    "police_helicopter",
    "drone"
  ],
  "quantity": 1
}
```

The active-Drone precondition is separate from this response group. A Police Helicopter can satisfy the incident requirement where the official mission permits it.

### 4x4 group

```json
{
  "resources": [
    "mountain_rescue_4x4",
    "sar_4x4"
  ],
  "quantity": 2
}
```

The quantity is two qualifying vehicles total, not two of each type.

## Personnel

### Available before generation

- 2 Search Advisors;
- 4 SAR Commanders.

### Required at the incident

- 1 Search Advisor;
- 2 SAR Commanders.

### Average minimum

- 10 Search Technicians.

The Search Technician figure is stored under `average_minimum`. It is not presented as a guaranteed exact headcount.

## High Risk Missing Person

**Canonical ID:** `635`  
**Police Stations:** 3  
**Police Cars:** 3  
**Average reward:** 15,275 credits

The live mission page may display a temporary reward multiplier. The structured record preserves the base average reward rather than replacing it with the temporary observation.

[Official UK mission record](https://www.missionchief.co.uk/einsaetze/635)

## Very High Risk Missing Person

**Canonical ID:** `636`  
**Police Stations:** 6  
**Police Cars:** 5  
**Average reward:** 18,750 credits

The remaining resource, personnel and patient model matches the High Risk mission.

[Official UK mission record](https://www.missionchief.co.uk/einsaetze/636)

## Patient behaviour

Both missions record:

- minimum patients: 1;
- maximum patients: 1;
- transport probability: 40%;
- critical-care probability: 5%;
- specialisation: General Internal;
- possible codes: C-1, C-2 and C-3.

## Canonical resources added

```text
data/uk/vehicles/
├── drone.json
├── operational-support-trailer.json
├── operational-support-van.json
├── personal-sar-vehicle.json
└── police-helicopter.json
```

## Machine-readable mission records

```text
data/uk/missions/
├── high-risk-missing-person.json
└── very-high-risk-missing-person.json
```

Repository validation checks every resource in all three alternative groups against the canonical resource dataset.
