# Fully Canonical Mission Batch 3

Batch 3 advances 28 additional Fire and Rescue missions through every verification gate using the existing verified Fire Engine and Fire Station key contract.

## Batch result

| ID | Mission | Fire Stations | Fire Engines | Base credits | Additional verified evidence |
|---:|---|---:|---:|---:|---|
| `32` | Harvester fire | 6 | 2 | 1,200 | Rural fire classification |
| `58` | Kitchen Fire | 2 | 2 | 1,000 | Preserved separately by official ID |
| `65` | Kitchen Fire | 2 | 2 | 1,000 | Preserved separately by official ID |
| `202` | Release of a person | 1 | 1 | 200 | — |
| `203` | Release of an item from a person | 1 | 1 | 200 | — |
| `313` | Natural gas leak | 2 | 2 | 800 | Rural fire classification |
| `334` | Arcing power lines | 1 | 1 | 500 | Rural and urban classifications |
| `352` | Small fire in nightclub | 2 | 2 | 3,000 | Nightclub POI; expands to Medium fire in nightclub |
| `365` | Ring Removal | 1 | 1 | 500 | — |
| `366` | Person Stuck in lift | 1 | 1 | 500 | Expands to Unwell Person Stuck in lift |
| `388` | Smell of burning (Residential) | 2 | 2 | 3,000 | Six resolved residential expansion missions |
| `399` | Fire in allotment (Small) | 1 | 1 | 700 | Allotment POI |
| `400` | Fire in allotment (Small) (Involving Cylinders) | 2 | 2 | 1,000 | Allotment POI |
| `421` | Late fire call | 1 | 1 | 500 | Rural and urban classifications |
| `435` | Person Locked Out of House | 1 | 1 | 500 | — |
| `468` | Tumble dryer fire in residential premises | 2 | 2 | 800 | — |
| `472` | Ceiling Collapse Minor | 1 | 1 | 600 | — |
| `475` | Underground electrical cable fire | 2 | 2 | 800 | Expands to medium variant |
| `535` | Lithium Battery Fire | 8 | 1 | 10,000 | — |
| `541` | Smoking Electrical Equipment | 1 | 1 | 800 | Rural and urban classifications |
| `570` | Fire in a paper mill | 2 | 4 | 780 | — |
| `577` | Person stuck in swing | 1 | 1 | 600 | — |
| `624` | Smell of petrol (domestic) | 1 | 1 | 1,500 | — |
| `638` | Fire - Electrical Installation | 1 | 2 | 1,500 | — |
| `668` | Take away shop fire (Small) | 3 | 2 | 3,000 | Take Away Shop POI; expands to medium variant |
| `772` | Vehicle Fluids Wash Down | 1 | 1 | 800 | — |
| `857` | Washing machine on fire | 3 | 1 | 1,010 | Launderette POI |
| `858` | Dryer on fire | 3 | 1 | 1,010 | Launderette POI |

## Evidence contract

Every promoted record satisfies all of the following:

- official mission ID and exact UK name match the canonical record;
- `requirements.firetrucks` maps to the same canonical `fire_engine` quantity;
- `prerequisites.fire_stations` maps to the same canonical Fire Station count;
- `prerequisites.main_building` is ignored only while its published value is exactly `0`;
- no unclassified requirement, chance or prerequisite key is present;
- no patient, personnel, probabilistic, conditional-resource, specialist-vehicle or overlay mechanic is omitted;
- base rewards are retained;
- published mission categories and POIs are retained;
- every represented expansion relationship resolves to an exact mission name in the retained official snapshot; and
- the final evidence-completeness audit is recorded in the Batch 3 verification registry.

## Deliberately withheld records

The candidate analyser also identified two superficially simple records:

- `318` — Reported fire in the open;
- `389` — Smell of burning (Commercial).

They were **not** promoted because one or more published expansion IDs could not be resolved to a retained official mission record. The unresolved relationship is treated as a blocker rather than being silently discarded.

## Coverage movement

```text
Before Batch 3
Canonical records:       79
Direct ID matches:       62
Fully canonical:         21
Remaining to canonical:  1,041

After Batch 3
Canonical records:       107
Direct ID matches:       90
Fully canonical:         49
Remaining to canonical:  1,013
```

Batch 3 raises fully canonical coverage from **1.98%** to **4.61%** of the complete 1,062-record official catalogue.

## Machine-readable evidence

Canonical records are stored under `data/uk/missions/`. Promotion decisions are stored in:

```text
data/uk/mission-verification-batches/fully-canonical-fire-batch-3.json
```

The base and batch registries are merged deterministically by:

```text
scripts/merge_verification_registry_batches.py
```

Strict quantity and prerequisite equivalence is enforced by:

```text
scripts/validate_official_key_mappings.py
```
