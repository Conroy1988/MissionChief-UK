# Changelog

All notable MissionChief UK changes are documented here.

The project follows semantic versioning for its public static-data API and release artefacts.

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
