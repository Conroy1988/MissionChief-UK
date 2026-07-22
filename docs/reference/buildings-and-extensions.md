# Buildings and Extensions Database

This reference defines how stations, support buildings, specialist extensions and destination buildings are documented.

## Production infrastructure model

Schema-controlled records are stored under:

```text
data/uk/infrastructure/
```

Each record identifies:

- canonical UK game name and ID;
- building or extension kind;
- service ownership;
- parent buildings where verified;
- mission-generation capabilities;
- evidence status and verification date;
- explicit omissions for unverified costs, timings or capacities.

## Current verified records

| Canonical ID | Name | Kind | Verified effect |
|---|---|---|---|
| `bomb_disposal_hq` | Bomb Disposal HQ | Building | Bomb Disposal mission precondition |
| `bomb_disposal_marine_unit_extension` | Bomb Disposal Marine Unit Extension | Extension | Coastal and marine Bomb Disposal precondition |
| `hart_base` | HART Base | Building | HART mission precondition |
| `aviation_firefighting_extension` | Aviation firefighting Extension | Extension | Airport-firefighting mission precondition |
| `airfield_operations_extension` | Airfield Operations Extension | Extension | Airfield-operations mission precondition |
| `mass_casualty_extension` | Mass Casualty Extension | Extension | Mass-casualty mission precondition |

Mapped mission preconditions are checked by the repository validator.

## Stage 19 airport infrastructure

### Aviation firefighting Extension

This extension is required by verified airport missions from Bird Strike Code B through Aircraft Accident Code F. The exact capitalization used by current UK mission pages is retained as the canonical display name.

### Airfield Operations Extension

Aircraft Accident Codes C and F require one or more Airfield Operations Extensions before generation. This precondition is distinct from the Airfield Operations Vehicles required at the incident.

### Mass Casualty Extension

Codes C and F include a Mass Casualty Extension precondition and a separate Mass Casualty Equipment dispatch requirement. The infrastructure and deployable resource must not be conflated.

### HART Base

HART Base is now a canonical infrastructure record because verified missions across several services use it as a generation precondition. It does not itself prove that a particular HART vehicle is required.

## Building record standard

Mature records should capture:

- canonical UK game name;
- building category and service;
- confirmed purchase cost;
- build time and level structure;
- vehicle capacity;
- personnel and classroom capacity;
- extension compatibility;
- mission-generation effects;
- unlock conditions;
- destination or transport function;
- alliance ownership behaviour, where relevant;
- evidence status and verification date.

## Evidence boundary

A verified infrastructure record applies only to populated fields. Current records confirm entity names and mission-precondition relationships; they do not yet publish costs, build durations, vehicle slots or personnel capacity.

## Planning guidance

A building recommendation must distinguish confirmed mechanics from account-specific strategy. Geography, available credits, staffing, alliance support and current mission bottlenecks can all change the correct expansion order.

## Future integration

These records will support the building planner, cost calculator, training planner and mission unlock explorer.
