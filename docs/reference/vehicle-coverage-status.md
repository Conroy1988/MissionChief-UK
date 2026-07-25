# UK Vehicle Coverage Status

This report is generated from the Stage 36A vehicle source ledger and the canonical files under `data/uk/vehicles/`.

The source ledger is deliberately evidence-tiered. Community-observed game vehicle type IDs are discovery evidence, not official verification. Exact labels, prices, staffing and market restrictions are promoted only when reproduced from the current UK game or published by the official Help Centre.

## Coverage summary

| Metric | Value |
|---|---:|
| Source-ledger entries | **73** |
| Canonical deployable-resource records | **92** |
| Ledger entries mapped to canonical records | **73** |
| Ledger entries awaiting canonical mapping | **0** |
| Canonical records without a ledger entry | **19** |
| Dangling canonical mappings | **0** |
| Identity coverage | **100.00%** |
| Verified labels | **27** |
| Community-candidate type IDs | **73** |

**Programme status:** `in-progress`

## Canonical field completeness

| Field | Complete | Coverage |
|---|---:|---:|
| Cost | 37 / 92 | 40.22% |
| Staffing | 30 / 92 | 32.61% |
| Training | 37 / 92 | 40.22% |
| Training Requirements | 22 / 92 | 23.91% |
| Building Requirements | 46 / 92 | 50.00% |
| Resource Class | 49 / 92 | 53.26% |
| Transport Capacity | 6 / 92 | 6.52% |
| Towing | 14 / 92 | 15.22% |
| Deployment | 20 / 92 | 21.74% |
| Capabilities | 92 / 92 | 100.00% |
| Verification Sources | 92 / 92 | 100.00% |

An omitted value is unknown, not zero. Field completeness is reported separately from identity coverage so partial records cannot be mistaken for complete economics or staffing data.

## Source-ledger entries awaiting canonical mapping

| Game type ID | Observed UK label | Service | Class | Label evidence |
|---:|---|---|---|---|
| — | None | — | — | — |

## Canonical records awaiting source-ledger mapping

| Canonical ID | UK label | Service |
|---|---|---|
| `aerial_appliance_truck` | Aerial Appliance Truck | fire |
| `ambulance_control_unit` | Ambulance Control Unit | ambulance |
| `armed_response_vehicle` | Armed Response Vehicle (ARV) | police |
| `bomb_disposal_crew` | Bomb Disposal Crew | bomb_disposal |
| `bomb_disposal_diver_crew` | Bomb Disposal Diver Crew | bomb_disposal |
| `bomb_disposal_diver_equipment` | Bomb Disposal Diver Equipment | bomb_disposal |
| `bomb_disposal_equipment` | Bomb Disposal Equipment | bomb_disposal |
| `breathing_apparatus_support_unit` | Breathing Apparatus Support Unit | fire_and_rescue |
| `cbrn_vehicle` | CBRN Vehicle | fire_and_rescue |
| `coastguard_rescue_helicopter` | Coastguard Rescue Helicopter | coastguard |
| `drone` | Drone | shared |
| `eiu` | EIU | police |
| `fire_engine` | Fire engine | fire |
| `firearms_personnel_carrier` | Firearms Personnel Carrier | police |
| `foam_unit` | Foam Unit | fire_and_rescue |
| `mud_decontamination_unit` | Mud Decontamination Unit | coastguard |
| `multiple_dog_carrier` | Multiple Dog Carrier | police |
| `personal_sar_vehicle` | Personal SAR Vehicle | search_and_rescue |
| `traffic_car` | Traffic Car | police |

## Evidence policy

- Official MissionChief UK pages and the official Help Centre are primary evidence.
- Current authenticated vehicle-market observations may verify IDs, costs, staffing, training and compatibility.
- Community userscripts may identify candidates and type IDs, but cannot independently verify market values.
- Values are never inferred from another locale or treated as zero when unavailable.
