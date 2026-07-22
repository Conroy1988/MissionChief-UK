# MissionChief UK Structured Dataset

This directory contains the production machine-readable records used by the MissionChief UK knowledgebase.

## Current inventory

```text
30 verified mission records
39 canonical vehicle-resource records
6 canonical infrastructure records
9 represented operational service groups
8 published mission-data batches
```

### Stage 19 mission records

- `587` — Aircraft Accident - Code C
- `588` — Aircraft Accident - Code F
- `593` — Bird Strike - Code B

### Stage 19 infrastructure records

- `aviation_firefighting_extension` — Aviation firefighting Extension
- `airfield_operations_extension` — Airfield Operations Extension
- `mass_casualty_extension` — Mass Casualty Extension
- `hart_base` — HART Base

### Stage 19 deployable resources

- `riv` — RIV
- `major_foam_tender` — Major Foam Tender
- `water_carrier` — Water Carrier
- `airfield_firefighting_command_vehicle` — Airfield Firefighting Command Vehicle
- `airfield_operations_vehicle` — Airfield Operations Vehicle
- `fire_officer` — Fire Officer
- `hazmat_unit` — HazMat Unit
- `cbrn_vehicle` — CBRN Vehicle
- `iccu` — ICCU
- `ambulance_control_unit` — Ambulance Control Unit
- `rescue_stairs` — Rescue Stairs
- `traffic_car` — Traffic Car
- `mass_casualty_equipment` — Mass Casualty Equipment

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
- Airfield Operations and airport firefighting.

Recovery, Railway Police and other specialist services remain future controlled population batches.

## Validation guarantees

The repository validator checks:

1. valid JSON syntax;
2. conformance with the applicable Draft 2020-12 schema;
3. unique identifiers within each record type;
4. valid date formats;
5. guaranteed, probabilistic and conditional mission resources against canonical IDs;
6. every resource inside every alternative requirement group;
7. that patient minimums do not exceed patient maximums;
8. specialist mission preconditions against canonical infrastructure records.

A mission fails validation when it references an unknown deployable resource or a mapped infrastructure entity that does not exist under `data/uk/infrastructure/`.

## Conditional-resource modelling

Stage 19 introduces `requirements.conditional`. Aircraft Accident Codes C and F use this for Traffic Cars that are required only when available.

Conditional requirements are neither guaranteed nor recommended. Their exact trigger is preserved in the `condition` field.

## Airfield alternative groups

Airfield incidents may contain several independent alternative groups. Some resources, especially Airfield Firefighting Command Vehicles, can appear in more than one group and as a dedicated requirement. Records preserve every official requirement row separately rather than inventing a minimum unique-vehicle total.

## Evidence boundary

Stage 19 records verify current mission-page fields, but do not yet publish purchase prices, staffing limits, training durations, infrastructure costs or dispatch-allocation behaviour across overlapping alternatives.

Temporary event multipliers are not stored as base rewards unless explicitly identified as observations rather than canonical values.
