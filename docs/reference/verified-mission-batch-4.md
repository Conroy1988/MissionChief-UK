# Verified Mission Batch 4 — Coastguard and Lifeboat

Stage 15 introduces the first production maritime dataset for MissionChief UK. It covers Coastguard mud rescue, inland rescue-boat support, ocean-only lifeboat missions and helicopter-assisted medivac.

!!! success "Verification boundary"
    Verification applies only to populated fields. Expanded vehicle names are stored as aliases where the official mission requirement uses an abbreviation such as CRV, ILB or ALB.

## Batch summary

| ID | Mission | Mission group | Confirmed resources | Average credits |
|---:|---|---|---|---:|
| `546` | Mud Rescue | Coastguard | 2 Coastguard Mud Rescue Units; 1 Mud Decontamination Unit | 6,000 |
| `567` | Rescue Boat Assist Coastguard Mud Rescue | Coastal Rescue | 2 Coastguard Mud Rescue Units; 1 Mud Decontamination Unit; 1 Inland Rescue Boat (Trailer) | 8,000 |
| `569` | Rescue Boat Assist Coastguard, Persons Cut off by Tide | Coastguard | 2 CRVs; 1 Inland Rescue Boat (Trailer) | 6,500 |
| `561` | Broken Down Boat | Ocean Rescue | 1 ILB **or** ALB | 6,000 |
| `562` | Medivac from vessel | Ocean Rescue | 1 ILB **or** ALB; 50% Coastguard Rescue Helicopter | 8,000 |

## Mud Rescue

**Canonical ID:** `546`  
**POIs:** Estuary, Harbour, Beach or Marina  
**Preconditions:** 3 Rescue Stations, 4 Coastguard Rescue Stations and 2 Mud Decontamination Extensions

### Resources and personnel

- 2 Coastguard Mud Rescue Units
- 1 Mud Decontamination Unit
- 30 Mud Rescue Operators available
- 15 Mud Rescue Operators required at the incident

### Patients

- Minimum: 1
- Maximum: 3
- Transport probability: 70%
- Codes: C-1, C-2 or C-3
- Specialisation: General Internal

[Official UK mission record](https://www.missionchief.co.uk/einsaetze/546)

## Rescue Boat Assist Coastguard Mud Rescue

**Canonical ID:** `567`  
**Mission group:** Coastal Rescue Missions  
**POIs:** Estuary, Harbour, Beach or Marina

This mission adds one Lifeboat Station and one Inland Rescue Boat (Trailer) to the verified Mud Rescue requirement set.

### Patients

- Minimum: 1
- Maximum: 3
- Transport probability: 80%
- Codes: C-1 or C-2

[Official UK mission record](https://www.missionchief.co.uk/einsaetze/567)

## Rescue Boat Assist Coastguard, Persons Cut off by Tide

**Canonical ID:** `569`  
**Preconditions:** 5 Rescue Stations, 3 Coastguard Rescue Stations and 1 Lifeboat Station

### Resources

- 2 CRVs
- 1 Inland Rescue Boat (Trailer)

### Patients

- Minimum: 1
- Maximum: 10
- Transport probability: 20%
- Codes: C-2 or C-3

[Official UK mission record](https://www.missionchief.co.uk/einsaetze/569)

## Broken Down Boat

**Canonical ID:** `561`  
**Mission group:** Ocean Rescue Missions  
**Precondition:** 1 Lifeboat Station  
**Vehicle restriction:** Ocean

The mission requires one qualifying lifeboat:

```json
{
  "resources": [
    "inshore_lifeboat",
    "all_weather_lifeboat"
  ],
  "quantity": 1
}
```

This is an alternative requirement: one ILB or one ALB, not one of each.

The official mission page displayed a temporary `x2` marker during this verification pass. The structured record retains the 6,000-credit base average shown in the official mission directory.

[Official UK mission record](https://www.missionchief.co.uk/einsaetze/561)

## Medivac from vessel

**Canonical ID:** `562`  
**Mission group:** Ocean Rescue Missions  
**Preconditions:** 3 Rescue Stations, 1 Lifeboat Station and 1 Helicopter Hangar  
**Vehicle restriction:** Ocean

### Resources

- 1 ILB or ALB
- 50% probability of requiring 1 Coastguard Rescue Helicopter

### Patients

- Exactly 1 patient
- Transport probability: 100%
- Critical-care probability: 40%
- Codes: C-1, C-2 or C-3
- Hand-off available to a Lifeboat Station

[Official UK mission record](https://www.missionchief.co.uk/einsaetze/562)

## Maritime modelling rules

Stage 15 establishes the following data rules:

1. official abbreviations remain canonical when that is how the mission page names the resource;
2. expanded names are searchable aliases rather than unsupported replacements;
3. an ILB-or-ALB requirement is represented as an alternative group;
4. trailer resources are explicitly distinguished from independently deployed boats;
5. ocean restrictions, custom spawn areas and hand-off destinations are stored separately from vehicle requirements;
6. temporary reward multipliers are not treated as base rewards.

## Machine-readable records

```text
data/uk/missions/
├── broken-down-boat.json
├── medivac-from-vessel.json
├── mud-rescue.json
├── rescue-boat-assist-coastguard-mud-rescue.json
└── rescue-boat-assist-coastguard-persons-cut-off-by-tide.json
```

All mission resources are checked against canonical vehicle records during validation.
