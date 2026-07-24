# Project Roadmap

MissionChief UK is maintained as an evidence-led information system rather than a one-off collection of articles.

## Core programme status

**Stages 1–35 are delivered.**

```text
1,079 canonical mission records
1,062 / 1,062 official missions fully canonical
59 deployable-resource records
19 infrastructure records
12 qualification records
Static data API v1.2.0
```

## Delivered foundation — Stages 1–12

- [x] project identity and information architecture
- [x] player journey and service-guide framework
- [x] vehicle, mission, building, personnel and training models
- [x] planning-tool architecture
- [x] evidence and verification standards
- [x] contribution controls and templates
- [x] Draft 2020-12 schemas and recursive validation
- [x] GitHub Pages delivery through Actions

## Delivered operational data — Stages 13–20

- [x] Fire and Rescue baseline and resource integrity
- [x] Ambulance and Police alternatives, patients and personnel
- [x] Coastguard, Lifeboat, trailer and ocean-rescue modelling
- [x] Mountain Rescue resources and explicit mission variants
- [x] Search and Rescue HQ, active Drone and missing-person operations
- [x] Bomb Disposal infrastructure and initial mission sequence
- [x] Airfield Operations, airport infrastructure and Code C/F incidents
- [x] Recovery Centres, HGV extensions and structured towing outcomes

## Delivered completion programme — Stages 21–35

### Stage 21 — Railway response

- [x] Railway Police and Railway fire response infrastructure
- [x] Road Rail Unit, EIU, BA support, Foam Unit and DSU resources
- [x] Railway Police and command personnel
- [x] passenger, goods and station incidents
- [x] personnel-range semantics
- [x] Railway service guide and Mission Batch 10

### Stage 22 — Specialist infrastructure

- [x] Police Helicopter Station
- [x] Public Order, Foam, Pump, Flood and Technical Rescue extensions
- [x] Mud Decontamination and Hovercraft extensions
- [x] referential enforcement and infrastructure Batch 2

### Stage 23 — Qualifications

- [x] production training schema
- [x] eleven verified operational-role records
- [x] qualification template and public catalogue
- [x] explicit separation of verified roles from unverified course details

### Stage 24 — Vehicle economics and staffing

- [x] structured credit, coin and crew fields
- [x] first official Coastguard economics set
- [x] market-data evidence standard
- [x] comparison-ready export fields

### Stage 25 — Bomb Disposal enrichment

- [x] busy beach and marina progression
- [x] small and large railway-station incidents
- [x] shed, loft and small building-site incidents
- [x] Mission Batch 11 with directory-level evidence boundaries

### Stage 26 — Airfield enrichment

- [x] Aircraft Accident Code A and Code D
- [x] Hot Brakes Code D
- [x] Bird Strike and Fuel Leak Code A
- [x] airport maintenance-hangar fire
- [x] Mission Batch 12

### Stage 27 — Recovery enrichment

- [x] motorbike and motocross recovery
- [x] HGV rollover and hazardous-goods recovery
- [x] bus, caravan and major multi-vehicle variants
- [x] collision between two buses
- [x] Mission Batch 13

### Stage 28 — Generated exports

- [x] deterministic mission, vehicle, infrastructure and training exports
- [x] version manifest and search index
- [x] validation and deployment integration

### Stage 29 — Mission lookup

- [x] browser-side mission search and service filtering
- [x] rendered preconditions, patients and requirement classes

### Stage 30 — Comparison

- [x] deployable-resource comparison
- [x] qualification comparison
- [x] visible unknown-value handling

### Stage 31 — Fleet planning

- [x] concurrent guaranteed-resource multiplier
- [x] independent alternative-group output
- [x] explicit scope limitations

### Stage 32 — Query catalogue

- [x] deterministic natural-language keyword matching
- [x] cross-collection generated search index
- [x] no unsupported generative inference

### Stage 33 — Generated FAQ

- [x] live collection counts
- [x] evidence-policy answers
- [x] Markdown and JSON outputs generated during builds

### Stage 34 — Static API

- [x] public v1 JSON endpoints
- [x] release versioning and manifest
- [x] OpenAPI 3.1 contract
- [x] API guide and compatibility policy

### Stage 35 — Complete canonical coverage

- [x] direct canonical records for all 1,062 official UK missions
- [x] strict source equivalence across requirements, patients, personnel, prisoners, recovery and operational metadata
- [x] lossless variants, overlays, relationships, duration, availability and generation controls
- [x] zero unmapped official requirement, chance or prerequisite keys
- [x] Batch 31 completion ledger and v1.2.0 publication

## Ongoing evidence maintenance

The numbered core programme and canonical mission backlog are complete. Remaining work is continuous source monitoring and evidence maintenance:

- reproduce additional vehicle prices, staffing and training durations;
- verify currently unavailable EOD and Recovery response tables;
- add new UK missions and game changes;
- test overlapping alternative-resource dispatch allocation;
- enrich infrastructure cost, capacity and parent-building data;
- maintain API compatibility and publish future versioned releases;
- improve tools when new verified fields support transparent calculations.

## Definition of complete

A subject is complete only when:

1. terminology and aliases are searchable;
2. exact values are verified and dated;
3. dependencies, alternatives, conditions and overlays are explicit;
4. evidence boundaries are stated;
5. related documentation and structured records are linked;
6. validation covers the relevant relationships;
7. a player can act without relying on an unexplained assumption.
