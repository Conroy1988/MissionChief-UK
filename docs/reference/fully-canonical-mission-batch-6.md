# Fully Canonical Mission Batch 6

Batch 6 promotes the six exact missions unlocked by the verified `heavy_rescue_vehicles` mapping. The retained official key is mapped to the UK **Rescue Support Vehicle**, with same-key probabilities handled separately where present.

## Batch result

| ID | Mission | Fire Stations | Fire Engines | Fire Officer | Aerial Appliance | Rescue Support Vehicle | Average credits |
|---:|---|---:|---:|---:|---|---:|---:|
| `59` | Animal Rescue | 6 | 1 | — | — | 1 | 900 |
| `139` | Fire in silo | 8 | 8 | 2 | 1 guaranteed | 1 | 3,000 |
| `314` | Rescue from stuck ride | 6 | 2 | 1 | 1 at 80% | 1 | 2,000 |
| `404` | Animal stuck between walls | 4 | 1 | — | — | 1 | 1,300 |
| `815` | Large Animal Rescue | 4 | 1 | — | 1 guaranteed | 1 | 2,000 |
| `824` | Fire in stables | 6 | 6 | 2 | 1 guaranteed | 1 | 4,500 |

## Mapping evidence

The official **Stuck Climber** page publishes one Rescue Support Vehicle. The retained catalogue represents that quantity using `requirements.heavy_rescue_vehicles`. The canonical resource record `rescue_support_vehicle` already preserves the same official source.

The mapping contract is:

| Official field | Canonical interpretation |
|---|---|
| `requirements.heavy_rescue_vehicles` | Rescue Support Vehicle quantity |
| `chances.heavy_rescue_vehicles` | Probability that the published quantity is required |

## Evidence safeguards

- Every record was selected by `scripts/report_canonical_candidates.py` after the mapping passed the complete deterministic suite.
- Exact official IDs, names, station prerequisites, resource quantities and rewards are retained.
- POIs for Farm, Silo and Theme Park are preserved where published.
- Rescue from stuck ride retains its 80% Aerial Appliance Truck probability.
- No unresolved relationships, patients, personnel, overlays, variants or unsupported additional fields are present.
- Strict key equivalence is mandatory for all six promotions.

## Coverage movement

```text
Before Batch 6
Canonical records:       127
Direct ID matches:       110
Fully canonical:         69
Remaining to canonical:  993

After Batch 6
Canonical records:       133
Direct ID matches:       116
Fully canonical:         75
Remaining to canonical:  987
```

Batch 6 raises fully canonical coverage from **6.50%** to **7.06%** of the 1,062-record official UK catalogue.

Promotion decisions are stored in:

```text
data/uk/mission-verification-batches/fully-canonical-fire-batch-6.json
```
