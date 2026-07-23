<div align="center">

<img src="assets/readme/mission-control-hero.svg" alt="MissionChief UK Operations Intelligence Platform" width="100%">

<br>

[![Open Command Centre](https://img.shields.io/badge/OPEN-COMMAND_CENTRE-1593D1?style=for-the-badge&logo=googlemaps&logoColor=white)](https://conroy1988.github.io/MissionChief-UK/)
[![Release](https://img.shields.io/badge/RELEASE-v1.1.0-1675A9?style=for-the-badge)](docs/releases/v1.1.0.md)
[![Stage](https://img.shields.io/badge/PROGRAMME-STAGE_34_COMPLETE-D63345?style=for-the-badge)](#-production-command-posture)
[![API](https://img.shields.io/badge/STATIC_API-v1.1.0-0B1D31?style=for-the-badge&logo=json&logoColor=white)](https://conroy1988.github.io/MissionChief-UK/api/)

[![Validate guide](https://github.com/Conroy1988/MissionChief-UK/actions/workflows/validate.yml/badge.svg)](https://github.com/Conroy1988/MissionChief-UK/actions/workflows/validate.yml)
[![Deploy Pages](https://github.com/Conroy1988/MissionChief-UK/actions/workflows/deploy-pages.yml/badge.svg)](https://github.com/Conroy1988/MissionChief-UK/actions/workflows/deploy-pages.yml)
[![Issues](https://img.shields.io/github/issues/Conroy1988/MissionChief-UK?label=INTELLIGENCE%20QUEUE&color=d63345)](https://github.com/Conroy1988/MissionChief-UK/issues)
[![Licence](https://img.shields.io/github/license/Conroy1988/MissionChief-UK?color=1593D1)](LICENSE)

### **Mission control for the United Kingdom game. Not another loose collection of tips.**

**1,062 official UK missions · 79 canonical mission records · 21 fully canonical missions · Instant command search · Fleet planning · Evidence governance · Versioned public data**

[**Command Centre**](https://conroy1988.github.io/MissionChief-UK/) · [**Complete Mission Lookup**](https://conroy1988.github.io/MissionChief-UK/tools/mission-lookup/) · [**Verification Status**](https://conroy1988.github.io/MissionChief-UK/reference/mission-verification-status/) · [**Fleet Planner**](https://conroy1988.github.io/MissionChief-UK/tools/fleet-planner/) · [**Resource Comparison**](https://conroy1988.github.io/MissionChief-UK/tools/resource-comparison/) · [**Static API**](https://conroy1988.github.io/MissionChief-UK/api/) · [**v1.1.0 Notes**](docs/releases/v1.1.0.md)

</div>

---

# 🚨 Mission Briefing

**MissionChief UK** is an independent operations-intelligence platform for the United Kingdom version of MissionChief.

It combines a complete official mission catalogue, conservative canonical records, browser-side command tools, strict validation and read-only public data. It is designed to answer operational questions without pretending that unknown game data is verified.

| Command question | Platform answer |
|---|---|
| What missions exist in the UK game? | Search the complete **1,062-record official UK catalogue**. |
| What does a mission require? | Read official requirement keys and use canonical mappings where they have been verified. |
| What unlocks the incident? | Inspect published prerequisites, buildings, extensions, personnel and specialist capabilities. |
| What is fully verified? | Use the five-gate verification programme and inspect the current fully canonical count. |
| What remains uncertain? | Evidence badges separate fully canonical, partially mapped and official-only source records. |
| Can another tool consume the data? | Use the versioned Static API and lossless official catalogue endpoints. |

> **Command principle:** information is operational only when it is easy to find, precise enough to act on and explicit about what is not yet known.

---

# 📡 Production Command Posture

The numbered programme is complete through **Stage 34**. MissionChief UK **v1.1.0** adds a complete official-data layer and a measurable route to 100% fully canonical mission intelligence without weakening the evidence standard.

| Intelligence domain | v1.1.0 baseline | Operational result |
|---|---:|---|
| **Official UK missions** | **1,062** | Complete searchable public UK mission catalogue with every published field retained |
| **Canonical missions** | **79** | Higher-trust normalized requirements, probabilities, alternatives, patients and preconditions |
| **Official/canonical ID matches** | **62** | Official records linked directly to canonical evidence |
| **Fully canonical missions** | **21** | Missions that passed identity, key mapping, operational and final evidence-completeness gates |
| **Official records awaiting canonical records** | **1,000** | Fully searchable source records whose internal keys remain visible and unguessed |
| **Canonical-only overlays** | **17** | Derived or overlay records without a standalone official mission ID |
| **Canonical resources** | **46** | Vehicles, boats, trailers, specialist equipment and deployment metadata |
| **Infrastructure** | **18** | Buildings and extensions enforced through schema-controlled references |
| **Qualifications** | **11** | Operational roles with unsupported course details deliberately omitted |
| **Canonical searchable entities** | **154** | Global command palette across missions, resources, infrastructure and training |
| **Public interface** | **Static API v1.1.0** | Versioned canonical exports plus separate complete official catalogue and verification endpoints |
| **Quality assurance** | **Cross-browser** | Chromium, Firefox, iPhone WebKit and iPad WebKit acceptance |

> [!IMPORTANT]
> **Official does not automatically mean canonically mapped.** The official catalogue proves that a mission and its published fields exist. Canonical dispatch interpretation is applied only where internal keys and semantics have been reproduced or suitably verified.

---

# 💯 Mission Verification Programme

Every official mission progresses through five enforced gates:

1. **Captured** — retained losslessly from the official UK feed.
2. **Identity verified** — official ID and exact UK name match a canonical record.
3. **Requirements mapped** — every requirement, chance and prerequisite key is verified or narrowly classified as non-operational.
4. **Operationally verified** — probabilities, patients, personnel, relationships, variants and conditional mechanics have reproducible evidence.
5. **Fully canonical** — final evidence-completeness audit passed.

Current progress:

| Verification gate | Current position |
|---|---:|
| Captured | **1,062 / 1,062 — 100%** |
| Identity verified | **62 / 1,062 — 5.84%** |
| Fully canonical | **21 / 1,062 — 1.98%** |
| Remaining to fully canonical | **1,041** |

Batch 1 established **11 fully canonical missions**. Batch 2 adds ten more, taking the current total to **21 fully canonical missions**.

The first two fully canonical batches cover IDs `0`, `1`, `2`, `3`, `4`, `6`, `7`, `8`, `9`, `10`, `11`, `13`, `14`, `15`, `16`, `17`, `18`, `19`, `23`, `24` and `27`.

[Review the live verification backlog →](https://conroy1988.github.io/MissionChief-UK/reference/mission-verification-status/)

---

# 🔎 Complete UK Mission Lookup

Mission Lookup combines two evidence tiers in one interface:

| Evidence tier | What it contains | How it is shown |
|---|---|---|
| **Canonical mapped** | 79 normalized project records | Verified resources, alternatives, probabilities, patients, personnel and preconditions where supported |
| **Official UK catalogue** | 1,062 public MissionChief UK records | Official fields and internal keys reproduced verbatim, with canonical mapping status made explicit |

Search covers:

- mission IDs and names;
- aliases, POIs and mission categories;
- service or generator filters;
- official requirement and probability keys;
- generation prerequisites;
- patients, personnel and qualifications;
- duration and seasonal availability;
- follow-up, expansion and subsequent missions;
- base mission IDs, overlays, additive overlays and variants; and
- every additional or newly introduced official field through the complete-record viewer.

The UI renders the first 100 matching cards for speed, while every official record remains searchable.

[Launch the complete UK Mission Lookup →](https://conroy1988.github.io/MissionChief-UK/tools/mission-lookup/)

---

# ⌨️ Command Surface

| Command route | Purpose |
|---|---|
| **Global Command Search** | Press `Ctrl+K`, `⌘K` or `/` to search all canonical collections from any page |
| **Mission Lookup** | Search the complete official catalogue and canonical mission evidence |
| **Verification Status** | Inspect every mission's current evidence gate, blockers and next action |
| **Resource Comparison** | Compare canonical vehicles and qualifications without hiding unknown fields |
| **Concurrent Fleet Planner** | Multiply guaranteed canonical requirements across simultaneous incidents |
| **Query Catalogue** | Match ordinary words and short questions against the canonical search index |
| **Official Mission Catalogue Reference** | Review source provenance, captured fields, refresh controls and accuracy boundaries |
| **Static Data API** | Consume versioned canonical JSON, generated FAQ, verification status and OpenAPI metadata |

All tools are browser-side and read-only. They do not authenticate against, access or modify a MissionChief account.

---

# 🗂️ Data Estate

```text
data/
├── uk/
│   ├── missions/                       79 canonical mission records
│   ├── mission-verification-registry.json
│   ├── official-key-mappings.json
│   ├── vehicles/                       46 canonical deployable resources
│   ├── infrastructure/                 18 buildings and extensions
│   └── training/                       11 qualification records
└── sources/
    └── missionchief-uk/
        ├── einsaetze.raw.json
        ├── mission-coverage.json
        ├── mission-verification-status.json
        └── official-key-inventory.json
```

Canonical public exports:

```text
docs/assets/data/v1/
├── manifest.json
├── missions.json
├── vehicles.json
├── infrastructure.json
├── training.json
├── search-index.json
├── faq.json
└── openapi.json
```

Complete official UK catalogue exports:

```text
docs/assets/data/official/
├── uk-missions.json
├── uk-mission-coverage.json
└── uk-mission-verification.json
```

The official browser catalogue preserves every source field and adds only `official_url`, `limited_availability` and normalized availability dates.

---

# 🧠 Evidence Contract

| Marker | Classification | Operational meaning |
|:---:|---|---|
| ✅ | **Verified** | Reproduced in the current UK game or supported by a suitable primary source |
| 🧮 | **Calculated** | Derived transparently from verified values with the method retained |
| 🎯 | **Recommended** | Strategic guidance that may vary by account, geography or play style |
| ⚠️ | **Review required** | Incomplete, contradictory, outdated or awaiting reproduction |
| 📡 | **Official catalogue** | Published by the UK mission feed but not necessarily normalized into canonical resources |

The platform never silently converts omitted values into zero, false or “not required”. Internal official keys remain visible until their UK meaning can be mapped safely.

---

# 🔄 Official Catalogue Maintenance

The dedicated refresh workflow checks the public UK mission feed every day and can also be run manually.

```text
Official UK feed
      ↓
JSON, ID and minimum-size validation
      ↓
SHA-256 source comparison
      ↓
Offline canonical coverage reconciliation
      ↓
Verified official-key mapping audit
      ↓
Lossless browser publication
      ↓
100% verification backlog regeneration
      ↓
Commit only when generated source state changed
      ↓
Dispatch Pages deployment and cross-browser acceptance
```

An unchanged source digest and unchanged verification state produce no commit and no deployment churn.

The offline audits verify:

- more than 1,000 official records;
- unique IDs and non-empty names;
- deterministic ordering;
- raw/public field equality;
- source URL, timestamp and SHA consistency;
- canonical match and gap arithmetic;
- official-key inventories;
- promoted mission key equivalence;
- exact verification stages, blockers and next actions;
- compact-file limits; and
- built-site equality with generated source assets.

---

# 🛡️ Validation Pipeline

```text
Canonical JSON schemas and relationships
        ↓
Offline official/canonical coverage reconciliation
        ↓
Complete official catalogue audit
        ↓
Official-to-canonical key mapping audit
        ↓
100% mission verification status generation
        ↓
Deterministic exports and generated FAQ
        ↓
Release-readiness, links and anchors
        ↓
Strict MkDocs build and built-site audit
        ↓
All JavaScript syntax checks
        ↓
Chromium acceptance against the built site
        ↓
GitHub Pages deployment
        ↓
Live HTTP and public-data smoke tests
        ↓
Chromium, Firefox, iPhone WebKit and iPad WebKit acceptance
        ↓
Versioned GitHub release
```

Local verification:

```bash
pip install -r requirements.txt
python scripts/validate_data.py
python scripts/reconcile_official_mission_coverage.py
python scripts/validate_official_mission_catalogue.py
python scripts/validate_official_key_mappings.py
python scripts/generate_mission_verification_status.py
python scripts/generate_exports.py
python scripts/generate_faq.py
python scripts/release_readiness.py
python scripts/audit_links.py
mkdocs build --strict --site-dir site
python scripts/release_readiness.py --site-dir site
npm install --no-audit --no-fund
npx playwright install --with-deps
for file in docs/javascripts/*.js; do node --check "$file"; done
npm run test:e2e
```

[Review the complete QA gates →](docs/quality-assurance.md)

---

# 🧭 Entry Points

| You are… | Begin here |
|---|---|
| **A new UK player** | [Start Here](https://conroy1988.github.io/MissionChief-UK/getting-started/) |
| **Searching for any UK mission** | [Complete Mission Lookup](https://conroy1988.github.io/MissionChief-UK/tools/mission-lookup/) |
| **Checking verification progress** | [Mission Verification Status](https://conroy1988.github.io/MissionChief-UK/reference/mission-verification-status/) |
| **Planning several incidents** | [Concurrent Fleet Planner](https://conroy1988.github.io/MissionChief-UK/tools/fleet-planner/) |
| **Comparing specialist capability** | [Resource Comparison](https://conroy1988.github.io/MissionChief-UK/tools/resource-comparison/) |
| **Understanding source accuracy** | [Official Mission Catalogue](docs/reference/official-mission-catalogue.md) and [Data Standard](docs/reference/data-standard.md) |
| **Building an integration** | [Static API](https://conroy1988.github.io/MissionChief-UK/api/) and [Generated Exports](docs/reference/data-exports.md) |
| **Submitting evidence** | [Contribution Standard](docs/contributing/index.md) and [Verification Workflow](docs/contributing/verification-workflow.md) |

---

# 🤝 Contribute

Useful contributions include reproducible mission requirements, screenshots or primary-source links, internal-key mappings, vehicle economics, staffing evidence, qualification details, accessibility findings and failures in any generated tool or endpoint.

Every accepted change should leave the platform more precise—not merely larger.

[Open an issue](https://github.com/Conroy1988/MissionChief-UK/issues/new/choose) · [Read the research checklist](docs/contributing/research-checklist.md) · [Review the roadmap](docs/ROADMAP.md)

---

# ⚖️ Independence

MissionChief UK is an independent community project created and maintained by [Conroy1988](https://github.com/Conroy1988). It is **not operated by, endorsed by or affiliated with SHPlay GmbH or the official MissionChief team**.

MissionChief names, trademarks, screenshots, game artwork and third-party materials remain the property of their respective owners. Original project code and content are released under the [MIT Licence](LICENSE), unless a file states otherwise.

<div align="center">

## 🚨 **Build the knowledge. Verify the intelligence. Command the game.**

[![Enter the Command Centre](https://img.shields.io/badge/ENTER_THE-COMMAND_CENTRE-1593D1?style=for-the-badge&logo=googlemaps&logoColor=white)](https://conroy1988.github.io/MissionChief-UK/)

</div>
