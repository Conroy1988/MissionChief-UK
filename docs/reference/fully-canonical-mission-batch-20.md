# Fully Canonical Mission Batch 20

Batch 20 promotes 3 analyser-approved missions unlocked by the lossless official patient contract.

## Batch result

| ID | Mission | Generator | Maximum patients | Average credits |
|---:|---|---|---:|---:|
| `408` | Small Fuel storage tank explosion | `firehouse_missions` | 6 | 7,000 |
| `409` | Large Fuel storage tank explosion | `firehouse_missions` | 8 | 12,000 |
| `410` | Fuel Storage Depot Explosion (Major Incident) | `firehouse_missions` | 20 | 20,000 |

## Evidence safeguards

- Every record was selected by the evidence-safe candidate analyser after all resource, prerequisite, relationship and patient blockers were cleared.
- Patient maxima and optional minima, specialisation captions and IDs, UK codes, transport and critical-care probabilities, first-responder probability and end-of-mission generation flags are preserved exactly when published.
- Resource probabilities remain distinct from patient probabilities.
- Duplicate relationship multiplicity, variants, overlays, unsupported generators and unmapped keys remain blocked.
- Strict resource-key and patient equivalence are mandatory for every promotion.

## Coverage movement

```text
Before Batch 20
Canonical records:       240
Direct ID matches:       223
Fully canonical:         182
Remaining to canonical:  880

After Batch 20
Canonical records:       243
Direct ID matches:       226
Fully canonical:         185
Remaining to canonical:  877
```

Batch 20 raises identity coverage to **21.28%** and fully canonical coverage to **17.42%**.

Promotion decisions are stored in:

```text
data/uk/mission-verification-batches/fully-canonical-fire-batch-20.json
```
