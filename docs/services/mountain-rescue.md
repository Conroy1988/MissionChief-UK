# Mountain Rescue Operational Progression

Mountain Rescue operations combine off-road response, technical rescue, search coordination, specialist personnel, difficult geography and cross-service medical support. The operational unit is therefore a regional response chain, not one 4x4 parked at a Mountain Rescue Station.

!!! info "Evidence boundary"
    Verified statements reproduce current canonical mission, vehicle, personnel and training records. Fleet sizes, reserve floors, placement patterns and commissioning sequences are recommendations. Vehicle economics, staffing, station capacities, specialist-course details and route-speed differences remain unknown where unpublished.

**Current evidence baseline:** 28 July 2026.

## Command doctrine

Use this order when expanding:

1. **Off-road access first** — maintain enough qualifying Mountain Rescue or SAR 4x4 capability for current mission pressure.
2. **Command and search support second** — Control Vans and Search Dog Units can be hard requirements even when 4x4 volume is sufficient.
3. **Preserve alternatives** — Mountain Rescue 4x4 **or** SAR 4x4 means one shared quantity across the group, not one of each.
4. **Overlay capability before activation** — HART and helicopter variants add separate infrastructure and response chains.
5. **Personnel before apparent fleet size** — Search Advisor, Cave Rescue Specialist and other roles can block completion independently of vehicles.
6. **Geography and recovery before another station** — remote travel and patient extraction can keep resources unavailable long after arrival.

[Open Mission Lookup](../tools/mission-lookup.md) · [Open Concurrent Fleet Planner](../tools/fleet-planner.md) · [Compare Resources](../tools/resource-comparison.md)

## Mountain response chain

```text
Mountain or remote-area mission pressure
                ↓
Mountain Rescue / SAR 4x4 alternatives
                ↓
Control, search dog and technical-rescue support
                ↓
Specialist personnel and overlay resources
                ↓
Patient access, treatment and transport
                ↓
Return to regional off-road reserve
```

## Verified core resources

| Resource | Verified function | Current evidence boundary |
|---|---|---|
| **Mountain Rescue 4x4** | Mountain rescue and off-road response | Price, crew and training remain unpublished |
| **SAR 4x4** | Search-and-rescue and off-road response | Price, crew and training remain unpublished |
| **Control Van** | Search coordination and incident command | Price, crew, training and building relationship remain unpublished |
| **Search Dog Unit** | Missing-person and terrain search | Price, crew, training and building relationship remain unpublished |
| **Rescue Support Vehicle** | Technical-rescue support | Price, crew and training remain unpublished |
| **ATV Carrier** | All-terrain HART support | HART Base; Tactical Command Course, 5 days, Rescue (EMS) Academy; price and staffing unpublished |
| **Coastguard Rescue Helicopter** | Air rescue, treatment and transport | SAR Airbase; Coastal Air Rescue Operations; verified aircraft contract documented in the Coastguard guide |
| **PRV / SRV / Welfare Vehicle** | HART and prolonged-incident support | Use the verified Ambulance and HART contracts rather than expanding abbreviations or inventing substitutes |

[Review the Vehicle Catalogue](../reference/vehicle-catalogue.md) · [Open Ambulance and HART progression](ambulance.md)

## Alternative 4x4 groups

When a mission publishes:

```text
Mountain Rescue 4x4 OR SAR 4x4 — quantity 2
```

any valid combination may satisfy the group where the game permits both resource types. The quantity applies to the group as a whole.

Do not convert this into:

- two Mountain Rescue 4x4s **plus** two SAR 4x4s;
- one fixed vehicle type without evidence;
- a claim that both vehicles have identical price, staffing or speed.

### Recommended off-road reserve

- Keep enough qualifying 4x4s for the largest relevant mission plus one protected regional route.
- Duplicate by travel-time zone when one remote incident empties several stations.
- Do not count a vehicle as reserve when its crew is normally assigned to another specialist.
- Use actual route and custom-spawn geography rather than station count alone.

## Command and search support

### Control Van

Control Vans provide verified search coordination and command on Mountain and SAR missions. A single central unit can become a regional failure point when two searches overlap.

Recommended posture:

- commission one reliable command route before repeated search missions;
- add replacement personnel before duplicating the vehicle;
- distribute command by travel-time region when one unit cannot reach the network reliably;
- preserve Control Van availability separately from general 4x4 capacity.

### Search Dog Unit

Search Dog Units are verified specialist search resources. Their economics and training remain unpublished in the current canonical record.

Recommended posture:

