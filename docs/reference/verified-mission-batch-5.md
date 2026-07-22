# Verified Mission Batch 5 — Mountain Rescue

Stage 16 introduces the first verified Mountain Rescue and specialist land-search records.

The batch models alternative 4x4 resources, technical-rescue support, search coordination, search dogs, probability-based personnel and additive HART or helicopter variants.

!!! success "Verification boundary"
    Every populated field is supported by an official UK mission page or the official mission directory. Missing values are intentional. Overlay requirements are never merged into the corresponding base mission.

## Batch summary

| Dataset ID | Official mission ID | Mission | Confirmed response | Average credits |
|---|---:|---|---|---:|
| `143` | `143` | Stuck Climber | 1 MR 4x4 or SAR 4x4; 1 Fire engine; 1 Rescue Support Vehicle; 50% Aerial Appliance | 650 |
| `756` | `756` | Overdue Hikers | 2 MR 4x4 or SAR 4x4; 1 Control Van; 1 Search Dog Unit | 6,400 |
| `753-helicopter-overlay` | `753` | Belay Failure Whilst Abseiling | 2 MR 4x4 or SAR 4x4; 1 Coastguard Rescue Helicopter | 6,000 |
| `755-hart-overlay` | `755` | Fall Whilst Fell Running | 1 MR 4x4 or SAR 4x4; 1 ATV Carrier | 2,600 |
| `760` | `760` | Amateur Explorers Trapped in Abandoned Mineshaft | 4 qualifying 4x4s plus command, dog, Fire, Police and Ambulance support | 25,400 |

## Stuck Climber

**Canonical ID:** `143`  
**Preconditions:** 4 Fire Stations, 1 Rescue Station and 2 Mountain Rescue Stations  
**Custom spawn area:** Yes

### Vehicle requirements

- 1 Mountain Rescue 4x4 **or** SAR 4x4;
- 1 Fire engine;
- 1 Rescue Support Vehicle;
- 50% probability of 1 Aerial Appliance Truck.

### Personnel and patients

- 75% probability of 1 Operational Team Leader;
- exactly 1 patient;
- 30% transport probability;
- General Internal specialisation;
- possible codes C-2 and C-3.

[Official UK mission record](https://www.missionchief.co.uk/einsaetze/143)

## Overdue Hikers

**Canonical ID:** `756`  
**Preconditions:** 3 Rescue Stations, 1 Police Station and 3 Mountain Rescue Stations  
**Custom spawn area:** Yes

### Vehicle requirements

- 2 Mountain Rescue 4x4s or SAR 4x4s in total;
- 1 Control Van;
- 1 Search Dog Unit.

### Patients

- maximum 3 patients;
- 25% transport probability;
- 0% critical-care probability;
- General Internal specialisation;
- possible codes C-2, C-3 and C-4.

The official page displayed a temporary `x2` marker. The dataset retains 6,400 as the base average and stores the multiplier only as an observation.

[Official UK mission record](https://police.missionchief.co.uk/einsaetze/756)

## Belay Failure Whilst Abseiling — helicopter overlay

**Dataset ID:** `753-helicopter-overlay`  
**Official mission ID:** `753`  
**Variant:** Additive helicopter overlay  
**POIs:** Ravine or Cliff  
**Preconditions:** 1 Rescue Station, 2 Mountain Rescue Stations and 1 Helicopter Hangar

### Requirements

- 2 Mountain Rescue 4x4s or SAR 4x4s in total;
- 1 Coastguard Rescue Helicopter;
- maximum 2 patients;
- 80% transport probability;
- 50% critical-care probability;
- Traumatology specialisation;
- possible codes C-1 and C-2.

The official mission directory lists the base version at 4,000 average credits. This record represents only the 6,000-credit helicopter overlay and carries the official mission ID through the structured `variant` field.

[Official UK overlay record](https://police.missionchief.co.uk/einsaetze/753?additive_overlays=a)

## Fall Whilst Fell Running — HART overlay

**Dataset ID:** `755-hart-overlay`  
**Official mission ID:** `755`  
**Variant:** Additive HART overlay  
**Preconditions:** 1 Rescue Station, 1 HART Base and 1 Mountain Rescue Station

### Requirements

- 1 Mountain Rescue 4x4 or SAR 4x4;
- 1 ATV Carrier;
- exactly 1 patient;
- 75% transport probability;
- 10% critical-care probability;
- Traumatology specialisation;
- possible codes C-2 and C-3.

The official mission directory lists the base version at 1,600 average credits. This record represents only the 2,600-credit HART overlay.

[Official UK overlay record](https://police.missionchief.co.uk/einsaetze/755?additive_overlays=a)

## Amateur Explorers Trapped in Abandoned Mineshaft

**Canonical ID:** `760`  
**POI:** Mineshaft  
**Preconditions:** 4 Fire Stations, 3 Rescue Stations, 3 Police Stations, 2 HART Bases and 5 Mountain Rescue Stations  
**Custom spawn area:** Yes

### Vehicle requirements

- 4 Mountain Rescue 4x4s or SAR 4x4s in total;
- 1 Control Van;
- 1 Search Dog Unit;
- 2 Fire engines;
- 2 Rescue Support Vehicles;
- 2 Police Cars;
- 2 PRVs;
- 2 SRVs;
- 1 Welfare Vehicle.

### Personnel available

- 2 Search Advisors;
- 2 Police Sergeants;
- 20 Cave Rescue Specialists.

### Personnel required

- 1 Search Advisor;
- 1 Police Sergeant;
- 10 Cave Rescue Specialists;
- 3 Fire Officers;
- 1 Ambulance Officer;
- 1 Operational Team Leader.

### Patients

- minimum 2 and maximum 6;
- 75% transport probability;
- 25% critical-care probability;
- General Internal specialisation;
- possible codes C-1, C-2, C-3 and C-4.

The official page displayed a temporary `x2` marker. The dataset stores 25,400 as the base average.

[Official UK mission record](https://www.missionchief.co.uk/einsaetze/760)

## Variant semantics

Overlay records use string dataset IDs so they do not collide with the numeric base mission ID:

```json
{
  "id": "755-hart-overlay",
  "variant": {
    "source_mission_id": 755,
    "kind": "additive-overlay",
    "key": "hart-atv-carrier"
  }
}
```

This preserves the official relationship while preventing the overlay requirement from contaminating the base mission.

## Machine-readable records

```text
data/uk/missions/
├── amateur-explorers-trapped-abandoned-mineshaft.json
├── belay-failure-abseiling-helicopter-overlay.json
├── fall-whilst-fell-running-hart-overlay.json
├── overdue-hikers.json
└── stuck-climber.json
```
