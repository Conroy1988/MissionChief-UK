# Vehicle Type ID Mapping Completion

Stage 36A now maps every observed UK vehicle type ID in the source ledger.

```text
73 observed vehicle type IDs
73 canonical mappings
0 unresolved identities
100% identity coverage
```

## Evidence model

- Type IDs remain marked as community candidates until reproduced directly from the current UK game interface.
- Official Help Centre pages verify labels and published operational attributes where available.
- Community-only identities are represented by canonical records with `community-report` status and deliberately omit unsupported values.
- Type 67, previously labelled `ILB Trainer` in the community map, is reconciled to the official Inland Rescue Boat trailer identity.
- Type 115 remains a separate Welfare Vehicle identity because the game exposes two different type IDs with the same visible label.

## Newly reconciled IDs

| IDs | Service groups |
|---|---|
| 9, 20, 34, 39, 97, 98, 115 | Ambulance |
| 16, 17, 26, 35, 36, 38, 73, 74 | Fire and Rescue |
| 25, 116 | Police |
| 61, 65 | Coastguard |
| 66, 67, 72 | Lifeboat |
| 80, 81 | Airfield Operations |
| 88, 89 | Search and Rescue |
| 105 | Recovery |
| 110, 111 | Bomb Disposal |

## Principal sources

- MissionChief Unit Naming Tool type-ID map
- MissionChief official UK Help Centre vehicle articles
- MissionChief UK community vehicle catalogue
- Current MissionChief UK community evidence for newly introduced Recovery and Cell Van identities
