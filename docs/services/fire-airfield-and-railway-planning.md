# Fire Airfield and Railway Response Planning

Airfield and railway expansion creates some of the most demanding Fire and Rescue response chains in MissionChief UK. Both domains combine specialist fire resources with command, access, trained personnel and other emergency services. A station or extension should therefore be activated only when the complete operational chain can respond without consuming the account's only frontline reserve.

!!! info "Evidence boundary"
    Verified values below are reproduced from the canonical UK mission, resource, infrastructure and training records. Fleet depth, placement patterns, reserve targets and activation sequences are strategic recommendations. Unpublished prices, build times, capacity, parent-building compatibility and unlock details remain unknown.

**Current evidence baseline:** 27 July 2026.

## Shared command doctrine

Use the same six questions for both domains:

1. **What generates the mission?** Identify every countable building or extension precondition.
2. **What must physically attend?** Separate guaranteed resources from alternatives, probabilities and conditional rows.
3. **Who must crew and command it?** Complete specialist training before the capability becomes operational.
4. **How does it reach the incident?** Place airport and rail-access resources against real route geography.
5. **What other services are part of the chain?** Ambulance, HART, Police, Railway Police and mass-casualty capacity may be operational dependencies.
6. **What remains after dispatch?** Preserve frontline, command and specialist reserve for another incident.

!!! warning "Do not double-count alternatives"
    A vehicle may appear in more than one independent alternative group. Do not assume one dispatched vehicle satisfies several groups simultaneously unless current dispatch behaviour has been reproduced and documented.

[Open Mission Lookup](../tools/mission-lookup.md) · [Open Concurrent Fleet Planner](../tools/fleet-planner.md) · [Compare Resources](../tools/resource-comparison.md)

## Verified mission-generation controls

| Control | Verified role | Current evidence boundary |
|---|---|---|
| **Aviation firefighting Extension** | Counts towards airfield-firefighting mission generation | Parent buildings, price, construction time and capacity are not published in the canonical record |
| **Airfield Operations Extension** | Counts towards generation of Aircraft Accident Codes C, D and F | Parent buildings, price, construction time and capacity are not published |
| **Railway fire response** | Countable precondition for railway-fire mission generation | Cost, capacity, construction time and precise building-interface classification remain unpublished |
| **Railway Police** | Countable precondition on railway mission families | Treat Police infrastructure and personnel as a separate operational dependency |

An activation count proves only that a mission may generate. It does not prove that the correct vehicles, trained personnel, access capability or cross-service support are ready.

---

# Airfield fire-response planning

## Airfield readiness chain

```text
Airport mission-generation extensions
                ↓
ARFF-trained firefighting fleet
                ↓
Airfield command and operations vehicles
                ↓
Foam + water + HazMat + access capability
                ↓
Police + Ambulance + HART + mass-casualty support
                ↓
Geographic reserve for another incident
```

## Verified airfield capability contracts

| Resource | Verified function | Verified training or mission relationship |
|---|---|---|
| **RIV** | Airfield firefighting | Requires **ARFF-Training**, three days at the Fire Academy |
| **Major Foam Tender** | Airfield firefighting and foam delivery | Requires **ARFF-Training**, three days at the Fire Academy; appears as dedicated and alternative capacity |
| **Airfield Firefighting Command Vehicle** | Airfield firefighting command | Requires **ARFF-Training**, three days at the Fire Academy; may appear in several independent command/control groups |
| **Airfield Operations Vehicle** | Dedicated airfield-operations response | Verified requirement on Aircraft Accident Codes C, D and F |
| **Water Carrier** | Bulk water supply | Verified as a guaranteed requirement on current UK airfield incident pages |
| **Rescue Stairs** | Aircraft access | Appears as an alternative to an Aerial Appliance Truck on Aircraft Accident Code F |

The canonical records do not currently publish purchase prices or staffing limits for most airfield vehicles. Do not treat those omissions as free, unrestricted or zero-crew capability.

## Aircraft Accident Code C pressure

Aircraft Accident Code C is already a major multi-service incident.

### Verified guaranteed Fire and airfield resources

