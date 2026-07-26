# MissionChief UK Delivery Acceleration

Stage 36B separates rapid guide-authoring feedback from release-grade verification.

## Delivery targets

| Change class | Previous target | Stage 36B target | Expected reduction |
|---|---:|---:|---:|
| Guide-only pull-request feedback | 6–10 minutes | 1–2 minutes | 75–85% |
| Structured-data or interface feedback | 8–15 minutes | 3–6 minutes | 55–70% |
| Complete exact-head validation | 8–15 minutes | 4–7 minutes | 45–65% |
| Merge-to-live Pages deployment | 10–20 minutes | 3–6 minutes | 60–80% |

These are engineering targets, not fabricated guarantees. GitHub Actions run durations should be recorded after Stage 36B lands so the estimates can be replaced with measured medians and p90 values.

## Initial measured benchmark

The first draft-PR self-test on 26 July 2026 included workflow, classifier, documentation and vehicle-validation changes. GitHub completed the selected fast lanes and final aggregate gate approximately **34 seconds after the pull request opened**. The full release-grade workflow was correctly skipped while the pull request remained a draft, and the Chromium lane was correctly skipped because no frontend file changed.

This is an initial mixed-change measurement rather than a long-term median. Stage 37 guide batches will supply the representative guide-only median and p90 figures.

## Validation lanes

### Draft pull requests

`validate.yml` classifies changed paths and runs only the smallest safe lanes:

- documentation build and link audit;
- structured-data validation;
- vehicle intelligence validation;
- Chromium interface smoke;
- workflow and classifier checks.

Guide-only Markdown changes do not invoke catalogue equivalence, public-data regeneration, Playwright WebKit installation, or release checks.

### Non-draft pull requests

`branch-validation-report.yml` runs the complete release-grade audit. Data integrity, documentation building, and workflow checks run in parallel. Browser tests reuse the single audited MkDocs artifact instead of rebuilding the site.

### Main and production

`deploy-pages.yml` performs compact exact-tree integrity checks, builds once, deploys, and runs HTTP smoke tests. The complete production browser matrix runs asynchronously in `production-pages-verification.yml`, bound to the exact deployed SHA. Release publication remains dependent on a successful exact-SHA Pages workflow.

## Safety boundaries

- Unknown or unpublished game values remain unknown; faster validation never relaxes evidence semantics.
- Full catalogue, mapping, schema, release, MkDocs and browser checks still gate every non-draft landing candidate.
- Workflow changes and release metadata fail closed into the full audit lane.
- Dedicated vehicle validation remains on `main` and through manual dispatch.
- Scheduled full audits continuously check the production baseline.
