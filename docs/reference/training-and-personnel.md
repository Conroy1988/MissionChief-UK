# Training and Personnel Database

Training and staffing are first-class dependencies rather than footnotes attached to vehicles.

## Production data

Stage 23 introduces schema-controlled qualification records under:

```text
data/uk/training/
```

The current production set verifies eleven operational roles:

- Railway Police Officer;
- Mobile Operations Manager;
- Search Advisor;
- SAR Commander;
- Search Technician;
- Cave Rescue Specialist;
- Airfield Operations Supervisor;
- Operational Team Leader;
- Police Sergeant;
- Police Inspector;
- Ambulance Officer.

## Evidence boundary

The mission pages verify that these roles exist and may be required or must be available before mission generation. They do **not** necessarily verify:

- the academy or classroom used;
- the exact course name;
- course duration;
- prerequisites;
- maximum class size;
- whether the qualification is transferable between vehicle types.

Unverified attributes are omitted rather than inferred.

## Record types

The training schema supports:

- `role-qualification` — an operational role verified by missions, with course details still potentially unknown;
- `course` — a directly verified named course with any confirmed duration and prerequisites.

A role record must not be presented as a complete course record unless the course interface has been reproduced.

## Personnel states

Mission records distinguish:

- `available` — qualified personnel that must exist before generation;
- `required` — exact personnel needed at the incident;
- `average_minimum` — an official average-minimum value rather than a guaranteed exact count;
- `ranges` — an explicit minimum-to-maximum requirement;
- `probabilistic` — chance-based personnel requirements.

## Dependency mapping

The database is designed to model:

```text
Mission → capability → vehicle → staffing → training → building or extension
```

Owning a vehicle alone does not prove that it can fulfil its intended operational role.

## Planning guidance

Training recommendations should include reserve depth. A station with exactly the minimum number of qualified personnel can become unusable when staff are assigned elsewhere or several missions overlap.
