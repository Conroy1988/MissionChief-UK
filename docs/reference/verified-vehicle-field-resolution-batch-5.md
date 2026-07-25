# Stage 36A — Field Resolution and Final Foam Appliance

This batch closes every tracked vehicle-data field with an explicit evidence outcome while preserving the distinction between published values and unavailable data.

## Delivered

- Water Ladder with CAFS, using the current official UK foam-vehicle contract;
- deterministic field-resolution registry for every canonical resource;
- nine tracked operational fields per resource;
- explicit `documented`, `not_applicable`, `not_published` or `review_required` outcomes;
- 100% decision coverage with zero unresolved field decisions;
- public JSON, generated documentation, CI and release-readiness enforcement.

## Integrity rule

A `not_published` decision is not a zero value. It means no reproducible current UK source publishes the field and the guide refuses to infer it.
