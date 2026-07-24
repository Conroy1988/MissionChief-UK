# Fully Canonical Mission Batch 7

Batch 7 promotes the nine exact missions unlocked by the verified `water_tankers` mapping. The official key is mapped to the UK **Water Carrier**, with same-key probabilities retained as probabilistic canonical requirements.

## Batch result

| ID | Mission | Fire Stations | Fire Engines | Fire Officer | Aerial Appliance | Water Carrier | Average credits |
|---:|---|---:|---:|---:|---|---|---:|
| `107` | Row of garages on fire | 8 | 5 | 1 | — | 1 at 20% | 3,000 |
| `153` | Hay shed fire - Large | 13 | 8 | 6 | 1 guaranteed | 2 guaranteed | 9,000 |
| `175` | Landfill fire | 8 | 4 | 3 | — | 1 guaranteed | 3,500 |
| `178` | Medium forest fire | 3 | 4 | 2 | — | 1 guaranteed | 4,000 |
| `248` | Burning manure pile | 7 | 2 | — | — | 1 guaranteed | 1,500 |
| `249` | Large Hay bale stack on fire | 7 | 3 | — | — | 1 guaranteed | 2,000 |
| `250` | Harvester on fire in field | 7 | 2 | — | — | 1 guaranteed | 1,000 |
| `402` | Fire in allotment (Large) | 8 | 6 | 3 | — | 1 at 30% | 3,000 |
| `406` | Stack of containers on fire | 10 | 8 | 6 | 1 at 40% | 1 at 60% | 8,000 |

## Mapping evidence

The official **Car workshop fire - persons reported** page publishes one Water Carrier with a 40% requirement probability. Existing canonical Water Carrier evidence is also retained from current UK airfield incidents.

The mapping contract is:

| Official field | Canonical interpretation |
|---|---|
| `requirements.water_tankers` | Water Carrier quantity |
| `chances.water_tankers` | Probability that the published Water Carrier quantity is required |

## Evidence safeguards

- Every record was selected by the evidence-safe candidate analyser after the Water Carrier mapping passed the complete deterministic suite.
- Exact official IDs, names, station prerequisites, resource quantities, probabilities and rewards are retained.
- POIs for Farm, Landfill site, Forest, Allotment and Container Holding Area are preserved.
- Stack of containers on fire retains independent Aerial Appliance Truck and Water Carrier probabilities.
- No unresolved relationships, patients, personnel, overlays, variants or unsupported additional fields are present.
- Strict key equivalence is mandatory for all nine promotions.

## Coverage movement

```text
Before Batch 7
Canonical records:       133
Direct ID matches:       116
Fully canonical:         75
Remaining to canonical:  987

After Batch 7
Canonical records:       142
Direct ID matches:       125
Fully canonical:         84
Remaining to canonical:  978
```

Batch 7 raises fully canonical coverage from **7.06%** to **7.91%** of the 1,062-record official UK catalogue.

Promotion decisions are stored in:

```text
data/uk/mission-verification-batches/fully-canonical-fire-batch-7.json
```
