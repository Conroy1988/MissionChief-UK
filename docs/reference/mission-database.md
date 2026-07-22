# Mission Database

The mission database provides one consistent reference model for every documented MissionChief UK mission.

## Mission record anatomy

Each mission page and structured record should contain:

- canonical mission name and game identifier;
- aliases and searchable terminology;
- service and mission-type classifications;
- points of interest and known unlock conditions;
- guaranteed resource requirements;
- probabilistic requirements with clearly stated probabilities;
- alternative resource groups where one of several vehicles can satisfy the same requirement;
- personnel availability and on-scene requirements;
- patient, critical-care, prisoner and transport behaviour;
- reward data;
- related mission variants;
- operational notes and common dispatch mistakes;
- evidence status, source trail and verification date.

## Requirement language

Requirements must distinguish between:

- **guaranteed** — always required under the documented conditions;
- **probabilistic** — may be requested, with the confirmed probability recorded;
- **alternative** — a confirmed quantity can be supplied by any one of the listed compatible resources;
- **conditional** — triggered only when another element exists, such as a patient, prisoner or optional game system;
- **recommended** — strategic advice rather than a game requirement.

An alternative group must not be flattened into multiple guaranteed requirements. For example, “1 RRV or Specialist Paramedic RRV” means one qualifying vehicle, not one of each.

## Patients and prisoners

Where confirmed, patient records should preserve:

- minimum and maximum patient counts;
- transport probability;
- critical-care probability;
- first-responder full-care probability;
- patient specialisation;
- possible patient codes.

Prisoner records should preserve confirmed maximum counts separately from police vehicle and personnel requirements.

## Personnel

Personnel availability preconditions and personnel actually required at the mission are different concepts. The database stores them independently so a guide does not confuse an unlock condition with the staffing needed to complete the incident.

## Dispatch interpretation

Where the interface separates resources into required, responding, on scene and still needed, the guide must preserve those distinctions. A unit already responding must not be presented as an additional outstanding requirement.

## Data relationship

Mission records reference canonical vehicle identifiers. Repository validation fails when a guaranteed, probabilistic or alternative resource does not have a matching record under `data/uk/vehicles/`.

The same architecture is designed to expand later to buildings, extensions, training and personnel identifiers, allowing calculators and APIs to consume the same evidence used by the documentation.

## Publication rule

No exact mission requirement, reward, probability, patient behaviour or personnel count should be published as verified without reproducible UK-game evidence or a suitable primary source.