- 1 Airfield Firefighting Command Vehicle;
- 2 Airfield Operations Vehicles;
- 1 Fire Engine;
- 1 Major Foam Tender;
- 1 Water Carrier;
- 2 Rescue Support Vehicles;
- 1 Welfare Vehicle.

### Independent alternative groups

- 7 Fire Engines **or** Major Foam Tenders;
- 6 Fire Officers **or** Airfield Firefighting Command Vehicles;
- 1 HazMat Unit **or** CBRN Vehicle;
- 1 ICCU **or** Ambulance Control Unit **or** Airfield Firefighting Command Vehicle.

The mission also includes Police, ambulance, HART and mass-casualty pressure. It verifies **75–175 patients**, with Airfield Operations Supervisor and other command personnel requirements.

### Verified generation baseline

```text
2 Aviation firefighting Extensions
1 Airfield Operations Extension
11 Fire Stations
11 Rescue Stations
3 HART Bases
1 Mass Casualty Extension
10 Police Stations
```

These values are mission preconditions, not a recommended expansion order.

## Aircraft Accident Code F pressure

Code F demonstrates why airport capability cannot be planned around one specialist vehicle.

### Verified guaranteed Fire and airfield resources

- 1 Airfield Firefighting Command Vehicle;
- 4 Airfield Operations Vehicles;
- 1 Fire Engine;
- 5 Major Foam Tenders;
- 1 Water Carrier;
- 2 Rescue Support Vehicles;
- 2 Welfare Vehicles.

### Independent alternative groups

- 10 Fire Engines **or** Major Foam Tenders;
- 6 Fire Officers **or** Airfield Firefighting Command Vehicles;
- 2 HazMat Units **or** CBRN Vehicles;
- 1 Aerial Appliance Truck **or** Rescue Stairs;
- 1 ICCU **or** Ambulance Control Unit **or** Airfield Firefighting Command Vehicle.

Code F verifies **150–250 patients** and two required Airfield Operations Supervisors.

### Verified generation baseline

```text
3 Aviation firefighting Extensions
2 Airfield Operations Extensions
15 Fire Stations
15 Rescue Stations
3 HART Bases
1 Mass Casualty Extension
10 Police Stations
```

The dedicated Airfield Firefighting Command Vehicle and the command/control alternatives are stored as separate rows. Build enough independently dispatchable resources to avoid relying on one command vehicle to satisfy several groups at once.

## Airfield activation gates

### Gate 1 — ARFF personnel complete

Every RIV, Major Foam Tender and Airfield Firefighting Command Vehicle included in the operational plan must have a usable ARFF-trained crew. The verified course lead time is three days at the Fire Academy.

### Gate 2 — dedicated airfield fleet complete

Do not count ordinary Fire appliances as replacements for dedicated airfield requirements unless the mission explicitly presents an alternative group.

### Gate 3 — water, foam and HazMat depth complete

Airport incidents can apply guaranteed Major Foam Tender and Water Carrier requirements alongside larger alternative firefighting groups. HazMat or CBRN demand is separate again.

### Gate 4 — command groups independently satisfiable

Count:

- the guaranteed Airfield Firefighting Command Vehicle;
- the Fire Officer or airfield-command alternative group;
- the incident-control alternative group;

as separate planning pressures until dispatch evidence proves safe overlap.

### Gate 5 — cross-service response complete

Confirm Police, HART, ambulance command, mass-casualty equipment and patient transport capacity before activating additional airport generators.

### Gate 6 — second-incident reserve complete

A Code C or Code F response can remove large numbers of specialists and ordinary Fire resources. Use the Fleet Planner to test an airport incident alongside a routine structure fire or another airport incident.

## Recommended airport base patterns

These are strategic patterns, not game requirements.

=== "Single airport cluster"

    Suitable when one airport area creates the relevant missions.

    - co-locate the core ARFF fleet near the airport POIs;
    - retain ordinary Fire reserve outside the specialist base;
    - keep Water Carrier, HazMat and command travel times within the same operating zone;
    - use alliance support as contingency rather than the only command or mass-casualty plan.

=== "Primary and relief base"

    Suitable when one large airport creates high specialist pressure.

    - keep the dedicated airfield fleet at the primary base;
    - place relief command, water, HazMat and frontline capacity at a nearby independent station;
    - maintain a replacement ARFF-trained cohort;
    - avoid storing every specialist and every trained crew at one failure point.

