# Verified Mission Batch 9 — Recovery Operations

Stage 20 introduces dedicated Recovery missions and recovery-enabled variants with structured towing data.

!!! success "Evidence boundary"
    Values below were checked against official MissionChief UK pages and the official mission directory on 22 July 2026. A verified record applies only to populated fields.

## Batch summary

| Dataset ID | Mission | Recovery dependency | Towing | Average credits |
|---|---|---|---|---:|
| `784` | Abandoned Car Obstructing Road | 1 Recovery Centre | Unavailable | 400 |
| `785` | Broken Down Car Obstructing Road | 1 Recovery Centre | Unavailable | 400 |
| `2-recovery-overlay` | Burning car | 1 Recovery Centre | 1 car | 670 |
| `13-hgv-recovery-overlay` | Burning truck | 1 HGV Recovery Extension | 1 truck | 1,280 |
| `129-recovery-overlay` | Multi vehicle RTC | 1 Recovery Centre | 2–4 cars | 1,900 |
| `782-recovery-overlay` | Non-Injury RTC with Police Car (Recovery Required) | 1 Recovery Centre | 1 car | 4,800 |

## Dedicated Recovery missions

### `784` — Abandoned Car Obstructing Road

Verified directory data:

- one Recovery Centre;
- Recovery Vehicle Missions classification;
- 400 average credits.

The individual response page was unavailable, so the record does not claim a towing quantity or dispatch-level resource.

### `785` — Broken Down Car Obstructing Road

Verified directory data:

- one Recovery Centre;
- Recovery Vehicle Missions classification;
- 400 average credits.

The same response-page evidence boundary applies.

## `2-recovery-overlay` — Burning car

The Recovery Centre variation requires:

- one Fire Station;
- one Recovery Centre;
- one Fire engine;
- exactly one car to tow;
- 670 average credits.

[Official mission page](https://police.missionchief.co.uk/einsaetze/2?additive_overlays=a)

## `13-hgv-recovery-overlay` — Burning truck

The HGV variation requires:

- two Fire Stations;
- one HGV Recovery Extension;
- two Fire engines;
- exactly one truck to tow;
- 1,280 average credits.

[Official mission page](https://www.missionchief.co.uk/einsaetze/13?additive_overlays=a)

## `129-recovery-overlay` — Multi vehicle RTC

Preconditions:

- three Fire Stations;
- ten Rescue Stations;
- one Police Station;
- one Recovery Centre.

Response and outcomes:

- two Fire engines;
- two Police Cars;
- one Traffic Car with 50% probability, only when available;
- one Operational Team Leader with 50% probability;
- three to seven patients;
- 50% transport probability;
- two to four cars to tow;
- 1,900 average credits.

[Official mission page](https://police.missionchief.co.uk/einsaetze/129?additive_overlays=a)

## `782-recovery-overlay` — Non-Injury RTC with Police Car

The documented enhanced variation verifies:

- three Police Stations;
- one Recovery Centre;
- three Police Sergeants available;
- two Police Cars;
- one Traffic Car;
- one Police Sergeant required;
- exactly one car to tow;
- 4,800 average credits.

[Official mission page](https://www.missionchief.co.uk/einsaetze/782?additive_overlays=a)

## Data interpretation

Towing quantities are stored under `recovery.assets`, not under emergency-vehicle requirements. Recovery infrastructure controls mission generation, while towing describes the post-response asset-clearing workload.

## Machine-readable files

```text
data/uk/missions/
├── abandoned-car-obstructing-road.json
├── broken-down-car-obstructing-road.json
├── burning-car-recovery-overlay.json
├── burning-truck-hgv-recovery-overlay.json
├── multi-vehicle-rtc-recovery-overlay.json
└── non-injury-rtc-police-car-recovery-overlay.json
```
