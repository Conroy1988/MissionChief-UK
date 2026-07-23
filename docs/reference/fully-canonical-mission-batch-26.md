# Fully Canonical Mission Batch 26

Batch 26 promotes 20 analyser-approved missions unlocked by the lossless official patient contract.

## Batch result

| ID | Mission | Generator | Maximum patients | Average credits |
|---:|---|---|---:|---:|
| `29` | Unknown Tanker Spill | `firehouse_missions` | — | 5,300 |
| `69` | Unknown Tanker Spill | `firehouse_missions` | — | 4,300 |
| `73` | Serious Accident Involving a Bus | `firehouse_missions` | 12 | 2,000 |
| `90` | Cyclist hit by HGV | `firehouse_missions` | 1 | 2,000 |
| `126` | HGV Fire | `firehouse_missions` | — | 1,400 |
| `128` | RTC Entrapment | `firehouse_missions` | 2 | 1,250 |
| `129` | Multi vehicle RTC | `firehouse_missions` | 7 | 1,600 |
| `130` | Multi vehicle RTC entrapment | `firehouse_missions` | 7 | 4,000 |
| `131` | HGV Lost its load | `firehouse_missions` | — | 1,500 |
| `133` | HGV Lost its load (milk) | `firehouse_missions` | — | 3,500 |
| `322` | Dangerous goods truck accident | `firehouse_missions` | 1 | 2,200 |
| `393` | Large fuel leak from vehicle (fast road) | `firehouse_missions` | — | 1,500 |
| `442` | LPG Fuelled vehicle fire (Persons Reported) | `firehouse_missions` | 1 | 3,500 |
| `443` | LPG Fuelled vehicle fire (fast road) (Persons Reported) | `firehouse_missions` | 1 | 3,700 |
| `444` | LPG Fuelled vehicle fire (fast road) | `firehouse_missions` | — | 3,500 |
| `451` | Bridge Strike (Double Decker Bus) (Persons reported) | `firehouse_missions` | 40 | 8,000 |
| `467` | Caravan roll over RTC (Fast Road) | `firehouse_missions` | — | 7,000 |
| `478` | Underground electrical cable fire (Major) | `firehouse_missions` | — | 16,000 |
| `484` | Tanker on fire | `firehouse_missions` | — | 10,000 |
| `485` | Tanker on fire (Persons reported) | `firehouse_missions` | 3 | 10,000 |

## Evidence safeguards

- Every record was selected by the evidence-safe candidate analyser after all resource, prerequisite, relationship and patient blockers were cleared.
- Patient maxima and optional minima, specialisation captions and IDs, UK codes, transport and critical-care probabilities, first-responder probability and end-of-mission generation flags are preserved exactly when published.
- Resource probabilities remain distinct from patient probabilities.
- Duplicate relationship multiplicity, variants, overlays, unsupported generators and unmapped keys remain blocked.
- Strict resource-key and patient equivalence are mandatory for every promotion.

## Coverage movement

```text
Before Batch 26
Canonical records:       257
Direct ID matches:       240
Fully canonical:         199
Remaining to canonical:  863

After Batch 26
Canonical records:       277
Direct ID matches:       260
Fully canonical:         219
Remaining to canonical:  843
```

Batch 26 raises identity coverage to **24.48%** and fully canonical coverage to **20.62%**.

Promotion decisions are stored in:

```text
data/uk/mission-verification-batches/fully-canonical-fire-batch-26.json
```
