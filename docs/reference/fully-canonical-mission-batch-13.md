# Fully Canonical Mission Batch 13

Batch 13 promotes the 12 exact missions unlocked by the verified Police Car and Police Station mappings. The candidate analyser admits only records from approved generator families with no unresolved prisoner, patient, personnel, duration, variant or overlay semantics.

## Batch result

| ID | Mission | Fire Stations | Police Stations | Key dispatch features | Average credits |
|---:|---|---:|---:|---|---:|
| `127` | Bin Lorry Fire | 7 | 1 | 3 Fire Engines, 2 Fire Officers, 1 Police Car, 1 Water Carrier | 2,000 |
| `392` | Large fuel leak from vehicle | 2 | 2 | 1 Fire Engine, 2 Police Cars, plus 2 Fire Engines or Rescue Support Vehicles | 1,500 |
| `419` | Scrapyard Fire | 16 | 3 | 14 Fire Engines, command, aerial, BA, water, HazMat/CBRN and 4 Police Cars | 15,000 |
| `440` | Sinkhole opened up in road | 1 | 2 | 1 Fire Engine and 2 Police Cars | 1,000 |
| `441` | LPG Fuelled vehicle fire | 3 | 2 | 3 Fire Engines and 1 Police Car | 2,000 |
| `466` | Caravan roll over RTC | 1 | 4 | 1 Fire Engine, 4 Police Cars, plus 1 Fire Engine or Rescue Support Vehicle | 5,000 |
| `476` | Underground electrical cable fire (Medium) | 6 | 2 | 4 Fire Engines, 1 Fire Officer and 2 Police Cars | 2,000 |
| `477` | Underground electrical cable fire (Large) | 13 | 6 | 8 Fire Engines, command/HazMat alternatives, 4 Police Cars and 50% Water Carrier | 8,000 |
| `670` | Take away shop fire (Large) | 13 | 2 | 6 Fire Engines, command, aerial and 2 Police Cars | 11,000 |
| `682` | Forest fire exercise | 15 | 2 | 10 Fire Engines, command, 4 Water Carriers and 2 Police Cars | 24,000 |
| `775` | Trees blocking the roads after heavy storm | 4 | 2 | 4 Fire Engines, 3 Rescue Support Vehicles and 5 Police Cars | 2,000 |
| `841` | Smoke coming from company premises | 6 | 2 | 4 Fire Engines, 1 aerial and 2 Police Cars | 5,000 |

## Relationship evidence

The following published relationships are retained and resolve to official catalogue records:

- Scrapyard Fire expands into **Scrapyard Fire Large** (`420`).
- Underground electrical cable fire (Medium) expands into the large incident (`477`).
- Underground electrical cable fire (Large) expands into the major incident (`478`).
- Smoke coming from company premises expands into **Fire in an office building - Major Incident** (`145`).

## Evidence safeguards

- Exact official IDs, names, prerequisites, resources, probabilities, POIs, rewards and relationships are retained.
- `police_cars` is represented as the canonical Police Car quantity; compatible substitution is not used to alter the published requirement identity.
- `police_stations` is represented as the minimum Police Station prerequisite.
- HazMat/CBRN and ICCU/Ambulance Control choices remain explicit alternative groups.
- Additive Fire Engine/Rescue Support requirements remain distinct from guaranteed Fire Engines.
- Strict key equivalence is mandatory for all 12 promotions.
- Standard police generator support does not admit prisoner-bearing records until prisoner semantics are modelled separately.

## Coverage movement

```text
Before Batch 13
Canonical records:       155
Direct ID matches:       138
Fully canonical:          97
Remaining to canonical:  965

After Batch 13
Canonical records:       167
Direct ID matches:       150
Fully canonical:         109
Remaining to canonical:  953
```

Batch 13 raises identity coverage to **14.12%** and fully canonical coverage to **10.26%** of the 1,062-record official UK catalogue.

Promotion decisions are stored in:

```text
data/uk/mission-verification-batches/fully-canonical-fire-batch-13.json
```
