# Fire Wildfire, Flood and Water-Rescue Planning

Wildfire, flood, water-damage pumping and inland water rescue are related by geography, but they are not interchangeable MissionChief UK capabilities. A resilient Fire and Rescue network must distinguish frontline suppression, bulk water, incident command, flood rescue, pump throughput, rescue boats, towing vehicles and cross-service support.

!!! info "Evidence boundary"
    Exact mission requirements, preconditions, resource relationships, costs and training names below are reproduced from the current canonical UK records. Placement patterns, reserve targets, activation order and fleet depth are recommendations. Unpublished vehicle staffing, extension economics, parent-building compatibility, build time, pump units and unlock details remain unknown.

**Current evidence baseline:** 28 July 2026.

## Four separate operating systems

| System | Verified operational core | Do not assume |
|---|---|---|
| **Wildfire suppression** | Fire Engines, Fire Officers, Water Carriers and incident-control support where listed | That a separate wildfire vehicle or extension is required when no canonical record publishes one |
| **Flood rescue** | Flood Rescue Units and Flood Rescue Extensions on the missions that publish them | That a Water Carrier, rescue boat or pump container automatically replaces a Flood Rescue Unit |
| **Water-damage pumping** | Water Damage Pump Extensions and mission-level pump-speed/water-volume fields | That owning a Water Carrier proves the required pump throughput |
| **Inland water rescue** | Inland Rescue Boat trailer, trained crew, Lifeboat Station and Lifeboat 4×4 towing path | That an untowed trailer or unrelated vessel is dispatch-ready |

Use [Mission Lookup](../tools/mission-lookup.md) to inspect the exact incident before dispatching or purchasing. Use the [Concurrent Fleet Planner](../tools/fleet-planner.md) to test multiple incidents without double-counting vehicles, trailers, carriers or crews.

---

# Wildfire planning

## Verified wildfire escalation

The canonical wildfire and forest-fire records scale through ordinary Fire resources rather than a dedicated wildfire-resource contract.

| Representative mission | Verified guaranteed response | Other verified pressure |
|---|---|---|
| **Little forest fire** | 1 Fire Engine | Forest POI; 1 Fire Station precondition |
| **Candle Light Picnic Starts Wildfire** | 2 Fire Engines, 1 Fire Officer, 1 Water Carrier | 3 Fire Stations; event-window record retained in the catalogue |
| **Medium forest fire** | 4 Fire Engines, 2 Fire Officers, 1 Water Carrier | Forest POI; 3 Fire Stations |
| **Large Forest Fire** | 10 Fire Engines, 4 Fire Officers, 1 Water Carrier | 1 ICCU **or** Ambulance Control Unit; Forest POI; 15 Fire Stations |
| **Large Forest Fire — HART overlay** | Large Forest Fire response plus 1 Welfare Vehicle | 1 HART Base precondition |

!!! warning "No invented wildfire fleet"
    The current canonical resource estate does not publish a dedicated wildfire vehicle requirement for these representative missions. Do not convert real-world terminology into an unsupported in-game purchase rule.

## Wildfire readiness chain

```text
Forest mission pressure
        ↓
Local frontline Fire Engine depth
        ↓
Distributed Fire Officer command
        ↓
Bulk-water support
        ↓
Incident control and welfare where published
        ↓
Reserve for simultaneous routine incidents
```

### Frontline volume

Large wildfire incidents can remove ten Fire Engines from the normal network. A fleet that can complete one forest fire but leaves every nearby town without routine coverage is not resilient.

Recommended planning method:

1. calculate the largest verified wildfire response currently relevant to the account;
2. map which stations will supply those appliances;
3. reserve separate engines for simultaneous urban and rural calls;
4. verify that specialist crews are not borrowed from the same frontline appliances;
5. test the plan with at least one additional ordinary Fire mission.

### Command distribution

Medium and large forest fires publish multiple Fire Officer requirements. Avoid storing every officer in a single urban command base when rural travel time makes the resource operationally distant.

Recommended posture:

