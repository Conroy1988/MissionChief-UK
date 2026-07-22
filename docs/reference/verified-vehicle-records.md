# Verified Vehicle Records

This page exposes the canonical deployable-resource records currently available in the MissionChief UK dataset.

Each record verifies only its populated attributes. Purchase prices, crew limits, training and station restrictions remain absent until reproduced from current UK interfaces.

!!! success "Evidence boundary"
    Empty or omitted attributes are preferable to unsupported values.

## Current records

| Canonical ID | UK requirement label | Service | Category |
|---|---|---|---|
| `fire_engine` | Fire engine | Fire and Rescue | Response |
| `aerial_appliance_truck` | Aerial Appliance Truck | Fire and Rescue | Specialist |
| `rescue_support_vehicle` | Rescue Support Vehicle | Fire and Rescue | Specialist support |
| `fire_officer` | Fire Officer | Fire and Rescue | Command |
| `water_carrier` | Water Carrier | Fire and Rescue | Water supply |
| `hazmat_unit` | HazMat Unit | Fire and Rescue | Hazardous materials |
| `cbrn_vehicle` | CBRN Vehicle | Fire and Rescue | CBRN response |
| `rapid_response_vehicle` | Rapid Response Vehicle | Ambulance | Response |
| `specialist_paramedic_rrv` | Specialist Paramedic RRV | Ambulance | Specialist response |
| `atv_carrier` | ATV Carrier | Ambulance/HART | Specialist support |
| `prv` | PRV | Ambulance | Specialist response |
| `srv` | SRV | Ambulance | Specialist response |
| `welfare_vehicle` | Welfare Vehicle | Ambulance | Support |
| `iccu` | ICCU | Ambulance | Command and control |
| `ambulance_control_unit` | Ambulance Control Unit | Ambulance | Command and control |
| `mass_casualty_equipment` | Mass Casualty Equipment | Ambulance | Mass casualty support |
| `police_car` | Police car | Police | Response |
| `police_helicopter` | Police Helicopter | Police | Air support |
| `traffic_car` | Traffic Car | Police | Traffic policing |
| `drone` | Drone | Shared | Aerial search and reconnaissance |
| `coastguard_rescue_vehicle` | CRV | Coastguard | Response |
| `coastguard_mud_rescue_unit` | Coastguard Mud Rescue Unit | Coastguard | Specialist rescue |
| `mud_decontamination_unit` | Mud Decontamination Unit | Coastguard | Specialist support |
| `coastguard_rescue_helicopter` | Coastguard Rescue Helicopter | Coastguard | Air rescue |
| `inland_rescue_boat_trailer` | Inland Rescue Boat (Trailer) | Lifeboat | Water-rescue trailer |
| `inshore_lifeboat` | ILB | Lifeboat | Ocean-rescue boat |
| `all_weather_lifeboat` | ALB | Lifeboat | Ocean-rescue boat |
| `mountain_rescue_4x4` | Mountain Rescue 4x4 | Mountain Rescue | Response |
| `sar_4x4` | SAR 4x4 | Search and Rescue | Response |
| `control_van` | Control Van | Search and Rescue | Command |
| `search_dog_unit` | Search Dog Unit | Search and Rescue | Specialist search |
| `operational_support_van` | Operational Support Van | Search and Rescue | Operational support |
| `operational_support_trailer` | Operational Support Trailer | Search and Rescue | Trailer |
| `personal_sar_vehicle` | Personal SAR Vehicle | Search and Rescue | Personnel support |
| `riv` | RIV | Airfield Operations | Airfield firefighting response |
| `major_foam_tender` | Major Foam Tender | Airfield Operations | Foam firefighting |
| `airfield_firefighting_command_vehicle` | Airfield Firefighting Command Vehicle | Airfield Operations | Command |
| `airfield_operations_vehicle` | Airfield Operations Vehicle | Airfield Operations | Airfield operations |
| `rescue_stairs` | Rescue Stairs | Airfield Operations | Aircraft access and rescue |

All records above were checked on 22 July 2026.

## Stage 19 Airfield Operations resources

### RIV and Major Foam Tender

Official pages use **RIV** as the response label. Bird Strike Code B accepts Fire Engines or RIVs in one alternative group and RIVs or Major Foam Tenders in another.

The Major Foam Tender also appears as a dedicated requirement on Aircraft Accident Codes C and F. Dedicated and alternative requirements remain separate.

### Airfield command and operations

The Airfield Firefighting Command Vehicle can appear:

- as a dedicated requirement;
- as an alternative to Fire Officers;
- as an alternative to ICCU or Ambulance Control Unit.

The dataset preserves each official row. It does not assume one command vehicle can satisfy multiple rows simultaneously.

Airfield Operations Vehicles are separate response assets. Airfield Operations Supervisors are personnel and are not represented as vehicles.

### Hazardous-materials alternatives

HazMat Units and CBRN Vehicles form an alternative group. The required quantity is the total number of qualifying resources, not the number of each type.

### Rescue Stairs

Aircraft Accident Code F accepts one Aerial Appliance Truck or Rescue Stairs for the aircraft-access requirement.

### Conditional Traffic Cars

Traffic Cars are stored as conditional resources where the official page states they are required only when available.

## Other established alternatives

The dataset also preserves:

- RRV or Specialist Paramedic RRV;
- ILB or ALB;
- Mountain Rescue 4x4 or SAR 4x4;
- Operational Support Van, Trailer or Personal SAR Vehicle;
- Police Helicopter or Drone.

## Machine-readable records

All 39 production records are stored as one JSON object per file under:

```text
data/uk/vehicles/
```

Repository validation fails when a guaranteed, probabilistic, conditional or alternative mission requirement references an unknown canonical resource.

## Still awaiting verification

The next attribute-level pass should reproduce:

1. credit and coin purchase prices;
2. minimum and maximum vehicle staffing;
3. exact training requirements and durations;
4. building and extension dependencies;
5. purchase limits and unlock conditions;
6. trailer towing or carrier relationships;
7. patient, prisoner and transport capabilities.
