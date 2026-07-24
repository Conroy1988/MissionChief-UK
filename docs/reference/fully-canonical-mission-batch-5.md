# Fully Canonical Mission Batch 5

Batch 5 promotes the **15 missions selected directly by the evidence-safe candidate analyser** after Batch 4. Every record uses an exact current official ID and name, only previously verified Fire Engine, Fire Officer and Aerial Appliance Truck mappings, and no unsupported operational fields.

## Batch result

| ID | Mission | Fire Stations | Fire Engines | Fire Officer | Aerial Appliance | Average credits |
|---:|---|---:|---:|---:|---:|---:|
| `232` | Manhole fire | 6 | 2 | 1 | — | 210 |
| `236` | Burning freight car | 6 | 5 | 1 | — | 1,500 |
| `317` | Burning Substation | 2 | 2 | 1 | — | 1,000 |
| `401` | Fire in allotment (Medium) | 6 | 4 | 2 | — | 2,000 |
| `481` | Fire in turbine | 6 | 4 | 2 | — | 6,000 |
| `482` | Fire in turbine (Nuclear Power station) | 8 | 6 | 3 | — | 8,000 |
| `513` | Cell Fire | 6 | 2 | 1 | — | 1,500 |
| `517` | Prison Wing Fire | 10 | 4 | 3 | — | 6,000 |
| `575` | Fire in wind turbine | 6 | 2 | 1 | — | 1,500 |
| `597` | Persons stuck on scaffolding | 4 | 1 | — | 1 | 1,200 |
| `669` | Take away shop fire (Medium) | 6 | 4 | 1 | — | 6,000 |
| `849` | Roof tiles loose in the gutter | 3 | 1 | — | 1 | 840 |
| `850` | Roof tiles loose on the roof | 3 | 1 | — | 1 | 840 |
| `851` | Gutter at risk of being blown off | 3 | 1 | — | 1 | 840 |
| `852` | Solar panels at risk of falling off the roof | 3 | 1 | — | 1 | 840 |

## Evidence safeguards

- The complete set was generated from the retained official snapshot by `scripts/report_canonical_candidates.py`.
- Every requirement, chance and prerequisite key was already classified in `data/uk/official-key-mappings.json`.
- Every relationship ID resolves to a retained official mission.
- No patients, personnel, overlays, variants, unsupported generator families or unresolved additional fields are present.
- Duplicate-name mission ID `236` uses an ID-qualified filename to preserve identity unambiguously.
- Strict key equivalence remains mandatory for every promotion.

## POIs and relationships retained

- Goods station — Burning freight car.
- Allotment — Fire in allotment (Medium).
- Power Plant — Fire in turbine, with expansion to Power station fire.
- Nuclear power station — nuclear turbine fire, with major-incident expansion.
- Prison — Cell Fire and Prison Wing Fire, with their published escalation paths.
- Windmill Park — Fire in wind turbine.
- Take Away Shop — medium fire, with expansion to the large incident.

## Coverage movement

```text
Before Batch 5
Canonical records:       112
Direct ID matches:       95
Fully canonical:         54
Remaining to canonical:  1,008

After Batch 5
Canonical records:       127
Direct ID matches:       110
Fully canonical:         69
Remaining to canonical:  993
```

Batch 5 raises fully canonical coverage from **5.08%** to **6.50%** of the complete 1,062-record official UK catalogue.

Promotion decisions are stored in:

```text
data/uk/mission-verification-batches/fully-canonical-fire-batch-5.json
```