- keep one command path within each major rural response zone;
- add geographic duplication before stacking several officers at one station;
- preserve incident-control alternatives as separate resources rather than assuming a Fire Officer satisfies an ICCU or Ambulance Control Unit row;
- include HART welfare capacity when the applicable mission variant publishes it.

### Water supply

Medium and large forest fires publish a Water Carrier requirement. Treat Water Carrier availability as a distinct fleet decision from foam, flood rescue and pump throughput.

A Water/Foam Carrier is canonically capable of satisfying a Water Carrier requirement and has verified Fire Support availability, cost and staffing. That does not prove that every water-support asset satisfies every mission-level pumping field.

### Rural placement patterns

=== "Compact rural zone"

    - place frontline engines across the approach routes rather than at one central station;
    - keep one locally available Fire Officer and Water Carrier after routine demand;
    - use alliance support for rare second major incidents without treating it as guaranteed capacity;
    - measure actual road response time to Forest POIs.

=== "Mixed urban and rural network"

    - keep rural cover independent from the urban reserve calculation;
    - distribute command and water support between the two demand types;
    - prevent large rural dispatches from stripping every urban station;
    - position relief appliances where they can reinforce either zone.

=== "Multiple rural regions"

    - build independently dispatchable response clusters;
    - duplicate command and bulk-water capability by travel-time region;
    - retain enough frontline depth for a large wildfire in one region and routine calls elsewhere;
    - use measured concurrency rather than station count alone to justify duplication.

## Wildfire readiness checklist

- [ ] representative forest-fire requirements have been checked in Mission Lookup;
- [ ] the required Fire Engine volume can dispatch without emptying the wider network;
- [ ] Fire Officers are distributed by rural response time;
- [ ] Water Carrier capability is available and locally crewed;
- [ ] incident-control alternatives are modelled as their own requirement group;
- [ ] Welfare Vehicle coverage is included where the HART variant applies;
- [ ] no unsupported wildfire vehicle or extension requirement has been invented;
- [ ] a simultaneous routine incident has been tested in Fleet Planner.

---

# Flood-rescue and pumping planning

## Verified capability contracts

| Capability | Verified contract | Current boundary |
|---|---|---|
| **Flood Rescue Extension** | Countable mission-generation precondition for flood-rescue missions | Parent buildings, price, build time and capacity are unpublished |
| **Water Damage Pump Extension** | Countable mission-generation precondition for water-damage-pump missions | Parent buildings, price, build time and capacity are unpublished |
| **Flood Rescue Unit** | Discrete Fire and Rescue dispatch resource with verified flood-rescue capability | Cost, staffing, capacity and station compatibility are unpublished |
| **Flood Rescue Unit (Trailer)** | 35,000 credits or 20 coins; Flood First Responder Training; compatible Coastguard/Lifeboat flood expansions | Course duration and crew capacity are not published in the retained record |
| **High Volume Pump Container** | 20,000 credits or 8 coins; Fire Station with Container Extension; transported by Container Vehicle | Mission substitution and pump-performance units are not inferred |

The Coastguard/Lifeboat Flood Rescue Unit trailer has six verified towing vehicle types:

- Coastguard Rescue Vehicle;
- Coastguard Commander;
- Coastguard Mud Rescue Unit;
- Coastguard Rope Rescue Unit;
- Coastguard Support Unit;
- Lifeboat 4×4 Vehicle.

A stored trailer without one of its compatible staffed towing vehicles is not a complete response chain.

## Representative flood pressure

| Mission | Verified guaranteed response | Generation and pump pressure |
|---|---|---|
| **Person trapped in flood water** | 2 Coastguard Rescue Vehicles, 1 Flood Rescue Unit | 1 Flood Rescue Extension, 3 Rescue Stations, 2 Coastguard Rescue Stations; 1 patient |
| **Major flooding in a neighborhood following bad weather** | 3 Fire Engines, 3 Flood Rescue Units, 2 Rescue Support Vehicles, 3 Water Carriers | 3 ICCU or Ambulance Control Unit alternatives; 2 Flood Rescue Extensions; 1 Water Damage Pump Extension; pump-speed value 1,500; water amount 95,000 |
| **Rising waters of the canal (Flood)** | 6 Fire Engines, 5 Flood Rescue Units, 4 Police Cars, 6 Rescue Support Vehicles, 4 Water Carriers | 5 ICCU or Ambulance Control Unit alternatives; 3 Flood Rescue Extensions; 1 Water Damage Pump Extension; pump-speed value 1,500; water amount 150,000 |