- maintain one dispatchable dog-search route in each active remote region;
- protect replacement staffing;
- test overlap with Police dog demand only where mission contracts allow the relevant resource;
- do not assume a Police DSU automatically substitutes for a Search Dog Unit.

## Base missions and overlays

Mountain Rescue uses distinct base and overlay records. The overlay adds its own preconditions and requirements; it does not rewrite the base mission into one universal contract.

### Stuck Climber

Verified pressure:

- 1 Fire Engine;
- 1 Rescue Support Vehicle;
- 1 Mountain Rescue 4x4 **or** SAR 4x4;
- 50% probability of 1 Aerial Appliance Truck;
- 75% probability of 1 Operational Team Leader;
- 1 patient generated at mission end;
- 30% transport probability.

This mission demonstrates guaranteed, alternative and probabilistic fields in one response. Preserve all three semantics.

### Overdue Hikers

Verified pressure:

- 1 Control Van;
- 1 Search Dog Unit;
- 2 Mountain Rescue 4x4s and/or SAR 4x4s across one alternative group;
- up to 3 patients generated at mission end;
- 25% transport probability;
- custom spawn area.

This is a search-coordination mission rather than a simple 4x4 dispatch.

### Fall Whilst Fell Running — HART overlay

Verified overlay pressure:

- 1 ATV Carrier;
- 1 Mountain Rescue 4x4 **or** SAR 4x4;
- 1 HART Base and 1 Mountain Rescue Station precondition;
- 1 patient generated at mission end;
- 75% transport probability and 10% critical-care probability.

The ATV Carrier requires the verified five-day Tactical Command Course. It should be commissioned with HART staffing rather than counted as generic Mountain Rescue capacity.

### Belay Failure Whilst Abseiling — helicopter overlay

Verified overlay pressure:

- 1 Coastguard Rescue Helicopter;
- 2 Mountain Rescue 4x4s and/or SAR 4x4s;
- 1 helicopter hangar and 2 Mountain Rescue Stations;
- up to 2 patients generated at mission end;
- 80% transport probability and 50% critical-care probability;
- Ravine or Cliff POI.

The helicopter, off-road vehicles and medical chain are independent requirements.

### Amateur Explorers Trapped in Abandoned Mineshaft

This verified major cross-service incident adds:

- multiple Mountain Rescue 4x4 / SAR 4x4 alternatives;
- Control Van and Search Dog support;
- PRV, SRV and Welfare Vehicle HART requirements;
- Cave Rescue Specialists and Search Advisor roles;
- Fire, Police, Ambulance and technical-rescue dependencies;
- patients generated at mission end.

Use the [Ambulance and HART guide](ambulance.md) and Mission Lookup to review the complete chain.

## Personnel-state planning

Verified roles across Mountain Rescue mission families include:

- Operational Team Leader;
- Search Advisor;
- Cave Rescue Specialist;
- Fire Officer;
- Ambulance Officer;
- Police Sergeant.

Mission records may publish personnel as:

- available before generation;
- required at the incident;
- probabilistic;
- ranged or average-minimum.

Do not flatten these into one exact staffing number. Vehicle crew and mission personnel are also separate contracts.

### Specialist cohorts

Recommended sequence:

1. **Commissioning cohort** — enough qualified personnel for the first complete response chain.
2. **Replacement cohort** — restores capability while the first team is committed.
3. **Regional cohort** — supports another geographic zone without borrowing the same staff.
4. **Expansion cohort** — trained against a confirmed vehicle or station plan.

## Six commissioning gates

| Gate | Question | Recommended pass condition |
|---|---|---|
| Off-road access | Can the largest current alternative-group quantity dispatch? | Enough qualifying 4x4s remain plus protected regional cover |
| Command/search | Are Control Van and Search Dog requirements supported? | No single command or dog unit controls the whole network |
| Personnel | Are the relevant required and available roles present? | Mission personnel and vehicle crews are not conflated |
| Overlay | Are HART or helicopter additions independently ready? | Every overlay precondition and resource can operate |
| Geography | Can units reach the custom spawn area and patient access point? | Route-based coverage is practical |
| Recovery | Can the remote region accept another call afterwards? | Vehicles, personnel and medical support return to useful positions |

## Recommended fleet templates

These are strategy templates, not official requirements.

### Foundation mountain network

| Capability | Recommended position |
|---|---|
| Qualifying 4x4s | 3–5 across the first remote response area |
| Protected reserve | At least 1 useful off-road route after a normal dispatch |
| Control | Alliance-backed initially, then 1 local Control Van when search demand repeats |
| Search dogs | 1 local route when repeated delays appear |
| HART / helicopter | Alliance-supported until the complete overlay chain can be commissioned |
| Personnel | Commissioning cohort for every active specialist role |

