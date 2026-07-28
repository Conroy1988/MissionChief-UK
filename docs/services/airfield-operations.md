# Airfield Operations Operational Progression

Airfield Operations combines aviation firefighting, runway coordination, airfield command, foam, water, hazardous-materials response, aircraft access, mass-casualty support and Police control. Airport readiness is therefore a cross-service operating system rather than a collection of specialist vehicles at one station.

!!! info "Evidence boundary"
    Verified statements reproduce current canonical mission, vehicle, infrastructure, personnel and training records. Fleet sizes, reserve floors, base patterns and activation sequences are recommendations. Extension economics, most vehicle-market prices and staffing, course transferability and airport unlock details remain unknown. Community-reported fields remain explicitly labelled.

**Current evidence baseline:** 28 July 2026.

## Command doctrine

Use this order when expanding:

1. **ARFF-trained suppression first** — RIV, Major Foam Tender and airfield command capability require qualified personnel before they are operational.
2. **Airfield Operations capability second** — dedicated operations vehicles and supervisor personnel are separate from firefighting volume.
3. **Water, foam and HazMat as independent pressure** — one resource class does not automatically replace the others.
4. **Command groups separately** — Airfield Firefighting Command can appear as a dedicated row and in several independent alternative groups.
5. **Mass-casualty and HART before maximum incidents** — patient scale and critical-care probability can exceed the airport fleet problem.
6. **Primary and relief bases before another extension** — airport mission generators should not exceed the cross-service response and regional reserve.

[Open Mission Lookup](../tools/mission-lookup.md) · [Open Concurrent Fleet Planner](../tools/fleet-planner.md) · [Compare Resources](../tools/resource-comparison.md)

## Airport response chain

```text
Aviation Firefighting / Airfield Operations extensions
                         ↓
ARFF-trained RIV, foam and command resources
                         ↓
Airfield Operations vehicles and supervisor personnel
                         ↓
Water, HazMat, aircraft access and Fire support
                         ↓
HART, Ambulance command and Mass Casualty Equipment
                         ↓
Police, traffic and supervision
                         ↓
Airport relief base and regional reserve restored
```

## Verified mission-generation controls

### Aviation firefighting Extension

The canonical extension:

- counts toward aviation-firefighting mission generation;
- is verified on Bird Strike and aircraft-accident mission families;
- leaves parent-building compatibility, price, construction time and capacity unpublished.

### Airfield Operations Extension

The canonical extension:

- counts toward generation of Aircraft Accident Codes C, D and F;
- is separate from the Aviation firefighting Extension;
- leaves parent-building compatibility, price, construction time and capacity unpublished.

!!! warning "Generator count is not response capacity"
    Activating the extension can increase airport mission eligibility. It does not create ARFF crews, operations vehicles, command, foam, water, HazMat, HART, Police or mass-casualty capacity.

## Verified airport resources

| Resource | Verified operational role | Training / evidence boundary |
|---|---|---|
| **RIV** | Airfield firefighting response | **ARFF-Training**, 3 days, Fire Academy; abbreviation remains unexpanded |
| **Major Foam Tender** | Airfield firefighting and foam delivery | **ARFF-Training**, 3 days, Fire Academy; used as dedicated and alternative resource |
| **Airfield Firefighting Command Vehicle** | Airport firefighting command | **ARFF-Training**, 3 days, Fire Academy; may appear as dedicated and alternative command resource |
| **Airfield Operations Vehicle** | Dedicated airfield-operations response | Verified on Aircraft Accident Codes C, D and F; market economics, staffing and training unpublished |
| **Water Carrier** | Bulk-water supply | Verified guaranteed airport requirement; market fields not fully published in the canonical record |
| **Rescue Stairs** | Aircraft access and rescue | Code F accepts this as an alternative to an Aerial Appliance Truck |
| **Mass Casualty Equipment** | Mass-casualty support | **SORT Training**, 3 days, Rescue (EMS) Academy |
| **PRV / SRV** | HART specialist response | **HART Training**, 5 days, Rescue (EMS) Academy |
| **Welfare Vehicle** | Sustained-incident welfare | HART Base resource; no HART course inferred |

[Open Fire airfield and railway planning](fire-airfield-and-railway-planning.md) · [Open Ambulance and HART progression](ambulance.md)

## Airfield Operations Supervisor boundary

The canonical mission data verifies **Airfield Operations Supervisor** as a personnel role.

A separate community-reported vehicle record uses the same display name and reports:

- alias `AOS`;
- 15,000 credits or 15 coins;
- maximum crew 2;
- Airfield Operations Extension requirement;
- supervision and trailer-towing capability.

