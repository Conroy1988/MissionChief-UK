# Fully Canonical Mission Batch 12

Batch 12 promotes **Tree on the road**, the exact mission unlocked by mapping the official three-way appliance group.

## Verified dispatch model

| ID | Mission | Fire Stations | Guaranteed | Additional alternative | Expansion | Average credits |
|---:|---|---:|---|---|---|---:|
| `12` | Tree on the road | 1 | 1 Fire Engine | 1 Fire Engine, Rescue Support Vehicle or Aerial Appliance Truck | Road accident | 310 |

The retained source represents the guaranteed Fire Engine and the three-way choice as additive requirements. The alternative therefore does not replace the guaranteed appliance.

## Evidence safeguards

- Exact official ID, UK name, prerequisite, reward and resource quantities are retained.
- The three-resource choice is represented through `requirements.alternatives`.
- The published expansion into Road accident is retained and resolves to official mission ID 25.
- No patients, personnel, probabilities, variants, overlays or unsupported additional fields are present.
- Strict key equivalence enforces both the guaranteed and alternative requirements.

## Coverage movement

```text
Before Batch 12
Canonical records:       154
Direct ID matches:       137
Fully canonical:          96
Remaining to canonical:  966

After Batch 12
Canonical records:       155
Direct ID matches:       138
Fully canonical:          97
Remaining to canonical:  965
```

Batch 12 raises identity coverage to **13.00%** and fully canonical coverage to **9.13%** of the 1,062-record official UK catalogue.

Promotion decisions are stored in:

```text
data/uk/mission-verification-batches/fully-canonical-fire-batch-12.json
```
