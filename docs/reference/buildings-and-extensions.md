# Buildings and Extensions Database

The production infrastructure database contains **18 schema-controlled records** used by verified mission preconditions.

## Production location

```text
data/uk/infrastructure/
```

## Canonical records

| Canonical ID | Name | Kind | Verified mission effect |
|---|---|---|---|
| `bomb_disposal_hq` | Bomb Disposal HQ | Building | Bomb Disposal generation |
| `bomb_disposal_marine_unit_extension` | Bomb Disposal Marine Unit Extension | Extension | Coastal Bomb Disposal generation |
| `hart_base` | HART Base | Building | HART-dependent generation |
| `aviation_firefighting_extension` | Aviation firefighting Extension | Extension | Airport-firefighting generation |
| `airfield_operations_extension` | Airfield Operations Extension | Extension | Airfield-operations generation |
| `mass_casualty_extension` | Mass Casualty Extension | Extension | Mass-casualty generation |
| `recovery_centre` | Recovery Centre | Building | Recovery missions and variations |
| `hgv_recovery_extension` | HGV Recovery Extension | Extension | Heavy-vehicle recovery variations |
| `railway_police` | Railway Police | Building | Railway Police generation |
| `railway_fire_response` | Railway fire response | Building | Specialist rail-fire generation |
| `police_helicopter_station` | Police Helicopter Station | Building | Police air-support generation |
| `police_public_order_extension` | Police Public Order Extension | Extension | Public-order generation |
| `foam_extension` | Foam Extension | Extension | Foam-dependent generation |
| `water_damage_pump_extension` | Water Damage Pump Extension | Extension | High-volume pumping generation |
| `flood_rescue_extension` | Flood Rescue Extension | Extension | Flood-rescue generation |
| `technical_rescue_extension` | Technical Rescue Extension | Extension | Technical-rescue generation |
| `mud_decontamination_extension` | Mud Decontamination Extension | Extension | Mud-rescue generation |
| `hovercraft_extension` | Hovercraft Extension | Extension | Hovercraft-dependent generation |

## Referential integrity

Mapped mission fields are validated against these canonical IDs. A mission fails validation when it claims a countable specialist precondition without a matching infrastructure record.

## Infrastructure is not a dispatched resource

A generation precondition does not automatically prove:

- that a vehicle from the building must attend;
- the building's vehicle capacity;
- staffing or classroom capacity;
- purchase price or construction duration;
- whether an extension is active by default.

Examples:

- Mass Casualty Extension is separate from Mass Casualty Equipment.
- Recovery Centre is separate from the number of assets to tow.
- Airfield Operations Extension is separate from Airfield Operations Vehicles.
- Active Drone counts are generation state, not automatically a Drone dispatch row.

## Evidence boundary

A verified infrastructure record applies only to populated fields. The current catalogue strongly covers identity and mission-generation relationships; many costs, construction times, capacities and parent-building relationships remain controlled evidence targets.

See [Specialist Infrastructure Batch 2](verified-infrastructure-batch-2.md) for the Stage 22 expansion.
