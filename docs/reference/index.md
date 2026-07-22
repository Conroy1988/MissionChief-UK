# Reference Database

The reference layer exposes concise human-readable records and machine-readable data generated from the same evidence-led production collections.

## Production inventory

```text
62 missions
46 deployable resources
18 infrastructure records
11 qualifications
13 mission batches
```

## Core references

- [Verified Mission Records](verified-mission-records.md)
- [Mission Database and Semantics](mission-database.md)
- [Verified Vehicle Records](verified-vehicle-records.md)
- [Vehicle Economics and Staffing](vehicle-economics-and-staffing.md)
- [Buildings and Extensions](buildings-and-extensions.md)
- [Training and Personnel](training-and-personnel.md)
- [Generated FAQ](generated-faq.md)
- [Generated Data Exports](data-exports.md)

## Verified batches

Mission Batches 2–13 document progressive Fire, Ambulance, Police, maritime, Mountain Rescue, Search and Rescue, Bomb Disposal, Airfield, Recovery and Railway evidence sets.

## Interactive access

The same records power:

- [Mission Requirement Lookup](../tools/mission-lookup.md)
- [Resource and Qualification Comparison](../tools/resource-comparison.md)
- [Concurrent Fleet Planner](../tools/fleet-planner.md)
- [Natural-Language Query Catalogue](../tools/query-catalogue.md)
- [Static Data API](../api/index.md)

## Design principles

- stable machine-readable identifiers;
- exact UK display names plus verified aliases;
- explicit data types and units;
- source and verification metadata;
- separate guaranteed, probabilistic, conditional and alternative requirements;
- relationships between missions, resources, infrastructure and qualifications;
- deterministic generated indexes;
- validation before publication;
- unknown values remain unknown rather than silently becoming zero.

See the [data standard](data-standard.md) for the complete publication contract.
