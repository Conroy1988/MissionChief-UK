# Verified Vehicle Records

This page exposes the canonical vehicle-resource records currently available in the MissionChief UK dataset.

Each record verifies only the populated attributes. Purchase prices, crew limits, training and station restrictions remain intentionally absent until those values are reproduced from the current UK vehicle market.

!!! success "Evidence boundary"
    A verified vehicle record does not mean every vehicle attribute has been verified. Empty or omitted fields are preferable to unsupported values.

## Current records

| Canonical ID | UK game name | Service | Category | Evidence status |
|---|---|---|---|---|
| `fire_engine` | Fire engine | Fire and Rescue | Response | Verified 22 July 2026 |
| `aerial_appliance_truck` | Aerial Appliance Truck | Fire and Rescue | Specialist | Verified 22 July 2026 |
| `rapid_response_vehicle` | Rapid Response Vehicle | Ambulance | Response | Verified 22 July 2026 |
| `specialist_paramedic_rrv` | Specialist Paramedic RRV | Ambulance | Specialist response | Verified 22 July 2026 |
| `police_car` | Police car | Police | Response | Verified 22 July 2026 |

## Fire engine

The Fire engine is the first canonical response resource in the dataset. Official UK mission pages repeatedly identify it as a guaranteed requirement, including Bin fire, Garden shed fire and Community Engagement (Fire).

**Not yet published:** purchase cost, maximum crew, station unlocks and training dependencies.

## Aerial Appliance Truck

The Aerial Appliance Truck record establishes the canonical specialist-resource identifier used by conditional mission requirements.

**Not yet published:** purchase cost, staffing, training and station restrictions.

## Rapid Response Vehicle

The Rapid Response Vehicle establishes the canonical `rapid_response_vehicle` identifier and the searchable alias `RRV`.

Official UK mission pages identify an RRV as one valid response option for HCP Home Visit and Palliative Care Visit.

**Not yet published:** purchase cost, staffing, training, patient capability limits and station restrictions.

## Specialist Paramedic RRV

The Specialist Paramedic RRV establishes a separate canonical specialist-response resource. It appears as an alternative to the standard RRV on verified UK ambulance mission pages.

The dataset preserves that relationship as an alternative resource group rather than treating both vehicles as simultaneously required.

**Not yet published:** purchase cost, staffing, training and station or extension dependencies.

## Police car

The Police car record establishes the canonical identifier used by mission requirements. Official UK mission records identify Police Cars as required or conditional policing resources.

**Not yet published:** purchase cost, crew model, custody behaviour and station restrictions.

## Machine-readable records

```text
data/uk/vehicles/
├── aerial-appliance-truck.json
├── fire-engine.json
├── police-car.json
├── rapid-response-vehicle.json
└── specialist-paramedic-rrv.json
```

Mission records reference these resources through their canonical IDs. Repository validation fails when a guaranteed, probabilistic or alternative requirement names a resource without a corresponding vehicle record.

## Next verification target

The next vehicle-data pass should reproduce current values directly from the UK vehicle market and station purchase interfaces, including:

1. price in credits and coins where applicable;
2. minimum and maximum personnel;
3. training requirements;
4. building and extension dependencies;
5. purchase limits and unlock conditions;
6. trailer, towing or carrier relationships;
7. patient, prisoner and transport capabilities.
