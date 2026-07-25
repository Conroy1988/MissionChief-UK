# Vehicle Field Resolution

Every canonical UK deployable resource has an explicit outcome for every tracked operational field.

This is **decision coverage**, not a claim that every value is published. A decision can be:

- `documented` — the canonical field contains evidence-tiered data;
- `not_applicable` — the field does not apply to the resource class;
- `not_published` — no reproducible current UK source publishes the value, so it remains omitted;
- `review_required` — evidence conflicts or requires manual adjudication.

## Resolution summary

| Metric | Value |
|---|---:|
| Canonical resources | **104** |
| Tracked fields per resource | **9** |
| Resolved decisions | **936 / 936** |
| Unresolved decisions | **0** |
| Decision coverage | **100.00%** |

## Field-by-field decision coverage

| Field | Resolved | Coverage | Outcome distribution |
|---|---:|---:|---|
| Cost | 104 / 104 | 100.00% | documented: 49, not_published: 55 |
| Staffing | 104 / 104 | 100.00% | documented: 32, not_applicable: 16, not_published: 56 |
| Training | 104 / 104 | 100.00% | documented: 37, not_applicable: 10, not_published: 57 |
| Training Requirements | 104 / 104 | 100.00% | documented: 22, not_applicable: 10, not_published: 72 |
| Building Requirements | 104 / 104 | 100.00% | documented: 58, not_published: 46 |
| Resource Class | 104 / 104 | 100.00% | documented: 61, not_published: 43 |
| Transport Capacity | 104 / 104 | 100.00% | documented: 6, not_applicable: 11, not_published: 87 |
| Towing | 104 / 104 | 100.00% | documented: 25, not_applicable: 6, not_published: 73 |
| Deployment | 104 / 104 | 100.00% | documented: 20, not_published: 84 |

## Integrity rule

Unknown values remain unknown. `not_published` never means zero, free, unrestricted or untrained. Raw factual completeness continues to be reported separately in the [Vehicle Coverage Status](vehicle-coverage-status.md) report.
