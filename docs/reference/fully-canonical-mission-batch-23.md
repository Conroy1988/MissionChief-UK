# Fully Canonical Mission Batch 23

Batch 23 promotes 3 analyser-approved missions unlocked by the lossless official patient contract.

## Batch result

| ID | Mission | Generator | Maximum patients | Average credits |
|---:|---|---|---:|---:|
| `507` | Small Abandoned Building Fire | `firehouse_missions` | — | 1,200 |
| `519` | Youths Setting Fire | `firehouse_missions` | — | 800 |
| `828` | Party centre on fire | `firehouse_missions` | 4 | 10,640 |

## Evidence safeguards

- Every record was selected by the evidence-safe candidate analyser after all resource, prerequisite, relationship and patient blockers were cleared.
- Patient maxima and optional minima, specialisation captions and IDs, UK codes, transport and critical-care probabilities, first-responder probability and end-of-mission generation flags are preserved exactly when published.
- Resource probabilities remain distinct from patient probabilities.
- Duplicate relationship multiplicity, variants, overlays, unsupported generators and unmapped keys remain blocked.
- Strict resource-key and patient equivalence are mandatory for every promotion.

## Coverage movement

```text
Before Batch 23
Canonical records:       250
Direct ID matches:       233
Fully canonical:         192
Remaining to canonical:  870

After Batch 23
Canonical records:       253
Direct ID matches:       236
Fully canonical:         195
Remaining to canonical:  867
```

Batch 23 raises identity coverage to **22.22%** and fully canonical coverage to **18.36%**.

Promotion decisions are stored in:

```text
data/uk/mission-verification-batches/fully-canonical-fire-batch-23.json
```
