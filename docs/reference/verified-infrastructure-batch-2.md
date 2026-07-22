# Verified Infrastructure Batch 2 — Specialist Facilities

Stage 22 expands the production infrastructure catalogue beyond Bomb Disposal, airport, railway and recovery entities.

!!! success "Evidence boundary"
    The current records verify official UK display names and mission-generation relationships. Costs, construction times, capacities and compatible parent buildings remain unpublished unless directly reproduced.

## Batch summary

| Canonical ID | Name | Kind | Service |
|---|---|---|---|
| `police_helicopter_station` | Police Helicopter Station | Building | Police |
| `foam_extension` | Foam Extension | Extension | Fire and Rescue |
| `water_damage_pump_extension` | Water Damage Pump Extension | Extension | Fire and Rescue |
| `flood_rescue_extension` | Flood Rescue Extension | Extension | Fire and Rescue |
| `technical_rescue_extension` | Technical Rescue Extension | Extension | Fire and Rescue |
| `police_public_order_extension` | Police Public Order Extension | Extension | Police |
| `mud_decontamination_extension` | Mud Decontamination Extension | Extension | Coastguard |
| `hovercraft_extension` | Hovercraft Extension | Extension | Coastguard |

## Referential integrity

Mission fields mapped to these records now fail validation when the corresponding canonical infrastructure entity is absent.

The validated fields are:

```text
police_helicopter_stations
foam_extensions
water_damage_pump_extensions
flood_rescue_extensions
technical_rescue_extensions
police_public_order_extensions
mud_decontamination_extensions
hovercraft_extensions
```

## Interpretation

A building or extension count is a mission-generation precondition. It does not, by itself, prove:

- that a particular vehicle must attend;
- how many vehicles the facility stores;
- what personnel it supplies;
- the purchase or construction cost;
- the build duration;
- whether an extension is enabled or disabled by default.

Those attributes remain separate evidence targets.