Do not treat community-reported vehicle fields as verified official economics, and do not conflate the vehicle with the mission personnel role.

## ARFF training and personnel

RIV, Major Foam Tender and Airfield Firefighting Command Vehicle use the verified three-day ARFF-Training course at the Fire Academy.

### Recommended cohort sequence

1. **Commissioning cohort** — enough trained personnel for the first complete ARFF response.
2. **Replacement cohort** — restores the same capability while the first crew is committed.
3. **Relief-base cohort** — supports another airport or geographic response zone.
4. **Expansion cohort** — trained against a confirmed vehicle and extension plan.

A fleet of several ARFF vehicles is not concurrently available when the same trained people are implicitly assigned to all of them.

### Personnel-state semantics

Verified airport roles include:

- Airfield Operations Supervisor;
- Operational Team Leader;
- Ambulance Officer;
- Police Sergeant;
- Police Inspector.

Mission records distinguish personnel:

- available before generation;
- required at the incident.

Keep those fields separate from vehicle crew, ARFF qualifications and community-reported vehicle capacity.

## Progression tier 1 — Bird Strike Code B

Verified guaranteed response:

- 1 Fire Engine;
- 2 PRVs;
- 1 SRV;
- 3 Water Carriers;
- 1 Welfare Vehicle.

Independent alternative groups:

- 4 Fire Engines and/or RIVs;
- 2 RIVs and/or Major Foam Tenders.

Other verified pressure:

- 1 Operational Team Leader;
- 1 Aviation firefighting Extension;
- 2 HART Bases;
- Medium or Large Airport runway POI.

### Planning implication

Code B is already a multi-system incident. The first airport generator should not activate until ARFF alternatives, three Water Carriers, HART and welfare can respond without emptying routine Fire and Ambulance cover.

## Progression tier 2 — Hot Brakes Code D

Verified guaranteed response:

- 1 Airfield Firefighting Command Vehicle;
- 4 Airfield Operations Vehicles;
- 5 Major Foam Tenders;
- 6 Water Carriers;
- 1 Fire Engine;
- 1 Mass Casualty Equipment resource;
- 4 Police Cars;
- 2 PRVs and 2 SRVs;
- 1 Welfare Vehicle.

Independent alternative groups:

- 1 ICCU, Ambulance Control Unit or Airfield Firefighting Command Vehicle;
- 1 Fire Officer or Airfield Firefighting Command Vehicle;
- 2 HazMat Units and/or CBRN Vehicles;
- 7 Fire Engines and/or Major Foam Tenders.

Conditional response:

- 2 Traffic Cars, only when available.

Personnel pressure:

- 2 Airfield Operations Supervisors;
- 2 Operational Team Leaders;
- 1 Police Sergeant;
- 1 Police Inspector.

Generation pressure:

- 3 Aviation firefighting Extensions;
- 2 Airfield Operations Extensions;
- 2 HART Bases;
- 1 Mass Casualty Extension;
- Large Airport runway POI.

### Planning implication

Hot Brakes Code D can require the same Airfield Firefighting Command resource as a dedicated unit and within two alternative groups. Do not count one vehicle three times without reproduced dispatch behaviour.

## Progression tier 3 — Aircraft Accident Code C

Verified guaranteed response:

- 1 Airfield Firefighting Command Vehicle;
- 2 Airfield Operations Vehicles;
- 1 Fire Engine;
- 1 Major Foam Tender;
- 1 Water Carrier;
- 2 Rescue Support Vehicles;
- 1 Mass Casualty Equipment resource;
- 8 Police Cars;
- 4 PRVs and 4 SRVs;
- 1 Welfare Vehicle.

Independent alternative groups:

- 1 ICCU, Ambulance Control Unit or Airfield Firefighting Command Vehicle;
- 6 Fire Officers and/or Airfield Firefighting Command Vehicles;
- 1 HazMat Unit or CBRN Vehicle;
- 7 Fire Engines and/or Major Foam Tenders.

Conditional response:

- 4 Traffic Cars, only when available.

Personnel pressure:

- 1 Airfield Operations Supervisor;
- 5 Operational Team Leaders;
- 1 Police Inspector and 2 Police Sergeants required;
- higher Police supervision values available before generation.

Patient pressure:

- 75–175 patients;
- General Internal specialisation;
- C-2/C-3 codes;
- 30% transport probability;
- 80% critical-care probability.

Generation pressure:

- 2 Aviation firefighting Extensions;
- 1 Airfield Operations Extension;
- 3 HART Bases;
- 1 Mass Casualty Extension;
- Medium or Large Airport runway POI.

