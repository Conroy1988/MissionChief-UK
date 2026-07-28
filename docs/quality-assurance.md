# Quality Assurance

MissionChief UK uses layered validation so canonical records, the complete official UK mission catalogue, generated exports, documentation, long-form guides and browser tools are checked before and after deployment.

## Browser coverage

| Project | Engine | Operational target |
|---|---|---|
| `chromium-desktop` | Chromium | Desktop Chrome-class browsers and complete interactive tests |
| `firefox-desktop` | Firefox | Desktop Firefox |
| `webkit-iphone` | WebKit | iPhone-sized iOS Safari behaviour |
| `webkit-ipad` | WebKit | iPad-sized Safari behaviour |

Playwright device profiles emulate viewport, touch, mobile mode and user-agent behaviour. They do not replace occasional checks on physical Apple hardware.

## Acceptance coverage

The suite verifies:

- Command Centre, Getting Started, Game Systems, every mature service guide, Strategy, Alliance Operations and every public intelligence-tool route;
- generated FAQ, API guide, official-catalogue reference and release notes;
- absence of JavaScript exceptions and first-party HTTP failures;
- responsive content without page-level horizontal overflow;
- mobile-safe long tables and code blocks;
- automatic long-page section navigation on pages with at least four major sections;
- visible keyboard focus for links, buttons, controls and section summaries;
- canonical mission lookup loading and filtering;
- complete official UK mission-catalogue availability;
- more than 1,000 unique official mission records;
- source SHA-256 and reconciliation arithmetic;
- official-only mission search and canonical mission search;
- distinct Canonical mapped and Official UK catalogue evidence states;
- structured patient, personnel, duration, variant and relationship fields;
- resource and qualification comparison;
- concurrent fleet multiplication;
- Account Readiness mission selection, protected reserve, readiness calculation and local save/load;
- deterministic query-catalogue results;
- the global command palette opening through `Ctrl+K` or `⌘K`;
- command-palette filtering, keyboard closure and mission-result deep linking;
- MkDocs Material instant-navigation reinitialisation;
- all canonical Static API endpoints and their cross-file counts; and
- critical WCAG A/AA violations on the main interactive and command surfaces.

## Content and navigation safeguards

Stage 41 adds production safeguards for the expanded long-form estate:

- `.md-content` and page bodies are constrained to the viewport;
- tables own their horizontal scrolling instead of expanding the page;
- code blocks scroll locally with touch-friendly behaviour;
- headings preserve scroll offset below the sticky header;
- focus-visible outlines are enforced across interactive content;
- a collapsed Page sections menu is generated after the title when a page has four or more `h2` sections;
- the Command Centre is excluded from generated section navigation; and
- print output omits the interactive section menu.

## Deterministic documentation audit

The repository audit checks:

- relative Markdown links;
- local HTML `href` and `src` references;
- GitHub Pages URLs pointing back into this project;
- MkDocs route resolution for both `page.md` and `page/index.md` layouts; and
- local heading anchors in README, changelog and documentation pages.

External websites are not ordinary build dependencies. The official UK mission feed is accessed only by its dedicated refresh workflow. The committed source snapshot keeps routine CI deterministic and protects deployment from transient upstream failures.

## Official catalogue integrity

The offline catalogue auditor checks:

- all required source and browser assets exist;
- the official source contains at least 1,000 missions;
- every mission has a unique ID and non-empty name;
- records are ordered deterministically by mission ID;
- source URL, timestamp and SHA-256 metadata agree across outputs;
- every official source field is preserved in the browser catalogue;
- only documented navigation fields are derived;
- canonical match, official-only and canonical-only counts are correct;
- requirement, chance and prerequisite inventories are current; and
- built official assets remain equivalent to committed source files.

The source-refresh workflow is content-addressed. An unchanged source SHA produces no commit. A changed source must pass importer validation, lossless publication, compaction and the offline audit before it can be committed and deployed.

## Validation layers

```text
Canonical JSON records
        ↓
Schema and relationship validation
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
Strict MkDocs build and built-site equality
        ↓
All JavaScript syntax validation
        ↓
Chromium interactive acceptance
        ↓
iPhone and iPad WebKit viewport acceptance
        ↓
Exact-SHA GitHub Pages deployment
        ↓
Production HTTP and API smoke tests
        ↓
Immutable release verification
```

A failed post-deployment browser or production smoke test marks the Pages workflow as failed and blocks automated release publication.

## Account Readiness trust boundary

The Account Readiness Planner:

- loads only first-party canonical versioned exports;
- calculates from canonical mission requirements and user-entered local inventory;
- treats blank values as unknown;
- subtracts explicit protected reserve;
- prevents known alternative capacity from being reused across independent groups;
- keeps towing/carrier allocation separate from response allocation;
- stores optional scenarios only in the current browser;
- imports or exports only through explicit JSON actions; and
- never authenticates against, scrapes or mutates MissionChief.

## Command-search trust boundary

The global command palette remains a read-only interface over `assets/data/v1/search-index.json`. It must escape record content, preserve omitted values as unknown, avoid account access and deep-link only through encoded first-party routes.

Mission Lookup additionally consumes the separate official catalogue. Official internal keys are reproduced verbatim and are not silently converted into canonical resource mappings.

## Failure diagnostics

Failed browser runs upload an Actions artifact containing Playwright reports and test results. Depending on the defect, this can include traces, screenshots, video, console errors and failed first-party network requests. Diagnostics are retained for 14 days.

Link-audit failures are emitted as:

```text
source-file.md:line: missing local target or anchor
```

## Local execution

Run repository and documentation checks:

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

Validate browser-side scripts:

```bash
for file in docs/javascripts/*.js; do node --check "$file"; done
```

Install and run browser acceptance:

```bash
npm install --no-audit --no-fund
npx playwright install --with-deps
npm run test:e2e
```

Run one project:

```bash
npm run test:e2e -- --project=chromium-desktop
```

Run against another deployment or local server:

```bash
MCUK_BASE_URL=http://127.0.0.1:8000/ npm run test:e2e
```

PowerShell:

```powershell
$env:MCUK_BASE_URL = "http://127.0.0.1:8000/"
npm run test:e2e
```

## Scope boundary

Automated tests cannot fully reproduce every physical device, assistive-technology combination, browser extension, poor network or subjective design preference. Repeatable data, browser, accessibility, link and layout defects are release-blocking; physical-device and qualitative reviews remain complementary checks.
