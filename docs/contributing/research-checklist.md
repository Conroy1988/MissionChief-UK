# Research and Verification Checklist

Use this checklist before proposing exact MissionChief UK data.

## Observation context

- [ ] UK game domain confirmed.
- [ ] Observation date recorded.
- [ ] Relevant building levels and extensions recorded.
- [ ] Premium, event or alliance context identified.
- [ ] Browser tools and userscripts noted where they may alter presentation.

## Evidence quality

- [ ] Exact game wording retained.
- [ ] Screenshot or reproducible navigation path available.
- [ ] Dynamic values distinguished from fixed values.
- [ ] Probabilistic behaviour repeated enough to support the claim.
- [ ] Conflicting evidence documented rather than discarded.

## Data integrity

- [ ] Canonical identifier follows repository conventions.
- [ ] Aliases are separated from the canonical name.
- [ ] Numeric values are stored as numbers.
- [ ] Unknown values are not guessed.
- [ ] Related object identifiers have been checked.
- [ ] Verification status matches the strength of evidence.

## Documentation quality

- [ ] Fact, calculation and recommendation are visibly separated.
- [ ] UK terminology is used consistently.
- [ ] Limitations and edge cases are stated.
- [ ] Existing pages and records have been searched for duplicates.
- [ ] Links and navigation build successfully.

## Final checks

```bash
python scripts/validate_data.py
mkdocs build --strict
```

A failed validation or strict documentation build must be resolved before publication.