## Progression tier 4 — Aircraft Accident Code F

Verified guaranteed response:

- 1 Airfield Firefighting Command Vehicle;
- 4 Airfield Operations Vehicles;
- 1 Fire Engine;
- 5 Major Foam Tenders;
- 1 Water Carrier;
- 2 Rescue Support Vehicles;
- 1 Mass Casualty Equipment resource;
- 12 Police Cars;
- 4 PRVs and 4 SRVs;
- 2 Welfare Vehicles.

Independent alternative groups:

- 1 Aerial Appliance Truck or Rescue Stairs;
- 1 ICCU, Ambulance Control Unit or Airfield Firefighting Command Vehicle;
- 6 Fire Officers and/or Airfield Firefighting Command Vehicles;
- 2 HazMat Units and/or CBRN Vehicles;
- 10 Fire Engines and/or Major Foam Tenders.

Conditional response:

- 6 Traffic Cars, only when available.

Personnel pressure:

- 2 Airfield Operations Supervisors;
- 5 Operational Team Leaders;
- 1 Police Inspector and 4 Police Sergeants required;
- higher Police command values available before generation.

Patient pressure:

- 150–250 patients;
- General Internal specialisation;
- C-2/C-3 codes;
- 15% transport probability;
- 80% critical-care probability.

Generation pressure:

- 3 Aviation firefighting Extensions;
- 2 Airfield Operations Extensions;
- 3 HART Bases;
- 1 Mass Casualty Extension;
- Large Airport runway POI.

## Independent alternatives and unique-resource risk

Airport missions may display the same qualifying resource in several independent groups.

Example Code F pressure:

```text
Dedicated Airfield Firefighting Command Vehicle: 1
Fire Officer OR Airfield Firefighting Command Vehicle: quantity 6
ICCU OR Ambulance Control Unit OR Airfield Firefighting Command Vehicle: quantity 1
```

The published rows do not prove the minimum number of unique Airfield Firefighting Command Vehicles when one type appears in several groups. Plan each group separately unless current dispatch behaviour has been reproduced.

## Conditional Traffic Cars

Verified airport incidents use `only_when_available` for Traffic Cars.

This means:

- the field is not a guaranteed requirement;
- it is not merely a recommendation;
- it should not be removed from the mission model;
- it should not be permanently over-dispatched as guaranteed airport demand.

Use the [Police and Public Safety guide](police.md) for Roads Policing training and regional reserve.

## Eight commissioning gates

| Gate | Question | Recommended pass condition |
|---|---|---|
| ARFF | Can RIV, foam and airfield command deploy with trained crews? | Commissioning and replacement ARFF cohorts exist |
| Operations | Are dedicated Airfield Operations Vehicles and supervisor personnel ready? | Operational and personnel rows are independently supported |
| Water/foam | Can published bulk-water and foam quantities deploy together? | One capability is not assumed to replace the other |
| Command | Does every independent alternative slot have its own valid resource? | No hidden double-counting remains |
| HazMat/access | Are HazMat/CBRN and aircraft-access alternatives ready? | Code-specific specialist groups can operate |
| Medical | Can HART, mass-casualty, welfare and patient demand be supported? | Airport response does not exhaust regional Ambulance reserve |
| Police | Are scene control, supervision and conditional Traffic Cars available? | Police personnel and vehicles are geographically ready |
| Recovery | Can the airport accept another incident afterwards? | Primary and relief bases restore useful specialist reserve |

## Recommended airport templates

These are strategy templates, not official requirements.

### Foundation airfield programme

| Capability | Recommended posture |
|---|---|
| Mission generation | One Aviation firefighting Extension only after Code B readiness |
| ARFF response | Enough trained RIV/foam capacity for the two published alternative groups |
| Water | Three Water Carrier routes before Code B activation |
| HART/welfare | Complete local or reliable alliance chain |
| Relief | One neighbouring Fire/Ambulance cluster protected from airport dispatch |

### Developing airport programme

| Capability | Recommended posture |
|---|---|
| Extensions | Airfield Operations activation only after dedicated operations vehicles are ready |
| Command | One dedicated ARFF command route plus independently staffed alternatives |
| Operations | Enough Airfield Operations Vehicles for the current Code C/D tier |
| Foam/water/HazMat | Quantity and geographic reserve tested separately |
| Medical | HART, Mass Casualty Equipment, welfare and command commissioned together |
| Police | Airport scene and supervisory response without exhausting routine patrol |

### Established airport programme

