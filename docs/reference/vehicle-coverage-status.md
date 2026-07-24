# UK Vehicle Coverage Status

This report is generated from the Stage 36A vehicle source ledger and the canonical files under `data/uk/vehicles/`.

The source ledger is deliberately evidence-tiered. Community-observed game vehicle type IDs are discovery evidence, not official verification. Exact labels, prices, staffing and market restrictions are promoted only when reproduced from the current UK game or published by the official Help Centre.

## Coverage summary

| Metric | Value |
|---|---:|
| Source-ledger entries | **73** |
| Canonical deployable-resource records | **64** |
| Ledger entries mapped to canonical records | **44** |
| Ledger entries awaiting canonical mapping | **29** |
| Canonical records without a ledger entry | **20** |
| Dangling canonical mappings | **0** |
| Identity coverage | **60.27%** |
| Verified labels | **19** |
| Community-candidate type IDs | **73** |

**Programme status:** `in-progress`

## Canonical field completeness

| Field | Complete | Coverage |
|---|---:|---:|
| Cost | 10 / 64 | 15.62% |
| Staffing | 10 / 64 | 15.62% |
| Training | 7 / 64 | 10.94% |
| Building Requirements | 10 / 64 | 15.62% |
| Transport Capacity | 2 / 64 | 3.12% |
| Deployment | 14 / 64 | 21.88% |
| Capabilities | 64 / 64 | 100.00% |
| Verification Sources | 64 / 64 | 100.00% |

An omitted value is unknown, not zero. Field completeness is reported separately from identity coverage so partial records cannot be mistaken for complete economics or staffing data.

## Source-ledger entries awaiting canonical mapping

| Game type ID | Observed UK label | Service | Class | Label evidence |
|---:|---|---|---|---|
| 9 | Air Ambulance | ambulance | aircraft | candidate |
| 16 | Rescue Pump | fire_and_rescue | vehicle | candidate |
| 17 | Combined Aerial Rescue Pump | fire_and_rescue | vehicle | candidate |
| 20 | OTL | ambulance | vehicle | candidate |
| 25 | Armed Traffic Car | police | vehicle | candidate |
| 26 | Heavy 4x4 Tanker | fire_and_rescue | vehicle | candidate |
| 34 | Ambulance Officer | ambulance | vehicle | candidate |
| 35 | BFU | fire_and_rescue | vehicle | candidate |
| 36 | F/WrC | fire_and_rescue | vehicle | candidate |
| 38 | RPF | fire_and_rescue | vehicle | candidate |
| 39 | Operational Support Unit | ambulance | vehicle | candidate |
| 61 | Flood Rescue Unit Trailer | coastguard | trailer | verified |
| 65 | Coastguard Rescue Helicopter Large | coastguard | aircraft | candidate |
| 66 | 4x4 Vehicle | lifeboat | vehicle | verified |
| 67 | ILB Trainer | lifeboat | trailer | candidate |
| 72 | Hovercraft Transporter | lifeboat | vehicle | verified |
| 73 | Light 4x4 | fire_and_rescue | vehicle | verified |
| 74 | Boat Trailer | fire_and_rescue | trailer | verified |
| 80 | Airfield Operations Supervisor | airfield_operations | vehicle | candidate |
| 81 | Medical Equipment Trailer | airfield_operations | trailer | candidate |
| 88 | SAR Flood Rescue Trailer | search_and_rescue | trailer | candidate |
| 89 | Drone Vehicle SAR HQ | search_and_rescue | vehicle | candidate |
| 97 | Patient Transport Service Ambulance | ambulance | vehicle | candidate |
| 98 | Critical Care Transfer Ambulance | ambulance | vehicle | candidate |
| 105 | Flatbed Recovery Vehicle | recovery | vehicle | candidate |
| 110 | EOD Response Vehicle | bomb_disposal | vehicle | candidate |
| 111 | EOD Medium Equipment Van | bomb_disposal | vehicle | candidate |
| 115 | Welfare Vehicle | ambulance | vehicle | candidate |
| 116 | Cell Van | police | vehicle | candidate |

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
| `inland_rescue_boat_trailer` | Inland Rescue Boat (Trailer) | lifeboat |
| `mud_decontamination_unit` | Mud Decontamination Unit | coastguard |
| `multiple_dog_carrier` | Multiple Dog Carrier | police |
| `personal_sar_vehicle` | Personal SAR Vehicle | search_and_rescue |
| `traffic_car` | Traffic Car | police |

## Evidence policy

- Official MissionChief UK pages and the official Help Centre are primary evidence.
- Current authenticated vehicle-market observations may verify IDs, costs, staffing, training and compatibility.
- Community userscripts may identify candidates and type IDs, but cannot independently verify market values.
- Values are never inferred from another locale or treated as zero when unavailable.
