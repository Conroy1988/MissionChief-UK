# Vehicle Economics and Staffing

Stage 24 introduces structured, schema-validated vehicle economics and crew data.

## Structured fields

Verified vehicle records may now include:

```json
{
  "cost": {
    "credits": 20000,
    "coins": 15
  },
  "staffing": {
    "minimum": 1,
    "maximum": 5
  }
}
```

Either field is omitted when the current UK vehicle market or a suitable official source does not verify it.

## First verified economics set

| Resource | Credits | Coins | Crew | Training |
|---|---:|---:|---:|---|
| CRV | 20,000 | 15 | 1–5 | — |
| Coastguard Mud Rescue Unit | 20,000 | 15 | 1–5 | Mud Rescue Training |
| Coastguard Rope Rescue Unit | 35,000 | 20 | 1–5 | Rope Rescue Training |
| Coastguard Commander | 25,000 | 15 | 1–5 | Coastal Command Training |

The official UK Help Center also verifies the available station types for these resources.

## Interpretation rules

- A mission requirement does not prove a vehicle-market cost.
- A personnel requirement does not prove a vehicle crew capacity.
- Maximum crew is not the same as the minimum qualified crew needed for a capability.
- A training label is stored only when the official source explicitly associates it with the vehicle.
- An empty or absent field means **unverified**, not zero.

## Evidence coverage

The production resource catalogue contains more resources than the initial economics set. Remaining prices and staffing limits continue to be review targets rather than assumed values.

## Primary source

The initial verified set is based on the official Mission Chief Help Center article covering Search and Rescue vehicles in the UK version.
