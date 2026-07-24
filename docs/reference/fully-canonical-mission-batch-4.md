# Fully Canonical Mission Batch 4

Batch 4 introduces the first chance-aware canonical mission set. It advances **five** Fire and Rescue missions after verifying the official Aerial Appliance Truck and Fire Officer requirement and probability keys against the retained UK catalogue.

## Batch result

| ID | Mission | Fire Stations | Fire Engines | Aerial Appliance | Fire Officer | Average credits |
|---:|---|---:|---:|---|---|---:|
| `21` | Chimney fire | 3 | 1 | 1 at 10% | 1 guaranteed | 1,900 |
| `22` | Roof fire | 3 | 3 | 1 guaranteed | 1 at 50% | 2,700 |
| `31` | Fireplace fire | 6 | 3 | — | 1 guaranteed | 1,310 |
| `301` | Unsafe Structure | 3 | 1 | 1 at 20% | — | 1,000 |
| `353` | Medium fire in nightclub | 6 | 4 | 1 at 10% | 1 guaranteed | 6,000 |

## New verified official-key mappings

| Official field | Canonical interpretation |
|---|---|
| `requirements.platform_trucks` | Aerial Appliance Truck quantity |
| `chances.platform_trucks` | Probability that the Aerial Appliance Truck quantity is required |
| `requirements.battalion_chief_vehicles` | Fire Officer quantity |
| `chances.battalion_chief_vehicles` | Probability that the Fire Officer quantity is required |

The validator treats these requirement keys as **chance-aware**. When no same-key chance is published, the resource is guaranteed. A probability from 1–99 creates an exact canonical probabilistic requirement. A value of 100 is guaranteed; a value of 0 is omitted.

## Identity and relationship integrity

- Chimney fire retains its published expansion to Roof fire.
- Roof fire retains the official self-referential follow-up.
- Unsafe Structure is bound to current official ID `301`; obsolete ID `344` belongs to a different mission and is not used.
- Medium fire in nightclub retains the Nightclub POI, expansion to Large fire in nightclub and Smoke Inhalation follow-up.
- The retained official source repeats the same Smoke Inhalation follow-up ID three times; the schema-compliant canonical relationship is stored once and the multiplicity is documented.
- Fifteen provisional records were removed after strict identity validation proved that their assumed IDs belonged to different UK missions. They were never accepted as evidence-valid Batch 4 records.

## Coverage movement

```text
Before Batch 4
Canonical records:       107
Direct ID matches:       90
Fully canonical:         49
Remaining to canonical:  1,013

After Batch 4
Canonical records:       112
Direct ID matches:       95
Fully canonical:         54
Remaining to canonical:  1,008
```

Batch 4 raises fully canonical coverage from **4.61%** to **5.08%** of the complete 1,062-record official UK catalogue.

## Evidence sources

The mapping semantics are supported by the official Roof fire record, which publishes one Aerial Appliance Truck, one Fire Officer and a 50% Fire Officer probability, together with the retained official JSON catalogue and verified canonical resource records.

Promotion decisions are stored in:

```text
data/uk/mission-verification-batches/fully-canonical-fire-batch-4.json
```

Strict chance-aware equivalence and aggregate identity diagnostics are enforced by:

```text
scripts/validate_official_key_mappings.py
scripts/report_promoted_mapping_failures.py
```
