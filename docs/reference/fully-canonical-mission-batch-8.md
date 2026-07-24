# Fully Canonical Mission Batch 8

Batch 8 promotes the six exact missions unlocked by the verified `mobile_command_vehicles` mapping. The official requirement is preserved as a qualifying alternative group: one **ICCU** or one **Ambulance Control Unit** satisfies each published command-unit quantity.

## Batch result

| ID | Mission | Fire Stations | Fire Engines | Fire Officer | Aerial Appliance | Rescue Support | Water Carrier | ICCU / Ambulance Control | Average credits |
|---:|---|---:|---:|---:|---|---|---|---|---:|
| `169` | Heathland fire - large | 13 | 8 | 3 | — | — | 1 guaranteed | 1 alternative | 8,000 |
| `177` | Large field fire | 20 | 10 | 6 | — | — | 2 guaranteed | 1 alternative | 7,000 |
| `243` | Large Forest Fire | 15 | 10 | 4 | — | — | 1 guaranteed | 1 alternative | 9,500 |
| `244` | Stack of tyres on fire | 15 | 15 | 6 | 2 guaranteed | — | 2 guaranteed | 1 alternative | 13,000 |
| `256` | Heathland fire - medium | 13 | 6 | 3 | — | — | 1 guaranteed | 1 alternative | 6,000 |
| `518` | Prison Wing Fire (Major Incident) | 15 | 8 | 5 | 1 guaranteed | 1 guaranteed | 1 at 5% | 1 alternative | 10,000 |

## Mapping evidence

Current UK mission pages publish the requirement label **ICCU or Ambulance Control Units**. Both canonical resources are independently verified and the mission schema already supports exact alternative-resource groups.

The mapping contract is:

| Official field | Canonical interpretation |
|---|---|
| `requirements.mobile_command_vehicles` | Quantity satisfied by ICCU or Ambulance Control Unit |
| Canonical representation | `requirements.alternatives` with resources `iccu` and `ambulance_control_unit` |

## Evidence safeguards

- Every record was selected by the evidence-safe candidate analyser after alternative-group mapping passed two consecutive deterministic validation cycles.
- Exact official IDs, names, station prerequisites, resource quantities, probabilities, rewards and POIs are retained.
- The official requirement is not inflated into two simultaneous guaranteed resources.
- Mission 518 retains its independent 5% Water Carrier probability.
- No unresolved relationships, patients, personnel, overlays, variants or unsupported additional fields are present.
- Strict key equivalence is mandatory for all six promotions, including exact alternative resource set and quantity.

## Coverage movement

```text
Before Batch 8
Canonical records:       142
Direct ID matches:       125
Fully canonical:          84
Remaining to canonical:  978

After Batch 8
Canonical records:       148
Direct ID matches:       131
Fully canonical:          90
Remaining to canonical:  972
```

Batch 8 raises identity coverage to **12.34%** and fully canonical coverage to **8.47%** of the 1,062-record official UK catalogue.

Promotion decisions are stored in:

```text
data/uk/mission-verification-batches/fully-canonical-fire-batch-8.json
```