!!! warning "Pump units remain unspecified"
    The canonical mission records publish numeric pump-speed and water-amount fields, but this guide does not invent engineering units or claim that a particular vehicle satisfies them without a reproduced dispatch contract.

## Flood response chain

```text
Flood or pump mission generator
            ↓
Flood Rescue Units and access resources
            ↓
Frontline Fire + Rescue Support
            ↓
Water Carrier and explicit pump throughput
            ↓
Command + Police + Coastguard/Lifeboat support
            ↓
Carrier, trailer and crew reserve
```

### Separate people rescue from water removal

A Flood Rescue Unit addresses a published rescue-resource requirement. Water-damage missions may also publish pump-speed and water-volume fields. These are separate operational constraints.

Do not assume:

- a rescue boat replaces a Flood Rescue Unit;
- a Water Carrier proves pump throughput;
- a High Volume Pump Container is usable without a Container Vehicle;
- one ICCU or Ambulance Control Unit satisfies several independent alternative quantities;
- extension count is equivalent to dispatch capacity.

### Pumping logistics

The High Volume Pump Container is a pod within the Fire container system. Operational availability requires:

1. a Fire Station with Container Extension;
2. the High Volume Pump Container;
3. an available Container Vehicle;
4. a staffed dispatch path;
5. enough carrier capacity for simultaneous container demand;
6. evidence that the selected resource satisfies the mission's current pump behaviour.

When one carrier serves several pods, the carrier can become the bottleneck even when every specialist container is owned.

### Flood geography

Place flood capability around response corridors rather than simply at the station with spare vehicle capacity.

Recommended inputs:

- river, canal, low-lying road and coastal access routes;
- distance between Flood Rescue Units and Water Carriers;
- towing-vehicle availability for trailers;
- container-carrier travel time;
- Police access and traffic-control support;
- Coastguard and Lifeboat station geography;
- second-incident reserve.

## Flood network patterns

=== "Single flood-response cluster"

    - one complete Flood Rescue Unit response chain;
    - nearby Fire Engines, Rescue Support and command;
    - one verified towing path for any trailer-based capability;
    - pump and carrier logistics documented separately;
    - alliance fallback for rare maximum-scale incidents.

=== "River or canal corridor"

    - distribute Flood Rescue Units along the waterway;
    - place Water Carriers and Rescue Support where they can reinforce either direction;
    - avoid centralising every command alternative at one end of the corridor;
    - duplicate towing or carrier capacity when travel distance creates a single point of failure.

=== "Regional severe-weather network"

    - maintain independently dispatchable flood groups across several zones;
    - duplicate critical rescue and pumping capability by geography;
    - preserve Fire, Police, Coastguard/Lifeboat and ambulance command capacity simultaneously;
    - test the verified canal-flood scale without exhausting the rest of the account.

---

# Inland water-rescue planning

## Inland Rescue Boat contract

The verified **Inland Rescue Boat (Trailer)** provides inland and coastal water-rescue capability. Its canonical contract publishes:

| Field | Verified value |
|---|---|
| Cost | **25,000 credits** or **15 coins** |
| Training | **Lifeboat Operations Training** |
| Building | **Lifeboat Station** |
| Towing vehicle | **Lifeboat 4×4 Vehicle** |
| Operating environment | Inland water and water |

The boat, towing vehicle and trained crew must be planned as one operational unit.

## Representative inland-water missions

### Canoeing accident

Verified requirements:

- 1 Fire Officer;
- 1 Inland Rescue Boat trailer;
- River POI;
- 6 Fire Stations, 2 Rescue Stations and 1 Technical Rescue Extension;
- 1–2 patients, generated at mission end;
- 90% transport probability and 30% critical-care probability.

