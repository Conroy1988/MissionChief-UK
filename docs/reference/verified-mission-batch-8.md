# Verified Mission Batch 8 — Airfield Operations

Stage 19 introduces the first fully populated airport and aircraft-incident records.

!!! success "Evidence boundary"
    Values below were checked against the official MissionChief UK mission pages on 22 July 2026. Missing prices, training and staffing attributes are intentional.

## Batch summary

| ID | Mission | POI | Average credits |
|---:|---|---|---:|
| `593` | Bird Strike - Code B | Medium/Large Airport (Runway) | 6,000 |
| `587` | Aircraft Accident - Code C | Medium/Large Airport (Runway) | 16,000 |
| `588` | Aircraft Accident - Code F | Large Airport (Runway) | 24,000 |

## `593` — Bird Strike - Code B

Preconditions:

- 7 Fire Stations;
- 6 Rescue Stations;
- 2 HART Bases;
- 1 Aviation firefighting Extension.

Response:

- 4 Fire Engines or RIVs;
- 3 Water Carriers;
- 2 RIVs or Major Foam Tenders;
- 1 Operational Team Leader;
- 2 PRVs;
- 1 SRV;
- 1 Welfare Vehicle.

The two alternative groups are independent.

[Official mission page](https://www.missionchief.co.uk/einsaetze/593)

## `587` — Aircraft Accident - Code C

Preconditions:

- 11 Fire Stations;
- 11 Rescue Stations;
- 10 Police Stations;
- 3 HART Bases;
- 2 Aviation firefighting Extensions;
- 1 Airfield Operations Extension;
- 1 Mass Casualty Extension.

Key response groups:

- 7 Fire Engines or Major Foam Tenders;
- 6 Fire Officers or Airfield Firefighting Command Vehicles;
- 1 HazMat Unit or CBRN Vehicle;
- 1 ICCU, Ambulance Control Unit or Airfield Firefighting Command Vehicle.

Dedicated resources include two Rescue Support Vehicles, one Water Carrier, one Major Foam Tender, one Airfield Firefighting Command Vehicle, two Airfield Operations Vehicles, four PRVs, four SRVs, one Welfare Vehicle, one Mass Casualty Equipment unit and eight Police Cars.

Four Traffic Cars are conditional and apply only when available.

Patient data:

- 75–175 patients;
- 30% transport probability;
- 80% critical-care probability;
- General Internal;
- codes C-2 and C-3.

[Official mission page](https://www.missionchief.co.uk/einsaetze/587)

## `588` — Aircraft Accident - Code F

Preconditions:

- 15 Fire Stations;
- 15 Rescue Stations;
- 10 Police Stations;
- 3 HART Bases;
- 3 Aviation firefighting Extensions;
- 2 Airfield Operations Extensions;
- 1 Mass Casualty Extension.

Key response groups:

- 10 Fire Engines or Major Foam Tenders;
- 6 Fire Officers or Airfield Firefighting Command Vehicles;
- 2 HazMat Units or CBRN Vehicles;
- 1 ICCU, Ambulance Control Unit or Airfield Firefighting Command Vehicle;
- 1 Aerial Appliance Truck or Rescue Stairs.

Dedicated resources include two Rescue Support Vehicles, one Water Carrier, five Major Foam Tenders, one Airfield Firefighting Command Vehicle, four Airfield Operations Vehicles, four PRVs, four SRVs, two Welfare Vehicles, one Mass Casualty Equipment unit and twelve Police Cars.

Six Traffic Cars are conditional and apply only when available.

Patient data:

- 150–250 patients;
- 15% transport probability;
- 80% critical-care probability;
- General Internal;
- codes C-2 and C-3.

[Official mission page](https://www.missionchief.co.uk/einsaetze/588)

## Overlapping alternatives

Airfield Firefighting Command Vehicles appear in dedicated and alternative requirements. The dataset preserves every official row separately. It does not calculate a minimum unique-vehicle total until dispatch-allocation behaviour has been reproduced.

## Machine-readable files

```text
data/uk/missions/
├── aircraft-accident-code-c.json
├── aircraft-accident-code-f.json
└── bird-strike-code-b.json
```
