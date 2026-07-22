<div align="center">

<img src="assets/readme/mission-control-hero.svg" alt="MissionChief UK Command Knowledge Centre" width="100%">

<br>

[![Documentation](https://img.shields.io/badge/OPEN-DOCUMENTATION-1593D1?style=for-the-badge&logo=readthedocs&logoColor=white)](https://conroy1988.github.io/MissionChief-UK/)
[![MissionChief UK](https://img.shields.io/badge/REGION-UNITED_KINGDOM-0B1D31?style=for-the-badge)](https://www.missionchief.co.uk/)
[![Evidence Standard](https://img.shields.io/badge/INTELLIGENCE-EVIDENCE_LED-1675A9?style=for-the-badge&logo=databricks&logoColor=white)](docs/reference/data-standard.md)
[![Project Stage](https://img.shields.io/badge/STATUS-STAGE_34_COMPLETE-D63345?style=for-the-badge)](#current-operational-state)

[![Deploy MissionChief UK Guide](https://github.com/Conroy1988/MissionChief-UK/actions/workflows/deploy-pages.yml/badge.svg)](https://github.com/Conroy1988/MissionChief-UK/actions/workflows/deploy-pages.yml)
[![Validate guide](https://github.com/Conroy1988/MissionChief-UK/actions/workflows/validate.yml/badge.svg)](https://github.com/Conroy1988/MissionChief-UK/actions/workflows/validate.yml)
[![Release](https://img.shields.io/github/v/release/Conroy1988/MissionChief-UK?style=flat-square&label=release)](https://github.com/Conroy1988/MissionChief-UK/releases/latest)
[![Last Commit](https://img.shields.io/github/last-commit/Conroy1988/MissionChief-UK?style=flat-square)](https://github.com/Conroy1988/MissionChief-UK/commits/main)
[![Issues](https://img.shields.io/github/issues/Conroy1988/MissionChief-UK?style=flat-square)](https://github.com/Conroy1988/MissionChief-UK/issues)
[![Licence](https://img.shields.io/github/license/Conroy1988/MissionChief-UK?style=flat-square)](LICENSE)

### The independent UK command knowledgebase for MissionChief

**Verified missions · Canonical resources · Infrastructure · Qualifications · Intelligence tools · Static API**

[**Enter Command Centre**](https://conroy1988.github.io/MissionChief-UK/) · [**Mission Lookup**](docs/tools/mission-lookup.md) · [**Fleet Planner**](docs/tools/fleet-planner.md) · [**Static API**](docs/api/index.md) · [**v1.0.0 Notes**](docs/releases/v1.0.0.md) · [**Contribute**](docs/contributing/index.md)

</div>

---

# 🚨 Mission Briefing

**MissionChief UK** is an independent, searchable and machine-readable knowledge centre for the United Kingdom version of MissionChief.

The project combines practical operational guides with canonical data, explicit evidence metadata, browser-side planning tools and versioned public exports. Unsupported values are omitted rather than presented as facts.

> **Command principle:** useful information must be easy to find, current enough to trust and precise enough to act on.

---

# 📡 Current Operational State

The numbered core programme is complete through **Stage 34**.

```text
62 verified mission records
46 canonical vehicle-resource records
18 canonical infrastructure records
11 qualification records
11 represented operational service groups
13 published mission-data batches
Static data API v1.0.0
```

| Domain | State | Delivered capability |
|---|---|---|
| **Documentation** | Operational | MkDocs Material, instant search, structured navigation and GitHub Pages |
| **Mission data** | Live | Preconditions, variants, resources, personnel, patients, prisoners, towing and rewards |
| **Vehicle data** | Live | Canonical labels, capabilities, deployment metadata and first verified economics set |
| **Infrastructure** | Live | 18 schema-controlled buildings/extensions with referential enforcement |
| **Qualifications** | Live | 11 role records with course details omitted unless directly verified |
| **Railway response** | Populated baseline | Railway Police, Railway fire response, rail resources and mission Batch 10 |
| **Bomb Disposal** | Expanded baseline | Coastal, railway and construction-site progression through Batch 11 |
| **Airfield Operations** | Expanded baseline | Codes A–F coverage, Hot Brakes and hangar fire through Batch 12 |
| **Recovery** | Expanded baseline | Cars, motorbikes, buses, caravans, HGVs and major collisions through Batch 13 |
| **Intelligence tools** | Live | Mission lookup, comparison, concurrent fleet planning and query catalogue |
| **Public API** | Live | Versioned JSON collections, manifest, search index, FAQ and OpenAPI contract |

> [!IMPORTANT]
> `verified` applies only to populated fields. An omitted value is unknown, not zero. Empty response arrays may represent directory-level evidence where the individual response table was unavailable.

## Delivery progression

```text
STAGES 01–12  Foundation, schemas, verification, contribution and delivery
STAGES 13–20  Core Fire, Ambulance, Police, maritime, mountain, SAR, EOD,
              airfield and recovery production data
STAGE 21      Railway Police and Railway Fire Response
STAGE 22      Specialist infrastructure catalogue
STAGE 23      Production qualification records
STAGE 24      Vehicle economics and staffing model
STAGE 25      Bomb Disposal enrichment
STAGE 26      Airfield Operations enrichment
STAGE 27      Recovery and HGV Recovery enrichment
STAGE 28      Generated public exports
STAGE 29      Mission requirement lookup
STAGE 30      Resource and qualification comparison
STAGE 31      Concurrent fleet planner
STAGE 32      Natural-language query catalogue
STAGE 33      Generated FAQ
STAGE 34      Static Data API v1
```

---

# 🗂️ Verified Data Programme

## Production collections

```text
data/uk/missions/         62 records
data/uk/vehicles/         46 records
data/uk/infrastructure/   18 records
data/uk/training/         11 records
```

The validator enforces:

- Draft 2020-12 schema conformance;
- unique identifiers and valid verification dates;
- mission-to-resource referential integrity;
- mapped infrastructure-precondition integrity;
- guaranteed, probabilistic, conditional and alternative requirements;
- patient, towing and personnel-range semantics;
- qualification-record conformance.

## Generated public exports

Every validation and Pages build generates:

```text
assets/data/v1/
├── manifest.json
├── missions.json
├── vehicles.json
├── infrastructure.json
├── training.json
├── search-index.json
├── faq.json
└── openapi.json
```

[Read the export contract →](docs/reference/data-exports.md)  
[Open the API guide →](docs/api/index.md)

---

# 🧠 Intelligence Tools

| Tool | Purpose |
|---|---|
| **Mission Lookup** | Search IDs, names, aliases, POIs and mission types |
| **Resource Comparison** | Compare vehicle economics, staffing, training and capabilities |
| **Qualification Comparison** | Compare verified role and course fields |
| **Concurrent Fleet Planner** | Multiply guaranteed requirements across simultaneous incidents |
| **Query Catalogue** | Deterministic natural-language matching across all collections |
| **Generated FAQ** | Build-time counts and evidence-policy answers |

All tools are read-only and consume the validated versioned exports. They do not access or modify a MissionChief account.

---

# ⚡ Rapid Access

| Route | Use it for | Access |
|---|---|---|
| **Start Here** | Account setup and early progression | [Open guide →](docs/getting-started/index.md) |
| **Emergency Services** | Service-specific operational references | [Browse services →](docs/services/index.md) |
| **Verified Vehicles** | Canonical deployable-resource records | [Open records →](docs/reference/verified-vehicle-records.md) |
| **Verified Missions** | Cross-service mission records | [Open records →](docs/reference/verified-mission-records.md) |
| **Railway Response** | Railway Police, rail resources and incidents | [Open guide →](docs/services/railway-response.md) |
| **Mission Lookup** | Search current mission requirements | [Open tool →](docs/tools/mission-lookup.md) |
| **Fleet Planner** | Model concurrent guaranteed requirements | [Open tool →](docs/tools/fleet-planner.md) |
| **Static API** | Consume versioned JSON data | [Open API →](docs/api/index.md) |
| **Release Notes** | Review the v1.0.0 production baseline | [Open notes →](docs/releases/v1.0.0.md) |
| **Community Verification** | Submit reproducible UK evidence | [Open workflow →](docs/contributing/verification-workflow.md) |

---

# 🧠 Evidence Classification

| Marker | Classification | Definition |
|:---:|---|---|
| ✅ | **Verified** | Reproduced in the current UK game or confirmed through a suitable primary source |
| 🧮 | **Calculated** | Derived from verified values with the method documented |
| 🎯 | **Recommended** | Strategic guidance that varies by account, geography or play style |
| ⚠️ | **Review required** | Incomplete, contradictory, outdated or awaiting reproduction |

[Read the data and evidence standard →](docs/reference/data-standard.md)

---

# ✅ Validation and Delivery

```text
JSON syntax and schemas
        ↓
Relationship and range validation
        ↓
Versioned exports and generated FAQ
        ↓
Repository and API readiness audit
        ↓
JavaScript syntax validation
        ↓
MkDocs strict build and built-site audit
        ↓
GitHub Pages deployment
        ↓
Live site and public API smoke test
        ↓
Versioned GitHub release
```

Local validation:

```bash
pip install -r requirements.txt
python scripts/validate_data.py
python scripts/generate_exports.py
python scripts/generate_faq.py
python scripts/release_readiness.py
node --check docs/javascripts/intelligence-tools.js
mkdocs build --strict --site-dir site
python scripts/release_readiness.py --site-dir site
```

---

# ⚖️ Independence and Attribution

This is an independent community project created and maintained by [Conroy1988](https://github.com/Conroy1988). It is **not operated by, endorsed by or affiliated with SHPlay GmbH or the official MissionChief team**.

MissionChief names, trademarks, screenshots, game artwork and third-party materials remain the property of their respective owners. Original project code and content are released under the [MIT Licence](LICENSE), unless a file states otherwise.

<div align="center">

## 🚨 **Build the knowledge. Verify the intelligence. Command the game.**

[![Enter Command Centre](https://img.shields.io/badge/ENTER_THE-COMMAND_CENTRE-1593D1?style=for-the-badge&logo=googlemaps&logoColor=white)](https://conroy1988.github.io/MissionChief-UK/)

</div>
