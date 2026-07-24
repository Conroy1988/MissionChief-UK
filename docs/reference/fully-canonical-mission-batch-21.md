# Fully Canonical Mission Batch 21

Batch 21 promotes 3 analyser-approved missions unlocked by the lossless official patient contract.

## Batch result

| ID | Mission | Generator | Maximum patients | Average credits |
|---:|---|---|---:|---:|
| `72` | Light Aircraft Crash | `firehouse_missions` | 4 | 4,000 |
| `805` | Severe chlorine leak | `firehouse_missions` | 15 | 9,560 |
| `823` | Fire in furniture shop | `firehouse_missions` | 4 | 12,270 |

## Evidence safeguards

- Every record was selected by the evidence-safe candidate analyser after all resource, prerequisite, relationship and patient blockers were cleared.
- Patient maxima and optional minima, specialisation captions and IDs, UK codes, transport and critical-care probabilities, first-responder probability and end-of-mission generation flags are preserved exactly when published.
- Resource probabilities remain distinct from patient probabilities.
- Duplicate relationship multiplicity, variants, overlays, unsupported generators and unmapped keys remain blocked.
- Strict resource-key and patient equivalence are mandatory for every promotion.

## Coverage movement

```text
Before Batch 21
Canonical records:       243
Direct ID matches:       226
Fully canonical:         185
Remaining to canonical:  877

After Batch 21
Canonical records:       246
Direct ID matches:       229
Fully canonical:         188
Remaining to canonical:  874
```

Batch 21 raises identity coverage to **21.56%** and fully canonical coverage to **17.70%**.

Promotion decisions are stored in:

```text
data/uk/mission-verification-batches/fully-canonical-fire-batch-21.json
```