### Vehicle trapped in flood water

Verified requirements:

- 2 Fire Engines;
- 1 Fire Officer;
- 1 Inland Rescue Boat trailer;
- 6 Fire Stations, 3 Rescue Stations and 1 Technical Rescue Extension;
- up to 4 patients with 40% transport probability.

These missions demonstrate that inland rescue may combine a Lifeboat trailer system with Fire generation and Fire command. Service ownership of the resource does not remove the need to plan the whole cross-service dispatch chain.

## Inland-water placement doctrine

- place the Lifeboat 4×4 and trailer together unless the game supports a reproduced alternative arrangement;
- keep trained personnel with the intended towing and launch base;
- position by road access to River and Lake POIs, not straight-line map distance;
- preserve a second towing path when one vehicle would cover several trailers;
- account for Fire Officer and frontline Fire requirements separately;
- plan ambulance capacity from the mission patient fields rather than assuming rescue completes medical care.

---

# Cross-service commissioning

Before activating another Flood Rescue, Water Damage Pump, Technical Rescue or related coastal generator:

1. select the largest representative mission currently relevant to the account;
2. list every guaranteed, alternative, patient, personnel and pump field;
3. map the vehicle, trailer, towing, carrier and training chain;
4. place the response against Forest, River, Lake, canal, road and coastal geography;
5. test the response alongside an ordinary Fire incident;
6. verify that no carrier, towing vehicle, command unit or trained cohort is counted twice;
7. activate one additional generator;
8. observe actual travel, pump and dispatch behaviour;
9. correct the measured bottleneck before further expansion.

## Common failures

| Failure | Operational symptom | Correction |
|---|---|---|
| Treating wildfire as a specialist-vehicle problem | Frontline and command volume remains insufficient | Build the verified Fire Engine, Fire Officer and Water Carrier depth |
| Activating Flood Rescue Extensions before units exist | Flood missions generate without a complete rescue chain | Staff and place the response before activation |
| Treating Water Carriers as pumps | Water assets attend but pump performance remains incomplete | Preserve the mission-level pump field and verify the correct resource |
| Owning a trailer without a towing reserve | Water-rescue capability cannot dispatch when the tow vehicle is committed | Keep a compatible staffed towing path |
| Owning pump pods without carriers | Containers remain stored during concurrent demand | Increase or distribute Container Vehicle capacity |
| Centralising rural and flood specialists | One distant incident removes capability from the whole network | Duplicate by travel-time zone or corridor |
| Planning Fire alone | Coastguard, Lifeboat, Police, HART or ambulance dependencies delay completion | Audit every service in the mission record |
| Guessing units or unpublished economics | Numeric fields become false operational facts | Keep the value and its boundary explicit |

## Readiness checklist

- [ ] wildfire planning uses verified mission pressure rather than an invented vehicle class;
- [ ] rural frontline reserve survives the largest relevant forest fire;
- [ ] Flood Rescue and Water Damage Pump extensions are treated as separate generators;
- [ ] Flood Rescue Units, Water Carriers and pump throughput are planned separately;
- [ ] High Volume Pump Containers have available Container Vehicles;
- [ ] water-rescue trailers have compatible towing vehicles and trained personnel;
- [ ] River, Lake, canal, coastal and rural road geography has been considered;
- [ ] cross-service command, Police, Coastguard/Lifeboat and medical support is ready;
- [ ] alternative quantities have not been double-counted;
- [ ] a simultaneous ordinary incident has been tested;
- [ ] unpublished values remain unknown rather than zero.

## Stage 37A continuation

Batch 5 completes the wildfire, flood, pumping and inland water-rescue operational layer. Return to [Fire & Rescue progression](fire-and-rescue.md), [specialist extension and container logistics](fire-and-rescue-specialists.md), [training and personnel planning](fire-training-and-personnel.md), or [airfield and railway response planning](fire-airfield-and-railway-planning.md).

Later Stage 37A work will cover major-incident resilience and mission-family pressure analysis derived from the complete canonical catalogue.
