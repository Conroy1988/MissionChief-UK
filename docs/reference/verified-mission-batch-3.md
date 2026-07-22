# Verified Mission Batch 3 — Ambulance and Police

Stage 14 expands the production dataset beyond Fire and Rescue. This batch introduces verified Ambulance patient mechanics, alternative vehicle requirements and a detailed Police public-order mission.

!!! success "Verification boundary"
    Verification applies only to populated fields. A blank requirement is not a claim that no vehicle is required; it means the available primary source did not expose that value during this verification pass.

## Batch summary

| ID | Mission | Service | Confirmed resources | Average credits |
|---:|---|---|---|---:|
| `522` | Community Engagement (Ambulance) | Ambulance | Not published in this record | 6,000 |
| `693` | HCP Home Visit | Ambulance | 1 RRV **or** Specialist Paramedic RRV | 500 |
| `762` | Palliative Care Visit | Ambulance | 1 RRV **or** Specialist Paramedic RRV | 500 |
| `622` | Group Throwing Flares | Police | 4 Police Cars | 2,500 |

## Community Engagement (Ambulance)

**Canonical ID:** `522`  
**Service:** Ambulance  
**POIs:** School or Mall  
**Precondition:** 1 Rescue Station  
**Average reward:** 6,000 credits

The official UK mission directory confirms the name, POIs, station precondition and average reward. The individual mission page was not available during the pass, so no vehicle requirement has been inferred.

[Official UK mission record](https://www.missionchief.co.uk/einsaetze/522)

## HCP Home Visit

**Canonical ID:** `693`  
**Service:** Ambulance  
**Preconditions:** 1 Rescue Station and 1 GP Surgery  
**Average reward:** 500 credits  
**Vehicle requirement:** 1 Rapid Response Vehicle or Specialist Paramedic RRV

### Patient behaviour

- Minimum patients: 1
- Maximum patients: 1
- Transport probability: 30%
- Specialisation: General Internal
- Possible code: C-4

[Official UK mission record](https://www.missionchief.co.uk/einsaetze/693)

## Palliative Care Visit

**Canonical ID:** `762`  
**Service:** Ambulance  
**Preconditions:** 1 Rescue Station and 1 GP Surgery  
**Average reward:** 500 credits  
**Vehicle requirement:** 1 Rapid Response Vehicle or Specialist Paramedic RRV

### Patient behaviour

- Minimum patients: 1
- Maximum patients: 1
- Transport probability: 5%
- Critical-care probability: 5%
- Specialisation: General Internal
- Possible codes: C-3 or C-4

[Official UK mission record](https://www.missionchief.co.uk/einsaetze/762)

## Group Throwing Flares

**Canonical ID:** `622`  
**Service:** Police  
**POI:** Stadium  
**Preconditions:** 2 Police Stations and 1 Police & Public Order Extension  
**Average reward:** 2,500 credits  
**Guaranteed requirement:** 4 Police Cars

### Personnel

Available before the mission can generate:

- 12 Level 2 Public Order Officers
- 2 Police Sergeants

Required at the incident:

- 6 Level 2 Public Order Officers
- 1 Police Sergeant

**Maximum prisoners:** 2

[Official UK mission record](https://police.missionchief.co.uk/einsaetze/622)

## Alternative resource semantics

The Ambulance records use an `alternatives` requirement group:

```json
{
  "resources": [
    "rapid_response_vehicle",
    "specialist_paramedic_rrv"
  ],
  "quantity": 1
}
```

This means one qualifying vehicle is required. It must not be interpreted as one of each vehicle.

## Machine-readable records

```text
data/uk/missions/
├── community-engagement-ambulance.json
├── group-throwing-flares.json
├── hcp-home-visit.json
└── palliative-care-visit.json
```

The records are validated against the mission schema, checked for valid patient ranges and checked against canonical vehicle IDs.
