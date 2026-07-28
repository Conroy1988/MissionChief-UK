# Bomb Disposal and EOD Operational Progression

Bomb Disposal progression is an infrastructure-led specialist programme that expands from local land ordnance into HART-supported building sites, railway incidents and multi-service marine operations. Current canonical mission records now publish Bomb Disposal crew, equipment, command, heavy-equipment and diver-resource quantities; vehicle-market economics, staffing and training remain separate unknowns.

!!! info "Evidence boundary"
    Verified statements reproduce current canonical mission, infrastructure, resource and personnel records. Fleet depth, reserve floors, placement patterns and activation sequences are recommendations. Bomb Disposal market vehicle names, prices, staffing, course requirements, HQ capacity and marine carrier relationships remain unknown unless separately reproduced.

**Current evidence baseline:** 28 July 2026.

## Command doctrine

Use this order when expanding:

1. **One complete land-response chain first** — HQ count alone does not prove crew, equipment, Fire, Police and medical support are available.
2. **Command and heavy equipment before large sites** — larger missions publish dedicated Bomb Disposal command and heavy-equipment rows.
3. **Marine capability as a separate system** — diver crews, diver equipment, Coastguard, Lifeboat and marine extensions are not land-resource substitutes.
4. **Active Drone prerequisite versus dispatch** — preserve generation and guaranteed-response fields independently.
5. **Cross-service readiness before another HQ** — HART, Police command, Railway Police, Coastguard and patient support may control completion.
6. **Regional reserve before maximum progression** — one high-complexity incident should not remove every Bomb Disposal resource from the account.

[Open Mission Lookup](../tools/mission-lookup.md) · [Open Concurrent Fleet Planner](../tools/fleet-planner.md) · [Compare Resources](../tools/resource-comparison.md)

## Bomb Disposal response chain

```text
Bomb Disposal HQ / Marine Unit generation
                ↓
Bomb Disposal crew and equipment
                ↓
Command / heavy / diver capability where published
                ↓
Fire and Police scene protection
                ↓
HART, Ambulance, Coastguard, Lifeboat or Railway support
                ↓
Specialist personnel and active-Drone conditions
                ↓
Regional specialist reserve restored
```

## Verified infrastructure

### Bomb Disposal HQ

The canonical infrastructure record verifies Bomb Disposal HQ as a mission-generation building. Current mission progression uses between one and three HQs in the representative set below.

The following remain unknown:

- construction cost;
- build duration;
- vehicle and personnel capacity;
- vehicle-market inventory;
- staffing rules.

### Bomb Disposal Marine Unit Extension

The verified extension:

- belongs to a Bomb Disposal HQ;
- enables marine and coastal Bomb Disposal mission preconditions;
- appears at quantities of one or two in current representative missions.

Extension cost, build time, capacity and associated vehicles remain unpublished.

!!! warning "Infrastructure is not response capacity"
    Adding an HQ or marine extension can make a mission eligible to generate. It does not create the Bomb Disposal crew, equipment, command, diver, Fire, Police, HART, Coastguard or Lifeboat response required at the incident.

## Canonical Bomb Disposal resource rows

Current verified missions use these resource identities:

| Canonical resource | Verified operational use | Current evidence boundary |
|---|---|---|
| `bomb_disposal_crew` | Land Bomb Disposal response | Market vehicle name, staffing, cost and training unpublished |
| `bomb_disposal_equipment` | Standard land ordnance equipment | Purchase/storage/transport contract unpublished |
| `bomb_disposal_command` | Command on higher-complexity incidents | Vehicle, crew, cost and training unpublished |
| `bomb_disposal_heavy_equipment` | Large building-site response | Market and carrier details unpublished |
| `bomb_disposal_diver_crew` | Marine/diver Bomb Disposal response | Vehicle/vessel, staffing, cost and training unpublished |
| `bomb_disposal_diver_equipment` | Marine ordnance equipment | Storage, towing or vessel relationship unpublished |

