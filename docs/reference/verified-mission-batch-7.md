# Verified Mission Batch 7 — Bomb Disposal

This batch establishes the first schema-controlled Bomb Disposal mission records and the first production infrastructure records.

## Evidence boundary

The official UK mission directory confirmed the mission IDs, names, POIs, average rewards and building/extension preconditions. Individual mission detail pages were not consistently retrievable during verification, so unavailable vehicle and personnel requirements remain empty.

## Batch summary

| ID | Mission | POI | Verified preconditions | Average credits |
|---:|---|---|---|---:|
| `829` | Unexploded WW2 Ordnance in Countryside | Forest, Farm, Heathland | 6 Fire, 6 Rescue, 10 Police, 1 Bomb Disposal HQ | 4,500 |
| `830` | Unexploded WW2 Ordnance on Quiet Beach | Beach | 6 Fire, 6 Rescue, 10 Police, 1 Coastguard, 1 Bomb Disposal HQ, 1 Marine Unit Extension | 5,500 |
| `832` | Unexploded WW2 Ordnance in Harbour | Harbour | 6 Fire, 6 Rescue, 20 Police, 9 Coastguard, 1 HART, 3 Bomb Disposal HQs, 2 Marine Unit Extensions, 1 active Drone | 15,000 |
| `839` | Unexploded WW2 Bomb Located at Building Site (Large) | None listed | 6 Fire, 15 Rescue, 20 Police, 1 HART, 3 Bomb Disposal HQs, 1 active Drone | 11,500 |

## Infrastructure references

Mission preconditions now resolve to canonical infrastructure IDs:

```text
bomb_disposal_hq
bomb_disposal_marine_unit_extension
```

Repository validation fails if a mission uses either Bomb Disposal precondition without the matching infrastructure record.

## Active equipment

`active_drones` is a mission-generation precondition. It must remain separate from the dispatch requirement list. A mission requiring one active Drone does not, by itself, prove that a Drone must be sent.

## Machine-readable records

```text
data/uk/missions/
├── unexploded-ww2-bomb-building-site-large.json
├── unexploded-ww2-ordnance-in-countryside.json
├── unexploded-ww2-ordnance-in-harbour.json
└── unexploded-ww2-ordnance-on-quiet-beach.json

data/uk/infrastructure/
├── bomb-disposal-hq.json
└── bomb-disposal-marine-unit-extension.json
```

## Next evidence target

The next Bomb Disposal pass should reproduce the individual mission response tables and the current HQ/extension interfaces, including exact EOD resources, personnel, training, costs and capacities.
