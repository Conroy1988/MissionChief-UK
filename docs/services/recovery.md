# Recovery and HGV Recovery Operational Progression

Recovery operations add a second workload after, or alongside, emergency response: disabled cars, collision vehicles and trucks must be cleared after the Fire, Police or Ambulance phase is supported. Canonical records store towing under `recovery.assets`, separately from dispatched emergency-resource requirements. This distinction is fundamental to safe planning.

!!! info "Evidence boundary"
    Verified statements reproduce current canonical mission, infrastructure, recovery-outcome, conditional and personnel records. Capacity templates, regional reserve and activation sequences are recommendations. Recovery Centre economics, vehicle-market inventory, staffing, towing speed/capacity and HGV extension details remain unknown unless directly reproduced.

**Current evidence baseline:** 28 July 2026.

## Command doctrine

Use this order when expanding:

1. **One complete car-recovery chain first** — a Recovery Centre should create useful clearing capacity, not only new missions.
2. **Towing outcomes separate from emergency response** — recovery assets are not fictional Fire, Police or Ambulance requirement rows.
3. **HGV as a separate progression gate** — truck towing and HGV mission generation require the dedicated extension.
4. **Road-corridor geography before duplication** — recovery time includes travel to the incident, towing and return-to-availability.
5. **Preserve conditional and probabilistic fields** — Traffic Cars and personnel may not be guaranteed.
6. **Regional reserve before more generators** — a multi-vehicle incident should not remove every recovery route from the account.

[Open Mission Lookup](../tools/mission-lookup.md) · [Open Concurrent Fleet Planner](../tools/fleet-planner.md)

## Recovery workload chain

```text
Recovery Centre / HGV Recovery generation
                  ↓
Emergency incident response where published
                  ↓
Car or truck recovery outcome
                  ↓
Towing and clearance workload
                  ↓
Vehicle returns to regional availability
                  ↓
Recovery reserve restored for another incident
```

## Verified infrastructure

### Recovery Centre

The canonical Recovery Centre:

- generates dedicated Recovery Vehicle Missions;
- enables recovery-enabled variants;
- provides car-towing capability.

The following remain unknown:

- purchase cost;
- construction time;
- capacity and staffing;
- vehicle-market inventory;
- towing economics and speed.

### HGV Recovery Extension

The canonical extension:

- enables HGV recovery mission generation;
- provides truck-towing capability;
- is a precondition on verified truck-recovery variants.

Compatible parent building, cost, build time and capacity remain unpublished.

!!! warning "Infrastructure is not a dispatch row"
    A Recovery Centre or HGV Recovery Extension is a generation and capability control. It must not be inserted into `requirements.guaranteed` as though the building or extension attends the incident.

## Recovery outcomes versus requirements

### Emergency-resource requirements

These describe vehicles or personnel required to resolve the incident phase, such as:

- Fire Engines;
- Police Cars;
- Traffic Cars;
- Operational Team Leaders;
- patients and medical support.

### Recovery assets

These describe the post-response towing workload:

```json
"recovery": {
  "assets": [
    {
      "asset_type": "car",
      "minimum": 2,
      "maximum": 4
    }
  ]
}
```

Do not create an invented `recovery_vehicle` emergency requirement from this object. Use the asset type and range exactly as published.

## Dedicated Recovery missions

### Abandoned Car Obstructing Road

Verified contract:

- 1 Recovery Centre;
- no published emergency-resource requirement;
- exactly 1 car recovery outcome;
- Recovery Vehicle Missions classification;
- 400 average credits.

### Broken Down Car Obstructing Road

Verified contract:

- 1 Recovery Centre;
- no published emergency-resource requirement;
- exactly 1 car recovery outcome;
- Recovery Vehicle Missions classification;
- 400 average credits.

These current canonical records supersede the older Stage 20 note that the towing outcome was unavailable. They still do not prove a vehicle-market name, price, crew or station capacity.

## Fire recovery variations

### Burning car

Verified variation:

- 1 Fire Station;
- 1 Recovery Centre;
- 1 Fire Engine;
- exactly 1 car to recover;
- 670 average credits.

The car is a towing outcome, not an additional Fire Engine requirement.

### Burning truck — HGV variation

Verified variation:

- 2 Fire Stations;
- 1 HGV Recovery Extension;
- 2 Fire Engines;
- exactly 1 truck to recover;
- 1,280 average credits.

This is the foundation HGV contract. The HGV extension does not replace Fire suppression, and the truck outcome does not create another Fire resource row.

## Collision recovery variations

### Multi vehicle RTC

Verified response:

- 2 Fire Engines;
- 2 Police Cars;
- 1 Traffic Car with 50% probability and `only_when_available` condition;
- 1 Operational Team Leader with 50% probability;
- 3–7 patients;
- 50% transport probability;
- 2–4 cars to recover;
- 1 Recovery Centre.

This mission combines emergency, medical, conditional, probabilistic and towing fields. Preserve every semantic separately.

### Non-Injury RTC with Police Car — Recovery Required

Verified response:

- 2 Police Cars;
- 1 Traffic Car;
- 1 Police Sergeant required;
- 3 Police Sergeants available before generation;
- exactly 1 car to recover;
- 1 Recovery Centre;
- 4,800 average credits.

The Police Sergeant available/required fields are personnel semantics, not vehicle crew counts.

### Multiple vehicle RTC — Major Incident recovery variation

Current verified directory evidence publishes:

- 1 Recovery Centre;
- the major-incident infrastructure preconditions;
- 10,300 average credits.

Response and towing outcomes remain unavailable in the current record. Do not copy the two-to-four car range from the ordinary Multi vehicle RTC into this major variation.

## Conditional and probabilistic semantics

### Traffic Car

The Multi vehicle RTC recovery overlay publishes one Traffic Car with:

- 50% probability;
- `only_when_available` condition.

This is neither a guaranteed resource nor a mere recommendation. Preserve both the probability and the condition.

### Operational Team Leader

The same mission publishes one Operational Team Leader with 50% probability. Do not dispatch the role as guaranteed on every variant or omit it entirely.

## Five commissioning gates

| Gate | Question | Recommended pass condition |
|---|---|---|
| Car recovery | Can one-car and multi-car outcomes be cleared without exhausting the network? | At least one protected regional recovery route remains |
| HGV | Can the dedicated truck workload be supported? | HGV extension activation follows verified truck-recovery readiness |
| Emergency response | Can Fire, Police, medical and personnel requirements operate independently? | Towing capacity is not counted as emergency response |
| Geography | Can assets be reached, cleared and the recovery route restored? | Road-corridor and return time are operationally practical |
| Evidence | Does the mission publish the towing range? | Unknown outcomes remain unknown rather than copied from another variant |

## Recommended capacity templates

These are strategic templates, not official Recovery Centre capacities.

### Foundation recovery network

| Capability | Recommended posture |
|---|---|
| Recovery infrastructure | 1 Recovery Centre only after one-car missions can be cleared reliably |
| Protected reserve | One useful car-recovery route outside a normal dispatch |
| Cross-service | Fire and Police response remains available for recovery-enabled variants |
| HGV | Delay extension activation until truck recovery is operationally supported |

### Developing recovery network

| Capability | Recommended posture |
|---|---|
| Car recovery | Enough regional capacity for the verified 2–4 car Multi vehicle RTC range |
| Geography | Separate recovery routes across main road corridors |
| Police/medical | Traffic, personnel and patient fields included in recovery variants |
| HGV | One complete truck-recovery route with geographic reserve |
| Concurrency | Dedicated mission plus one recovery-enabled emergency incident tested together |

### Established recovery network

| Capability | Recommended posture |
|---|---|
| Car recovery | Independently dispatchable routes across major regions |
| HGV recovery | Multiple geographic routes when one extension area becomes a travel bottleneck |
| Major incidents | Recovery reserve protected while Fire, Police and Ambulance assets remain committed |
| Evidence handling | Unknown major-variation towing outcomes remain excluded from capacity calculations |
| Recovery | Towing and return-to-position time included before declaring readiness |