The canonical IDs are valid mission requirements. They must not be converted into invented vehicle-market names or economics.

## Active Drone semantics

Bomb Disposal missions can publish either or both of these fields:

- `active_drones` as a generation prerequisite;
- `drone` as a guaranteed response resource.

For example, the large building-site and harbour missions require one active Drone before generation **and** publish one guaranteed Drone at the incident.

Do not assume every active-Drone precondition dispatches equipment automatically. Conversely, do not remove a guaranteed Drone row merely because the account already satisfies the generation prerequisite.

The verified Drone equipment contract is documented in [Search and Rescue HQ progression](search-and-rescue.md).

## Land progression

### Unexploded WW2 Ordnance in Countryside

Verified response:

- 1 Bomb Disposal Crew;
- 1 Bomb Disposal Equipment resource;
- 2 Fire Engines;
- 2 Fire Officers;
- 2 Police Cars;
- 1 Operational Team Leader;
- 1 Bomb Disposal HQ;
- Forest, Farm or Heathland POI.

This is the foundation land-response contract: ordinary Bomb Disposal crew/equipment plus Fire, Police and Ambulance-personnel support.

### Unexploded WW2 Grenade Located in Loft

Verified response:

- 1 Bomb Disposal Crew;
- 1 Bomb Disposal Equipment resource;
- 1 Fire Engine;
- 1 Fire Officer;
- 3 Police Cars;
- 1 Ambulance;
- 1 PRV and 1 SRV;
- 1 Operational Team Leader;
- 2 Bomb Disposal HQs and 1 HART Base.

The incident demonstrates that a modest Bomb Disposal requirement can still create a separate HART and patient-response dependency.

### Unexploded WW2 Bomb at Building Site — Large

Verified response:

- 1 Bomb Disposal Command resource;
- 2 Bomb Disposal Crews;
- 1 Bomb Disposal Heavy Equipment resource;
- 1 guaranteed Drone;
- 2 Fire Engines and 2 Fire Officers;
- 10 Police Cars;
- 1 Ambulance, 1 PRV and 1 SRV;
- 1 ICCU, Ambulance Control Unit or Airfield Firefighting Command Vehicle alternative slot;
- 1 Operational Team Leader;
- 1 Police Sergeant and 1 Police Inspector;
- 3 Bomb Disposal HQs, 1 HART Base and 1 active Drone precondition.

This is the representative high-complexity land contract. Command, heavy equipment, HART and Police supervision become independent capacity chains.

## Marine progression

### Unexploded WW2 Ordnance on Quiet Beach

Verified response:

- 1 Bomb Disposal Diver Crew;
- 1 Bomb Disposal Diver Equipment resource;
- 1 CRV;
- 1 Fire Engine and 1 Fire Officer;
- 2 Police Cars;
- 1 Operational Team Leader;
- 1 Bomb Disposal HQ;
- 1 Marine Unit Extension;
- 1 Coastguard Rescue Station;
- Beach POI.

The marine extension and diver resources form a separate commissioning gate from ordinary land crew/equipment.

### Unexploded WW2 Ordnance in Harbour

Verified response:

- 1 Bomb Disposal Command resource;
- 2 Bomb Disposal Diver Crews;
- 1 Bomb Disposal Diver Equipment resource;
- 1 guaranteed Drone;
- 2 CRVs, 2 Coastguard Commanders and 1 Coastguard Support Unit;
- 1 ILB and 1 ALB;
- 8 Police Cars;
- 1 Ambulance, 1 PRV and 1 SRV;
- 1 Fire Officer;
- 1 Operational Team Leader;
- 1 Police Sergeant and 1 Police Inspector;
- 3 Bomb Disposal HQs and 2 Marine Unit Extensions;
- 1 HART Base, 1 active Drone and 9 Coastguard Rescue Stations.

The harbour mission is a regional maritime major incident. Bomb Disposal is only one component of the verified response.

