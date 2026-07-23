# Fully Canonical Mission Batch 4

Batch 4 introduces the first chance-aware canonical mission set. It advances 20 Fire and Rescue missions after verifying the official Aerial Appliance Truck and Fire Officer requirement and probability keys.

## Batch result

| ID | Mission | Fire Stations | Fire Engines | Aerial Appliance | Fire Officer | Base credits |
|---:|---|---:|---:|---|---|---:|
| `21` | Chimney fire | 2 | 1 | 1 at 10% | 1 guaranteed | 1,300 |
| `22` | Roof fire | 3 | 3 | 1 guaranteed | 1 at 50% | 2,700 |
| `31` | Fireplace fire | 2 | 2 | — | 1 guaranteed | 620 |
| `180` | Fire involving Acetylene cylinders | 8 | 4 | — | 1 guaranteed | 4,000 |
| `344` | Unsafe Structure | 2 | 1 | 1 at 20% | — | 1,000 |
| `353` | Medium fire in nightclub | 5 | 4 | 1 at 10% | 1 guaranteed | 4,000 |
| `361` | Warehouse fire | 5 | 3 | 1 guaranteed | 1 guaranteed | 3,000 |
| `452` | Small fire in hospital | 3 | 2 | 1 guaranteed | 1 guaranteed | 3,000 |
| `456` | Plane fire (Small) | 3 | 2 | — | 1 guaranteed | 3,000 |
| `460` | Motorbike showroom fire | 3 | 2 | — | 1 guaranteed | 3,000 |
| `494` | Freighter fire (Small) | 3 | 3 | 1 guaranteed | — | 2,500 |
| `512` | Fire in Chinese restaurant | 3 | 2 | — | 1 guaranteed | 1,500 |
| `520` | Shed fire on roof | 3 | 2 | — | 1 guaranteed | 1,500 |
| `547` | Extraction system fire | 3 | 2 | 1 guaranteed | 1 guaranteed | 1,800 |
| `672` | Fire in Hotel (Small) | 3 | 2 | — | 1 guaranteed | 2,500 |
| `708` | Small Fire in Supermarket | 3 | 2 | — | 1 guaranteed | 2,500 |
| `734` | Pub Fire (Small) | 3 | 2 | — | 1 guaranteed | 2,500 |
| `768` | Small Restaurant Kitchen fire | 3 | 2 | — | 1 guaranteed | 2,500 |
| `774` | Small fire in Cinema | 3 | 2 | 1 guaranteed | 1 guaranteed | 2,500 |
| `779` | Small fire in museum | 3 | 2 | 1 guaranteed | 1 guaranteed | 2,500 |

## New verified official-key mappings

| Official field | Canonical interpretation |
|---|---|
| `requirements.platform_trucks` | Aerial Appliance Truck quantity |
| `chances.platform_trucks` | Probability that the Aerial Appliance Truck quantity is required |
| `requirements.battalion_chief_vehicles` | Fire Officer quantity |
| `chances.battalion_chief_vehicles` | Probability that the Fire Officer quantity is required |

The validator treats these requirement keys as **chance-aware**. When no same-key chance is published, the resource is guaranteed. A probability from 1–99 creates an exact canonical probabilistic requirement. A value of 100 is guaranteed; a value of 0 is omitted.

## Relationship integrity

- Roof fire retains the official self-referential follow-up.
- Medium fire in nightclub retains Smoke Inhalation once in the schema-compliant relationship list and records that the official source repeats the same ID three times.
- Every other published expansion and follow-up ID resolves to an exact retained official mission name.
- POIs for Nightclub, Warehouse, Hospital, Small Airfield, Motorbike Dealership, Cargo port, Chinese Restaurant, High rise, Take Away Shop, Hotel, Supermarket, Pub, Restaurant, Cinema and Museum are retained.

## Coverage movement

```text
Before Batch 4
Canonical records:       107
Direct ID matches:       90
Fully canonical:         49
Remaining to canonical:  1,013

After Batch 4
Canonical records:       127
Direct ID matches:       110
Fully canonical:         69
Remaining to canonical:  993
```

Batch 4 raises fully canonical coverage from **4.61%** to **6.50%** of the complete 1,062-record official UK catalogue.

## Evidence sources

The mapping semantics are supported by the official Roof fire record, which publishes one Aerial Appliance Truck, one Fire Officer and a 50% Fire Officer probability, together with the retained official JSON catalogue and existing verified canonical resource records.

Promotion decisions are stored in:

```text
data/uk/mission-verification-batches/fully-canonical-fire-batch-4.json
```

Strict chance-aware equivalence is enforced by:

```text
scripts/validate_official_key_mappings.py
```
