# Mission Database

The mission database provides one consistent reference model for every documented MissionChief UK mission.

## Mission record anatomy

Each mission page and structured record should contain:

- canonical mission name and game identifier;
- aliases and searchable terminology;
- service and mission-group classification;
- known unlock conditions and POIs;
- guaranteed resource requirements;
- probabilistic requirements with confirmed probabilities;
- conditional requirements with their exact trigger;
- alternative resource groups where one of several resources can satisfy a requirement;
- personnel that are available, required, average-minimum or probability-based;
- patient, prisoner, transport and hand-off behaviour;
- reward data;
- custom spawn-area and vehicle-environment restrictions;
- explicit base, additive-overlay or mission-variation relationships;
- evidence status, source trail and verification date.

## Requirement language

Requirements must distinguish between:

- **guaranteed** — always required under the documented conditions;
- **probabilistic** — may be requested, with the confirmed probability recorded;
- **conditional** — required only when a stated condition is true;
- **alternative** — one qualifying resource from a defined group satisfies the requirement;
- **recommended** — strategic advice rather than a game requirement.

## Conditional requirements

Stage 19 introduces first-class conditional resources:

```json
{
  "resource": "traffic_car",
  "quantity": 4,
  "condition": "only_when_available"
}
```

This is used where official airfield pages state that Traffic Cars are required only when available. A conditional requirement must not be flattened into a guaranteed count or omitted as merely optional advice.

## Alternative requirements

An alternative group such as:

```json
{
  "resources": [
    "fire_engine",
    "major_foam_tender"
  ],
  "quantity": 7
}
```

means seven qualifying resources in total. It must not be interpreted as seven of each type.

The same model is used for:

- RRV or Specialist Paramedic RRV;
- ILB or ALB;
- Mountain Rescue 4x4 or SAR 4x4;
- Operational Support Van, Trailer or Personal SAR Vehicle;
- Police Helicopter or Drone;
- Fire Engine or RIV;
- RIV or Major Foam Tender;
- Fire Officer or Airfield Firefighting Command Vehicle;
- HazMat Unit or CBRN Vehicle;
- ICCU, Ambulance Control Unit or Airfield Firefighting Command Vehicle;
- Aerial Appliance Truck or Rescue Stairs.

## Overlapping airfield alternatives

Airfield Firefighting Command Vehicles may appear as:

1. a dedicated guaranteed resource;
2. an alternative to Fire Officers;
3. an alternative to ICCU or Ambulance Control Unit.

The structured records preserve every official row separately. They do not infer whether one vehicle can satisfy multiple rows or calculate a minimum unique-vehicle total without dispatch-level evidence.

## Mission variants and overlays

Some official mission IDs have base, additive-overlay or mission-variation states. These must remain distinct.

An overlay record uses a unique string dataset ID while preserving the official mission ID:

```json
{
  "id": "755-hart-overlay",
  "variant": {
    "source_mission_id": 755,
    "kind": "additive-overlay",
    "key": "hart-atv-carrier"
  }
}
```

This prevents overlay-only requirements from being incorrectly applied to a base mission.

## Personnel states

Personnel can be represented in four independent states:

- `available` — must exist before generation;
- `required` — exact incident requirement;
- `average_minimum` — official average-minimum value that is not an exact guaranteed count;
- `probabilistic` — chance-based incident personnel.

A probability-based or average-minimum role must not be presented as guaranteed.

## Specialist preconditions

The schema supports explicit preconditions for general stations and specialist infrastructure, including:

- HART Bases;
- Coastguard and Lifeboat facilities;
- Mountain Rescue Stations and Search and Rescue HQs;
- Bomb Disposal HQs and Marine Unit Extensions;
- Aviation firefighting Extensions;
- Airfield Operations Extensions;
- Mass Casualty Extensions;
- active Drones.

Mapped specialist preconditions are validated against canonical infrastructure records. A generation precondition does not itself prove that a specific vehicle is required at the incident.

## Dispatch interpretation

Where the interface separates resources into required, responding, on scene and still needed, the guide must preserve those distinctions. A unit already responding must not be presented as an additional outstanding requirement.

## Data relationship

Mission records reference canonical deployable-resource and infrastructure identifiers. This allows future calculators and APIs to consume the same evidence used by the documentation.

Repository validation checks guaranteed, probabilistic, conditional and alternative resource references against the canonical vehicle dataset.

## Publication rule

No exact mission requirement, reward or probability should be published as verified without reproducible UK-game evidence or a suitable primary source.

Temporary reward multipliers must not replace the documented base reward. When a live mission page displays an event multiplier, the directory value and the observation must be recorded separately.
