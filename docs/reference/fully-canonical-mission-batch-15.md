# Fully Canonical Mission Batch 15

Batch 15 promotes **Scrapyard Fire Large**, the exact mission unlocked by the verified HART secondary-response mapping.

## Verified dispatch model

| ID | Mission | Fire Stations | Police Stations | Guaranteed resources | Alternative groups | Average credits |
|---:|---|---:|---:|---|---|---:|
| `420` | Scrapyard Fire Large | 20 | 3 | 20 Fire Engines, 6 Fire Officers, 1 SRV, 1 BA Support Unit, 2 Aerial Appliance Trucks, 4 Police Cars and 2 Water Carriers | 1 HazMat Unit or CBRN Vehicle; 1 ICCU or Ambulance Control Unit | 20,000 |

## HART identity safeguard

The official `hazard_response_secondary` field is displayed as **SRV** and maps to canonical resource `srv`. It is not the Fire and Rescue Service `rescue_support_vehicle`; both resources remain separate canonical identities.

## Evidence safeguards

- Exact official ID, UK name, Scrap yard POI, station prerequisites, reward and every resource quantity are retained.
- The official SRV remains a guaranteed HART resource.
- HazMat/CBRN and ICCU/Ambulance Control choices remain explicit alternative groups.
- No patients, prisoners, personnel, probabilities, relationships, variants, overlays or unsupported additional fields are present.
- Strict key equivalence is mandatory.

## Coverage movement

```text
Before Batch 15
Canonical records:       168
Direct ID matches:       151
Fully canonical:         110
Remaining to canonical:  952

After Batch 15
Canonical records:       169
Direct ID matches:       152
Fully canonical:         111
Remaining to canonical:  951
```

Batch 15 raises identity coverage to **14.31%** and fully canonical coverage to **10.45%** of the 1,062-record official UK catalogue.

Promotion decisions are stored in:

```text
data/uk/mission-verification-batches/fully-canonical-fire-batch-15.json
```
