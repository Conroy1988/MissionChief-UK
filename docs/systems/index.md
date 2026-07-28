# Game Systems

Game systems connect the canonical mission, resource, infrastructure and personnel records. Use this section when a problem affects several services rather than one fleet.

## System command map

| System | Operational question | Primary guide |
|---|---|---|
| Mission generation | Why can this incident appear? | [Missions and Dispatching](missions-and-dispatching.md) |
| Requirement semantics | Is a resource guaranteed, alternative, conditional or probabilistic? | [Missions and Dispatching](missions-and-dispatching.md) |
| Buildings and extensions | Does infrastructure generate missions or provide response capability? | [Buildings and Extensions](buildings-and-extensions.md) |
| Personnel and qualifications | Is a vehicle or role operationally staffed? | [Training and Personnel](../reference/training-and-personnel.md) |
| Patients and transport | Will treatment, transport and destination turnaround exhaust cover? | [Ambulance and HART](../services/ambulance.md) |
| Prisoners and custody | Can scene response and custody transport remain independent? | [Police and Public Safety](../services/police.md) |
| Towing, trailers and carriers | Is the complete logistics chain deployable? | [Vehicle Catalogue](../reference/vehicle-catalogue.md) |
| Geography | Will resources reach incidents, access points and destinations? | [Station Placement](../strategy/station-placement.md) |
| Cross-service readiness | Can all hard partner services operate concurrently? | [Account Progression](../strategy/account-progression.md) |
| Alliance contingency | Is external support governed and sustainable? | [Alliance Operations](../alliances/index.md) |

## Evidence model

The production platform keeps these layers separate:

```text
Generation preconditions
        ↓
Mission requirement semantics
        ↓
Deployable resource and personnel contracts
        ↓
Patient / prisoner / recovery outcomes
        ↓
Geographic and destination cycle
        ↓
Return to operational reserve
```

A failure can occur at any layer. Buying another vehicle will not correct a missing extension, unavailable qualified role, incomplete towing chain, distant destination or consumed reserve.

## Canonical semantics

### Unknown is not zero

Missing cost, capacity, staffing, course or unlock data remains unknown. It must not be treated as free, unlimited or unnecessary.

### Generation is not dispatch

A building, extension, active equipment item or available-personnel threshold can permit mission generation without becoming a dispatched resource row.

### Ownership is not readiness

A resource should count as operational only when it is correctly located, staffed, trained and able to fulfil its complete logistics chain.

### Outcomes are not vehicle requirements

Patient, prisoner and recovery fields describe work produced by an incident. They are not automatically converted into fictional vehicle quantities.

## Operational tools

- [Mission Lookup](../tools/mission-lookup.md) — inspect one current canonical mission;
- [Account Readiness Planner](../tools/account-readiness.md) — compare several incidents with user-entered inventory and reserve;
- [Resource Comparison](../tools/resource-comparison.md) — compare populated canonical resource or qualification fields;
- [Concurrent Fleet Planner](../tools/fleet-planner.md) — multiply published guaranteed quantities;
- [Query Catalogue](../tools/query-catalogue.md) — retrieve evidence across all canonical collections.

## Service-specific application

The [Emergency Services index](../services/index.md) applies these systems to Fire, Ambulance/HART, Police, Coastguard/Lifeboat, Mountain Rescue, SAR HQ, Bomb Disposal, Airfield, Recovery and Railway operations.