=== "Multiple airport zones"

    Suitable when airport POIs or extensions are geographically separated.

    - assign each airport a minimum complete response chain;
    - centralise only low-frequency resources that can still meet route-time expectations;
    - duplicate command and foam capacity when travel time or concurrency proves the need;
    - do not assume a specialist committed at one airport remains available to another.

## Airport readiness checklist

- [ ] mission-generating extension counts are understood;
- [ ] ARFF training is complete before vehicles are counted as operational;
- [ ] dedicated airfield requirements are not replaced by ordinary appliances without an explicit alternative;
- [ ] guaranteed and alternative firefighting groups can be satisfied separately;
- [ ] command and incident-control groups are not double-counted;
- [ ] Water Carrier, foam and HazMat capability are available together;
- [ ] Police, HART, ambulance and mass-casualty dependencies are ready;
- [ ] airport POIs have realistic road-response coverage;
- [ ] a major airport dispatch leaves usable Fire and command reserve;
- [ ] unpublished costs, staffing and building compatibility remain unknown.

---

# Railway fire-response planning

## Railway readiness chain

```text
Railway fire response + Railway Police generation
                         ↓
Road Rail access + frontline Fire response
                         ↓
Breathing apparatus + foam + water + command
                         ↓
Railway Police + EIU + railway personnel
                         ↓
Ambulance + HART + mass-casualty capability
                         ↓
Corridor and tunnel reserve
```

## Verified railway capability contracts

| Resource | Verified function | Planning consequence |
|---|---|---|
| **Road Rail Unit** | Road and railway access; railway incident response | Treat access as a distinct capability, not another ordinary Fire appliance |
| **Breathing Apparatus Support Unit** | Breathing-apparatus support | Appears as guaranteed or probabilistic depending on the incident |
| **Foam Unit** | Foam response | Verified deployable requirement on railway and major-incident pages |
| **Water Carrier** | Bulk water supply | Can be required alongside Foam Units and ordinary Fire Engines |
| **EIU** | Railway investigation and support | Keep the abbreviation unexpanded until a primary source verifies its full name |
| **Fire Officer** | Incident command | Major railway incidents can require several officers simultaneously |

## Goods Train Fire pressure

The fully enhanced Goods Train Fire railway variant verifies:

- 4 Fire Engines;
- 3 Fire Officers;
- 1 Breathing Apparatus Support Unit;
- 1 EIU;
- 1 Foam Unit;
- 1 Road Rail Unit;
- 1 Water Carrier;
- 1 ICCU **or** Ambulance Control Unit.

Its verified generation baseline includes:

```text
13 Fire Stations
1 Foam Extension
1 Railway fire response
1 Railway Police
```

It also requires Railway Police personnel. This is a useful commissioning test because it exercises the core railway-fire chain without the full tunnel and mass-casualty scale.

## Passenger Train Fire in Tunnel pressure

Passenger Train Fire in Tunnel verifies a substantially larger response:

### Guaranteed Fire and railway resources

- 6 Fire Engines;
- 6 Fire Officers;
- 2 Breathing Apparatus Support Units;
- 2 Foam Units;
- 2 Road Rail Units;
- 1 Water Carrier;
- 1 EIU;
- 2 Rescue Support Vehicles;
- 1 Welfare Vehicle.

### Independent alternative groups

- 1 ICCU **or** Ambulance Control Unit **or** Airfield Firefighting Command Vehicle;
- 1 ICCU **or** Ambulance Control Unit;
- 1 HazMat Unit **or** CBRN Vehicle.

The mission verifies **25–150 patients**, Mobile Operations Manager and Railway Police personnel requirements, Police resources, HART, mass-casualty equipment and ambulance capacity.

### Verified generation baseline

```text
20 Fire Stations
2 Foam Extensions
2 Railway fire responses
1 Railway Police
18 Rescue Stations
2 HART Bases
1 Mass Casualty Extension
10 Police Stations
```

A railway network that can complete smaller surface incidents may still fail this mission through access, breathing-apparatus, foam, command, patient or cross-service concurrency.

## Railway activation gates

### Gate 1 — corridor access mapped

