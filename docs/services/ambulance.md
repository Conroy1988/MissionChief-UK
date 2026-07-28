# Ambulance and HART Operational Progression

Ambulance resilience depends on more than the number of vehicles parked at stations. A complete network must treat patients, transport, critical care, hospitals, trained personnel, HART response, incident command, mass-casualty equipment, welfare and air medical support as connected but separate operating systems.

!!! info "Evidence boundary"
    Verified statements reproduce current canonical mission, vehicle, infrastructure and training records. Fleet sizes, reserve floors, placement patterns and activation sequences are recommendations. Unpublished prices, staffing limits, station capacities, hospital rules, course transferability and unlock details remain unknown.

**Current evidence baseline:** 28 July 2026.

## Command doctrine

Use this order when expanding:

1. **Routine treatment and transport first** — ordinary patient demand must not consume every dispatchable Ambulance.
2. **Patient throughput second** — treatment, transport probability, destination availability and vehicle return time form one capacity chain.
3. **Specialist training before activation** — HART, command, mass-casualty and air-medical vehicles are not operational until qualified crews are available.
4. **Command and welfare as hard resources** — when a mission publishes these rows, frontline volume does not substitute for them.
5. **Geography before duplication** — place resources against mission density, travel time, hospitals and specialist response zones.
6. **Protected reserve before another generator** — expansion is safer when a second incident can be supported without dismantling the first response.

[Open Mission Lookup](../tools/mission-lookup.md) · [Open Concurrent Fleet Planner](../tools/fleet-planner.md) · [Compare Resources](../tools/resource-comparison.md)

## The patient-throughput chain

```text
Patient-generating mission
          ↓
Treatment-capable response
          ↓
Critical-care capability where published
          ↓
Transport decision and destination
          ↓
Hospital access and handoff
          ↓
Vehicle returns to useful geography
          ↓
Reserve restored for the next patient
```

A patient is not an instantaneous one-vehicle transaction. Travel, treatment, transport and return time can remove capacity long after the initial dispatch.

## Verified capability contracts

| Resource | Verified operational role | Verified building or training relationship | Current evidence boundary |
|---|---|---|---|
| **Ambulance** | Patient treatment and transport | Available from a Small Ambulance Station | Cost, staffing limits and station capacity remain unpublished in the canonical record |
| **Rapid Response Vehicle** | Ambulance first response; valid option for HCP Home Visit and Palliative Care Visit | Available from a HART Base or Small Ambulance Station | Cost, staffing and training remain unpublished |
| **Specialist Paramedic RRV** | Specialist-paramedic response; valid alternative on HCP and palliative visits | Building, cost, staffing and training are unpublished | Do not infer that it replaces an Ambulance for every patient or transport requirement |
| **PRV** | Specialist HART response | HART Base; **HART Training**, 5 days, Rescue (EMS) Academy | Price and staffing remain unpublished |
| **SRV** | Specialist HART response | HART Base; **HART Training**, 5 days, Rescue (EMS) Academy | Price and staffing remain unpublished |
| **Ambulance Control Unit** | Ambulance incident command | HART Base or Small Ambulance Station; **Tactical Command Course**, 5 days, Rescue (EMS) Academy | Price, staffing and capacity remain unpublished |
| **Mass Casualty Equipment** | Mass-casualty support | **SORT Training**, 3 days, Rescue (EMS) Academy | Building, price, staffing and capacity remain unpublished in the retained record |
| **Welfare Vehicle** | Incident welfare support | HART Base | No HART training requirement is inferred; price and staffing remain unpublished |
| **Air Ambulance / HEMS** | Air medical response, patient treatment and transport | Helicopter Station; **Critical care**, 5 days, Rescue (EMS) Academy | Market economics and staffing remain unpublished |

[Review the complete Vehicle Catalogue](../reference/vehicle-catalogue.md) · [Review Training and Personnel](../reference/training-and-personnel.md)