## Transparent concurrency examples

### Dedicated car mission plus Multi vehicle RTC

Calculated published recovery workload:

- 1 car from the dedicated mission;
- 2–4 cars from the RTC;
- combined range of **3–5 cars**.

Emergency pressure still includes Fire, Police, conditional Traffic Car, probabilistic Operational Team Leader and patients.

### Burning car plus Burning truck

Calculated published recovery workload:

- 1 car;
- 1 truck;
- two separate asset classes and infrastructure paths.

This does not prove the same market vehicle can recover both classes.

## Geographic doctrine

### Urban road network

- Place Recovery Centres near repeated RTC and obstruction demand.
- Include congestion, tow destination and return time.
- Keep Police and Fire reserve outside recovery-enabled incidents.
- Duplicate capacity when one recovery route becomes the persistent blocker.

### Motorway and trunk-road network

- Align car and HGV recovery with major corridors.
- Place HGV capability by travel time rather than extension count alone.
- Preserve Roads Policing and scene-control support.
- Test simultaneous car and truck outcomes.

### Rural network

- Keep regional recovery capacity local enough to avoid long closures.
- Use actual road routes rather than map distance.
- Protect one ordinary emergency-response route while recovery is travelling.
- Treat alliance support as contingency.

## Recovery-to-readiness

After towing begins or an incident clears:

1. identify every recovery route still travelling, towing or returning;
2. restore one regional car-recovery route first;
3. restore HGV capability in the relevant corridor;
4. confirm Fire, Police, Ambulance and personnel reserve has recovered;
5. review patients and custody activity still active;
6. rerun the selected concurrent recovery scenario;
7. correct repeated geographic or asset-class shortages before more infrastructure activation.

Mission completion is not proof that towing and regional availability are restored.

## Common failures

| Failure | Operational symptom | Correction |
|---|---|---|
| Creating a fictional Recovery Vehicle requirement | Data and dispatch advice claim a row the source does not publish | Keep towing under `recovery.assets` |
| Treating infrastructure as a dispatched vehicle | Recovery Centre or extension appears in an emergency response | Preserve it as a precondition/capability |
| Copying outcomes between variants | A major variation receives unsupported towing numbers | Keep unavailable outcomes unknown |
| Treating conditional Traffic Cars as guaranteed | Roads resources are over-dispatched | Preserve probability and condition |
| Ignoring patient and personnel fields | Recovery planning misses medical and command pressure | Audit the complete mission record |
| Treating car and truck recovery as identical | HGV readiness is overstated | Preserve asset class and extension semantics |
| Counting only arrival time | Recovery seems available while still towing/returning | Include the complete clearing cycle |
| Expanding while depleted | New recovery missions generate before reserve returns | Restore readiness before more centres/extensions |

## Operational readiness checklist

- [ ] Recovery Centre and HGV Recovery Extension are treated as infrastructure;
- [ ] towing outcomes remain under `recovery.assets`;
- [ ] no fictional emergency recovery-resource row has been created;
- [ ] car and truck asset classes remain separate;
- [ ] published minimum/maximum ranges are preserved;
- [ ] unavailable outcomes remain unknown;
- [ ] conditional and probabilistic Traffic Car/OTL fields are retained;
- [ ] Fire, Police, Ambulance, patient and personnel dependencies are included;
- [ ] road geography and full towing-return time are tested;
- [ ] concurrent car/HGV workloads have been modelled;
- [ ] unpublished economics and capacities remain unknown rather than zero.

## Stage 37H completion

The Recovery and HGV Recovery programme now covers:

- Recovery Centre and HGV extension progression;
- dedicated and recovery-enabled missions;
- car and truck towing outcomes;
- separation of recovery workload from emergency response;
- conditional and probabilistic semantics;
- scalable regional templates;
- geography, concurrency and recovery-to-readiness.

The next service programme is **Stage 37I — Railway Police and Railway Fire operational progression**.
