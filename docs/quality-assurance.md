# Quality Assurance

MissionChief UK uses layered validation so canonical records, the complete official UK mission catalogue, generated exports, documentation and browser tools are checked before and after deployment.

## Browser coverage

The Playwright acceptance suite runs against:

| Project | Engine | Operational target |
|---|---|---|
| `chromium-desktop` | Chromium | Desktop Chrome-class browsers |
| `firefox-desktop` | Firefox | Desktop Firefox |
| `webkit-iphone` | WebKit | iPhone-sized iOS Safari behaviour |
| `webkit-ipad` | WebKit | iPad-sized Safari behaviour |

Playwright device profiles emulate viewport, touch, mobile mode and user-agent behaviour. They do not replace occasional checks on physical Apple hardware.

## Acceptance coverage

The suite verifies:

- Command Centre and every public intelligence-tool route;
- generated FAQ, API guide, official-catalogue reference and release notes;
- absence of JavaScript exceptions and first-party HTTP failures;
- responsive content without page-level horizontal overflow;
- canonical mission lookup loading and filtering;
- complete official UK mission-catalogue availability;
- more than 1,000 unique official mission records;
- source SHA-256 and reconciliation arithmetic;
- official-only mission search and canonical mission search;
- separate Canonical mapped and Official UK catalogue evidence states;
- structured patient, personnel, duration, variant and relationship fields;
- complete official record display;
- one shared official-catalogue browser request per page lifecycle;
- resource and qualification comparison;
- concurrent fleet multiplication;
- deterministic query-catalogue results;
- the global command palette opening through `Ctrl+K` or `⌘K`;
- command-palette search against the generated canonical search index;
- collection filtering, keyboard closure and mission-result deep linking;
- iPhone viewport operation of the command palette;
- MkDocs Material instant-navigation reinitialisation;
- all eight canonical Static API endpoints and their cross-file counts;
- the two complete official-catalogue endpoints; and
- critical WCAG A/AA violations on the main interactive surfaces.

The deterministic documentation audit additionally checks:

- relative Markdown links;
- local HTML `href` and `src` references;
- GitHub Pages URLs that point back into this project;
- MkDocs page-route resolution for both `page.md` and `page/index.md` layouts; and
- local heading anchors in README, changelog and documentation pages.

External websites are not ordinary build dependencies. The official UK mission feed is accessed only by its dedicated refresh workflow, not by routine validation or deployment. The committed source snapshot makes normal CI deterministic and protects deployment from transient upstream failures.

## Official catalogue integrity

The offline catalogue auditor checks:

- all required source and browser assets exist;
- the official source contains at least 1,000 missions;
- every mission has a unique ID and non-empty name;
- records are ordered deterministically by mission ID;
- compact tracked files remain below repository-content limits;
- source URL, timestamp and SHA-256 metadata agree across all outputs;
- every official source field is preserved in the public browser catalogue;
- only the documented navigation fields are derived;
- canonical match, official-only and canonical-only counts are correct;
- reconciliation lists are complete and correctly ordered;
- canonical/official name mismatches are current;
- requirement, chance and prerequisite inventories are current; and
- built official assets are byte-equivalent in meaning to their committed source files.

The source-refresh workflow is content-addressed. An unchanged source SHA produces no commit. A changed source must pass importer validation, lossless publication, compaction and the offline audit before it can be committed and deployed.

## Validation layers

```text
Canonical JSON records
        ↓
Schema and referential validation
        ↓
Committed official UK catalogue
        ↓
Losslessness, checksum and reconciliation audit
        ↓
Generated canonical exports and FAQ
        ↓
Repository/API readiness audit
        ↓
Documentation link and anchor audit
        ↓
Strict MkDocs build and built-site equality checks
        ↓
All JavaScript syntax validation
        ↓
Chromium acceptance against the built site
        ↓
Catalogue, command-palette, deep-link and mobile acceptance
        ↓
GitHub Pages deployment
        ↓
HTTP, canonical API and official-data smoke tests
        ↓
Chromium, Firefox, iPhone WebKit and iPad WebKit acceptance
```

A failed post-deployment browser test marks the Pages workflow as failed and prevents automated release publication.

## Command-search trust boundary

The global command palette remains a read-only interface over `assets/data/v1/search-index.json`. It searches the canonical collections and must:

- load only the generated first-party canonical search index;
- expose no arbitrary HTML from data records;
- escape record content before rendering;
- avoid MissionChief authentication and account access;
- preserve omitted values as unknown;
- link mission records into Mission Lookup using an encoded query; and
- link other collections into Query Catalogue using the same encoded-query contract.

Mission Lookup additionally consumes the separate official catalogue. Official internal keys are reproduced verbatim and are not silently converted into canonical vehicle, personnel or infrastructure mappings.

## Failure diagnostics

Failed browser runs upload an Actions artifact containing:

```text
playwright-report/
test-results/
```

Depending on the failure, this can include:

- HTML test report;
- Playwright trace;
- screenshot;
- retained video;
- console and network failure details.

Artifacts are retained for 14 days.

Link-audit failures are printed directly in the Actions log using this format:

```text
source-file.md:line: missing local target or anchor
```

## Local execution

Run deterministic repository checks:

```bash
python scripts/validate_data.py
python scripts/validate_official_mission_catalogue.py
python scripts/generate_exports.py
python scripts/generate_faq.py
python scripts/release_readiness.py
python scripts/audit_links.py
mkdocs build --strict --site-dir site
python scripts/release_readiness.py --site-dir site
```

Validate every browser-side script:

```bash
for file in docs/javascripts/*.js; do node --check "$file"; done
```

Install browser-test dependencies and browser binaries:

```bash
npm install --no-audit --no-fund
npx playwright install --with-deps
```

Run the complete suite against the public site:

```bash
npm run test:e2e
```

Run one browser project:

```bash
npm run test:e2e -- --project=chromium-desktop
```

Run only the complete official-catalogue acceptance specification:

```bash
npm run test:e2e -- tests/e2e/official-mission-catalogue.spec.mjs
```

Run only the command-palette acceptance specification:

```bash
npm run test:e2e -- tests/e2e/command-palette.spec.mjs
```

Run against another deployment or local server:

```bash
MCUK_BASE_URL=http://127.0.0.1:8000/ npm run test:e2e
```

On Windows PowerShell:

```powershell
$env:MCUK_BASE_URL = "http://127.0.0.1:8000/"
npm run test:e2e
```

## Scope boundary

Automated tests can detect repeatable browser, accessibility, network and data-contract defects. They cannot fully reproduce:

- every physical iPhone or iPad model;
- assistive-technology combinations;
- unusual browser extensions or content blockers;
- poor mobile networks; or
- subjective readability and visual-design preferences.