## Infrastructure controls

### Small Ambulance Station

The current canonical vehicle records verify the Small Ambulance Station as a source for:

- Ambulances;
- Rapid Response Vehicles;
- Ambulance Control Units.

Its purchase cost, build time, vehicle capacity and personnel capacity remain outside the current verified infrastructure record. Do not turn absent values into zero.

### HART Base

The HART Base is the operational home for:

- PRV;
- SRV;
- Rapid Response Vehicle/Fly Car;
- Ambulance Control Unit/Mobile Command;
- Welfare Vehicle.

A HART Base should be planned as a complete response system rather than a garage for isolated specialist purchases.

### Helicopter Station

The official vehicle record verifies the Helicopter Station relationship for Air Ambulance/HEMS. Air medical capability should be positioned by regional travel value and hospital geography rather than used as a substitute for routine local Ambulance capacity.

### Mass Casualty Extension

Verified major incidents use Mass Casualty Extensions as mission-generation preconditions. Parent-building compatibility, price, build time and capacity remain unknown unless directly reproduced in the infrastructure programme.

!!! warning "Generation is not response"
    A building or extension count can permit a mission to generate. It does not prove that transport, command, HART, welfare, trained personnel or hospital throughput is ready.

## Patient-field semantics

Canonical missions may publish several independent patient fields.

| Field | Meaning | Planning consequence |
|---|---|---|
| `minimum` / `maximum` | Published patient range | Plan against the upper boundary when testing resilience |
| `generated_at_end` | Patients appear when the operational phase completes | Keep treatment and transport reserve available for the later demand |
| `transport_probability` | Chance that a patient requires transport | Preserve the probability; do not convert it into a guaranteed exact count |
| `critical_care_probability` | Chance that critical-care support is required | Maintain critical-care resilience without treating every patient as guaranteed critical care |
| `specializations` | Published clinical destination or treatment category | Check hospital and department planning separately |
| `codes` | Published patient-code set | Preserve the source values rather than inventing severity conversion rules |

### No automatic ambulance conversion

The guide does not use a rule such as “one Ambulance per patient” unless a mission or game mechanism explicitly publishes that contract. Patient count, treatment capacity and transport demand are related but not identical fields.

## Six expansion gates

| Gate | Question | Recommended pass condition |
|---|---|---|
| Routine reserve | Can ordinary patient missions dispatch while another Ambulance is transporting? | Useful treatment/transport capacity remains in each main response cluster |
| Throughput | Can vehicles complete treatment, transport and return without persistent queue growth? | Hospital and travel pressure no longer consumes the whole fleet |
| Specialist readiness | Are the required vehicle, crew, qualification and base available together? | The complete chain is staffed before related mission generation expands |
| Command | Can every independent incident-control slot receive its own qualifying resource? | No command unit is counted across several alternative groups simultaneously |
| Geography | Can routine, HART and air resources reach their intended demand? | Placement improves actual route coverage and return time |
| Recovery | Can the network restore reserve after a high-patient incident? | Returning, transporting and repositioning resources are included in the readiness test |

## Routine ambulance planning

### Measure concurrent patient work

Do not size routine capacity from the largest patient count alone. Record:

- active patients awaiting treatment;
- patients likely to require transport;
- Ambulances already travelling to hospitals;
- units returning from distant destinations;
- simultaneous non-patient vehicle requirements;
- protected local reserve.

### Recommended reserve model

These are strategy recommendations, not game requirements.

- Keep at least one useful treatment/transport route outside a normal local dispatch.
- In dense areas, neighbouring stations may share reserve when route times are short.
- In dispersed areas, retain local Ambulances because hospital journeys can create long absences.
- Do not count an RRV, HART vehicle or Air Ambulance as routine transport reserve unless a reproduced game contract supports the intended use.
- Increase frontline volume when queue growth is caused by transport and return time rather than specialist scarcity.

### Hospital and destination pressure

