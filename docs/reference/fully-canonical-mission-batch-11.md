# Fully Canonical Mission Batch 11

Batch 11 promotes **Fuel spill from car**, the exact mission unlocked by mapping `oneof_fire_engine_or_rescue` to a qualifying Fire Engine or Rescue Support Vehicle group.

## Verified dispatch model

| ID | Mission | Fire Stations | Guaranteed | Additional alternative | Average credits |
|---:|---|---:|---|---|---:|
| `30` | Fuel spill from car | 1 | 1 Fire Engine | 1 Fire Engine or Rescue Support Vehicle | 400 |

The two requirement lines are additive. The mission therefore needs one guaranteed Fire Engine and one further qualifying appliance; the alternative must not replace the guaranteed appliance.

## Evidence safeguards

- Exact official ID, UK name, prerequisite, reward and resource quantities are retained.
- The official Fire Engine or Rescue Support Vehicle choice is represented through `requirements.alternatives`.
- No patients, personnel, probabilities, relationships, variants, overlays or unsupported additional fields are present.
- Strict key equivalence enforces both the guaranteed and alternative requirements.

## Coverage movement

```text
Before Batch 11
Canonical records:       153
Direct ID matches:       136
Fully canonical:          95
Remaining to canonical:  967

After Batch 11
Canonical records:       154
Direct ID matches:       137
Fully canonical:          96
Remaining to canonical:  966
```

Batch 11 raises identity coverage to **12.90%** and fully canonical coverage to **9.04%** of the 1,062-record official UK catalogue.

Promotion decisions are stored in:

```text
data/uk/mission-verification-batches/fully-canonical-fire-batch-11.json
```