Place Road Rail Units against the actual railway POIs and corridors that can generate incidents. A central unit may be numerically available but operationally weak when route distance is high.

### Gate 2 — surface incident chain complete

Commission the network against a representative surface railway fire before increasing generator counts:

- frontline Fire Engines;
- Fire Officers;
- Road Rail Unit;
- Breathing Apparatus Support Unit;
- Foam Unit;
- Water Carrier;
- Railway Police and EIU support.

### Gate 3 — tunnel escalation complete

Tunnel incidents require greater duplication and mass-casualty depth. Do not activate the second Railway fire response merely because the first surface-response chain works.

### Gate 4 — personnel available and required states covered

Railway missions distinguish personnel who must be available before generation from personnel required at the incident. Maintain both the generation pool and the dispatchable incident crew.

### Gate 5 — cross-service command complete

Ambulance command, HART, Police, Railway Police and mass-casualty resources must be able to mobilise without borrowing the same unit into two independent alternative groups.

### Gate 6 — corridor reserve complete

Test two incidents in the same corridor and incidents at opposite ends of the network. Duplicate the resource that actually becomes the bottleneck: access, foam, breathing apparatus, command, water or travel time.

## Recommended railway placement patterns

=== "Single corridor"

    - place the first complete railway-fire chain near the highest-density rail POIs;
    - keep a Road Rail Unit, Foam Unit and Breathing Apparatus Support Unit within the same response cluster;
    - preserve ordinary Fire reserve for non-rail incidents;
    - use a nearby second station for command and water relief.

=== "Hub-and-spoke network"

    - place specialist access and support at major rail hubs;
    - distribute frontline and command capacity along the corridor;
    - verify that spokes remain covered when the hub fleet is committed;
    - duplicate Road Rail access when one unit cannot meet opposite-direction demand.

=== "Multiple corridors or tunnels"

    - build independently dispatchable chains by geography;
    - keep at least the verified tunnel-response depth available across the relevant zones before activating maximum generation;
    - distribute Railway Police and railway personnel with the Fire resources they support;
    - avoid making one central mass-casualty or ambulance-command unit the hidden network bottleneck.

## Common airfield and railway failures

| Failure | Operational symptom | Correction |
|---|---|---|
| Activating generation before specialist readiness | Large incidents appear while dedicated resources or training are incomplete | Delay further activation and finish the complete chain |
| Counting one command vehicle several times | The fleet plan passes on paper but dispatch leaves an unsatisfied group | Model every independent alternative row separately |
| Centralising every specialist | One incident removes capability from the entire network | Duplicate by airport or rail corridor |
| Ignoring access resources | Ordinary Fire capacity arrives but rail-specific requirements remain open | Treat Road Rail and aircraft-access capability separately |
| Planning Fire in isolation | Police, HART, ambulance or mass-casualty deficits delay completion | Audit the whole cross-service response |
| Training only one ARFF crew | A committed vehicle removes all qualified airport capacity | Train a replacement cohort |
| Treating extension count as capability | Missions generate correctly but response resources are missing | Link every generator to a staffed fleet and reserve plan |
| Guessing unpublished values | Missing costs, capacity or building compatibility become false facts | Preserve the field as unknown |

## Joint commissioning sequence

1. Select one representative mission family in Mission Lookup.
2. Record every guaranteed, alternative, conditional and personnel row.
3. Build the dedicated specialist and cross-service response chain.
4. Complete ARFF or other verified training before activation.
5. Place resources against airport POIs or railway corridors.
6. Test the mission with a simultaneous routine Fire incident.
7. Activate one new mission generator.
8. Observe dispatch failures, travel times and resource reuse.
9. Correct the measured bottleneck before activating another generator.

## Stage 37A continuation

Batch 4 consolidates airfield and railway Fire planning without replacing the detailed [Airfield Operations](airfield-operations.md) and [Railway Response](railway-response.md) evidence pages. Return to [Fire & Rescue progression](fire-and-rescue.md), [specialist extension and container logistics](fire-and-rescue-specialists.md), or [training and personnel planning](fire-training-and-personnel.md).

Later Stage 37A batches will cover wildfire and water rescue, major-incident resilience, and mission-family pressure analysis derived from the complete canonical catalogue.