A fleet can be numerically sufficient and still fail operationally when every Ambulance is travelling to or returning from a distant destination.

Recommended audit:

1. identify the mission clusters generating the most transports;
2. record typical hospital journey and return times;
3. note specialisation or department pressure where published;
4. distribute stations to reduce total patient-cycle time;
5. retest concurrent demand before adding another specialist service.

## Specialist-paramedic and RRV work

The verified **HCP Home Visit** and **Palliative Care Visit** missions each publish one alternative slot:

```text
Rapid Response Vehicle OR Specialist Paramedic RRV
```

These missions demonstrate a specialist first-response decision, not a universal vehicle substitution rule.

### HCP Home Visit

Verified patient contract:

- one patient;
- General Internal specialisation;
- C-4 code;
- patient generated at mission end;
- 30% transport probability.

### Palliative Care Visit

Verified patient contract:

- one patient;
- General Internal specialisation;
- C-3/C-4 codes;
- patient generated at mission end;
- 5% transport probability;
- 5% critical-care probability.

Recommended use:

- keep at least one valid response option within the relevant area;
- preserve routine Ambulance reserve for patients that later require transport;
- do not buy duplicate specialist vehicles without measured geographic or concurrency pressure;
- leave vehicle economics, staffing and training unknown where the canonical record does not publish them.

## HART commissioning

### The HART response chain

```text
HART-related mission pressure
          ↓
HART Base
          ↓
PRV + SRV + trained cohorts
          ↓
Command + welfare where published
          ↓
Operational Team Leaders and other personnel
          ↓
Routine Ambulance and transport reserve
```

### Representative verified chain

**Amateur Explorers Trapped in Abandoned Mineshaft** publishes:

- 2 PRVs;
- 2 SRVs;
- 1 Welfare Vehicle;
- 1 incident-control alternative slot;
- 2–6 patients generated at mission end;
- 75% transport probability and 25% critical-care probability;
- 1 required Operational Team Leader;
- 2 HART Bases as a generation precondition;
- Fire, Police, Mountain Rescue, Search Advisor and Cave Rescue dependencies.

This is a cross-service mission. Owning the HART vehicles alone does not complete the response chain.

### Training cohorts

PRV and SRV each use the verified five-day HART Training course.

Recommended cohort sequence:

1. **Commissioning cohort** — enough trained staff to dispatch the first planned PRV/SRV chain.
2. **Replacement cohort** — enough qualified staff to restore capability when the first group is committed.
3. **Geographic cohort** — duplicate qualified capacity in another response zone when travel time creates the bottleneck.
4. **Expansion cohort** — train ahead of additional vehicles only when the fleet addition is part of the active plan.

Do not assume one trained cohort can crew several vehicles simultaneously.

## Ambulance command

The Ambulance Control Unit is a verified command-and-control resource with a five-day Tactical Command Course.

Major missions may publish several independent alternative groups containing:

- ICCU;
- Ambulance Control Unit;
- Airfield Firefighting Command Vehicle.

Each group is separate. One Ambulance Control Unit should not be counted several times because its type appears in each row.

### Recommended command posture

| Network stage | Recommended posture |
|---|---|
| Foundation | One trained command route before activating mission families that repeatedly need it |
| Developing | Command resource plus a replacement crew; alliance support for exceptional second incidents |
| Established | Independently crewed command resources distributed by response zone and tested against simultaneous major incidents |

## Mass-casualty planning

Mass Casualty Equipment uses verified three-day SORT Training. It is separate from:

- Ambulance quantity;
- Ambulance Control Units;
- PRV/SRV capacity;
- Welfare Vehicles;
- hospital capacity;
- critical-care resources.

Representative pressure includes:

