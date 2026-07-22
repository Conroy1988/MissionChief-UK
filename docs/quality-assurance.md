# Quality Assurance

MissionChief UK uses layered validation so structured data, generated exports, documentation and interactive tools are checked before and after deployment.

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
- generated FAQ, API guide and release notes;
- absence of JavaScript exceptions and first-party HTTP failures;
- responsive content without page-level horizontal overflow;
- mission lookup loading and filtering;
- resource and qualification comparison;
- concurrent fleet multiplication;
- deterministic query-catalogue results;
- MkDocs Material instant-navigation reinitialisation;
- all eight static API endpoints and their cross-file counts;
- critical WCAG A/AA violations on the main interactive surfaces.

The deterministic documentation audit additionally checks:

- relative Markdown links;
- local HTML `href` and `src` references;
- GitHub Pages URLs that point back into this project;
- MkDocs page-route resolution for both `page.md` and `page/index.md` layouts;
- local heading anchors in README, changelog and documentation pages.

External websites are not treated as deterministic build dependencies because availability, anti-bot controls and redirects can change independently of this repository. Official evidence URLs remain recorded in the production data and are reviewed through the evidence-maintenance process.

## Validation layers

```text
Canonical JSON records
        ↓
Schema and referential validation
        ↓
Generated exports and FAQ
        ↓
Repository/API readiness audit
        ↓
Documentation link and anchor audit
        ↓
Strict MkDocs build
        ↓
Chromium acceptance against the built site
        ↓
GitHub Pages deployment
        ↓
HTTP/API smoke test
        ↓
Chromium, Firefox, iPhone WebKit and iPad WebKit acceptance
```

A failed post-deployment browser test marks the Pages workflow as failed and prevents automated release publication.

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

Run the deterministic repository checks:

```bash
python scripts/validate_data.py
python scripts/generate_exports.py
python scripts/generate_faq.py
python scripts/release_readiness.py
python scripts/audit_links.py
mkdocs build --strict --site-dir site
python scripts/release_readiness.py --site-dir site
```

Install browser-test dependencies and browser binaries:

```bash
npm install
npx playwright install --with-deps
```

Run against the public site:

```bash
npm run test:e2e
```

Run one browser project:

```bash
npm run test:e2e -- --project=chromium-desktop
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
- poor mobile networks;
- subjective readability and visual-design preferences.
