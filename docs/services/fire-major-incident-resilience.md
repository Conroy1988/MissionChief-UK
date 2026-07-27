# Fire Major-Incident Resilience

Major-incident readiness is not proved by owning one large fleet. It is proved when the account can commit a high-load response, preserve essential cover elsewhere, sustain command and welfare support, and return the network to a dispatchable state after the incident clears.

!!! info "Evidence boundary"
    Exact requirements, patient ranges, personnel fields and training relationships below are reproduced from the current canonical UK records. Reserve floors, readiness states, mutual-support layers and recovery procedures are operational recommendations. They are not hidden MissionChief rules or guaranteed unlock thresholds.

**Current evidence baseline:** 28 July 2026.

## Major incident as a capacity state

A mission becomes operationally major when its combined demand creates one or more of these conditions:

- a large proportion of frontline Fire Engines is committed;
- several command or incident-control requirements must be satisfied independently;
- rare specialists become single points of failure;
- another service controls completion despite the Fire fleet being present;
- patient scale creates sustained ambulance, critical-care and hospital pressure;
- travel and return times prevent rapid restoration of local cover;
- a second serious mission cannot be accepted without alliance support.

The mission title does not need to contain **Major Incident** for these conditions to occur.

## Five resilience layers

| Layer | Planning question | Failure signal |
|---|---|---|
| **Incident response** | Can every guaranteed, alternative, personnel and patient field be supported? | A requirement remains open despite a large attendance |
| **Protected reserve** | What staffed capability remains outside the incident? | Nearby routine missions cannot be dispatched |
| **Command and support** | Are control, mass-casualty and welfare resources independently available? | Frontline resources arrive but command or support stalls completion |
| **Regional continuity** | Can another response zone operate without borrowing the same units? | One incident empties several neighbouring areas |
| **Recovery** | How quickly can the fleet, crews and specialist chains become available again? | The incident clears but the network remains functionally depleted |

[Open Mission Lookup](../tools/mission-lookup.md) · [Open Concurrent Fleet Planner](../tools/fleet-planner.md) · [Compare Resources](../tools/resource-comparison.md)

---

# Representative major-incident pressure

These missions demonstrate different forms of resilience pressure. They are examples, not a complete ranking of the catalogue.

## Building collapse

The verified **Building collapse** major variant requires:

- 4 Fire Engines;
- 4 Fire Officers;
- 3 Rescue Support Vehicles;
- 1 Police Car;
- two independent incident-control alternative groups;
- 8–20 patients;
- 100% critical-care probability;
- 1 Operational Team Leader.

This incident is not the largest frontline draw, but it can expose command duplication, technical-rescue concentration and critical-care capacity early in an account's development.

## Multiple vehicle RTC — Major Incident

The verified response includes:

- 6 Fire Engines;
- 8 Fire Officers;
- 2 Rescue Support Vehicles;
- 6 Police Cars;
- 1 Mass Casualty Equipment resource;
- two independent incident-control alternative groups;
- 30–150 patients with Traumatology specialisation.

The principal risk is not only appliance volume. Eight Fire Officers, two command groups and mass-casualty support may consume resources that appear plentiful when viewed service by service.

## Hotel fire — major

The verified major hotel-fire response includes:

- 14 Fire Engines;
- 8 Fire Officers;
- 2 Aerial Appliance Trucks;
- 1 Breathing Apparatus Support Unit;
- 2 Rescue Support Vehicles;
- 1 Water Carrier;
- 6 Police Cars;
- 1 Mass Casualty Equipment resource;
- two independent incident-control alternative groups;
- up to 50 patients with 100% critical-care probability;
- 1 Operational Team Leader.

The record also publishes repeated follow-up mission relationships. Recovery planning should therefore account for continuing demand after the initial attendance rather than assuming every committed resource returns immediately.

## Bridge collapse — major

The verified response includes:

- 18 Fire Engines;
- 5 Fire Officers;
- 5 Aerial Appliance Trucks;
- 6 Rescue Support Vehicles;
- 12 Police Cars;
- 2 PRVs and 2 SRVs;
- 1 Welfare Vehicle;
- 1 Mass Casualty Equipment resource;
- two independent incident-control alternative groups;
- 20–50 patients;
- 95% transport probability and 80% critical-care probability.