| Mission | Verified ambulance-side pressure |
|---|---|
| **Multiple vehicle RTC — Major Incident** | Mass Casualty Equipment; two command groups; 30–150 patients |
| **Aircraft Accident — Code F** | 4 PRVs, 4 SRVs, Mass Casualty Equipment, command alternatives, 150–250 patients |
| **Bridge collapse — major** | 2 PRVs, 2 SRVs, Welfare Vehicle, Mass Casualty Equipment, two command groups, 20–50 patients |
| **Passenger Train Caught in Landslide — Major Incident** | 4 PRVs, 4 SRVs, 2 Welfare Vehicles, Mass Casualty Equipment, three command slots and 50–200 patients |

### Calculated concurrency example

**Bridge collapse — major** plus **Amateur Explorers Trapped in Abandoned Mineshaft** creates a transparent combined guaranteed commitment of:

- 4 PRVs;
- 4 SRVs;
- 2 Welfare Vehicles;
- 1 Mass Casualty Equipment resource;
- 3 independent incident-control slots;
- up to 56 patients.

This is a calculation from two verified records, not an official combined mission. Treatment, transports, critical-care demand, personnel and every non-Ambulance service remain additional constraints.

## Air medical operations

Air Ambulance/HEMS provides verified air medical response, treatment and transport capability and requires the five-day Critical care course.

Recommended deployment logic:

- position by regional travel-time advantage rather than visual map centre;
- protect local ground-Ambulance capacity instead of using HEMS to conceal a routine fleet shortage;
- maintain a replacement trained cohort where one aircraft is a critical regional dependency;
- include hospital destination and return geography in the coverage model;
- do not assume HEMS satisfies every mission-specific critical-care or transport field without reproduced evidence.

## Personnel-state planning

Mission records distinguish personnel who must be **available before generation** from personnel **required at the incident**.

Ambulance and HART planning may involve:

- Operational Team Leader;
- Ambulance Officer;
- other cross-service command and specialist roles.

Do not merge these semantics into one number. A qualification can be a generation prerequisite, an incident attendance requirement or both on different missions.

## Recommended fleet templates

These are capability templates, not official requirements.

### Foundation network

Suitable for a compact account with routine patient demand.

| Capability | Recommended position |
|---|---|
| Routine Ambulances | 4–6 distributed around mission and hospital geography |
| Protected reserve | At least 1 useful treatment/transport route after a normal dispatch |
| RRV/specialist response | Add one verified option when the related mission pressure appears |
| Command | Prepare one trained command route before repeated command demand |
| HART | Alliance-supported until the complete local vehicle/training chain can be commissioned |
| Air medical | Add only when geography and trained staffing provide measurable value |

### Developing network

Suitable when transports and simultaneous patient incidents are common.

| Capability | Recommended position |
|---|---|
| Routine Ambulances | 8–12 across two or more response clusters, adjusted for transport cycle time |
| Protected reserve | At least 2 useful treatment/transport routes across the network |
| RRV/specialist response | Distributed to prevent one distant response from covering every visit |
| HART | One complete trained PRV/SRV response group with replacement personnel |
| Command | One Ambulance Control Unit plus replacement trained crew |
| Mass casualty | One SORT-trained equipment route before activating repeated large-patient generators |
| Welfare | Available with the HART chain where published missions require it |

### Established network

Suitable for wide geography and sustained concurrency.

| Capability | Recommended position |
|---|---|
| Routine Ambulances | Sized from measured active patients, transports, return times and protected reserve |
| HART | Independently dispatchable groups across major travel-time zones |
| Command | Multiple trained units capable of satisfying separate command slots |
| Mass casualty and welfare | Duplicated when two reference incidents expose a single point of failure |
| Air medical | Regional aircraft and qualified reserve aligned with hospital geography |
| Personnel | Commissioning, replacement and expansion cohorts documented by vehicle and zone |

## Geographic planning

### Dense urban network

- Place Ambulances around mission density and hospital routes.
- Share some reserve across close stations, but include congestion and transport absence.
- Distribute command and HART so one incident does not remove the entire citywide specialist chain.
- Monitor hospital return time rather than station distance alone.

### Rural or dispersed network

