# Mountain Rescue

Mountain Rescue missions combine off-road response, technical rescue, search coordination, specialist personnel and cross-service support.

This guide is based on the first verified Stage 16 records. It does not yet publish vehicle prices, training durations, station build costs or fixed crew capacities.

!!! success "Evidence boundary"
    Values labelled verified come from current UK mission pages. Strategic recommendations are identified separately and must not be read as game requirements.

## Core service model

The first verified Mountain Rescue missions use the following building and resource relationships:

```text
Mountain Rescue Station
        ↓
Mountain Rescue 4x4 or SAR 4x4
        ↓
Search, technical rescue and patient access
        ↓
Control, search dogs, Fire, Ambulance, Police or helicopter support
```

## Canonical resources

| Resource | Canonical ID | Verified use |
|---|---|---|
| Mountain Rescue 4x4 | `mountain_rescue_4x4` | Alternative off-road response resource |
| SAR 4x4 | `sar_4x4` | Alternative off-road response resource |
| Control Van | `control_van` | Search and incident coordination |
| Search Dog Unit | `search_dog_unit` | Missing-person and terrain search |
| Rescue Support Vehicle | `rescue_support_vehicle` | Technical-rescue support |
| ATV Carrier | `atv_carrier` | HART additive-overlay support |
| PRV | `prv` | Specialist Ambulance resource; abbreviation preserved |
| SRV | `srv` | Specialist Ambulance resource; abbreviation preserved |
| Welfare Vehicle | `welfare_vehicle` | Prolonged-incident welfare support |

## Alternative 4x4 requirements

When the UK mission page states **Mountain Rescue 4x4 or SAR 4x4**, the dataset records an alternative group:

```json
{
  "resources": [
    "mountain_rescue_4x4",
    "sar_4x4"
  ],
  "quantity": 1
}
```

This means one qualifying 4x4. It does not mean one of each.

## Base missions and additive overlays

Some Mountain Rescue missions have separate HART or helicopter overlays. The guide preserves these as distinct records rather than merging the extra requirement into the base mission.

Examples:

- **Belay Failure Whilst Abseiling** — the helicopter overlay adds a Helicopter Hangar precondition and a Coastguard Rescue Helicopter;
- **Fall Whilst Fell Running** — the HART overlay adds a HART Base precondition and an ATV Carrier.

Overlay records use a string dataset ID and retain the official numeric mission ID inside the structured `variant` object.

## Personnel

Mountain Rescue records may distinguish:

- personnel that must be available before the mission can generate;
- personnel required at the incident;
- personnel requested only with a confirmed probability.

Verified roles currently include:

- Operational Team Leader;
- Search Advisor;
- Cave Rescue Specialist;
- Fire Officer;
- Ambulance Officer;
- Police Sergeant.

## Current verified missions

- [Stuck Climber](../reference/verified-mission-batch-5.md#stuck-climber)
- [Overdue Hikers](../reference/verified-mission-batch-5.md#overdue-hikers)
- [Belay Failure Whilst Abseiling — helicopter overlay](../reference/verified-mission-batch-5.md#belay-failure-whilst-abseiling-helicopter-overlay)
- [Fall Whilst Fell Running — HART overlay](../reference/verified-mission-batch-5.md#fall-whilst-fell-running-hart-overlay)
- [Amateur Explorers Trapped in Abandoned Mineshaft](../reference/verified-mission-batch-5.md#amateur-explorers-trapped-in-abandoned-mineshaft)

## Planning guidance

!!! tip "Recommended, not required"
    Keep enough qualifying 4x4 capacity to satisfy the largest mission you currently generate. The first verified batch ranges from one qualifying 4x4 to four.

!!! tip "Recommended, not required"
    Treat Control Vans, Search Dog Units and specialist personnel as network resources rather than automatically duplicating every asset at every Mountain Rescue Station.

## Still awaiting verification

The following values remain intentionally unpublished until reproduced from the current UK vehicle market and training interfaces:

- vehicle purchase prices;
- minimum and maximum vehicle crews;
- exact training courses and durations;
- station and extension purchase limits;
- whether aliases such as PRV and SRV have a single official expanded UK name;
- dispatch-radius and response-speed differences between Mountain Rescue and SAR 4x4 resources.
