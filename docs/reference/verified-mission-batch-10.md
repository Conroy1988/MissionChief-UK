# Verified Mission Batch 10 — Railway Response

Stage 21 introduces Railway Police and Railway fire response infrastructure, specialist rail resources and five fully structured railway missions.

!!! success "Evidence boundary"
    Values below were checked against official MissionChief UK mission pages on 22 July 2026. A verified record applies only to populated fields.

## Batch summary

| Dataset ID | Mission | Patients | Average credits |
|---|---|---:|---:|
| `807` | Evacuation of Stranded Passenger Train | 5–50 | 13,600 |
| `372-railway-full-overlay` | Passenger Train Derailment | 30–150 | 20,200 |
| `134-railway-overlay` | Goods Train Fire | — | 3,000 |
| `291-railway-police-overlay` | Person under train | 1 | 7,800 |
| `792-railway-police-overlay` | Mass influx of sick people - railway station | 35–70 | 8,100 |

## Evacuation of Stranded Passenger Train

This mission establishes Road Rail Unit, EIU, Breathing Apparatus Support Unit, Railway Police Officer and Mobile Operations Manager requirements in one complete response table.

Key generation requirements:

- 15 Fire Stations;
- 12 Rescue Stations;
- 9 Police Stations;
- 1 HART Base;
- 2 Search and Rescue HQs;
- 1 Railway fire response;
- 1 Railway Police.

[Official mission page](https://www.missionchief.co.uk/einsaetze/807)

## Passenger Train Derailment

The fully enhanced variant preserves HART, Mass Casualty, Railway fire response and Railway Police as one explicit overlay. It verifies 30–150 patients, 30% transport probability and 50% critical-care probability.

[Official mission page](https://police.missionchief.co.uk/einsaetze/372?additive_overlays=abc)

## Goods Train Fire

The railway overlay verifies one Road Rail Unit, one EIU, one Breathing Apparatus Support Unit, one Water Carrier and an ICCU/Ambulance Control Unit alternative.

[Official mission page](https://police.missionchief.co.uk/einsaetze/134?additive_overlays=b)

## Person under train

The Railway Police overlay verifies one critical patient and the official firefighter range of 14–42. The range is stored under `personnel.ranges`.

[Official mission page](https://police.missionchief.co.uk/einsaetze/291?additive_overlays=a)

## Mass influx of sick people - railway station

The Railway Police overlay records a 10% Breathing Apparatus Support Unit probability, 35–70 patients, 25% transport probability and 20% critical-care probability.

The observed page displayed a temporary x2 event multiplier. The canonical average remains 8,100 credits.

[Official mission page](https://police.missionchief.co.uk/einsaetze/792?additive_overlays=a)

## Machine-readable files

```text
data/uk/missions/
├── evacuation-of-stranded-passenger-train.json
├── passenger-train-derailment-railway-overlay.json
├── goods-train-fire-railway-overlay.json
├── person-under-train-railway-overlay.json
└── mass-influx-sick-railway-station-overlay.json
```
