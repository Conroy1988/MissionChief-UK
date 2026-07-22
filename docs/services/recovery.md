# Recovery and HGV Recovery

Recovery operations cover obstructing vehicles, police seizures, collision clear-up and HGV towing in MissionChief UK.

## Current verified scope

Stage 20 publishes:

- Recovery Centre generation preconditions;
- HGV Recovery Extension generation preconditions;
- dedicated Recovery Vehicle Missions;
- recovery-enabled Fire and Police mission variations;
- car and truck towing ranges;
- a conditional resource that is both probability-based and available-only.

## Infrastructure

### Recovery Centre

The Recovery Centre generates dedicated Recovery Vehicle Missions and enables recovery variations of Fire, Police and Ambulance incidents.

The current record verifies the building name and its mission-generation relationship. Purchase price, capacity, staffing and vehicle inventory remain unpublished until reproduced from the current building interface.

### HGV Recovery Extension

The HGV Recovery Extension enables truck, bus, caravan and heavy-vehicle recovery variations.

The guide does not currently claim a parent building, cost, construction time or slot capacity because those attributes were not exposed by the mission pages used for Stage 20.

## Towing is not a dispatch requirement

Official mission pages place towing quantities under **Other information**, separately from Vehicle and Personnel Requirements.

The dataset therefore stores towing as:

```json
{
  "recovery": {
    "assets": [
      {
        "asset_type": "car",
        "minimum": 2,
        "maximum": 4
      }
    ]
  }
}
```

This does not create a fictional `Recovery Vehicle` dispatch row. It records the verified operational outcome: how many cars or trucks must be towed.

## Mission variations

Recovery often appears as an additive variation of an existing mission:

- Burning car gains one Recovery Centre and one car to tow;
- Burning truck gains one HGV Recovery Extension and one truck to tow;
- Multi vehicle RTC gains one Recovery Centre and two to four cars to tow.

These records use unique string IDs while preserving the official source mission ID.

## Conditional and probabilistic resources

The verified Multi vehicle RTC recovery variation states that one Traffic Car has a 50% requirement probability and applies only when available.

Both conditions are retained:

```json
{
  "resource": "traffic_car",
  "quantity": 1,
  "condition": "only_when_available",
  "probability": 0.5
}
```

## Evidence boundary

The dedicated Abandoned Car and Broken Down Car pages were not retrievable during Stage 20 verification. Their IDs, names, rewards, Recovery Centre preconditions and mission type are verified from the official directory; unavailable towing and dispatch details remain omitted.

## Related records

- [Verified Mission Batch 9](../reference/verified-mission-batch-9.md)
- [Mission Database](../reference/mission-database.md)
- [Buildings and Extensions](../reference/buildings-and-extensions.md)
