# Verified Mission Records

This catalogue is the first production population of the MissionChief UK structured mission dataset.

Every record on this page is backed by the official UK game mission reference and has a matching machine-readable JSON record under `data/uk/missions/`.

!!! success "Verification boundary"
    Verification applies only to the values explicitly recorded. It does not imply that every hidden mechanic, event modifier, expansion path or mission variation has been independently reproduced.

## Initial fire mission set

| ID | Mission | Required resources | Unlock requirement | Average credits | Verification |
|---:|---|---|---|---:|---|
| `0` | Bin fire | 1 Fire engine | 1 Fire Station | 110 | Verified 22 July 2026 |
| `1` | Container fire | 1 Fire engine | 1 Fire Station | 170 | Verified 22 July 2026 |
| `208` | Domestic smoke alarm activation | 1 Fire engine | 1 Fire Station | 600 | Verified 22 July 2026 |

## Bin fire

**Canonical ID:** `0`  
**Service:** Fire and Rescue  
**Average reward:** 110 credits  
**Guaranteed requirement:** 1 Fire engine

The official mission page also identifies the following possible follow-up missions:

- Phonebox on fire
- Burning leaves
- Burning bus shelter

[Official UK mission record](https://www.missionchief.co.uk/einsaetze/0)

## Container fire

**Canonical ID:** `1`  
**Service:** Fire and Rescue  
**Average reward:** 170 credits  
**Guaranteed requirement:** 1 Fire engine

[Official UK mission record](https://www.missionchief.co.uk/einsaetze/1)

## Domestic smoke alarm activation

**Canonical ID:** `208`  
**Service:** Fire and Rescue  
**Average reward:** 600 credits  
**Guaranteed requirement:** 1 Fire engine

The official mission page lists two expandable missions:

- House fire
- House fire (Persons Reported)

[Official UK mission record](https://www.missionchief.co.uk/einsaetze/208)

## Machine-readable records

```text
data/uk/missions/
├── bin-fire.json
├── container-fire.json
└── domestic-smoke-alarm-activation.json
```

These records are validated against `data/schema/mission.schema.json` by the repository validation workflow.

## Population policy

The next mission batches should be added in controlled groups. Each batch must:

1. preserve the official UK mission ID;
2. use the exact current UK mission name;
3. distinguish guaranteed and probabilistic requirements;
4. record the official source URL;
5. include the verification date;
6. pass schema and documentation validation.