## Railway progression

### Unexploded ordnance at Small Train Station

Verified response:

- 1 Bomb Disposal Crew;
- 1 Bomb Disposal Equipment resource;
- 1 EIU;
- 2 Fire Engines and 2 Fire Officers;
- 4 Police Cars;
- 1 Ambulance, 1 PRV and 1 SRV;
- 1 Operational Team Leader;
- 1 Police Sergeant;
- 4 Railway Police Officers;
- 2 Bomb Disposal HQs;
- 3 Railway Police buildings and 1 HART Base.

This mission demonstrates that railway Bomb Disposal readiness depends on EIU, Railway Police infrastructure and personnel as well as the ordinary Bomb Disposal chain.

## Personnel-state planning

Representative Bomb Disposal missions publish:

- Operational Team Leader required at the incident;
- Police Sergeant required and available values;
- Police Inspector required and available values;
- Railway Police Officer required and available values.

Available-before-generation and required-at-incident values remain separate. Bomb Disposal crew resource quantities are also not interchangeable with mission personnel-role fields.

## Six commissioning gates

| Gate | Question | Recommended pass condition |
|---|---|---|
| Land response | Are crew and standard equipment independently available? | One complete land chain plus regional reserve exists |
| Command/heavy | Can large incidents receive command and heavy equipment? | No high-complexity mission depends on one unverified substitute |
| Marine | Are diver crew/equipment and partner maritime resources ready? | Marine extensions activate only after the whole response exists |
| Drone | Are active equipment and guaranteed dispatch semantics both met? | Generation and response fields are modelled independently |
| Cross-service | Are Fire, Police, HART, Coastguard, Lifeboat or Railway dependencies ready? | The complete mission contract can operate |
| Recovery | Can another specialist incident begin afterwards? | Crew, equipment, command and partner services return to useful regions |

## Recommended progression templates

These are strategic templates, not official unlock requirements.

### Foundation programme

| Capability | Recommended posture |
|---|---|
| Bomb Disposal infrastructure | 1 HQ only after one complete land-response chain is ready |
| Land response | 1 crew and standard-equipment route with protected regional fallback |
| Fire/Police support | Local response capacity that remains available after ordinary dispatch |
| HART | Alliance-supported until HART-dependent Bomb Disposal missions become relevant |
| Marine | Do not activate until diver resources and Coastguard response are complete |

### Developing programme

| Capability | Recommended posture |
|---|---|
| HQs | Two operational regions or enough coverage for two-HQ mission pressure |
| Land response | Duplicate crew/equipment by travel-time zone |
| Command | One dedicated command route with replacement staffing once command missions unlock |
| HART/Police | PRV/SRV, command and Police supervision tested together |
| Railway | EIU and Railway Police dependencies commissioned before railway ordnance demand |
| Drone | Active equipment and one deployable response path where guaranteed missions require it |

### Established programme

| Capability | Recommended posture |
|---|---|
| HQs | Three-HQ progression backed by actual specialist depth rather than building count alone |
| Land response | Multiple independently dispatchable crew/equipment groups |
| Heavy/command | Protected command and heavy-equipment reserve |
| Marine | At least one complete diver/maritime group with regional backup |
| Cross-service | HART, Coastguard, Lifeboat, Railway and Police command chains tested concurrently |
| Recovery | Specialist resources restored before more HQ/extension activation |

## Transparent concurrency calculations

### Large building site plus quiet beach

Calculated guaranteed Bomb Disposal commitment:

- 1 Bomb Disposal Command;
- 2 land Bomb Disposal Crews;
- 1 Heavy Equipment resource;
- 1 Diver Crew;
- 1 standard Diver Equipment resource;
- 1 guaranteed Drone;
- plus the independent Fire, Police, Ambulance, HART and Coastguard responses.

### Harbour plus countryside

Calculated guaranteed Bomb Disposal commitment:

