# Changelog

All notable MissionChief UK changes are documented here.

The project follows semantic versioning for its public static-data API and release artefacts.

## [Unreleased]

No unreleased changes are currently recorded.

## [1.4.0] — 2026-07-28

### Complete operational-guide programme

- Delivered mature evidence-labelled progression guides for Fire and Rescue, Ambulance and HART, Police and Public Safety, Coastguard and Lifeboat, Mountain Rescue, Search and Rescue HQ, Bomb Disposal and EOD, Airfield Operations, Recovery and HGV Recovery, and Railway Police/Railway Fire Response.
- Added buildings, extensions, resources, personnel, training, mission progression, geography, cross-service dependency, concurrency, common-failure and recovery-to-readiness guidance for every represented service group.
- Added the live Fire mission-family pressure analysis over the versioned canonical mission export.
- Preserved verified facts, transparent calculations and recommended strategy as distinct evidence states.

### Cross-service strategy and alliance operations

- Replaced the strategy frameworks with complete cross-service account progression, readiness states, service sequencing, dependency matrices and station-placement doctrine.
- Added route-, destination-, access-, response-cluster, specialist-hub and relief-base planning for urban, rural, coastal and multi-region accounts.
- Added Alliance Operations for members, dispatchers and administrators, including onboarding, least privilege, contribution-policy models, shared infrastructure, mutual support, donor reserve, events, major incidents, recruitment and moderation.
- Kept community policy separate from game-enforced mechanics.

### Account Readiness Planning Suite

- Added local-only multi-mission scenarios with explicit protected reserve.
- Added exact guaranteed-resource aggregation and capacity-aware allocation across independent alternative groups.
- Added separate required-at-incident and available-before-generation personnel checks.
- Added published towing/carrier compatibility checks and recovery-workload reporting without creating fictional resource rows.
- Added Ready, Watch, Degraded and Unavailable states while preserving blank inventory as unknown.
- Added reversible browser-local save/load/delete plus explicit JSON import/export.
- Added no MissionChief authentication, scraping or account mutation capability.

### UX, accessibility and navigation

- Replaced the remaining Getting Started and Game Systems framework pages with mature operational guidance.
- Added collapsed accessible page-section navigation to long non-home pages.
- Added mobile-safe content, table, code-block and media containment.
- Added consistent keyboard focus, sticky-header heading offsets and accessible labels for generated task-list controls.
- Expanded acceptance to every mature service, strategy, alliance and tool route on Chromium desktop, iPhone WebKit and iPad WebKit.
- Expanded critical WCAG A/AA checks across primary command and interactive surfaces.
- Increased full browser-lane installation headroom without weakening any validation gate.

### Release and compatibility

- Advanced the production programme to Stage 42 and the compatible data publication to v1.4.0.
- Retained the Static Data API v1 contract, existing envelopes, canonical identifiers and populated-field semantics.
- Added deterministic release-asset synchronisation for compatible semantic-version publications.
- Reconciled README, Command Centre, roadmap, API guide, release notes, completion report, generated FAQ, OpenAPI and versioned exports.
- Required exact-SHA GitHub Pages deployment, production smoke tests and immutable release publication.

## [1.3.0] — 2026-07-25

### Complete deployable-resource intelligence

- Expanded the canonical deployable-resource estate from 59 to 104 vehicles, aircraft, vessels, trailers, containers and specialist equipment.
- Mapped all 73 observed MissionChief UK vehicle type IDs with zero unresolved identities and 100% identity coverage.
- Added the complete official UK container fleet, Container Extension and verified bidirectional carrier relationships.
- Added official economics, staffing, training-duration, building-compatibility, resource-class, capacity, towing and deployment contracts where reproducible.
- Added Water Ladder with CAFS with verified official cost, crew and Fire Support building compatibility.
- Resolved all nine tracked operational fields for every canonical resource: 936 / 936 explicit evidence-safe decisions and zero unresolved decisions.
- Added deterministic field-resolution schemas, registries, public JSON endpoints, evidence pages, regression tests and permanent CI enforcement.
- Preserved raw documented-value completeness separately from decision coverage; unpublished values remain unknown rather than being converted into zeroes or guesses.

### Release and publication integrity

- Advanced the production programme to Stage 36 and the compatible Static Data API publication to v1.3.0.
- Reconciled README, roadmap, Command Centre, API documentation, generated FAQ, OpenAPI metadata and release artefacts with the completed Stage 36A baseline.
- Extended built-site release validation to cover the vehicle-coverage and field-resolution evidence endpoints.
- Retained the canonical API v1 contract and all existing mission, infrastructure and qualification identifiers.

## [1.2.0] — 2026-07-24

### Complete canonical UK mission catalogue

- Added 795 new direct canonical records and completed strict source-equivalence audits for 41 existing records.
- Promoted all 836 previously incomplete official missions in Batch 31.
- Reached 1,062 / 1,062 direct official/canonical ID matches and 1,062 / 1,062 fully canonical missions.
- Expanded the canonical mission collection from 284 to 1,079 records while retaining 17 intentional overlays and derived records.
- Reduced the official mission backlog and unmapped-key backlog to zero.
- Added lossless operational metadata contracts for variants, relationships, availability, duration, generation rules, source flags and capability thresholds.
- Added 11 verified deployable-resource records and one verified infrastructure record.
- Added strict operational metadata equivalence to validation, refresh, deployment and release controls.
- Hardened duplicate-name filename generation for official IDs containing slash variants.
- Published Static Data API v1.2.0 without breaking the v1 contract.

## [1.1.0] — 2026-07-24

### Complete UK mission catalogue

