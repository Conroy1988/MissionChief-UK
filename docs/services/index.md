# Emergency Services

This section provides operational references for every service group currently represented in the MissionChief UK guide and structured dataset.

## Active service guides

- [Fire and Rescue progression](fire-and-rescue.md) — **Stage 37A Batch 1**
- [Fire specialist extensions and containers](fire-and-rescue-specialists.md) — **Stage 37A Batch 2**
- [Fire training and personnel planning](fire-training-and-personnel.md) — **Stage 37A Batch 3**
- [Fire airfield and railway response planning](fire-airfield-and-railway-planning.md) — **Stage 37A Batch 4**
- [Fire wildfire, flood and water-rescue planning](fire-wildfire-flood-water-rescue.md) — **Stage 37A Batch 5**
- [Fire major-incident resilience](fire-major-incident-resilience.md) — **Stage 37A Batch 6**
- [Fire mission-family pressure analysis](fire-mission-family-pressure.md) — **Stage 37A Batch 7**
- [Ambulance and HART operational progression](ambulance.md) — **Stage 37B**
- [Police and Public Safety operational progression](police.md) — **Stage 37C**
- [Coastguard and Lifeboat operational progression](coastguard-and-lifeboat.md) — **Stage 37D**
- [Mountain Rescue operational progression](mountain-rescue.md) — **Stage 37E**
- [Search and Rescue HQ operational progression](search-and-rescue.md) — **Stage 37E**
- [Bomb Disposal and EOD operational progression](bomb-disposal.md) — **Stage 37F**
- [Airfield Operations operational progression](airfield-operations.md) — **Stage 37G**
- [Recovery and HGV Recovery operational progression](recovery.md) — **Stage 37H**
- [Railway Police and Railway Fire operational progression](railway-response.md) — **Stage 37I**

## Stage 37 operational-guide programme — complete

Stage 37 converts the completed mission and resource intelligence estate into practical, evidence-labelled operating guidance. The completed programmes are:

- **Stage 37A — Fire and Rescue:** progression, specialists, containers, training, airfield, railway, severe weather, major incidents and live mission-family pressure;
- **Stage 37B — Ambulance and HART:** patient throughput, routine transport, specialist response, HART commissioning, command, mass casualty, welfare, HEMS, scalable fleets and recovery;
- **Stage 37C — Police and Public Safety:** routine patrol, custody, armed, roads, dog, mounted, public order, air support, railway dependencies, scalable fleets and recovery;
- **Stage 37D — Coastguard and Lifeboat:** shore response, command, mud/rope/flood rescue, vessels, air rescue, trailer/towing logistics, geography, scalable fleets and recovery;
- **Stage 37E — Mountain Rescue and Search and Rescue HQ:** off-road response, search command, dogs, drones, operational support, personnel semantics, overlays, geography, scalable fleets and recovery;
- **Stage 37F — Bomb Disposal and EOD:** land, heavy, marine and railway ordnance progression, specialist-resource semantics, active Drone handling, cross-service readiness, geography and recovery;
- **Stage 37G — Airfield Operations:** extension progression, ARFF training, operations, command, water/foam/HazMat/access capability, Code B/D/C/F tiers, airport-base architecture and recovery;
- **Stage 37H — Recovery and HGV Recovery:** car/truck outcome semantics, dedicated/overlay missions, conditional resources, regional capacity, geography and recovery;
- **Stage 37I — Railway Police and Railway Fire:** infrastructure, rail access, investigation, BA/foam support, personnel, station/freight/tunnel/major-incident tiers, corridor architecture and recovery.

Recommendations remain clearly separated from verified game facts. Unpublished economics, staffing, capacities, training, towing relationships, hospital/custody/launch rules and unlock details remain unknown rather than being inferred.

The next programme is **Stage 38 — Cross-Service Account Progression**.

## Cross-service intelligence

The production data models shared dependencies rather than treating each service as isolated. Examples include:

- Railway incidents combining Fire, Railway Police, ordinary Police, Ambulance, HART and Search and Rescue;
- Bomb Disposal missions combining specialist crews/equipment with Fire, Police, HART, Coastguard, Lifeboat, Drone and Railway capability;
- Airfield incidents combining ARFF, operations, command, foam, water, HazMat, HART, Police and mass-casualty systems;
- wildfire and flood incidents combining Fire command, water supply, HART welfare, Police, Coastguard/Lifeboat and pumping capacity;
- inland water rescue using Lifeboat trailers within Fire-generated mission families;
- major incidents combining independent command slots, mass-casualty support, welfare, specialist access and regional reserve erosion;
- patient-heavy incidents where hospital journeys and critical-care pressure outlast the initial dispatch;
- public-order incidents combining educated officer cohorts, supervision, custody, patients and specialist transport;
- maritime incidents combining shore, vessel, air, towing, trained personnel and patient handoff;
- remote searches combining off-road access, command, dogs, drones, personnel, HART and air rescue;
- Recovery missions and variations separating emergency response from post-incident car/truck towing workloads.

## Standard service-guide structure

Every completed service guide documents:

1. buildings and extensions;
2. vehicles, trailers, aircraft and boats;
3. personnel capacities and qualifications;
4. training courses and classroom planning;
5. mission unlocks and cross-service dependencies;
6. fleet templates by account stage;
7. placement and geographic coverage;
8. common dispatch failures and remedies;
9. relevant scripts and intelligence tools;
10. evidence status and last-verification date.

## Ongoing maintenance

Future service work is treated as evidence enrichment rather than a missing core programme. New UK missions, vehicles, prices, training details and rule changes should enter through the existing schemas, validation pipeline and versioned API.
