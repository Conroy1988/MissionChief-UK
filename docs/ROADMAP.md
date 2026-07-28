# Project Roadmap

MissionChief UK is maintained as an evidence-led operational information system rather than a one-off collection of articles.

## Programme status

**Stages 1–42 are delivered.**

```text
Release: v1.4.0
API contract: v1
Official UK missions: 1,062
Canonical mission records: 1,079
Fully canonical official records: 1,062 / 1,062
Deployable-resource records: 104
Infrastructure records: 20
Training and role records: 12
Observed vehicle type IDs mapped: 73 / 73
Vehicle field decisions resolved: 936 / 936
Service operational programmes: complete
Cross-service strategy: complete
Alliance Operations: complete
Account Readiness Planner: complete
UX and accessibility audit: complete
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

## Delivered operational data — Stages 13–27

- [x] Fire, Ambulance and Police baseline modelling
- [x] Coastguard, Lifeboat, trailer and ocean-rescue contracts
- [x] Mountain Rescue and Search and Rescue HQ
- [x] Bomb Disposal and EOD
- [x] Airfield Operations
- [x] Recovery and HGV Recovery
- [x] Railway Police and Railway Fire Response
- [x] specialist infrastructure and qualifications
- [x] vehicle economics, staffing, training and logistics enrichment
- [x] explicit patient, prisoner, recovery, personnel and variant semantics

## Delivered data and tool platform — Stages 28–36

- [x] Stage 28 — deterministic generated exports
- [x] Stage 29 — complete browser-side mission lookup
- [x] Stage 30 — resource and qualification comparison
- [x] Stage 31 — concurrent fleet planning
- [x] Stage 32 — deterministic query catalogue
- [x] Stage 33 — generated FAQ
- [x] Stage 34 — Static Data API v1
- [x] Stage 35 — complete canonical coverage for all current official UK missions
- [x] Stage 36 — complete deployable-resource identity and field-decision coverage
- [x] Stage 36B — path-aware draft validation and exact ready-state release gates

## Delivered operational-guide programme — Stage 37A–37I

- [x] Fire and Rescue progression, specialist systems, training, airfield/railway, severe weather, major incidents and live mission-family pressure
- [x] Ambulance and HART patient throughput, specialist response, command, mass casualty, welfare and HEMS
- [x] Police and Public Safety patrol, custody, armed, roads, dog, mounted, public order, air support and railway dependencies
- [x] Coastguard and Lifeboat shore, vessel, air, trailer, towing, mud, rope and flood rescue
- [x] Mountain Rescue and Search and Rescue HQ off-road, search, command, drone, dog and personnel systems
- [x] Bomb Disposal and EOD land, heavy, marine and railway ordnance response
- [x] Airfield Operations ARFF, command, operations, foam, water, HazMat, access and casualty tiers
- [x] Recovery and HGV Recovery outcome semantics, overlays, regional capacity and recovery-to-readiness
- [x] Railway Police and Railway Fire corridor, hub, tunnel, command and major-incident resilience

## Delivered strategy and operations — Stages 38–41

### Stage 38 — Cross-Service Account Progression

- [x] universal expansion gates and readiness states
- [x] foundation through mature regional account models
- [x] cross-service dependency and handoff matrix
- [x] route-, destination-, access-, cluster-, hub- and relief-base station placement
- [x] urban, rural, coastal and alliance-supported assumptions

### Stage 39 — Alliance Operations

- [x] member, dispatcher and administrator modes
- [x] onboarding, permissions and least privilege
- [x] contribution-policy and shared-infrastructure models
- [x] mutual support, donor reserve, events and major incidents
- [x] recruitment, inactivity, moderation and external-tool boundaries

### Stage 40 — Account Readiness Planning Suite

- [x] local-only mission scenarios and explicit protected reserve
- [x] guaranteed resource aggregation
- [x] capacity-aware allocation across independent alternative groups
- [x] personnel generation and incident thresholds
- [x] separate towing/carrier and recovery-workload checks
- [x] reversible browser storage and JSON import/export
- [x] no MissionChief authentication, scraping or mutation

### Stage 41 — Guide UX, Accessibility and Navigation

- [x] replace remaining Getting Started and Game Systems frameworks
- [x] accessible long-page section navigation
- [x] mobile-safe tables, code blocks, media and content containment
- [x] visible keyboard focus and sticky-heading offsets
- [x] complete programme route acceptance on Chromium, iPhone and iPad WebKit
- [x] critical WCAG A/AA checks on primary command and interactive surfaces

## Stage 42 — v1.4.0 release and completion report

**Status: complete when the exact release SHA is deployed and published.**

- [x] compatible semantic version selected
- [x] release metadata advanced to v1.4.0 / Stage 42
- [x] release notes and completion report written
- [x] public README, Command Centre, API and roadmap reconciled
- [ ] deterministic exports and generated FAQ synchronised
- [ ] complete release-grade validation passed
- [ ] exact release head merged to `main`
- [ ] GitHub Pages production deployment verified
- [ ] immutable annotated `v1.4.0` tag and GitHub Release published

## Maintenance programme

After v1.4.0, work enters controlled maintenance lanes rather than a new completion backlog:

1. **Upstream drift** — changed official missions, resources, documentation or field semantics;
2. **Evidence enrichment** — directly reproduced unknown economics, staffing, capacity, training or substitution fields;
3. **Defect correction** — canonical, guide, tool, accessibility, CI or production regressions; and
4. **Compatible enhancement** — additive guidance or browser capabilities that preserve the v1 contract.

Priority maintenance targets include:

- new UK missions, vehicles and game changes through fail-closed drift review;
- direct reproduction of currently unpublished infrastructure, vehicle and course fields;
- authenticated-interface reproduction of community-candidate resource identities;
- continued validation of overlapping alternatives and live substitution behaviour;
- routing and geographic optimisation only when suitable location and privacy controls exist;
- API compatibility and future versioned releases; and
- physical-device checks to complement automated browser coverage.

## Definition of complete

A subject is complete only when:

1. terminology and aliases are searchable;
2. exact values are verified and dated where published;
3. dependencies, alternatives, conditions and overlays are explicit;
4. unpublished and not-applicable fields have explicit decisions;
5. evidence boundaries are stated;
6. related documentation and structured records are linked;
7. validation covers the relevant relationships; and
8. a player can act without relying on an unexplained assumption.
