# UK Vehicle Coverage Status

This report is generated from the Stage 36A vehicle source ledger and the canonical files under `data/uk/vehicles/`.

The source ledger is deliberately evidence-tiered. Community-observed game vehicle type IDs are discovery evidence, not official verification. Exact labels, prices, staffing and market restrictions are promoted only when reproduced from the current UK game or published by the official Help Centre.

## Coverage summary

| Metric | Value |
|---|---:|
| Source-ledger entries | **73** |
| Canonical deployable-resource records | **104** |
| Ledger entries mapped to canonical records | **73** |
| Ledger entries awaiting canonical mapping | **0** |
| Canonical records without a ledger entry | **31** |
| Dangling canonical mappings | **0** |
| Identity coverage | **100.00%** |
| Verified labels | **27** |
| Community-candidate type IDs | **73** |

**Programme status:** `complete`

## Canonical field completeness

| Field | Complete | Coverage |
|---|---:|---:|
| Cost | 49 / 104 | 47.12% |
| Staffing | 32 / 104 | 30.77% |
| Training | 37 / 104 | 35.58% |
| Training Requirements | 22 / 104 | 21.15% |
| Building Requirements | 58 / 104 | 55.77% |
| Resource Class | 61 / 104 | 58.65% |
| Transport Capacity | 6 / 104 | 5.77% |
| Towing | 25 / 104 | 24.04% |
| Deployment | 20 / 104 | 19.23% |
| Capabilities | 104 / 104 | 100.00% |
| Verification Sources | 104 / 104 | 100.00% |

An omitted value is unknown, not zero. Field completeness is reported separately from identity coverage so partial records cannot be mistaken for complete economics or staffing data.

## Field decision coverage

| Metric | Value |
|---|---:|
| Resolved field decisions | **936 / 936** |
| Unresolved field decisions | **0** |
| Decision coverage | **100.00%** |

| Field | Resolved | Coverage |
|---|---:|---:|
| Cost | 104 / 104 | 100.00% |
| Staffing | 104 / 104 | 100.00% |
| Training | 104 / 104 | 100.00% |
| Training Requirements | 104 / 104 | 100.00% |
| Building Requirements | 104 / 104 | 100.00% |
| Resource Class | 104 / 104 | 100.00% |
| Transport Capacity | 104 / 104 | 100.00% |
| Towing | 104 / 104 | 100.00% |
| Deployment | 104 / 104 | 100.00% |

Decision coverage distinguishes documented values, fields that are not applicable, and values that are not published by a reproducible current UK source. It does not convert unknown values into zeroes or guesses. Canonical-only equipment and overlay records do not block completion when every observed ledger identity is mapped and every tracked field has an explicit decision.

## Source-ledger entries awaiting canonical mapping

| Game type ID | Observed UK label | Service | Class | Label evidence |
|---:|---|---|---|---|
| — | None | — | — | — |

## Canonical records without an observed source-ledger ID

| Canonical ID | UK label | Service |
|---|---|---|
| `aerial_appliance_truck` | Aerial Appliance Truck | fire |
| `ambulance_control_unit` | Ambulance Control Unit | ambulance |
| `armed_response_vehicle` | Armed Response Vehicle (ARV) | police |
| `basu_container` | BASU Container | fire_and_rescue |
| `bomb_disposal_crew` | Bomb Disposal Crew | bomb_disposal |
| `bomb_disposal_diver_crew` | Bomb Disposal Diver Crew | bomb_disposal |
| `bomb_disposal_diver_equipment` | Bomb Disposal Diver Equipment | bomb_disposal |
| `bomb_disposal_equipment` | Bomb Disposal Equipment | bomb_disposal |
| `breathing_apparatus_support_unit` | Breathing Apparatus Support Unit | fire_and_rescue |
| `bulk_foam_container` | Bulk Foam Container | fire_and_rescue |
| `cbrn_vehicle` | CBRN Vehicle | fire_and_rescue |
| `coastguard_rescue_helicopter` | Coastguard Rescue Helicopter | coastguard |
| `command_container` | Command Container | fire_and_rescue |
| `container_vehicle` | Container Vehicle | fire_and_rescue |
| `drone` | Drone | shared |
| `eiu` | EIU | police |
| `fire_engine` | Fire engine | fire |
| `firearms_personnel_carrier` | Firearms Personnel Carrier | police |
| `foam_unit` | Foam Unit | fire_and_rescue |
| `hazmat_container` | HazMat Container | fire_and_rescue |
| `high_volume_pump_container` | High Volume Pump Container | fire_and_rescue |
| `misting_container` | Misting Container | fire_and_rescue |
| `mud_decontamination_unit` | Mud Decontamination Unit | coastguard |
| `multiple_dog_carrier` | Multiple Dog Carrier | police |
| `operational_support_unit_container` | Operational Support Unit Container | fire_and_rescue |
| `personal_sar_vehicle` | Personal SAR Vehicle | search_and_rescue |
| `rescue_container` | Rescue Container | fire_and_rescue |
| `traffic_car` | Traffic Car | police |
| `water_container` | Water Container | fire_and_rescue |
| `water_ladder_with_cafs` | Water Ladder with CAFS | fire_and_rescue |
| `welfare_container` | Welfare Container | fire_and_rescue |

## Evidence policy

- Official MissionChief UK pages and the official Help Centre are primary evidence.
- Current authenticated vehicle-market observations may verify IDs, costs, staffing, training and compatibility.
- Community userscripts may identify candidates and type IDs, but cannot independently verify market values.
- Values are never inferred from another locale or treated as zero when unavailable.
