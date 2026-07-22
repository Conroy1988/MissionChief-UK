# Bomb Disposal and EOD

Bomb Disposal missions introduce a specialist progression chain built around Bomb Disposal HQs, marine capability, multi-service preconditions and active equipment.

## Current verified scope

Stage 18 verifies:

- Bomb Disposal HQ mission preconditions;
- Bomb Disposal Marine Unit Extension preconditions;
- land, coastal, harbour and building-site mission progression;
- Fire, Rescue, Police, Coastguard and HART dependencies;
- active-Drone mission-generation preconditions;
- official POIs and base average rewards.

!!! warning "Response-table boundary"
    The official mission directory was available during verification, but the individual mission pages were not consistently cacheable. Vehicle and personnel requirements are therefore left unpublished rather than inferred.

## Infrastructure

### Bomb Disposal HQ

The Bomb Disposal HQ is a verified building precondition. The first controlled batch ranges from one HQ for the countryside and quiet-beach missions to three HQs for harbour and large building-site incidents.

### Bomb Disposal Marine Unit Extension

The marine extension is required by coastal and harbour ordnance missions. One extension is confirmed for Quiet Beach; two are confirmed for Harbour.

The guide does not yet publish construction costs, build duration, capacity or associated vehicles.

## Active Drone semantics

An active Drone in the mission directory is a **precondition**. It does not automatically prove that a Drone must be dispatched.

This distinction is already used by Search and Rescue HQ missions and now also applies to higher-complexity Bomb Disposal missions.

## First verified mission set

| ID | Mission | Bomb Disposal infrastructure | Average credits |
|---:|---|---|---:|
| `829` | Unexploded WW2 Ordnance in Countryside | 1 HQ | 4,500 |
| `830` | Unexploded WW2 Ordnance on Quiet Beach | 1 HQ, 1 Marine Unit Extension | 5,500 |
| `832` | Unexploded WW2 Ordnance in Harbour | 3 HQs, 2 Marine Unit Extensions | 15,000 |
| `839` | Unexploded WW2 Bomb Located at Building Site (Large) | 3 HQs | 11,500 |

## Planning implications

The verified progression demonstrates that Bomb Disposal cannot be planned in isolation:

- coastal incidents require Coastguard infrastructure;
- larger incidents add HART and active-Drone preconditions;
- Police Station requirements rise from 10 to 20;
- Rescue Station requirements rise from 6 to 15;
- marine missions require dedicated extensions.

## Still awaiting direct verification

The following remain unpublished until reproduced from the current interfaces:

1. EOD vehicle names and quantities;
2. Bomb Disposal personnel roles and staffing;
3. marine-unit vehicles and carrier relationships;
4. HQ and extension prices, build times and capacities;
5. training requirements;
6. patient or prisoner mechanics where applicable.
