# Buildings and Extensions Database

This reference defines how stations, support buildings, specialist extensions and destination buildings are documented.

## Production infrastructure model

Stage 18 introduces the first schema-controlled infrastructure records under:

```text
data/uk/infrastructure/
```

Each record identifies:

- canonical UK game name and ID;
- building or extension kind;
- service ownership;
- valid parent buildings where verified;
- mission-generation capabilities;
- evidence status and verification date;
- explicit omissions for unverified costs, timings or capacities.

## First verified records

| Canonical ID | Name | Kind | Verified effect |
|---|---|---|---|
| `bomb_disposal_hq` | Bomb Disposal HQ | Building | Bomb Disposal mission precondition |
| `bomb_disposal_marine_unit_extension` | Bomb Disposal Marine Unit Extension | Extension | Coastal and marine Bomb Disposal precondition |

Mission fields referencing these entities are checked by the repository validator.

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

## Extension record standard

Extensions require their own records because they may affect:

- which vehicles can be purchased;
- which personnel courses become relevant;
- which missions may generate;
- available capacity;
- operating cost and expansion order.

## Evidence boundary

A verified infrastructure record applies only to populated fields. Stage 18 confirms the Bomb Disposal entities and their mission-precondition relationships; it does not yet publish costs, build durations, vehicle slots or personnel capacity.

## Planning guidance

A building recommendation must distinguish confirmed mechanics from account-specific strategy. Geography, available credits, staffing, alliance support and current mission bottlenecks can all change the correct expansion order.

## Future integration

These records will support the building planner, cost calculator, training planner and mission unlock explorer.
