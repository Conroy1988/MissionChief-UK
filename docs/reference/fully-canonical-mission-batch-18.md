# Fully Canonical Mission Batch 18

Batch 18 promotes 7 analyser-approved missions unlocked by the lossless official patient contract.

## Batch result

| ID | Mission | Generator | Maximum patients | Average credits |
|---:|---|---|---:|---:|
| `149` | Building collapse | `firehouse_missions` | 20 | 9,000 |
| `189` | Hotel fire (small) | `firehouse_missions` | 6 | 3,000 |
| `233` | Person under tree | `firehouse_missions` | 1 | 1,000 |
| `242` | Nuclear Power Station Incident (Major Incident) | `firehouse_missions` | 80 | 35,000 |
| `394` | Odour of chemicals | `firehouse_missions` | 14 | 4,000 |
| `398` | Residential Fire (Hoarder level 7-9) | `firehouse_missions` | 1 | 6,000 |
| `403` | Substance in letter | `firehouse_missions` | 2 | 6,000 |

## Evidence safeguards

- Every record was selected by the evidence-safe candidate analyser after all resource, prerequisite, relationship and patient blockers were cleared.
- Patient maxima and optional minima, specialisation captions and IDs, UK codes, transport and critical-care probabilities, first-responder probability and end-of-mission generation flags are preserved exactly when published.
- Resource probabilities remain distinct from patient probabilities.
- Duplicate relationship multiplicity, variants, overlays, unsupported generators and unmapped keys remain blocked.
- Strict resource-key and patient equivalence are mandatory for every promotion.

## Coverage movement

```text
Before Batch 18
Canonical records:       229
Direct ID matches:       212
Fully canonical:         171
Remaining to canonical:  891

After Batch 18
Canonical records:       236
Direct ID matches:       219
Fully canonical:         178
Remaining to canonical:  884
```

Batch 18 raises identity coverage to **20.62%** and fully canonical coverage to **16.76%**.

Promotion decisions are stored in:

```text
data/uk/mission-verification-batches/fully-canonical-fire-batch-18.json
```
