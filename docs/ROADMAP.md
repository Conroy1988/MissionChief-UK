# Project Roadmap

MissionChief UK is developed as a maintained information system rather than a one-off collection of articles.

## Delivered foundation

- [x] Searchable MkDocs Material documentation site
- [x] GitHub Pages deployment
- [x] Evidence and verification standards
- [x] Structured mission, vehicle and infrastructure schemas
- [x] Recursive JSON Schema validation
- [x] Mission-to-resource referential-integrity checks
- [x] Mission-to-infrastructure precondition checks
- [x] Patient and towing range semantics
- [x] Issue forms and pull-request evidence controls
- [x] Script compatibility, installation and recovery framework
- [x] Planning-tool architecture

## Delivered data stages

### Stages 12–17

- [x] Initial Fire mission and resource records
- [x] Ambulance and Police alternatives, patients and personnel
- [x] Coastguard, Lifeboat, trailer and ocean-rescue modelling
- [x] Mountain Rescue resources and mission variants
- [x] Search and Rescue HQ, active-Drone and missing-person operations

### Stage 18 — Bomb Disposal and EOD baseline

- [x] Bomb Disposal HQ and Marine Unit Extension records
- [x] first production infrastructure schema
- [x] mission-to-infrastructure validation
- [x] countryside, beach, harbour and large building-site missions
- [x] Bomb Disposal service guide and Mission Batch 7
- [ ] exact EOD vehicle and personnel records
- [ ] HQ and extension costs, capacities and construction times
- [ ] railway Bomb Disposal and remaining mission variants

Unchecked Stage 18 items remain controlled enrichment work and must not be guessed.

### Stage 19 — Airfield Operations

- [x] Aviation firefighting and Airfield Operations extension records
- [x] Mass Casualty Extension and HART Base infrastructure records
- [x] airport runway POI distinctions
- [x] RIV, Major Foam Tender and Water Carrier records
- [x] Airfield Firefighting Command and Airfield Operations vehicles
- [x] shared command, hazardous-materials, casualty and traffic resources
- [x] conditional Traffic Car requirements
- [x] Bird Strike Code B and Aircraft Accident Codes C/F
- [x] Airfield Operations service guide and Mission Batch 8
- [ ] remaining Code A/D and Hot Brakes missions
- [ ] airport maintenance-hangar and control-tower incidents
- [ ] prices, staffing, training and extension construction data
- [ ] dispatch-allocation testing for overlapping command alternatives

### Stage 20 — Recovery and HGV recovery operations

- [x] Recovery Centre infrastructure record
- [x] HGV Recovery Extension infrastructure record
- [x] mission-to-Recovery infrastructure validation
- [x] structured car, truck and generic-vehicle towing ranges
- [x] towing minimum/maximum semantic validation
- [x] conditional requirements with optional probability
- [x] base versus recovery-enabled mission variants
- [x] dedicated Recovery Vehicle Missions
- [x] Recovery service guide and Mission Batch 9
- [ ] Recovery Centre and HGV extension prices, capacity and construction data
- [ ] directly verified Recovery vehicle inventory and staffing
- [ ] remaining HGV, bus, caravan and railway recovery variants

Unchecked Stage 20 enrichment items require direct building or vehicle-interface evidence.

## Current production baseline

```text
36 verified mission records
39 canonical vehicle-resource records
8 canonical infrastructure records
10 represented operational service groups
9 published mission batches
```

## Stage 21 — Railway Police and railway fire response

Next controlled targets:

- [ ] Railway Police and Railway fire response infrastructure records
- [ ] Railway Police and specialist rail-response resources
- [ ] rail POI distinctions and aliases
- [ ] base versus Railway Police mission variations
- [ ] passenger, goods and level-crossing incidents
- [ ] rail incidents with HGV Recovery dependencies
- [ ] Railway service guide
- [ ] verified Railway mission batch

## Later structured-data stages

- [ ] broader building and extension production records
- [ ] training and qualification production records
- [ ] current vehicle prices and staffing limits
- [ ] remaining Bomb Disposal enrichment
- [ ] remaining Airfield Operations enrichment
- [ ] remaining Recovery enrichment
- [ ] generated indexes and public data exports

## Interactive intelligence layer

- [ ] Mission requirement lookup
- [ ] Vehicle and training comparison tools
- [ ] Station and fleet planning calculators
- [ ] Natural-language query catalogue
- [ ] FAQ generated from verified records
- [ ] Public API or versioned exports

## Definition of complete

A subject is complete only when:

1. terminology and aliases are searchable;
2. exact values are verified and dated;
3. dependencies, alternatives, conditions and overlays are explicit;
4. evidence boundaries are stated;
5. related documentation and structured records are linked;
6. validation covers the relevant relationships;
7. a player can act without relying on an unexplained assumption.
