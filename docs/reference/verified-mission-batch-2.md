# Verified Mission Batch 2

The second production batch expands the structured mission dataset from simple single-resource incidents into overlays, timed missions, points of interest and conditional multi-service requirements.

!!! info "Base rewards"
    Credit values on this page are the base average rewards. Temporary event multipliers are not included.

## Batch summary

| ID | Mission | Guaranteed resources | Conditional resources | Base average credits |
|---:|---|---|---|---:|
| `2` | Burning car | 1 Fire engine | None | 370 |
| `6` | Garden shed fire | 2 Fire engines | None | 600 |
| `521` | Community Engagement (Fire) | 1 Fire engine | None | 6,000 |
| `797` | Person in large enclosure | 1 Fire engine | 1 Aerial Appliance Truck at 15%; 1 Police car at 30% | 1,180 |

## Burning car

**Canonical ID:** `2`  
**Unlock:** 1 Fire Station  
**Guaranteed:** 1 Fire engine  
**Base average reward:** 370 credits

The base mission is recorded separately from the Recovery Centre additive-overlay variant, which the official mission directory lists at a higher reward and with a towing requirement.

Possible expansions:

- Garage fire
- Caravan fire
- Burning trailer

Possible follow-ups:

- Burning motorbike
- Burning leaves

[Official UK mission directory](https://www.missionchief.co.uk/einsaetze)

## Garden shed fire

**Canonical ID:** `6`  
**Unlock:** 2 Fire Stations  
**Guaranteed:** 2 Fire engines  
**Base average reward:** 600 credits

Possible follow-ups:

- Burning leaves
- Roof fire

[Official UK mission record](https://www.missionchief.co.uk/einsaetze/6)

## Community Engagement (Fire)

**Canonical ID:** `521`  
**Unlock:** 1 Fire Station  
**Guaranteed:** 1 Fire engine  
**Duration:** 60 minutes  
**Points of interest:** School or Mall  
**Base average reward:** 6,000 credits

[Official UK mission record](https://www.missionchief.co.uk/einsaetze/521)

## Person in large enclosure

**Canonical ID:** `797`  
**Unlock:** 3 Fire Stations, 2 Rescue Stations and 2 Police Stations  
**Point of interest:** Zoo  
**Base average reward:** 1,180 credits

Guaranteed resource:

- 1 Fire engine

Conditional resources:

- 1 Aerial Appliance Truck with a 15% requirement probability;
- 1 Police car with a 30% requirement probability.

The official page also lists one patient, a 60% transport probability, General Internal specialisation, possible codes C-2 and C-3, and between three and nine minimum firefighters.

[Official UK mission record](https://www.missionchief.co.uk/einsaetze/797)

## Machine-readable records

```text
data/uk/missions/
├── burning-car.json
├── community-engagement-fire.json
├── garden-shed-fire.json
└── person-in-large-enclosure.json
```

These files use the expanded mission schema, including structured preconditions, mission types, points of interest, duration and probabilistic requirements.