- Keep routine transport capacity local because destination journeys may be long.
- Use air medical coverage where it creates a verified time advantage.
- Duplicate HART and command by travel-time zone before central fleet size becomes the only metric.
- Treat alliance assistance as contingency rather than guaranteed local cover.

### Cross-service major-incident network

- Position Ambulance command near Fire, Police, Railway, Airfield and SAR major-incident geography.
- Ensure HART bases do not become one shared point of failure.
- Test welfare, mass-casualty equipment, PRV/SRV and command slots separately.
- Include trained personnel and hospital throughput in every concurrency test.

## Recovery-to-readiness

After a patient-heavy or HART incident clears:

1. identify vehicles still treating, transporting, returning or repositioning;
2. restore routine Ambulance cover in exposed zones;
3. confirm PRV/SRV and trained cohorts are genuinely available;
4. return command, welfare and mass-casualty equipment to useful geography;
5. review hospital and critical-care pressure still in progress;
6. retest the chosen reference incident with protected reserve;
7. correct recurring shortages before activating further generators.

Mission completion is not proof that the Ambulance network is ready for another major incident.

## Common failures

| Failure | Operational symptom | Correction |
|---|---|---|
| Counting patients as a fixed Ambulance total | Fleet planning uses an unsupported conversion | Preserve patient, treatment and transport fields separately |
| Buying HART vehicles before training | Specialist vehicles exist but cannot form a reliable response chain | Complete commissioning and replacement cohorts first |
| Using one command unit for several slots | Major incidents retain unsatisfied command groups | Allocate one qualifying resource per independent group |
| Ignoring transport cycle time | Vehicles exist but remain absent at hospitals or on return journeys | Size and place the routine fleet from full patient-cycle time |
| Counting RRV as transport reserve | Treatment response appears available but patients cannot be moved | Preserve Ambulance transport capacity separately |
| Owning Mass Casualty Equipment without SORT staff | Large incidents remain blocked | Train the verified crew before activation |
| Centralising HART and welfare | One specialist incident removes regional capacity | Duplicate by travel-time zone and concurrency |
| Treating HEMS as routine fleet replacement | Local transport shortages persist | Use air medical capability for measured geographic or clinical value |
| Planning Ambulance in isolation | Fire, Police, SAR, Railway or Airfield requirements delay completion | Audit the whole mission contract |
| Expanding while degraded | New missions generate before transport and specialist reserve recover | Restore readiness before further activation |

## Operational readiness checklist

- [ ] routine treatment and transport reserve survives a normal dispatch;
- [ ] patient ranges, transport probability and critical-care probability remain separate;
- [ ] hospital journey and return time are included in fleet planning;
- [ ] RRV and Specialist Paramedic RRV are used only where verified;
- [ ] PRV and SRV crews have completed five-day HART Training;
- [ ] Ambulance Control Unit crews have completed the five-day Tactical Command Course;
- [ ] Mass Casualty Equipment has a SORT-trained dispatch path;
- [ ] welfare is available where a guaranteed mission row requires it;
- [ ] HEMS has Critical care-trained personnel and meaningful regional placement;
- [ ] each independent command slot has its own qualifying resource;
- [ ] Operational Team Leader and other personnel states are preserved correctly;
- [ ] HART, command and mass-casualty chains have replacement depth;
- [ ] two reference incidents have been tested together in Fleet Planner;
- [ ] alliance assistance is treated as contingency;
- [ ] unpublished values remain unknown rather than zero.

## Stage 37B completion

The Ambulance and HART operational programme now covers:

- routine patient treatment and transport;
- patient-throughput and hospital-return pressure;
- specialist RRV work;
- HART commissioning and trained cohorts;
- command, welfare and mass-casualty resilience;
- HEMS and critical-care coverage;
- scalable fleet templates;
- geography, concurrency and recovery-to-readiness.

The next service programme is **Stage 37C — Police and Public Safety operational progression**.
