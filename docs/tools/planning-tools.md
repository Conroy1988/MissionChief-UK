# Planning Tools Programme

Stage 8 converts the structured reference database into practical decision-support tools.

## Planned tools

### Fleet Planner

Compares owned vehicles and qualified staffing against a selected mission set or service profile.

### Building Planner

Models proposed stations, extensions, capacity and confirmed costs without altering live account data.

### Training Planner

Identifies qualification gaps between owned vehicles, available personnel and operational objectives.

### Mission Requirement Explorer

Displays guaranteed, probabilistic and conditional mission requirements without merging those categories.

### Coverage Planner

Supports manual geographic planning using station locations, destination buildings and specialist-resource distribution. Any travel estimate must disclose its routing assumptions.

### Cost Calculator

Combines confirmed purchase and expansion values while preserving the source and verification date of every input.

## Engineering principles

- Structured data is the single source of truth.
- Calculations must be reproducible.
- Assumptions must be visible.
- Unknown values must not silently become zero.
- Recommendations must remain distinct from verified game mechanics.
- Tools should degrade safely when data is incomplete.

## Delivery order

1. Read-only lookup and filtering.
2. Requirement comparison.
3. Cost and training calculations.
4. Saved planning scenarios.
5. Geographic and optimisation features.

The first implementation should favour transparent calculations over opaque optimisation.
