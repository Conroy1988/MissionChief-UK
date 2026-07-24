# Fully Canonical Mission Batch 2

This batch advances ten additional low-complexity Fire and Rescue missions through every verification gate.

## Batch result

| ID | Mission | Fire Stations | Fire Engines | Base credits | Additional verified evidence |
|---:|---|---:|---:|---:|---|
| `13` | Burning truck | 2 | 2 | 980 | — |
| `14` | Little field fire | 2 | 2 | 1,000 | Expands to Little forest fire |
| `15` | Little forest fire | 1 | 1 | 1,010 | Forest POI |
| `16` | Caravan fire | 2 | 2 | 1,100 | — |
| `17` | Postbox on fire | 1 | 1 | 340 | Follow-ups: Burning leaves, Roof fire |
| `18` | Out of control bonfire | 1 | 1 | 700 | — |
| `19` | Burning trailer | 1 | 1 | 650 | Follow-ups: Burning leaves, Roof fire |
| `23` | Grease Fire | 3 | 1 | 1,200 | — |
| `24` | Burning bus shelter | 3 | 1 | 900 | Bus stop POI |
| `27` | Garage fire | 4 | 2 | 1,400 | — |

## Evidence contract

Every record in this batch satisfies all of the following:

- the official mission ID and exact UK name match the canonical record;
- `requirements.firetrucks` is mapped to the same quantity of canonical `fire_engine` resources;
- `prerequisites.fire_stations` is mapped to the same canonical Fire Station count;
- `prerequisites.main_building` is accepted as non-operational only because the published value is exactly `0`;
- no unclassified requirement, chance or prerequisite key is present;
- no patient, personnel, probability, conditional-resource or specialist-vehicle mechanic is omitted;
- the base average reward is retained;
- published POIs, expansion missions and follow-up relationships are represented; and
- the final evidence-completeness audit is explicitly recorded in the mission-verification registry.

## Coverage movement

```text
Before Batch 2
Canonical records:       69
Direct ID matches:       52
Fully canonical:         11
Remaining to canonical:  1,051

After Batch 2
Canonical records:       79
Direct ID matches:       62
Fully canonical:         21
Remaining to canonical:  1,041
```

Batch 2 raises fully canonical coverage from **1.04%** to **1.98%** of the 1,062-record official UK catalogue.

## Machine-readable records

```text
data/uk/missions/burning-truck.json
data/uk/missions/little-field-fire.json
data/uk/missions/little-forest-fire.json
data/uk/missions/caravan-fire.json
data/uk/missions/postbox-on-fire.json
data/uk/missions/out-of-control-bonfire.json
data/uk/missions/burning-trailer.json
data/uk/missions/grease-fire.json
data/uk/missions/burning-bus-shelter.json
data/uk/missions/garage-fire.json
```

The promotion decisions are retained under `data/uk/mission-verification-registry.json` and are checked by `scripts/validate_official_key_mappings.py`.
