# Verified Vehicle Records

The production dataset contains **46 canonical deployable-resource records**. A record verifies only its populated attributes; omitted prices, crew limits or training remain unknown rather than zero.

## Current records

| Canonical ID | UK label | Service |
|---|---|---|
| `fire_engine` | Fire engine | Fire and Rescue |
| `aerial_appliance_truck` | Aerial Appliance Truck | Fire and Rescue |
| `rescue_support_vehicle` | Rescue Support Vehicle | Fire and Rescue |
| `fire_officer` | Fire Officer | Fire and Rescue |
| `water_carrier` | Water Carrier | Fire and Rescue |
| `hazmat_unit` | HazMat Unit | Fire and Rescue |
| `cbrn_vehicle` | CBRN Vehicle | Fire and Rescue |
| `breathing_apparatus_support_unit` | Breathing Apparatus Support Unit | Fire and Rescue |
| `foam_unit` | Foam Unit | Fire and Rescue |
| `road_rail_unit` | Road Rail Unit | Fire and Rescue / Railway |
| `rapid_response_vehicle` | Rapid Response Vehicle | Ambulance |
| `specialist_paramedic_rrv` | Specialist Paramedic RRV | Ambulance |
| `atv_carrier` | ATV Carrier | Ambulance / HART |
| `prv` | PRV | Ambulance |
| `srv` | SRV | Ambulance |
| `welfare_vehicle` | Welfare Vehicle | Ambulance |
| `iccu` | ICCU | Ambulance |
| `ambulance_control_unit` | Ambulance Control Unit | Ambulance |
| `mass_casualty_equipment` | Mass Casualty Equipment | Ambulance |
| `police_car` | Police car | Police |
| `police_helicopter` | Police Helicopter | Police |
| `traffic_car` | Traffic Car | Police |
| `dog_support_unit` | Dog Support Unit (DSU) | Police |
| `eiu` | EIU | Police / Railway |
| `drone` | Drone | Shared |
| `coastguard_rescue_vehicle` | CRV | Coastguard |
| `coastguard_mud_rescue_unit` | Coastguard Mud Rescue Unit | Coastguard |
| `coastguard_rope_rescue_unit` | Coastguard Rope Rescue Unit | Coastguard |
| `coastguard_commander` | Coastguard Commander | Coastguard |
| `mud_decontamination_unit` | Mud Decontamination Unit | Coastguard |
| `coastguard_rescue_helicopter` | Coastguard Rescue Helicopter | Coastguard |
| `inland_rescue_boat_trailer` | Inland Rescue Boat (Trailer) | Lifeboat |
| `inshore_lifeboat` | ILB | Lifeboat |
| `all_weather_lifeboat` | ALB | Lifeboat |
| `mountain_rescue_4x4` | Mountain Rescue 4x4 | Mountain Rescue |
| `sar_4x4` | SAR 4x4 | Search and Rescue |
| `control_van` | Control Van | Search and Rescue |
| `search_dog_unit` | Search Dog Unit | Search and Rescue |
| `operational_support_van` | Operational Support Van | Search and Rescue |
| `operational_support_trailer` | Operational Support Trailer | Search and Rescue |
| `personal_sar_vehicle` | Personal SAR Vehicle | Search and Rescue |
| `riv` | RIV | Airfield Operations |
| `major_foam_tender` | Major Foam Tender | Airfield Operations |
| `airfield_firefighting_command_vehicle` | Airfield Firefighting Command Vehicle | Airfield Operations |
| `airfield_operations_vehicle` | Airfield Operations Vehicle | Airfield Operations |
| `rescue_stairs` | Rescue Stairs | Airfield Operations |

## Verified economics and staffing

The first exact market-data set covers CRV, Coastguard Mud Rescue Unit, Coastguard Rope Rescue Unit and Coastguard Commander. See [Vehicle Economics and Staffing](vehicle-economics-and-staffing.md).

## Requirement interpretation

The dataset preserves:

- dedicated guaranteed requirements;
- probability-based requirements;
- conditional resources such as Traffic Cars only when available;
- independent alternative groups;
- trailer and operating-environment metadata where verified.

A resource appearing in several alternative rows is not assumed to satisfy all rows simultaneously.

## Acronym safety

Labels such as RIV, ICCU, CBRN and EIU remain unexpanded when the current primary source does not supply a verified full name.

## Machine-readable records

Every record is stored under `data/uk/vehicles/`, validated against `vehicle.schema.json` and exported through `assets/data/v1/vehicles.json` during deployment.
