# MissionChief UK Structured Dataset

This directory contains the production machine-readable records used by the MissionChief UK knowledgebase, intelligence tools and static data API.

## Current inventory

```text
62 verified mission records
46 canonical vehicle-resource records
18 canonical infrastructure records
11 qualification records
11 represented operational service groups
13 published mission-data batches
```

## Collections

```text
data/uk/missions/         Mission requirements, variants and outcomes
data/uk/vehicles/         Deployable vehicles, trailers, boats and equipment
data/uk/infrastructure/   Buildings and extensions used by preconditions
data/uk/training/         Operational roles and verified course details
```

## Service coverage

The production dataset contains records across:

- Fire and Rescue;
- Ambulance and HART;
- Police and Public Order;
- Coastguard, Lifeboat and Ocean Rescue;
- Mountain Rescue;
- Search and Rescue HQ;
- Bomb Disposal and EOD;
- Airfield Operations;
- Recovery and HGV Recovery;
- Railway Police and Railway Fire Response;
- cross-service specialist operations.

## Requirement semantics

Mission records keep these concepts independent:

- guaranteed resources;
- probability-based resources;
- conditional resources;
- alternative resource groups;
- available, required, average-minimum, ranged and probabilistic personnel;
- patients and prisoners;
- towing outcomes;
- building and extension generation preconditions;
- base missions, additive overlays and mission variations.

## Validation guarantees

The repository validator checks:

1. valid JSON syntax;
2. applicable Draft 2020-12 schemas;
3. unique identifiers within each record type;
4. valid verification dates;
5. all mission resource references against canonical vehicle-resource IDs;
6. every resource inside alternative groups;
7. mapped infrastructure preconditions against canonical records;
8. patient, towing and personnel minimum/maximum ranges;
9. training and qualification record conformance.

## Generated outputs

During validation and GitHub Pages deployment, the repository produces:

```text
docs/assets/data/v1/
├── manifest.json
├── missions.json
├── vehicles.json
├── infrastructure.json
├── training.json
├── search-index.json
├── faq.json
└── openapi.json
```

The export release is controlled by `data/version.json`.

## Evidence boundary

`verified` applies only to populated fields. An omitted value is unknown, not zero. Empty response arrays may indicate that directory-level generation evidence was available while the individual response table was not.

Temporary event multipliers remain observations and never replace canonical average-credit values.