This mission creates simultaneous pressure on frontline, aerial, technical-rescue, HART, Police, welfare and medical transport capacity.

## Passenger Train Caught in Landslide — Major Incident

This railway/SAR major incident verifies a much wider dependency chain:

- 10 Fire Engines and 8 Fire Officers;
- 4 Rescue Support Vehicles;
- 2 Road Rail Units;
- 1 Breathing Apparatus Support Unit and 1 Foam Unit;
- 1 Water Carrier;
- 2 EIU and 2 Dog Support Units;
- 4 PRVs and 4 SRVs;
- 2 Welfare Vehicles;
- 1 Control Van and 1 Search Dog Unit;
- 10 Police Cars;
- 1 Mass Casualty Equipment resource;
- three incident-control slots across two independent alternative groups;
- HazMat or CBRN capability;
- Police helicopter or Drone capability;
- five Operational Support Van, Operational Support Trailer or Personal SAR Vehicle alternatives;
- 50–200 patients.

Verified personnel requirements include Mobile Operations Managers, Operational Team Leaders, Police command roles, Railway Police Officers and a Search Advisor. This is a clear example of a Fire-generated mission whose completion depends on a regional cross-service system.

---

# Calculated concurrency stress tests

The totals below are transparent calculations from verified guaranteed requirements. They are not official combined missions.

## Stress test A — Bridge collapse plus major RTC

### Calculated guaranteed commitment

| Capability | Combined demand |
|---|---:|
| Fire Engines | **24** |
| Fire Officers | **13** |
| Aerial Appliance Trucks | **5** |
| Rescue Support Vehicles | **8** |
| Police Cars | **18** |
| Mass Casualty Equipment | **2** |
| PRVs | **2** |
| SRVs | **2** |
| Welfare Vehicles | **1** |
| Maximum patients | **200** |
| Independent incident-control slots | **4** |

The four control slots must be modelled separately. A single ICCU or Ambulance Control Unit should not be counted four times merely because its type appears in each alternative group.

## Stress test B — Major hotel fire plus HART large forest fire

### Calculated guaranteed commitment

| Capability | Combined demand |
|---|---:|
| Fire Engines | **24** |
| Fire Officers | **12** |
| Aerial Appliance Trucks | **2** |
| Breathing Apparatus Support Units | **1** |
| Rescue Support Vehicles | **2** |
| Water Carriers | **2** |
| Police Cars | **6** |
| Mass Casualty Equipment | **1** |
| Welfare Vehicles | **1** |
| Maximum patients | **50** |
| Independent incident-control slots | **3** |

This pairing demonstrates how an urban major fire and a rural incident can consume the same command, water and frontline network even though their geography and specialist profiles differ.

!!! warning "Guaranteed totals are not the whole response"
    Patient treatment, transport, critical care, personnel availability, travel time and any probabilistic or conditional fields remain additional pressures. The tables above do not convert patient counts into an invented ambulance total.

---

# Reserve-erosion model

Use staffed and dispatchable resources rather than purchased inventory.

```text
Available now
− committed guaranteed resources
− resources selected for alternative groups
− unavailable, returning or repositioning resources
− protected local response floor
= deployable reserve
```

## What counts as available now

Count a resource only when:

- the vehicle, trailer, container or vessel exists;
- the required crew and qualification are present;
- the towing or carrier path is available;
- the resource is not already committed or returning;
- its travel time makes it operationally relevant;
- the same crew is not assigned to another counted vehicle.

## Protected reserve

A protected reserve is capability deliberately withheld from the major incident so another area remains functional. It may include:

- frontline Fire Engines;
- one local command route;
- one rescue-support route;
- water or aerial capability where geography requires it;
- specialist resources needed by active extension families;
- cross-service command and medical capacity.

The size of the reserve is a recommendation based on account geography and mission history, not a published game minimum.

## Recommended readiness states

These labels are operational shorthand, not MissionChief statuses.

