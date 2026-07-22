# Verified Mission Batch 12 — Airfield Enrichment

Stage 26 extends the Airfield Operations baseline from Codes B/C/F to the smaller Code A progression, Code D, Hot Brakes and an airport maintenance-hangar incident.

## Batch summary

| ID | Mission | Evidence depth | Credits |
|---:|---|---|---:|
| `586` | Aircraft Accident - Code A | Directory generation data | 8,000 |
| `589` | Aircraft Accident - Code D | Full response table | 16,000 |
| `590` | Hot Brakes - Code D | Full response table | 18,000 |
| `591` | Aircraft Leaking Fuel - Code A | Directory generation data | 2,000 |
| `592` | Bird Strike - Code A | Directory generation data | 3,000 |
| `719` | Airport maintenance hangar fire | Full response and patient table | 18,150 |

## Code A progression

The Code A records use the Small Airport runway POI and require one Aviation firefighting Extension. Aircraft Accident adds HART, Mass Casualty, Rescue and Police dependencies; Fuel Leak and Bird Strike establish lower-scale unlock points.

## Code D and Hot Brakes

Both Large Airport missions verify:

- Airfield Operations and Aviation firefighting extension dependencies;
- Police Sergeant and Police Inspector availability;
- conditional Traffic Cars;
- Major Foam Tender, Water Carrier and hazardous-material alternatives;
- Airfield Operations Supervisor, Ambulance Officer and Operational Team Leader personnel.

Hot Brakes increases the qualifying Fire/foam and Water Carrier totals compared with Aircraft Accident Code D.

## Airport maintenance hangar fire

This record verifies independent alternative rows for:

- Fire Engine or RIV;
- HazMat Unit or CBRN Vehicle;
- ICCU or Ambulance Control Unit;
- Aerial Appliance Truck or Rescue Stairs.

It also contains a dedicated Aerial Appliance requirement, so the two rows must not be collapsed without dispatch-level evidence.

The observed mission page displayed an event multiplier. The canonical average remains 18,150 credits.

## Evidence boundary

Directory-only records intentionally leave response arrays empty. Full-response records preserve every displayed row but do not infer minimum unique-vehicle totals across overlapping alternatives.
