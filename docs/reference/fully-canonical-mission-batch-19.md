# Fully Canonical Mission Batch 19

Batch 19 promotes 4 analyser-approved missions unlocked by the lossless official patient contract.

## Batch result

| ID | Mission | Generator | Maximum patients | Average credits |
|---:|---|---|---:|---:|
| `527` | Factory Fire (Major Incident) | `firehouse_missions` | 5 | 25,000 |
| `528` | Factory Fire (Major Incident) (Persons Reported) | `firehouse_missions` | 20 | 30,000 |
| `602` | Motorcycle Hits Pedestrian | `firehouse_missions` | 1 | 2,000 |
| `704` | Fire at a recycling factory | `firehouse_missions` | — | 14,500 |

## Evidence safeguards

- Every record was selected by the evidence-safe candidate analyser after all resource, prerequisite, relationship and patient blockers were cleared.
- Patient maxima and optional minima, specialisation captions and IDs, UK codes, transport and critical-care probabilities, first-responder probability and end-of-mission generation flags are preserved exactly when published.
- Resource probabilities remain distinct from patient probabilities.
- Duplicate relationship multiplicity, variants, overlays, unsupported generators and unmapped keys remain blocked.
- Strict resource-key and patient equivalence are mandatory for every promotion.

## Coverage movement

```text
Before Batch 19
Canonical records:       236
Direct ID matches:       219
Fully canonical:         178
Remaining to canonical:  884

After Batch 19
Canonical records:       240
Direct ID matches:       223
Fully canonical:         182
Remaining to canonical:  880
```

Batch 19 raises identity coverage to **21.00%** and fully canonical coverage to **17.14%**.

Promotion decisions are stored in:

```text
data/uk/mission-verification-batches/fully-canonical-fire-batch-19.json
```
