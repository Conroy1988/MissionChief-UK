# MissionChief UK Delivery Acceleration

Stage 36B separates rapid guide-authoring feedback from release-grade validation.

## Delivery targets

| Change class | Previous target | Stage 36B target | Expected reduction |
|---|---:|---:|---:|
| Guide-only pull-request feedback | 6–10 minutes | 1–2 minutes | 75–85% |
| Structured-data or interface feedback | 8–15 minutes | 3–6 minutes | 55–70% |
| Complete exact-head validation | 8–15 minutes | 4–7 minutes | 45–65% |
| Merge-to-live Pages deployment | 10–20 minutes | 3–6 minutes | 60–80% |

These are engineering targets, not fabricated guarantees. GitHub Actions run durations should be recorded after Stage 36B lands so the estimates can be replaced with measured medians and p90 values.

## Initial measured benchmarks

The first draft-PR self-test on 26 July 2026 included workflow, classifier, documentation and vehicle-validation changes. GitHub completed the selected fast lanes and final aggregate gate approximately **34 seconds after the pull request opened**. The full release-grade lanes were correctly skipped while the pull request remained a draft, and the Chromium lane was correctly skipped because no frontend file changed.

The activation pull request initially changed only `validate.yml`. GitHub selected the workflow/classifier lane and skipped documentation, structured data, vehicle and Chromium jobs. The aggregate gate completed **52 seconds after the draft was created**.

The final ready-state benchmark launched the complete data/evidence audit and strict site/browser audit simultaneously. Both lanes passed on the same exact head, confirming that draft speed does not weaken the landing boundary.

These are activation measurements rather than long-term medians. Stage 37 guide batches will supply representative guide-only median and p90 figures.

## Validation lanes

### Draft pull requests

`validate.yml` classifies changed paths and runs only the smallest safe lanes:

- documentation build and link audit;
- structured-data validation;
- vehicle intelligence validation;
- Chromium interface smoke;
- workflow and classifier checks.

Guide-only Markdown changes do not invoke catalogue equivalence, public-data regeneration, Playwright WebKit installation, or release checks.

### Ready pull requests

The same active `validate.yml` workflow runs two complete release-grade jobs in parallel:

- complete data, synchronizer, evidence and release-integrity audit;
- strict documentation, built-site, Chromium and WebKit audit.

A single aggregate result requires every selected lane to pass. Maintaining one workflow identity avoids duplicate runs and removes workflow-registration ambiguity.

### Main and production

`deploy-pages.yml` performs compact exact-tree integrity checks, builds once, deploys, and runs HTTP smoke tests. The complete production browser matrix runs asynchronously in `production-pages-verification.yml`, bound to the exact deployed SHA. Release publication remains dependent on a successful exact-SHA Pages workflow.

## Safety boundaries

- Unknown or unpublished game values remain unknown; faster validation never relaxes evidence semantics.
- Full catalogue, mapping, schema, release, MkDocs and browser checks still gate every ready landing candidate.
- Workflow changes and release metadata fail closed.
- Dedicated vehicle validation remains on `main` and through manual dispatch.
- Production browser verification remains bound to the exact deployed SHA.
