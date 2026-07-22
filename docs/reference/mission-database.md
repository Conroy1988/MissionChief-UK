# Mission Database

The mission database will provide one consistent reference model for every documented MissionChief UK mission.

## Mission record anatomy

Each mission page and structured record should contain:

- canonical mission name and game identifier;
- aliases and searchable terminology;
- service classification;
- known unlock conditions;
- guaranteed resource requirements;
- probabilistic requirements with clearly stated probabilities;
- personnel and training dependencies;
- patient, prisoner and transport behaviour;
- reward data;
- related mission variants;
- operational notes and common dispatch mistakes;
- evidence status, source trail and verification date.

## Requirement language

Requirements must distinguish between:

- **guaranteed** — always required under the documented conditions;
- **probabilistic** — may be requested, with the confirmed probability recorded;
- **conditional** — triggered only when another element exists, such as a patient or prisoner;
- **recommended** — strategic advice rather than a game requirement.

## Dispatch interpretation

Where the interface separates resources into required, responding, on scene and still needed, the guide must preserve those distinctions. A unit already responding must not be presented as an additional outstanding requirement.

## Data relationship

Mission records are designed to reference canonical vehicle, building, extension, training and personnel identifiers. This allows future calculators and APIs to consume the same evidence used by the documentation.

## Publication rule

No exact mission requirement, reward or probability should be published as verified without reproducible UK-game evidence or a suitable primary source.