| Capability | Recommended posture |
|---|---|
| Code F fleet | Full guaranteed and alternative-group response plus protected relief reserve |
| ARFF training | Multiple independently dispatchable cohorts across primary and relief bases |
| Aircraft access | Rescue Stairs/Aerial route protected as a hard specialist chain |
| Medical | Large-patient and critical-care system tested with another regional incident |
| Police | Supervision, Traffic Cars and patrol reserve distributed geographically |
| Recovery | Airport capability restored before additional generator growth |

## Base architecture

### Primary airport base

- Holds the core ARFF, operations and airport-command resources.
- Aligns trained personnel with the intended vehicles.
- Provides immediate runway coverage.
- Must not contain every regional copy of water, HazMat, HART or Police command.

### Relief airport base

- Sits outside the same single point of failure.
- Reinforces Code C/F demand.
- Preserves replacement ARFF and operations crews.
- Can support another airport or regional major incident.

### Regional support ring

- Fire, Water Carrier, HazMat/CBRN and Rescue Support;
- HART, Ambulance command, Mass Casualty Equipment and Welfare;
- Police patrol, supervision and Roads Policing;
- hospital and patient-transport capacity.

## Transparent concurrency example

**Aircraft Accident Code F** plus **Bird Strike Code B** creates a calculated guaranteed commitment of:

- 1 dedicated Airfield Firefighting Command Vehicle;
- 4 Airfield Operations Vehicles;
- 5 Major Foam Tenders;
- 4 Water Carriers;
- 6 PRVs and 5 SRVs;
- 3 Welfare Vehicles;
- 1 Mass Casualty Equipment resource;
- 13 Police Cars;
- plus the independent alternative groups from both missions.

Maximum Code F patients remain 250; Code B does not publish a patient range in the current record. This is a transparent sum of verified requirements, not an official combined mission.

## Recovery-to-readiness

After an airport incident:

1. identify ARFF, operations, command, water, HazMat, HART and Police resources still committed;
2. restore minimum runway firefighting and operations cover first;
3. return trained ARFF and supervisor personnel to useful bases;
4. restore Water Carrier, foam, HazMat and aircraft-access reserve;
5. rebuild HART, mass-casualty, welfare and Police command capacity;
6. review patients and hospital transports still active;
7. rerun the chosen airport concurrency scenario;
8. correct recurring specialist or relief-base shortages before more extension activation.

Mission completion is not proof that runway, ARFF and regional medical readiness are restored.

## Common failures

| Failure | Operational symptom | Correction |
|---|---|---|
| Activating airport generators before training | Airport missions appear without crewed ARFF response | Complete commissioning and replacement cohorts |
| Counting one command vehicle several times | Alternative groups remain open | Allocate one valid resource per independent group |
| Treating foam and water as one capability | Missions retain an unsatisfied bulk-resource row | Preserve each requirement separately |
| Confusing supervisor role and vehicle | Personnel or vehicle planning uses the wrong contract | Keep verified role and community vehicle record distinct |
| Converting conditional Traffic Cars to guarantee | Roads units are over-allocated | Preserve `only_when_available` |
| Centralising every specialist | One Code F incident empties the region | Build relief-base and regional support layers |
| Planning Fire alone | HART, Police, patients or command block completion | Audit the full cross-service contract |
| Treating mission completion as airport readiness | Patients and returning specialists leave runway cover depleted | Run the recovery sequence |
| Guessing extension economics | Missing price/capacity becomes false data | Leave unpublished fields unknown |

## Operational readiness checklist

- [ ] Aviation firefighting and Airfield Operations extensions are treated separately;
- [ ] RIV, Major Foam Tender and Airfield Command crews have three-day ARFF training;
- [ ] operations vehicles and supervisor personnel are independently ready;
- [ ] same-named community vehicle data is labelled correctly;
- [ ] water, foam, HazMat and aircraft-access capability are separate;
- [ ] every alternative group has its own valid resource allocation;
- [ ] conditional Traffic Cars remain conditional;
- [ ] HART, mass casualty, welfare and Ambulance command are ready;
- [ ] Police Sergeant, Inspector and Airfield Supervisor states are supported;
- [ ] primary and relief bases preserve regional reserve;
- [ ] two airport incidents have been tested together;
- [ ] patient and critical-care pressure is included;
- [ ] unpublished values remain unknown rather than zero.

## Stage 37G completion

The Airfield Operations programme now covers:

- extension progression;
- ARFF vehicles, training and personnel;
- operations, command, water, foam, HazMat and aircraft access;
- Code B, D, C and F response tiers;
- alternative and conditional semantics;
- scalable airport-base architecture;
- cross-service medical and Police resilience;
- concurrency and recovery-to-readiness.

The next service programme is **Stage 37H — Recovery and HGV Recovery operational progression**.