- 1 Bomb Disposal Command;
- 2 Diver Crews and 1 Diver Equipment resource;
- 1 land Crew and 1 standard Equipment resource;
- 1 guaranteed Drone;
- plus 1 ILB, 1 ALB, Coastguard command/support, Fire, Police and HART dependencies.

These are transparent sums from verified records, not official combined missions. Market staffing and transport assumptions remain unknown.

## Geographic doctrine

### Land network

- Position crew/equipment by road coverage to countryside, residential and construction POIs.
- Keep Police and Fire support local enough to protect the scene without emptying adjacent regions.
- Place command/heavy capability where it can reinforce several HQ regions.
- Include HART and patient-response travel time.

### Coastal and harbour network

- Align marine extensions with Coastguard, Lifeboat and usable harbour/beach geography.
- Keep diver crew/equipment and maritime command within the same operational region.
- Preserve ILB/ALB and Coastguard reserve for non-ordnance incidents.
- Treat marine response as a full regional chain rather than a single extension.

### Railway network

- Align Bomb Disposal coverage with Railway Police, EIU and rail corridors.
- Preserve Railway Police Officer and supervisory personnel reserve.
- Include Fire, HART and ordinary Police support.
- Test railway and non-rail ordnance incidents together.

## Recovery-to-readiness

After an ordnance incident:

1. identify Bomb Disposal crews, equipment, command, heavy or diver resources still committed;
2. restore one complete land-response chain first;
3. return active and deployed Drone capability to useful status;
4. rebuild HART, Police, Fire, Coastguard, Lifeboat or Railway reserve;
5. return marine specialists to the region where their extension generates missions;
6. rerun the chosen concurrent scenario;
7. correct repeated specialist or partner-service shortages before adding more HQs or extensions.

Mission completion is not proof that all specialist and partner resources are restored.

## Common failures

| Failure | Operational symptom | Correction |
|---|---|---|
| Treating HQ count as fleet capacity | Missions generate without crew/equipment | Commission the response chain before another HQ |
| Reusing land resources for marine rows | Beach/harbour incidents remain open | Preserve diver crew/equipment requirements |
| Inventing market vehicle details | Canonical mission IDs become unsupported purchase claims | Keep market economics and staffing unknown |
| Confusing active Drone with dispatch | Generation or response planning omits one of the two fields | Model prerequisite and guaranteed resource separately |
| Planning Bomb Disposal alone | HART, Police, Coastguard, Lifeboat or Railway rows remain open | Audit the full mission contract |
| Centralising command/heavy capability | One large incident removes regional progression | Duplicate by travel-time and concurrency |
| Ignoring personnel states | Vehicles attend while Sergeant, Inspector or Railway roles remain unmet | Preserve available and required semantics |
| Expanding while degraded | New missions appear before specialist reserve returns | Restore readiness before further activation |

## Operational readiness checklist

- [ ] at least one complete land crew/equipment chain is dispatchable;
- [ ] command and heavy-equipment rows are available where published;
- [ ] marine diver crew/equipment remain separate from land response;
- [ ] HQ and extension counts are not treated as response resources;
- [ ] active Drone and guaranteed Drone fields are modelled independently;
- [ ] Operational Team Leader and Police personnel states are ready;
- [ ] Fire, Police, HART, Coastguard, Lifeboat and Railway dependencies are included;
- [ ] two representative ordnance missions have been tested together;
- [ ] regional specialist reserve and recovery are documented;
- [ ] market names, prices, staffing and training remain unknown where unpublished.

## Stage 37F completion

The Bomb Disposal and EOD operational programme now covers:

- land, building-site, railway, beach and harbour progression;
- crew, standard equipment, command, heavy and diver-resource pressure;
- HQ, marine-extension and active-Drone semantics;
- cross-service Fire, Police, HART, Coastguard, Lifeboat and Railway readiness;
- scalable infrastructure templates;
- concurrency, geography and recovery-to-readiness.

The next service programme is **Stage 37G — Airfield Operations progression**.
