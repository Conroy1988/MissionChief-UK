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
- alternative resource groups where one of several vehicles can satisfy a requirement;
- personnel that are available, required or probability-based;
- patient, prisoner, transport and hand-off behaviour;
- reward data;
- custom spawn-area and vehicle-environment restrictions;
- explicit base, additive-overlay or mission-variation relationships;
- evidence status, source trail and verification date.

## Requirement language

Requirements must distinguish between:

- **guaranteed** — always required under the documented conditions;
- **probabilistic** — may be requested, with the confirmed probability recorded;
- **alternative** — one qualifying resource from a defined group satisfies the requirement;
- **conditional** — triggered only when another element exists;
- **recommended** — strategic advice rather than a game requirement.

## Alternative requirements

An alternative group such as:

```json
{
  "resources": [
    "mountain_rescue_4x4",
    "sar_4x4"
  ],
  "quantity": 2
}
```

means two qualifying 4x4 resources in total. It must not be interpreted as two of each vehicle.

The same model is used for:

- Rapid Response Vehicle or Specialist Paramedic RRV;
- ILB or ALB;
- Mountain Rescue 4x4 or SAR 4x4.

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

This prevents an ATV Carrier, Coastguard Rescue Helicopter, active drone or other overlay-only requirement from being incorrectly applied to the base mission.

## Personnel probabilities

Personnel can be represented in three independent states:

```json
{
  "personnel": {
    "available": [],
    "required": [],
    "probabilistic": [
      {
        "role": "Operational Team Leader",
        "quantity": 1,
        "probability": 0.75
      }
    ]
  }
}
```

A probability-based role must not be presented as guaranteed.

## Specialist preconditions

The schema currently supports explicit precondition fields for:

- Fire, Rescue and Police Stations;
- HART Bases and GP Surgeries;
- Police & Public Order Extensions;
- Coastguard Rescue Stations and Lifeboat Stations;
- Helicopter Hangars;
- Mud Decontamination and Hovercraft Extensions;
- Mountain Rescue Stations;
- Search and Rescue HQs;
- active drones.

A building precondition does not itself prove that a specific vehicle is required.

## Trailer, vessel and environment distinctions

The dataset treats `Inland Rescue Boat (Trailer)` as a different resource from ILB and ALB ocean-rescue boats.

Trailer status, operating environment and mission requirement are recorded separately. Exact towing compatibility must not be inferred unless reproduced from the current UK game.

## Dispatch interpretation

Where the interface separates resources into required, responding, on scene and still needed, the guide must preserve those distinctions. A unit already responding must not be presented as an additional outstanding requirement.

## Data relationship

Mission records reference canonical vehicle, building, extension, training and personnel identifiers. This allows future calculators and APIs to consume the same evidence used by the documentation.

Repository validation checks guaranteed, probabilistic and alternative vehicle references against the canonical vehicle dataset.

## Publication rule

No exact mission requirement, reward or probability should be published as verified without reproducible UK-game evidence or a suitable primary source.

Temporary reward multipliers must not replace the documented base reward. When a live mission page displays an event multiplier, the directory value and the observation must be recorded separately.
