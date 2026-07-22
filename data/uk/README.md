# MissionChief UK Structured Dataset

This directory contains the production machine-readable records used by the MissionChief UK knowledgebase.

## Current inventory

```text
36 verified mission records
39 canonical vehicle-resource records
8 canonical infrastructure records
10 represented operational service groups
9 published mission-data batches
```

### Stage 20 mission records

- `784` — Abandoned Car Obstructing Road
- `785` — Broken Down Car Obstructing Road
- `2-recovery-overlay` — Burning car recovery variation
- `13-hgv-recovery-overlay` — Burning truck HGV recovery variation
- `129-recovery-overlay` — Multi vehicle RTC recovery variation
- `782-recovery-overlay` — Non-Injury RTC with Police Car recovery variation

### Stage 20 infrastructure records

- `recovery_centre` — Recovery Centre
- `hgv_recovery_extension` — HGV Recovery Extension

The full inventories remain available through the public reference pages and the JSON files under this directory.

## Service coverage

The production dataset now contains records across:

- Fire and Rescue;
- Ambulance and HART support;
- Police;
- Coastguard;
- Lifeboat and Ocean Rescue;
- Mountain Rescue and land search;
- Search and Rescue HQ and drone-enabled operations;
- Bomb Disposal and EOD mission generation;
- Airfield Operations and airport firefighting;
- Recovery and HGV recovery operations.

Railway Police, railway fire response and other specialist services remain future controlled population batches.

## Validation guarantees

The repository validator checks:

1. valid JSON syntax;
2. conformance with the applicable Draft 2020-12 schema;
3. unique identifiers within each record type;
4. valid date formats;
5. guaranteed, probabilistic and conditional mission resources against canonical IDs;
6. every resource inside every alternative requirement group;
7. that patient minimums do not exceed patient maximums;
8. that towing minimums do not exceed towing maximums;
9. specialist mission preconditions against canonical infrastructure records.

A mission fails validation when it references an unknown deployable resource, an invalid towing range or a mapped infrastructure entity that does not exist under `data/uk/infrastructure/`.

## Recovery modelling

Stage 20 introduces `recovery.assets` for the number and type of assets that must be towed after an incident.

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

Towing is kept separate from the Vehicle and Personnel Requirements table. It must not be converted into a fictional emergency-response vehicle requirement.

## Conditional-resource modelling

`requirements.conditional` can now preserve an optional probability as well as its trigger. Multi vehicle RTC uses this for a Traffic Car with a 50% requirement probability that applies only when available.

## Evidence boundary

The dedicated Abandoned Car and Broken Down Car response pages were unavailable during Stage 20 verification. Their directory-visible fields are verified; unavailable towing and response details remain intentionally absent.

Temporary event multipliers are not stored as base rewards unless explicitly identified as observations rather than canonical values.
