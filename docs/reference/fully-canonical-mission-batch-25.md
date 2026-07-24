# Fully Canonical Mission Batch 25

Batch 25 promotes 3 analyser-approved missions unlocked by the lossless official patient contract.

## Batch result

| ID | Mission | Generator | Maximum patients | Average credits |
|---:|---|---|---:|---:|
| `625` | Gain entry - houseboat (concern for welfare) | `firehouse_missions` | 1 | 6,000 |
| `677` | Fire on a cruise ship at the dock | `firehouse_missions` | 35 | 20,500 |
| `718` | Canoeing accident | `firehouse_missions` | 2 | 3,450 |

## Evidence safeguards

- Every record was selected by the evidence-safe candidate analyser after all resource, prerequisite, relationship and patient blockers were cleared.
- Patient maxima and optional minima, specialisation captions and IDs, UK codes, transport and critical-care probabilities, first-responder probability and end-of-mission generation flags are preserved exactly when published.
- Resource probabilities remain distinct from patient probabilities.
- Duplicate relationship multiplicity, variants, overlays, unsupported generators and unmapped keys remain blocked.
- Strict resource-key and patient equivalence are mandatory for every promotion.

## Coverage movement

```text
Before Batch 25
Canonical records:       254
Direct ID matches:       237
Fully canonical:         196
Remaining to canonical:  866

After Batch 25
Canonical records:       257
Direct ID matches:       240
Fully canonical:         199
Remaining to canonical:  863
```

Batch 25 raises identity coverage to **22.60%** and fully canonical coverage to **18.74%**.

Promotion decisions are stored in:

```text
data/uk/mission-verification-batches/fully-canonical-fire-batch-25.json
```
