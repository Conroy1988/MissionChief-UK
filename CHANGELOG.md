# Changelog

All notable MissionChief UK changes are documented here.

The project follows semantic versioning for its public static-data API and release artefacts.

## [Unreleased]

No unreleased changes are currently recorded.

## [1.1.0] — 2026-07-23

### Complete UK mission catalogue

- Added a lossless snapshot of all 1,062 missions published by the public MissionChief UK mission feed.
- Preserved every official top-level and nested mission field with source URL, retrieval time and SHA-256 provenance.
- Added offline reconciliation reporting against 107 canonical mission records.
- Identified 90 direct official/canonical ID matches, 972 official records awaiting direct canonical records and 17 canonical overlay or derived records without standalone official IDs.
- Added inventories for every published requirement, chance and prerequisite key.
- Added separate public catalogue, coverage and verification endpoints under `assets/data/official/`.

### 100% verification programme

- Added five evidence gates: captured, identity verified, requirements mapped, operationally verified and fully canonical.
- Added a machine-readable base mission-verification registry and scalable batch registries.
- Added deterministic registry merging with duplicate-decision protection.
- Added deterministic per-mission blockers and next actions.
- Added an official-key mapping registry requiring evidence for every mapped requirement, chance and prerequisite key.
- Added strict key-equivalence validation for missions promoted to fully canonical.
- Added offline coverage reconciliation so canonical batches update official/canonical match counts without redownloading the source feed.
- Added an evidence-safe candidate analyser across the complete retained official catalogue.
- The analyser resolves relationship IDs, creates collision-free paths for duplicate mission names and blocks overlays, unsupported service families, probabilities, patients, personnel and unresolved relationships.
- Fully canonicalized 49 missions across three Fire and Rescue batches.
- Batch 1: IDs `0`, `1`, `2`, `3`, `4`, `6`, `7`, `8`, `9`, `10`, `11`.
- Batch 2: IDs `13`, `14`, `15`, `16`, `17`, `18`, `19`, `23`, `24`, `27`.
- Batch 3: IDs `32`, `58`, `65`, `202`, `203`, `313`, `334`, `352`, `365`, `366`, `388`, `399`, `400`, `421`, `435`, `468`, `472`, `475`, `535`, `541`, `570`, `577`, `624`, `638`, `668`, `772`, `857`, `858`.
- Withheld two otherwise simple candidates because their official expansion relationships referenced IDs absent from the retained source snapshot.
- Expanded the canonical mission collection from 62 to 107 records.
- Published a generated verification dashboard and `uk-mission-verification.json` endpoint.

### Mission Lookup

- Expanded Mission Lookup from the canonical mission set to the complete official UK catalogue.
- Added search across IDs, names, POIs, generators, categories, requirements and prerequisites.
- Added service/generator and evidence-coverage filters.
- Added distinct Canonical mapped and Official UK catalogue evidence states.
- Added structured expandable views for patients, personnel, duration, follow-ups, expansion missions, overlays, variants and all additional fields.
- Added a complete official JSON record viewer for every matched or official-only mission.
- Shared one compact catalogue payload across lookup and detail views.
- Retained the first 100 matching cards for rendering performance while keeping every record searchable.

### Command experience

- Added a site-wide verified-data command palette available through `Ctrl+K`, `⌘K` or `/`.
- Added instant search across canonical missions, deployable resources, infrastructure and qualifications.
- Added collection filters, keyboard result navigation, responsive mobile presentation and focus restoration.
- Added encoded deep links from mission results into Mission Lookup and from other collections into the Query Catalogue.
- Added a persistent header launcher and prominent landing-page command-search control.

### Validation and automation

- Added a deterministic importer for the official UK mission feed.
- Added content-addressed refresh behaviour so an unchanged source produces no commit.
- Added a daily and manually dispatchable catalogue refresh workflow.
- Added automatic Pages deployment after a real official-source or generated verification-state change.
- Added an offline catalogue auditor covering IDs, names, ordering, field preservation, checksums, reconciliation, inventories and built-site equality.
- Added verification-registry batch merging to CI, deployment, release publication and catalogue refresh.
- Added official-to-canonical key mapping validation to every publication path.
- Added candidate-report generation and retained Actions artifacts for subsequent canonical batches.
- Added browser acceptance coverage for catalogue completeness, official-only search, canonical search, structured metadata, complete records and horizontal containment.
- Protected catalogue source, automation, verification, browser and QA assets as release-critical.

### Compatibility

- Retained all canonical API v1 paths, envelopes, canonical IDs and evidence semantics.
- Published the complete official catalogue and verification status as separate data tiers rather than silently mixing internal official keys into the canonical API.
- Added no MissionChief authentication, account access or data mutation capability.

## [1.0.1] — 2026-07-22

### Quality assurance

- Added Playwright acceptance testing for Chromium and Firefox desktop browsers.
- Added WebKit acceptance profiles for iPhone and iPad layouts.
- Added functional tests for mission lookup, comparison, fleet planning, deterministic query search and MkDocs instant navigation.
- Added live public-API consistency checks across all eight v1 endpoints.
- Added critical WCAG A/AA scanning with `@axe-core/playwright`.
- Added page-level horizontal-overflow, first-party HTTP failure and JavaScript runtime checks.
- Added retained Playwright reports, traces, screenshots and videos for failed Actions runs.
- Added Chromium testing against the locally built site before deployment and full cross-browser testing after Pages deployment.
- Added deterministic local documentation-link and heading-anchor validation.
- Corrected Firefox instant-navigation cancellation handling and WebKit comparison-layout overflow.

### Release engineering

- Made smoke, browser and readiness checks derive the expected version from `data/version.json`.
- Generalized automated publication for compatible v1 semantic-version releases.
- Required release notes and protected release tags from pointing at a different deployed commit.
- Reordered validation so deterministic failures occur before browser downloads.
- Protected browser-test configuration and QA documentation as release-critical assets.

### Compatibility

- Retained all API v1 paths, envelopes, canonical IDs and evidence semantics.
- Retained the v1.0.0 collection counts; no canonical data records changed in this patch.

## [1.0.0] — 2026-07-22

### Added

- Completed the numbered core programme through Stage 34.
- Published 62 mission records, 46 deployable-resource records, 18 infrastructure records and 11 qualification records.
- Added Railway Police and railway fire-response coverage.
- Expanded Bomb Disposal, Airfield Operations and Recovery mission sequences.
- Added vehicle economics and staffing fields with the first verified Coastguard market dataset.
- Added deterministic versioned JSON exports, manifest, search index, generated FAQ and OpenAPI 3.1 contract.
- Added mission lookup, resource and qualification comparison, concurrent fleet planning and deterministic evidence search.
- Added repository, built-site and deployed-Pages release-readiness checks.
- Added automated v1 publication after successful deployment and live endpoint checks.

### Validation

- Draft 2020-12 schema validation.
- Unique record identifiers and verification-date checks.
- Mission-to-resource and mission-to-infrastructure referential integrity.
- Patient, towing and personnel-range semantic checks.
- Deterministic generated-export comparison.
- Strict MkDocs build and live GitHub Pages smoke testing.

### Evidence boundaries

- Omitted values remain unknown rather than being treated as zero.
- Directory-only mission records do not invent unavailable response tables.
- Towing outcomes remain separate from emergency dispatch resources.
- Alternative, conditional and probabilistic requirements retain their distinct meanings.
