# Mission Database

The mission database provides one consistent evidence model for every documented MissionChief UK mission.

## Mission record anatomy

A mature record can contain:

- canonical mission name, game ID and aliases;
- service, mission groups and POIs;
- station, building, extension and active-resource preconditions;
- guaranteed, probabilistic, conditional and alternative resources;
- available, required, average-minimum, ranged and probabilistic personnel;
- patients, prisoners, transport and hand-off behaviour;
- recovery and towing outcomes;
- reward values and observed event multipliers;
- base, additive-overlay or mission-variation identity;
- evidence status, source trail and verification date.

## Requirement language

- **Guaranteed** — always required under the documented mission state.
- **Probabilistic** — may be required at the stated probability.
- **Conditional** — applies only when the stated trigger is true and may also carry a probability.
- **Alternative** — the stated total may be supplied by any combination of listed resources.
- **Recommended** — strategy, not a game requirement.

### Conditional probability

```json
{
  "resource": "traffic_car",
  "quantity": 1,
  "condition": "only_when_available",
  "probability": 0.5
}
```

This preserves both facts rather than flattening the requirement into guaranteed or optional.

### Alternative groups

```json
{
  "resources": ["fire_engine", "major_foam_tender"],
  "quantity": 7
}
```

This means seven qualifying resources in total, not seven of each type.

Established alternatives include:

- RRV or Specialist Paramedic RRV;
- ILB or ALB;
- Mountain Rescue 4x4 or SAR 4x4;
- Operational Support Van, Trailer or Personal SAR Vehicle;
- Police Helicopter or Drone;
- Fire Engine or RIV;
- RIV or Major Foam Tender;
- Fire Officer or Airfield Firefighting Command Vehicle;
- HazMat Unit or CBRN Vehicle;
- ICCU or Ambulance Control Unit;
- Aerial Appliance Truck or Rescue Stairs.

## Personnel states

Personnel use five independent forms:

- `available` — must exist before generation;
- `required` — exact incident requirement;
- `average_minimum` — official average-minimum value, not an exact count;
- `ranges` — explicit minimum and maximum, such as 14–42 firefighters;
- `probabilistic` — chance-based personnel requirement.

Repository validation rejects personnel ranges where the minimum exceeds the maximum.

## Recovery and towing

Official recovery pages place towing under **Other information**, separately from Vehicle and Personnel Requirements.

```json
{
  "recovery": {
    "assets": [
      {
        "asset_type": "car",
        "minimum": 2,
        "maximum": 4
      }
    ]
  }
}
```

Towing must not be converted into a fictional emergency-resource requirement. Recovery Centre and HGV Recovery Extension counts remain mission-generation preconditions.

## Mission variants

Base, additive-overlay and mission-variation states remain distinct.

```json
{
  "id": "129-recovery-overlay",
  "variant": {
    "source_mission_id": 129,
    "kind": "additive-overlay",
    "key": "recovery-centre"
  }
}
```

The major multi-vehicle RTC recovery record uses `mission-variation` because its official URL exposes an overlay index rather than an additive-overlay key.

## Specialist preconditions

The schema supports mapped canonical infrastructure including:

- HART, Mass Casualty and Public Order;
- Coastguard Mud Decontamination and Hovercraft;
- Mountain Rescue and Search and Rescue HQ;
- Bomb Disposal HQ and Marine Unit Extension;
- Aviation firefighting and Airfield Operations;
- Recovery Centre and HGV Recovery Extension;
- Railway Police and Railway fire response;
- Police Helicopter Station;
- Foam, Water Damage Pump, Flood Rescue and Technical Rescue extensions.

Mapped fields fail validation when their canonical infrastructure record is absent.

An infrastructure count controls mission generation; it does not automatically prove a dispatch resource.

## Overlapping rows

Some resources occur as both dedicated requirements and members of independent alternative groups. The dataset preserves every official row and does not infer whether one physical vehicle can satisfy several rows simultaneously.

## Dispatch interpretation

Required, responding, on-scene and still-needed values must remain distinct. A unit already responding must not be presented as an additional outstanding requirement.

## Publication rule

No exact requirement, personnel value, towing quantity, reward or probability is published as verified without reproducible UK-game evidence or a suitable primary source.

Temporary event multipliers remain observations and never replace canonical average-credit values.
