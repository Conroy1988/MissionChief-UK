# Project Roadmap

MissionChief UK is maintained as an evidence-led information system rather than a one-off collection of articles.

## Core programme status

**Stages 1–36 are delivered.**

```text
1,079 canonical mission records
1,062 / 1,062 official missions fully canonical
104 deployable-resource records
20 infrastructure records
12 qualification records
73 / 73 observed vehicle type IDs mapped
936 / 936 vehicle field decisions resolved
Static Data API v1.3.0
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

- [x] Stage 21 — Railway response
- [x] Stage 22 — Specialist infrastructure
- [x] Stage 23 — Qualifications
- [x] Stage 24 — Vehicle economics and staffing
- [x] Stage 25 — Bomb Disposal enrichment
- [x] Stage 26 — Airfield enrichment
- [x] Stage 27 — Recovery enrichment
- [x] Stage 28 — Deterministic generated exports
- [x] Stage 29 — Complete browser-side mission lookup
- [x] Stage 30 — Resource and qualification comparison
- [x] Stage 31 — Concurrent fleet planning
- [x] Stage 32 — Deterministic query catalogue
- [x] Stage 33 — Generated FAQ
- [x] Stage 34 — Static Data API v1
- [x] Stage 35 — Complete canonical coverage for all 1,062 official UK missions

## Stage 36A — Complete deployable-resource coverage

**Status: complete.**

- [x] establish an evidence-tiered UK vehicle type ledger
- [x] compare source identities with canonical deployable-resource records
- [x] publish identity and raw field-completeness coverage separately
- [x] block duplicate IDs, dangling mappings and stale generated reports in CI
- [x] map every observed current UK vehicle type ID
- [x] create or reconcile every missing canonical resource identity
- [x] add official economics, staffing, training, building, towing, capacity and deployment contracts where reproducible
- [x] classify every tracked field as documented, not applicable, not published or review required
- [x] reach 73 / 73 observed identities with zero unresolved mappings
- [x] resolve 936 / 936 field decisions across 104 canonical resources
- [x] publish permanent schemas, JSON endpoints, evidence pages and regression enforcement
- [x] preserve unpublished values as unknown rather than zero

### Completion result

```text
104 canonical deployable resources
73 / 73 observed vehicle type IDs mapped
0 unresolved observed identities
9 tracked operational fields per resource
936 / 936 explicit field decisions resolved
0 unresolved field decisions
100% identity coverage
100% field-decision coverage
```

Canonical-only resources without an observed type-ID entry are explicit overlays or equipment records and do not represent an unresolved observed identity.

## Ongoing evidence maintenance

The numbered completion programmes are delivered. Remaining work is continuous source monitoring and evidence enrichment:

- reproduce additional published prices, staffing and training durations when suitable evidence appears;
- directly reproduce community-candidate type IDs in the current authenticated UK interface;
- verify currently unavailable EOD and Recovery response tables;
- add new UK missions, vehicles and game changes through fail-closed drift review;
- test overlapping alternative-resource dispatch allocation;
- enrich infrastructure cost, capacity and parent-building data;
- maintain API compatibility and publish future versioned releases;
- improve tools only when new verified fields support transparent calculations.

## Definition of complete

A subject is complete only when:

1. terminology and aliases are searchable;
2. exact values are verified and dated where they are published;
3. dependencies, alternatives, conditions and overlays are explicit;
4. unpublished and not-applicable fields have explicit decisions;
5. evidence boundaries are stated;
6. related documentation and structured records are linked;
7. validation covers the relevant relationships; and
8. a player can act without relying on an unexplained assumption.
