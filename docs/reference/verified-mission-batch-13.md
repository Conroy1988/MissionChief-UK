# Verified Mission Batch 13 — Recovery Enrichment

Stage 27 broadens Recovery beyond cars and basic HGV incidents into motorbikes, buses, caravans, hazardous-goods vehicles and major multi-vehicle collisions.

!!! warning "Generation-level evidence"
    The official directory verifies mission identity, reward and generation preconditions. Individual response and towing tables were unavailable for this batch, so no towing quantity is inferred.

## Batch summary

| Dataset ID | Mission | Recovery dependency | Credits |
|---|---|---|---:|
| `3-recovery-overlay` | Burning motorbike | Recovery Centre | 640 |
| `73-hgv-recovery-overlay` | Serious Accident Involving a Bus | HGV Recovery Extension | 2,300 |
| `266-recovery-overlay` | Motorcross Accident | Recovery Centre | 300 |
| `268-hgv-recovery-overlay` | HGV Rollover Down Embankment | HGV Recovery Extension | 4,800 |
| `322-hgv-recovery-overlay` | Dangerous goods truck accident | HGV Recovery Extension | 2,500 |
| `371-recovery-variation` | Multiple vehicle RTC - Major Incident | Recovery Centre | 10,300 |
| `466-hgv-recovery-overlay` | Caravan roll over RTC | HGV Recovery Extension | 5,300 |
| `791` | Collision between two buses | 2 HGV Recovery Extensions | 11,800 |

## Variant identity

Most records are additive overlays. The major multi-vehicle RTC uses the official `overlay_index=3` URL and is therefore represented as a `mission-variation` rather than assuming an additive-overlay key.

## Terminology

The UK directory currently displays **Motorcross Accident**. The conventional spelling **Motocross Accident** is retained as an alias without replacing the official label.

## Evidence boundary

This batch does not infer:

- the Recovery vehicle dispatched;
- number of vehicles to tow;
- towing destinations;
- recovery personnel;
- probabilities or patients absent from the directory view.

These fields require the individual mission response page.