| State | Recommended meaning |
|---|---|
| **Ready** | The reference major incident can be dispatched while protected local and specialist reserve remains available |
| **Degraded** | The current incident can be completed, but one critical capability or response zone has no independent reserve |
| **Recovery** | The incident is clearing, but vehicles, crews, trailers, containers or command resources have not returned to useful positions |
| **Unavailable** | Another reference major incident would require alliance assistance or leave essential missions unsupported |

Do not describe the network as ready merely because the mission has turned green or completed.

---

# Command and support bottlenecks

## Independent command slots

Many major incidents publish more than one alternative group using ICCU, Ambulance Control Unit or Airfield Firefighting Command Vehicle. Each displayed group is independent.

The verified training contracts include:

| Resource | Verified training |
|---|---|
| **ICCU** | Mobile command — **5 days**, Fire Academy |
| **Ambulance Control Unit** | Tactical Command Course — **5 days**, Rescue (EMS) Academy |
| **Mass Casualty Equipment** | SORT Training — **3 days**, Rescue (EMS) Academy |

Command resilience therefore depends on vehicles, trained crews, academy lead time and geographic distribution.

### Recommended command rule

Maintain enough independently crewed control resources for the number of simultaneous alternative-group slots in the chosen stress scenario, plus a local fallback where the account's geography requires it.

This is a resilience recommendation, not an official minimum.

## Welfare support

Welfare Vehicles are verified HART Base resources. Some high-load incidents require one or more directly.

Do not treat welfare as decorative support. When it is a guaranteed row, the mission requires the resource regardless of how many suppression or rescue vehicles are present.

A single central Welfare Vehicle may become a regional bottleneck when:

- two long-duration incidents overlap;
- travel time between regions is high;
- a railway, flood or wildfire mission is already using the resource;
- HART demand commits the same base's other vehicles.

## Mass-casualty support

Mass Casualty Equipment has verified SORT training. A single item can become a hard blocker when two mass-casualty missions overlap.

Plan the equipment separately from:

- ambulance quantity;
- Ambulance Control Units;
- HART PRV/SRV capacity;
- hospital capacity;
- critical-care resources.

---

# Regional support architecture

Use layered support rather than one central reserve.

## Layer 1 — local first response

The local cluster supplies the initial frontline, command and common specialist response without emptying itself completely.

## Layer 2 — neighbouring reinforcement

Neighbouring clusters reinforce the incident while retaining a documented minimum for their own routine demand.

## Layer 3 — strategic regional reserve

Rare aerial, technical-rescue, command, welfare, mass-casualty, container and cross-service resources are held or distributed so one incident does not consume every copy.

## Layer 4 — alliance mutual support

Alliance support is a contingency layer. It should not be treated as guaranteed capacity unless the alliance has an explicit and reliable operating arrangement.

### Mutual-support risks

- the assisting member may be handling their own incident;
- response travel may be longer than local duplication;
- several members may rely on the same rare alliance resource;
- borrowed resources may leave the donor area exposed;
- command, personnel or towing dependencies may still remain local.

Use alliance help to absorb exceptional peaks, not to conceal a permanent local capability gap.

---

# Cross-service single points of failure

Audit the entire response chain, not only Fire resources.

## Ambulance and HART

Check:

- command-unit alternatives;
- Mass Casualty Equipment;
- PRV and SRV depth;
- Welfare Vehicles;
- Operational Team Leaders;
- patient transport and critical-care pressure.

## Police

Check:

- guaranteed Police Car volume;
- Railway Police infrastructure and officers where applicable;
- Police Sergeant and Inspector fields;
- EIU, Dog Support and air-support dependencies;
- whether traffic or scene-control demand affects other active incidents.

## Search and Rescue

Check:

- Search Advisor availability;
- Search Dog Units;
- Drone or Police Helicopter alternatives;
- Operational Support or Personal SAR capacity;
- geographic travel to rail, rural and remote incidents.

## Fire specialists

Check:

- aerial appliances;
- Rescue Support Vehicles;
- Breathing Apparatus Support Units;
- foam and water resources;
- Road Rail Units;
- HazMat or CBRN alternatives;
- containers, carriers and trained crews.

