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
- personnel and training dependencies;
- patient, prisoner, transport and hand-off behaviour;
- reward data;
- custom spawn-area and vehicle-environment restrictions;
- related mission variants;
- operational notes and common dispatch mistakes;
- evidence status, source trail and verification date.

## Requirement language

Requirements must distinguish between:

- **guaranteed** — always required under the documented conditions;
- **probabilistic** — may be requested, with the confirmed probability recorded;
- **alternative** — one qualifying resource from a defined group satisfies the requirement;
- **conditional** — triggered only when another element exists, such as a patient or prisoner;
- **recommended** — strategic advice rather than a game requirement.

## Alternative requirements

An alternative group such as:

```json
{
  "resources": [
    "inshore_lifeboat",
    "all_weather_lifeboat"
  ],
  "quantity": 1
}
```

means one ILB or one ALB. It must not be interpreted as requiring both resources.

The same model is used by verified Ambulance missions where an RRV or Specialist Paramedic RRV can satisfy one response requirement.

## Maritime mission fields

Stage 15 adds explicit fields for:

- Coastguard Rescue Stations;
- Lifeboat Stations;
- Helicopter Hangars;
- Mud Decontamination and Hovercraft Extensions;
- custom mission spawn areas;
- restricted vehicle environments such as `Ocean`;
- patient or prisoner hand-off destinations such as a Lifeboat Station.

These fields remain separate from vehicle requirements. A Lifeboat Station precondition does not itself prove that a particular boat is required.

## Trailer and vessel distinction

The dataset treats `Inland Rescue Boat (Trailer)` as a different resource from ILB and ALB ocean-rescue boats.

Trailer status, operating environment and vehicle requirement are recorded separately. Exact towing or carrier compatibility must not be inferred unless reproduced from the current UK game.

## Dispatch interpretation

Where the interface separates resources into required, responding, on scene and still needed, the guide must preserve those distinctions. A unit already responding must not be presented as an additional outstanding requirement.

## Data relationship

Mission records reference canonical vehicle, building, extension, training and personnel identifiers. This allows future calculators and APIs to consume the same evidence used by the documentation.

Repository validation currently checks guaranteed, probabilistic and alternative vehicle references against the canonical vehicle dataset.

## Publication rule

No exact mission requirement, reward or probability should be published as verified without reproducible UK-game evidence or a suitable primary source.

Temporary reward multipliers must not replace the documented base reward. When a live mission page displays an event multiplier, the directory value and the observation should be recorded separately.
