# Fully Canonical Mission Batch 14

Batch 14 promotes **Fire in Derelict Shop**, the sole relationship-safe mission unlocked by the verified Ambulance Station prerequisite mapping.

## Verified dispatch model

| ID | Mission | Fire Stations | Police Stations | Ambulance Stations | Guaranteed resources | Average credits |
|---:|---|---:|---:|---:|---|---:|
| `703` | Fire in Derelict Shop | 12 | 2 | 2 | 4 Fire Engines, 2 Fire Officers, 1 Rescue Support Vehicle, 1 BA Support Unit, 1 Aerial Appliance Truck and 2 Police Cars | 7,000 |

## Evidence safeguards

- Exact official ID, UK name, all station prerequisites, reward and resource quantities are retained.
- The retained internal `rescue_stations` prerequisite is represented as the UK Ambulance Station requirement.
- Missions 354 and 355 remain blocked because their repeated Smoke Inhalation follow-up IDs carry multiplicity that the current canonical relationship schema cannot preserve.
- No patients, prisoners, personnel, probabilities, variants, overlays or unsupported additional fields are present.
- Strict key equivalence is mandatory.

## Coverage movement

```text
Before Batch 14
Canonical records:       167
Direct ID matches:       150
Fully canonical:         109
Remaining to canonical:  953

After Batch 14
Canonical records:       168
Direct ID matches:       151
Fully canonical:         110
Remaining to canonical:  952
```

Batch 14 raises identity coverage to **14.22%** and fully canonical coverage to **10.36%** of the 1,062-record official UK catalogue.

Promotion decisions are stored in:

```text
data/uk/mission-verification-batches/fully-canonical-fire-batch-14.json
```