A major incident is operationally incomplete when any one of these required chains is absent.

---

# Recovery-to-readiness doctrine

Incident completion is the beginning of recovery, not proof of restored readiness.

## Recovery sequence

1. **Record the depleted capabilities.** Identify every vehicle, crew, trailer, container, specialist and command unit still committed or travelling.
2. **Restore local cover first.** Reposition useful frontline and command resources into exposed response zones.
3. **Release shared dependencies.** Confirm towing vehicles, Container Vehicles and specialist crews are genuinely available again.
4. **Rebuild cross-service reserve.** Check Police, HART, Ambulance, Railway and SAR capacity rather than looking only at Fire stations.
5. **Reassess active missions.** A cleared major incident may leave follow-ups, transports or other calls still consuming resources.
6. **Return specialists to operational geography.** A vehicle back in the fleet but far from its response area is not fully restored.
7. **Re-run the reference stress scenario.** Do not declare Ready until the network can again support the chosen test with protected reserve.
8. **Correct recurring deficits.** Duplicate the measured bottleneck before activating more mission generators or expanding into another specialist family.

## Recovery priorities

Recommended order:

1. life-critical medical and patient transport;
2. local frontline Fire and command cover;
3. hard-blocking specialists;
4. towing and carrier chains;
5. welfare and sustained-incident support;
6. strategic reserve positioning.

The exact order may change with active incidents and geography.

---

# Common major-incident failures

| Failure | Operational symptom | Correction |
|---|---|---|
| Counting purchased rather than staffed resources | The inventory looks sufficient but several vehicles cannot dispatch together | Audit crews, qualifications and assignment ownership |
| Reusing one command unit across alternative groups | Multiple groups remain unsatisfied at the incident | Allocate one qualifying resource per independent slot |
| Sending the protected reserve | The major incident completes while routine local missions stall | Define and preserve a local response floor |
| Centralising all rare specialists | A single incident removes capability from the entire region | Distribute by travel-time zone and concurrency |
| Planning Fire without other services | Suppression resources arrive but Police, HART, SAR or medical rows remain open | Model the full mission contract |
| Treating mission completion as restored readiness | Follow-ups and returning units leave the network depleted | Run the recovery-to-readiness sequence |
| Treating alliance help as guaranteed | A second incident fails when the expected support is unavailable | Maintain local core capacity and use alliance help as contingency |
| Ignoring patient pressure | Vehicle requirements are met but treatment and transport dominate the incident | Plan medical command, transport and critical-care capacity separately |
| Expanding while Degraded | New missions generate before reserve is restored | Correct the bottleneck before further activation |

# Major-incident readiness checklist

- [ ] at least one representative major incident has been selected in Mission Lookup;
- [ ] every guaranteed, alternative, patient and personnel field is recorded;
- [ ] each independent command slot has its own qualifying resource;
- [ ] available capacity is based on staffed and positioned resources;
- [ ] a protected local response floor is defined;
- [ ] rare aerial, rescue-support, welfare and mass-casualty resources are not single points of failure;
- [ ] Police, HART, Ambulance, Railway and SAR dependencies are included;
- [ ] two representative incidents have been tested together in Fleet Planner;
- [ ] alliance support is treated as contingency rather than guaranteed reserve;
- [ ] towing, carrier and trained-crew chains are included;
- [ ] recovery and repositioning are complete before the network returns to Ready;
- [ ] further expansion waits until recurring deficits are corrected;
- [ ] unpublished values remain unknown rather than zero.

## Stage 37A continuation

Batch 6 establishes major-incident resilience, regional support and recovery-to-readiness doctrine. Return to [Fire & Rescue progression](fire-and-rescue.md), [training and personnel planning](fire-training-and-personnel.md), [airfield and railway planning](fire-airfield-and-railway-planning.md), or [wildfire, flood and water-rescue planning](fire-wildfire-flood-water-rescue.md).

The final Stage 37A package will publish mission-family pressure analysis derived from the complete canonical catalogue and close the Fire operational-guide programme.