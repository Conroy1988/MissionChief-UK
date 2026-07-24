# Fully Canonical Mission Batch 22

Batch 22 promotes 4 analyser-approved missions unlocked by the lossless official patient contract.

## Batch result

| ID | Mission | Generator | Maximum patients | Average credits |
|---:|---|---|---:|---:|
| `749` | Carbon monoxide poisoning in a school | `firehouse_missions` | 25 | 6,000 |
| `793` | Lightning strike at event | `firehouse_missions` | 50 | 5,000 |
| `794` | Tram derailed | `firehouse_missions` | 50 | 2,440 |
| `795` | Bridge collapse (major) | `firehouse_missions` | 50 | 20,115 |

## Evidence safeguards

- Every record was selected by the evidence-safe candidate analyser after all resource, prerequisite, relationship and patient blockers were cleared.
- Patient maxima and optional minima, specialisation captions and IDs, UK codes, transport and critical-care probabilities, first-responder probability and end-of-mission generation flags are preserved exactly when published.
- Resource probabilities remain distinct from patient probabilities.
- Duplicate relationship multiplicity, variants, overlays, unsupported generators and unmapped keys remain blocked.
- Strict resource-key and patient equivalence are mandatory for every promotion.

## Coverage movement

```text
Before Batch 22
Canonical records:       246
Direct ID matches:       229
Fully canonical:         188
Remaining to canonical:  874

After Batch 22
Canonical records:       250
Direct ID matches:       233
Fully canonical:         192
Remaining to canonical:  870
```

Batch 22 raises identity coverage to **21.94%** and fully canonical coverage to **18.08%**.

Promotion decisions are stored in:

```text
data/uk/mission-verification-batches/fully-canonical-fire-batch-22.json
```