### Developing network

| Capability | Recommended position |
|---|---|
| Qualifying 4x4s | 6–10 across two or more remote clusters |
| Protected reserve | At least 2 useful off-road routes across the network |
| Control and search dogs | One of each per main travel-time zone where demand justifies it |
| HART | One complete ATV/PRV/SRV support chain with replacement personnel |
| Air rescue | One regional route or reliable alliance support |
| Cave/search personnel | Required and replacement cohorts aligned with mission geography |

### Established network

| Capability | Recommended position |
|---|---|
| Qualifying 4x4s | Sized from measured concurrent remote incidents and extraction duration |
| Control / dogs | Independently dispatchable resources by region |
| HART / air rescue | Regional specialist groups without shared personnel failure points |
| Technical rescue | Rescue Support and Fire capability distributed by route coverage |
| Personnel | Commissioning, replacement and expansion cohorts documented by role and zone |
| Medical reserve | Patient access, transport and critical-care support tested with remote travel time |

## Geographic doctrine

### Compact upland region

- Distribute 4x4s across access routes rather than one visual centre.
- Keep command and dog support within practical travel time.
- Use alliance air or HART support for rare overlays while local frontline resilience is built.
- Protect one off-road response route for a second incident.

### Multiple mountain regions

- Build independently dispatchable clusters.
- Duplicate Control Van and Search Dog capability by region before stacking vehicles at one base.
- Position HART and helicopter support by cross-region travel advantage.
- Track personnel assignment so one cohort is not counted in several regions.

### Cave and remote technical-rescue network

- Align Cave Rescue Specialists with command, dogs, Fire and HART support.
- Include Welfare and prolonged-incident logistics.
- Preserve patient transport and critical-care reserve.
- Test long return times before declaring readiness restored.

## Transparent concurrency example

**Overdue Hikers** plus the **Belay Failure helicopter overlay** creates a calculated commitment of:

- 4 qualifying Mountain Rescue/SAR 4x4 slots;
- 1 Control Van;
- 1 Search Dog Unit;
- 1 Coastguard Rescue Helicopter;
- up to 5 patients generated at mission end.

This is a transparent sum of two verified mission records, not an official combined mission. Crew, personnel, transport, critical care, travel and cross-service requirements remain additional constraints.

## Recovery-to-readiness

After a remote incident:

1. identify 4x4s, command, dogs, aircraft and specialist teams still committed;
2. restore one local off-road response route first;
3. return command and search resources to useful geography;
4. confirm HART, helicopter and technical-rescue personnel are genuinely available;
5. review patients, transports and cross-service calls still active;
6. rerun the selected concurrency scenario;
7. correct recurring geographic, command or personnel bottlenecks before further expansion.

## Common failures

| Failure | Operational symptom | Correction |
|---|---|---|
| Requiring both 4x4 types | The plan doubles an official alternative group | Apply the quantity to the group as a whole |
| Counting only off-road vehicles | Missions remain open for command, dogs or specialists | Audit the complete chain |
| Treating overlays as universal | Every base mission receives unsupported HART or helicopter demand | Preserve distinct variant records |
| Converting probability to guarantee | Optional Aerial or personnel pressure is over-dispatched | Preserve the published probability |
| Counting crew as specialist personnel | Vehicles exist but role requirements remain open | Audit personnel states separately |
| Centralising command and dogs | One incident removes regional search capability | Duplicate by travel-time zone |
| Ignoring remote extraction time | The mission clears but medical and 4x4 reserve remains absent | Include recovery and return time |
| Expanding unpublished economics | Missing price or capacity becomes false data | Leave unknown fields unknown |

## Operational readiness checklist

- [ ] Mountain Rescue/SAR 4x4 alternative quantities are interpreted correctly;
- [ ] protected off-road reserve survives a normal dispatch;
- [ ] Control Van and Search Dog capability is available where required;
- [ ] probabilistic and overlay requirements remain separate;
- [ ] ATV Carrier crews have the verified Tactical Command training;
- [ ] required/available/probabilistic personnel states are preserved;
- [ ] Cave Rescue and Search Advisor dependencies are staffed;
- [ ] patient generation, transport and critical care are included;
- [ ] custom spawn and real route geography has been tested;
- [ ] two remote incidents have been tested together;
- [ ] alliance support is contingency;
- [ ] unpublished values remain unknown rather than zero.

## Continue Stage 37E

Mountain Rescue progression operates alongside the [Search and Rescue HQ guide](search-and-rescue.md). The two services share off-road, command, search and aerial dependencies while retaining separate infrastructure and mission-generation semantics.
