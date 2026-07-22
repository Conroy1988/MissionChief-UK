# Airfield Operations

Airfield Operations covers airport firefighting, aircraft rescue, runway operations and the cross-service response required by serious aviation incidents in MissionChief UK.

## Current verified scope

Stage 19 publishes:

- Aviation firefighting and Airfield Operations extensions;
- HART and Mass Casualty infrastructure dependencies;
- RIVs, Major Foam Tenders and Water Carriers;
- Airfield Firefighting Command and Airfield Operations vehicles;
- aircraft-access, hazardous-materials, casualty and traffic-policing resources;
- Bird Strike Code B;
- Aircraft Accident Codes C and F.

## Airport points of interest

The first verified missions use:

- `Medium Airport (Runway)`;
- `Large Airport (Runway)`.

A POI label is stored independently from building and extension preconditions.

## Alternative-resource interpretation

Airfield incidents contain several independent alternative groups. For example, Aircraft Accident Code F includes:

```text
10 Fire Engines OR Major Foam Tenders
6 Fire Officers OR Airfield Firefighting Command Vehicles
2 HazMat Units OR CBRN Vehicles
1 ICCU OR Ambulance Control Unit OR Airfield Firefighting Command Vehicle
1 Aerial Appliance Truck OR Rescue Stairs
```

Each line is a separate requirement. Resources appearing in more than one group must not be assumed to satisfy both simultaneously without dispatch-level reproduction.

## Conditional Traffic Cars

Traffic Cars are stored as conditional requirements with the condition `only_when_available`. They are not guaranteed requirements and are not merely strategic recommendations.

## Command and supervision

Verified personnel roles include:

- Airfield Operations Supervisor;
- Ambulance Officer;
- Operational Team Leader;
- Police Sergeant;
- Police Inspector.

Personnel available before mission generation and personnel required at the incident remain separate fields.

## Patient scale

Aircraft Accident Code C verifies 75–175 patients. Code F verifies 150–250 patients. Both use General Internal specialisation, codes C-2/C-3 and an 80% critical-care probability.

## Evidence boundary

The current records verify the fields displayed on official UK mission pages. They do not yet publish purchase prices, vehicle staffing limits, training durations, extension costs or minimum unique-vehicle totals across overlapping alternative groups.

## Related records

- [Verified Mission Batch 8](../reference/verified-mission-batch-8.md)
- [Verified Vehicle Records](../reference/verified-vehicle-records.md)
- [Buildings and Extensions](../reference/buildings-and-extensions.md)
