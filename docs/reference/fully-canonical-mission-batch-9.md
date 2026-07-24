# Fully Canonical Mission Batch 9

Batch 9 promotes the three exact missions unlocked by the verified guaranteed `hazmat_vehicles` mapping. The official requirement is preserved as a qualifying alternative group: each published quantity may be satisfied by **HazMat Units** or **CBRN Vehicles**.

## Batch result

| ID | Mission | Fire Stations | Fire Engines | Fire Officer | Rescue Support | Water Carrier | HazMat / CBRN | Average credits |
|---:|---|---:|---:|---:|---|---|---|---:|
| `180` | Fire involving Acetylene cylinders | 11 | 2 | 1 | — | — | 1 alternative | 4,000 |
| `251` | Fire in munitions dump | 11 | 4 | 1 | — | 1 guaranteed | 1 alternative | 3,500 |
| `469` | Tram fire | 10 | 6 | 4 | 1 | — | 1 alternative | 6,000 |

## Mapping evidence

Current UK mission pages publish the requirement label **HazMat Units or CBRN Vehicles**. Both canonical resources are independently verified.

The mapping contract is:

| Official field | Canonical interpretation |
|---|---|
| `requirements.hazmat_vehicles` | Quantity satisfied by HazMat Unit or CBRN Vehicle |
| Canonical representation | `requirements.alternatives` with resources `hazmat_unit` and `cbrn_vehicle` |

Chance-based HazMat/CBRN requirements remain blocked until probabilistic alternative groups are separately implemented and validated.

## Evidence safeguards

- Every record was selected by the evidence-safe candidate analyser after the guaranteed alternative mapping passed the complete deterministic suite.
- Exact official IDs, names, prerequisites, resource quantities, rewards and POIs are retained.
- The official requirement is not inflated into simultaneous HazMat and CBRN resources.
- Tram fire retains its published expansion into Tram fire (Persons Reported).
- No patients, personnel, variants, overlays or unsupported additional fields are present.
- Strict key equivalence is mandatory for all three promotions.

## Coverage movement

```text
Before Batch 9
Canonical records:       148
Direct ID matches:       131
Fully canonical:          90
Remaining to canonical:  972

After Batch 9
Canonical records:       151
Direct ID matches:       134
Fully canonical:          93
Remaining to canonical:  969
```

Batch 9 raises identity coverage to **12.62%** and fully canonical coverage to **8.76%** of the 1,062-record official UK catalogue.

Promotion decisions are stored in:

```text
data/uk/mission-verification-batches/fully-canonical-fire-batch-9.json
```
