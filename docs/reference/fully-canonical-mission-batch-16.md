# Fully Canonical Mission Batch 16

Batch 16 promotes the two exact missions unlocked by the verified Foam Unit and Foam Extension contracts.

## Batch result

| ID | Mission | Fire Stations | Police Stations | Ambulance Stations | Foam Extensions | Key dispatch features | Average credits |
|---:|---|---:|---:|---:|---:|---|---:|
| `734` | Fire in a lithium battery manufacturing factory | 20 | 6 | 1 | 2 | 12 Fire Engines, 2 Foam Units, 2 Rescue Support Vehicles, BA support, 3 aerials, 6 Police Cars, 2 Water Carriers, 2 HazMat/CBRN and command alternative | 11,500 |
| `735` | Fire in an abandoned hospital | 8 | 2 | — | 1 | 4 Fire Engines, 2 Fire Officers, Rescue Support, BA support, 1 aerial, 2 Police Cars and 1 Water Carrier | 7,500 |

## Mapping evidence

The retained `requirements.foam` field represents guaranteed **Foam Units**. The `prerequisites.fire_support_count` field represents the minimum **Foam Extension** count shown on current UK mission pages.

## Evidence safeguards

- Exact official IDs, UK names, POIs, prerequisites, rewards and all resource quantities are retained.
- Factory and Hospital POIs remain explicit.
- HazMat/CBRN and ICCU/Ambulance Control choices remain alternative groups rather than duplicated guaranteed resources.
- No patients, prisoners, personnel, probabilities, relationships, variants, overlays or unsupported additional fields are present.
- Strict key equivalence is mandatory for both promotions.

## Coverage movement

```text
Before Batch 16
Canonical records:       169
Direct ID matches:       152
Fully canonical:         111
Remaining to canonical:  951

After Batch 16
Canonical records:       171
Direct ID matches:       154
Fully canonical:         113
Remaining to canonical:  949
```

Batch 16 raises identity coverage to **14.50%** and fully canonical coverage to **10.64%** of the 1,062-record official UK catalogue.

Promotion decisions are stored in:

```text
data/uk/mission-verification-batches/fully-canonical-fire-batch-16.json
```