- Added a lossless snapshot of all 1,062 missions published by the public MissionChief UK mission feed.
- Preserved every official top-level and nested mission field with source URL, retrieval time and SHA-256 provenance.
- Added offline reconciliation reporting against 284 canonical mission records.
- Identified 267 direct official/canonical ID matches, 795 official records awaiting direct canonical records and 17 canonical overlay or derived records without standalone official IDs.
- Added inventories for every published requirement, chance and prerequisite key.
- Added separate public catalogue, coverage and verification endpoints under `assets/data/official/`.

### 100% verification programme

- Added five evidence gates: captured, identity verified, requirements mapped, operationally verified and fully canonical.
- Added a machine-readable base mission-verification registry and scalable batch registries.
- Added deterministic registry merging with duplicate-decision protection.
- Added deterministic per-mission blockers and next actions.
- Added an official-key mapping registry requiring evidence for every mapped requirement, chance and prerequisite key.
- Added strict chance-aware key-equivalence validation for missions promoted to fully canonical.
- Added aggregate diagnostics that report every promoted mission identity or mapping failure in one run.
- Added offline coverage reconciliation so canonical batches update official/canonical match counts without redownloading the source feed.
- Added an evidence-safe candidate analyser across the complete retained official catalogue.
- Added a ranked official-key mapping backlog with retained Actions artifacts.
- The analysers resolve relationship IDs, create collision-free paths for duplicate names and block overlays, unsupported service families, patients, personnel and unresolved relationships.
- Fully canonicalized 226 missions across 30 Fire and Rescue batches.
- Batch 1: IDs `0`, `1`, `2`, `3`, `4`, `6`, `7`, `8`, `9`, `10`, `11`.
- Batch 2: IDs `13`, `14`, `15`, `16`, `17`, `18`, `19`, `23`, `24`, `27`.
- Batch 3: IDs `32`, `58`, `65`, `202`, `203`, `313`, `334`, `352`, `365`, `366`, `388`, `399`, `400`, `421`, `435`, `468`, `472`, `475`, `535`, `541`, `570`, `577`, `624`, `638`, `668`, `772`, `857`, `858`.
- Batch 4: IDs `21`, `22`, `31`, `301`, `353`.
- Batch 5: IDs `232`, `236`, `317`, `401`, `481`, `482`, `513`, `517`, `575`, `597`, `669`, `849`, `850`, `851`, `852`.
- Batch 6: IDs `59`, `139`, `314`, `404`, `815`, `824`.
- Batch 7: IDs `107`, `153`, `175`, `178`, `248`, `249`, `250`, `402`, `406`.
- Batch 8: IDs `169`, `177`, `243`, `244`, `256`, `518`.
- Batch 9: IDs `180`, `251`, `469`.
- Batch 10: IDs `134`, `579`.
- Batch 11: IDs `30`.
- Batch 12: IDs `12`.
- Batch 13: IDs `127`, `392`, `419`, `440`, `441`, `466`, `476`, `477`, `670`, `682`, `775`, `841`.
- Batch 14: IDs `703`.
- Batch 15: IDs `420`.
- Batch 16: IDs `734`, `735`.
- Batch 17: IDs `20`, `25`, `64`, `75`, `108`, `168`, `171`, `204`, `241`, `255`, `268`, `315`, `320`, `323`, `324`, `325`, `326`, `327`, `328`, `330`, `333`, `362`, `367`, `369`, `371`, `372`, `373`, `375`, `396`, `397`, `422`, `423`, `470`, `473`, `514`, `515`, `516`, `606`, `607`, `626`, `639`, `662`, `666`, `667`, `678`, `683`, `685`, `686`, `723`, `724`, `725`, `727`, `774`, `798`, `804`, `840`, `847`, `856`.
- Batch 18: IDs `149`, `189`, `233`, `242`, `394`, `398`, `403`.
- Batch 19: IDs `527`, `528`, `602`, `704`.
- Batch 20: IDs `408`, `409`, `410`.
- Batch 21: IDs `72`, `805`, `823`.
- Batch 22: IDs `749`, `793`, `794`, `795`.
- Batch 23: IDs `507`, `519`, `828`.
- Batch 24: IDs `300`.
- Batch 25: IDs `625`, `677`, `718`.
- Batch 26: IDs `29`, `69`, `73`, `90`, `126`, `128`, `129`, `130`, `131`, `133`, `322`, `393`, `442`, `443`, `444`, `451`, `467`, `478`, `484`, `485`.
- Batch 27: IDs `687`, `688`, `717`, `733`.
- Batch 28: IDs `806`.
- Batch 29: IDs `810`.
- Batch 30: IDs `565`.

- Added verified Aerial Appliance Truck and Fire Officer requirement and chance mappings.
- Added a verified mapping from `heavy_rescue_vehicles` to the UK Rescue Support Vehicle, including same-key probability handling.
- Preserved requirement probabilities as canonical probabilistic resources instead of flattening them into guaranteed responses.
- Removed 15 provisional Batch 4 records after aggregate identity validation proved that their assumed IDs belonged to different current UK missions.
- Corrected Chimney fire to the published 1,900-credit average and Roof fire expansion relationship.
- Promoted all 15 records generated by the evidence-safe candidate analyser after Batch 4.
- Promoted all six exact records unlocked by the Rescue Support Vehicle mapping.
- Confirmed all 226 promoted missions pass exact official identity and strict key equivalence.
- Exhausted the current mapping contract again: zero further candidates are immediately safe without another official-key mapping.
- Expanded the canonical mission collection from 62 to 284 records.
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
- Added aggregate promoted-mission diagnostics and official-to-canonical key mapping validation to every publication path.
- Added candidate and key-backlog reports with retained Actions artifacts.
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
