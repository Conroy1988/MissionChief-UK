# Fully Canonical Mission Batch 10

Batch 10 promotes the two exact missions unlocked by the verified `mobile_air_vehicles` mapping. The official field represents the UK **Breathing Apparatus Support Unit**, with same-key probabilities supported by the mapping contract.

## Batch result

| ID | Mission | Fire Stations | Fire Engines | Fire Officer | Aerial Appliance | Water Carrier | BA Support Unit | ICCU / Ambulance Control | Average credits |
|---:|---|---:|---:|---:|---|---|---|---|---:|
| `134` | Goods Train Fire | 13 | 4 | 3 | — | 1 | 1 | 1 alternative | 2,000 |
| `579` | Fire in heritage building | 13 | 8 | 4 | 1 | — | 1 | 1 alternative | 13,000 |

## Mapping evidence

Current UK mission pages publish **Breathing Apparatus Support Units** as guaranteed or probabilistic requirements. The retained feed field `mobile_air_vehicles` maps to the canonical resource `breathing_apparatus_support_unit`.

| Official field | Canonical interpretation |
|---|---|
| `requirements.mobile_air_vehicles` | Breathing Apparatus Support Unit quantity |
| `chances.mobile_air_vehicles` | Probability that the published quantity is required |

## Evidence safeguards

- Both records were selected by the evidence-safe candidate analyser after the mapping passed the complete deterministic suite.
- Exact official IDs, names, prerequisites, resource quantities, rewards and POIs are retained.
- Goods Train Fire preserves all four official POIs.
- ICCU or Ambulance Control Unit remains a qualifying alternative group.
- No unresolved relationships, patients, personnel, variants, overlays or unsupported additional fields are present.
- Strict key equivalence is mandatory for both promotions.

## Coverage movement

```text
Before Batch 10
Canonical records:       151
Direct ID matches:       134
Fully canonical:          93
Remaining to canonical:  969

After Batch 10
Canonical records:       153
Direct ID matches:       136
Fully canonical:          95
Remaining to canonical:  967
```

Batch 10 raises identity coverage to **12.81%** and fully canonical coverage to **8.95%** of the 1,062-record official UK catalogue.

Promotion decisions are stored in:

```text
data/uk/mission-verification-batches/fully-canonical-fire-batch-10.json
```
