# Changelog

All notable MissionChief UK changes are documented here.

The project follows semantic versioning for its public static-data API and release artefacts.

## [Unreleased]

### Command experience

- Added a site-wide verified-data command palette available through `Ctrl+K`, `⌘K` or `/`.
- Added instant search across missions, deployable resources, infrastructure and qualifications.
- Added collection filters, keyboard result navigation, responsive mobile presentation and focus restoration.
- Added encoded deep links from mission results into Mission Lookup and from other collections into the Query Catalogue.
- Added a persistent header launcher plus a prominent landing-page command-search control.

### Quality assurance

- Added Playwright acceptance coverage for command-palette search, filtering, closure, mission deep links and iPhone viewport operation.
- Added all-JavaScript syntax validation to the validation and deployment workflows.
- Documented the command-search trust boundary and dedicated local test command.

### Compatibility

- Retained the v1.0.1 static API, canonical IDs, collection counts and evidence semantics.
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