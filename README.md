<div align="center">

<img src="assets/readme/mission-control-hero.svg" alt="MissionChief UK Command Knowledge Centre" width="100%">

<br>

[![Documentation](https://img.shields.io/badge/OPEN-DOCUMENTATION-1593D1?style=for-the-badge&logo=readthedocs&logoColor=white)](https://conroy1988.github.io/MissionChief-UK/)
[![MissionChief UK](https://img.shields.io/badge/REGION-UNITED_KINGDOM-0B1D31?style=for-the-badge)](https://www.missionchief.co.uk/)
[![Evidence Standard](https://img.shields.io/badge/INTELLIGENCE-EVIDENCE_LED-1675A9?style=for-the-badge&logo=databricks&logoColor=white)](docs/reference/data-standard.md)
[![Project Stage](https://img.shields.io/badge/STATUS-STAGE_13_VERIFIED_DATA-D63345?style=for-the-badge)](#current-operational-state)

[![Deploy MissionChief UK Guide](https://github.com/Conroy1988/MissionChief-UK/actions/workflows/deploy-pages.yml/badge.svg)](https://github.com/Conroy1988/MissionChief-UK/actions/workflows/deploy-pages.yml)
[![Validate guide](https://github.com/Conroy1988/MissionChief-UK/actions/workflows/validate.yml/badge.svg)](https://github.com/Conroy1988/MissionChief-UK/actions/workflows/validate.yml)
[![Last Commit](https://img.shields.io/github/last-commit/Conroy1988/MissionChief-UK?style=flat-square)](https://github.com/Conroy1988/MissionChief-UK/commits/main)
[![Issues](https://img.shields.io/github/issues/Conroy1988/MissionChief-UK?style=flat-square)](https://github.com/Conroy1988/MissionChief-UK/issues)
[![Licence](https://img.shields.io/github/license/Conroy1988/MissionChief-UK?style=flat-square)](LICENSE)

### The independent UK command knowledgebase for MissionChief

**Game intelligence · Verified missions · Vehicle records · Strategy · Scripts · Structured data · Community verification**

[**Enter the Command Centre**](https://conroy1988.github.io/MissionChief-UK/) · [**Start Here**](docs/getting-started/index.md) · [**Verified Vehicles**](docs/reference/verified-vehicle-records.md) · [**Verified Missions**](docs/reference/verified-mission-records.md) · [**Compatibility**](docs/scripts/compatibility-centre.md) · [**Contribute**](docs/contributing/index.md)

</div>

---

# 🚨 Mission Briefing

**MissionChief UK** is an independent, searchable command knowledge centre for the United Kingdom version of MissionChief.

It is being built as a maintained information system rather than another partial wiki or loose collection of tips. The platform connects practical guides with structured, source-aware records so players can understand not only *what* to do, but *why the information can be trusted*.

The knowledgebase is designed to answer operational questions such as:

- What should I build next?
- Which vehicles, extensions, and training courses does a mission require?
- Which requirements are guaranteed and which are probabilistic?
- How should a station or specialist fleet be configured?
- Which scripts are useful, safe, maintained, and compatible with the UK game?
- How do alliances, transport, patients, prisoners, credits, and progression work?
- Which information is verified fact, calculated guidance, recommendation, or still awaiting confirmation?

> **Command principle:** useful information must be easy to find, current enough to trust, and precise enough to act on.

<table>
<tr>
<td width="25%" align="center"><strong>🔎 FIND</strong><br><sub>Search guides, aliases, missions, vehicles, buildings, and training.</sub></td>
<td width="25%" align="center"><strong>✅ VERIFY</strong><br><sub>Separate reproduced facts from calculation, advice, and uncertainty.</sub></td>
<td width="25%" align="center"><strong>🧭 PLAN</strong><br><sub>Connect progression, fleet, staffing, geography, and cost decisions.</sub></td>
<td width="25%" align="center"><strong>🛡️ RECOVER</strong><br><sub>Document safe installation, compatibility, troubleshooting, and rollback.</sub></td>
</tr>
</table>

---

# 📡 Current Operational State

The project has progressed beyond its Stage 10 architecture milestone into **Stage 13 verified-data expansion**.

The full documentation and schema architecture is established, and the repository now contains a growing verified catalogue rather than framework-only placeholders.

| Domain | Current state | Delivered capability |
|---|---|---|
| **Command Centre** | Operational | MkDocs Material site, custom MissionChief identity, instant search, structured navigation, and GitHub Pages deployment |
| **Getting started** | Active | First-expansion and account-progression pathways |
| **Game systems** | Active | Missions, dispatching, buildings, extensions, and progression architecture |
| **Service encyclopaedia** | Active | Fire, Ambulance, Police, Coastguard/Lifeboat, and specialist-service structure |
| **Vehicle reference** | Verified records live | Schema-backed records, aliases, roles, capacities, sources, and verification metadata |
| **Mission reference** | Verified batches live | Guaranteed and probabilistic requirements, rewards, unlock context, sources, and verification metadata |
| **Cross-reference integrity** | Operational | Mission resource identifiers are validated against the vehicle catalogue |
| **Dataset manifest** | Operational | UK dataset inventory and bounded publication posture |
| **Buildings reference** | Framework delivered | Buildings and extensions database specification |
| **Personnel and training** | Framework delivered | Qualification, staffing, alias, and training reference structure |
| **Planning tools** | Programme established | Calculator and decision-support architecture for later verified data |
| **Scripts and compatibility** | Operational framework | Tool catalogue, compatibility centre, browser/device posture, installation, troubleshooting, and recovery standards |
| **Community verification** | Operational framework | Evidence submissions, reproduction expectations, review workflow, and editorial controls |
| **Glossary and aliases** | Operational framework | UK terminology, alternative labels, abbreviations, and search normalisation |
| **Validation** | Operational | JSON schema validation, mission-to-vehicle reference validation, and strict MkDocs build |

> [!IMPORTANT]
> Stage 13 means verified data is now being published through the live reference pages. It does **not** claim that every UK mission, vehicle, building, training course, cost, or edge case has already been catalogued.

## Delivery progression

```text
STAGES 01–02  Foundation, scope, identity and player journey
STAGES 03–07  Vehicle, mission, building, personnel and training frameworks
STAGES 08–10  Planning tools, community verification, compatibility and recovery
STAGES 11–12  Initial verified mission and vehicle datasets with stronger schemas
STAGE 13      Dataset manifest, cross-reference integrity and published verified-data pages
```

---

# 🗂️ Verified Data Programme

## Verified vehicle records

The live vehicle catalogue now demonstrates the complete record contract with real UK resource data. Mature records can include:

- canonical identifier and display name;
- alternative names and search aliases;
- service and operational role;
- transport or capability flags;
- training and personnel implications;
- source trail and verification date; and
- evidence classification.

[Open verified vehicle records →](docs/reference/verified-vehicle-records.md)

## Verified mission records

Mission records now support both deterministic and probabilistic requirements.

The model distinguishes:

- guaranteed resource requirements;
- chance-based resource requirements;
- minimum unlock and station context;
- patient, prisoner, transport, and extension dependencies;
- reward and duration information where verified;
- aliases and search terms;
- source and last-verified metadata; and
- confidence/evidence classification.

The mission schema was expanded specifically so probability-based requirements are represented explicitly rather than flattened into misleading guaranteed counts.

[Open verified mission records →](docs/reference/verified-mission-records.md)  
[Open verified mission batch 2 →](docs/reference/verified-mission-batch-2.md)

## Referential integrity

Structured validation checks that mission requirement identifiers resolve to known vehicle records. A mission cannot silently reference a misspelled, missing, or invented resource ID and still pass the repository validation contract.

## Dataset manifest

The UK dataset manifest provides a bounded view of which structured collections exist and how they are intended to be consumed. It is the basis for later exports, calculators, generated indexes, and potential APIs without pretending the current catalogue is complete.

---

# 🛰️ Command Network

<table>
<tr>
<td width="25%" align="center"><h3>🚒</h3><strong>Fire & Rescue</strong><br><sub>Stations, appliances, specialist units, extensions, staffing, and mission capability.</sub></td>
<td width="25%" align="center"><h3>🚑</h3><strong>Ambulance</strong><br><sub>Patients, transport, hospitals, response assets, clinical resources, and specialist care.</sub></td>
<td width="25%" align="center"><h3>🚓</h3><strong>Police</strong><br><sub>Custody, prisoners, public order, investigation, firearms, and specialist policing.</sub></td>
<td width="25%" align="center"><h3>🚁</h3><strong>Air Operations</strong><br><sub>Helicopters, aircraft, bases, operational roles, and deployment requirements.</sub></td>
</tr>
<tr>
<td align="center"><h3>🚤</h3><strong>Maritime</strong><br><sub>Coastguard, lifeboat, inland rescue, trailers, and seagoing operations.</sub></td>
<td align="center"><h3>⛰️</h3><strong>Specialist Rescue</strong><br><sub>Mountain rescue, technical capability, and cross-service response.</sub></td>
<td align="center"><h3>🏗️</h3><strong>Infrastructure</strong><br><sub>Buildings, extensions, classrooms, hospitals, dispatch centres, and placement.</sub></td>
<td align="center"><h3>📡</h3><strong>Command Systems</strong><br><sub>Dispatching, missions, finance, alliances, account progression, and tooling.</sub></td>
</tr>
</table>

---

# ⚡ Rapid Access

| Operational route | Use it for | Access |
|---|---|---|
| **New Player Control** | Account setup, first buildings, early fleets, and expansion order | [Deploy guide →](docs/getting-started/index.md) |
| **Game Systems** | Credits, coins, missions, patients, prisoners, transport, buildings, and dispatching | [Open systems →](docs/systems/index.md) |
| **Emergency Services** | Vehicles, personnel, training, stations, and specialist resources | [Browse services →](docs/services/index.md) |
| **Verified Vehicles** | Current schema-backed resource records | [Open records →](docs/reference/verified-vehicle-records.md) |
| **Verified Missions** | Current guaranteed and probabilistic mission records | [Open records →](docs/reference/verified-mission-records.md) |
| **Strategy Room** | Progression, placement, staffing, fleet composition, coverage, and financial efficiency | [Open strategy →](docs/strategy/index.md) |
| **Alliance Operations** | Roles, funds, events, shared buildings, rules, and coordination | [Open alliance guides →](docs/alliances/index.md) |
| **Scripts & Tools** | LSSM, userscripts, browsers, devices, permissions, compatibility, and recovery | [Inspect tools →](docs/scripts/index.md) |
| **Planning Tools** | Verified-data calculators, comparisons, and future account-planning workflows | [Open programme →](docs/tools/planning-tools.md) |
| **Community Verification** | Submit, reproduce, classify, and review operational intelligence | [Verification workflow →](docs/contributing/verification-workflow.md) |

---

# 🧠 Intelligence Classification

This project deliberately separates evidence from opinion.

| Marker | Classification | Definition |
|:---:|---|---|
| ✅ | **Verified** | Reproduced in the current UK game or confirmed through a reliable primary source |
| 🧮 | **Calculated** | Derived from verified values with the method documented |
| 🎯 | **Recommended** | Operational guidance that can vary by account, geography, alliance, or play style |
| ⚠️ | **Review required** | Potentially outdated, incomplete, contradictory, or awaiting reproduction |

Mature records include verification dates and source trails wherever practical. MissionChief changes over time; undocumented assumptions are not promoted to facts.

[Read the data and evidence standard →](docs/reference/data-standard.md)

---

# 🗃️ Knowledgebase Architecture

```text
MISSIONCHIEF UK COMMAND CENTRE
│
├── Human-readable operational intelligence
│   ├── Getting started and account progression
│   ├── Missions, dispatch, transport, finance and buildings
│   ├── Emergency-service references
│   ├── Strategy, fleet, staffing and geographic planning
│   ├── Alliance operations
│   └── Scripts, compatibility and recovery
│
├── Structured reference data
│   ├── Verified vehicles and aliases
│   ├── Verified missions and requirements
│   ├── Buildings and extensions
│   ├── Personnel and training
│   ├── Dataset manifest
│   └── Future calculators, exports and APIs
│
├── Evidence and governance
│   ├── Verification classifications
│   ├── Source and last-verified metadata
│   ├── Community reproduction workflow
│   ├── Editorial requirements
│   └── Schema and referential-integrity validation
│
└── Delivery platform
    ├── GitHub repository
    ├── MkDocs Material website
    ├── Instant full-text search
    ├── Automated GitHub Pages deployment
    └── Pull-request validation gates
```

## Repository structure

```text
.
├── .github/workflows/
├── assets/readme/
├── docs/
│   ├── getting-started/
│   ├── systems/
│   ├── services/
│   ├── strategy/
│   ├── alliances/
│   ├── scripts/
│   ├── reference/
│   ├── tools/
│   └── contributing/
├── data/
│   ├── schema/
│   └── uk/
├── scripts/validate_data.py
├── mkdocs.yml
├── requirements.txt
└── README.md
```

---

# 🧩 Scripts, Devices, and Compatibility

Tools are not listed merely because they exist. Each mature entry should identify:

- what the tool changes;
- how it is installed and updated;
- which browsers and devices it supports;
- whether it is actively maintained;
- which permissions and data access it requires;
- whether it conflicts with another tool;
- recommended UK configuration;
- known limitations and warning signs; and
- safe disable, recovery, and rollback procedures.

The compatibility centre covers LSSM, userscripts, browser extensions, MissionChief Map Command Toolkit, MissionChief Command Nexus, and other community tooling without treating inclusion as endorsement.

[Open the compatibility centre →](docs/scripts/compatibility-centre.md)  
[Open installation and recovery →](docs/scripts/installation-and-recovery.md)

---

# ✅ Validation and Delivery

Every push to `main` and every pull request is expected to pass the repository-owned validation workflow:

```text
Checkout
   ↓
Python 3.12
   ↓
Install documentation dependencies
   ↓
Validate structured JSON documents
   ↓
Validate mission resource references against vehicle IDs
   ↓
Build MkDocs with --strict
```

The public command centre is deployed through GitHub Pages. Validation and deployment remain separate so malformed data, broken navigation, invalid references, or strict-build failures cannot be presented as verified publication.

Local validation:

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate

pip install -r requirements.txt
python scripts/validate_data.py
mkdocs build --strict
mkdocs serve
```

Open `http://127.0.0.1:8000` for the local site.

---

# 🤝 Contribute Operational Intelligence

Corrections, verified values, screenshots, reproducible observations, strategy analysis, aliases, and tool documentation are welcome.

Before submitting information:

1. distinguish observed fact from calculation or recommendation;
2. include the MissionChief UK context;
3. provide a source or reproducible test where possible;
4. state when the information was last verified;
5. use canonical structured identifiers and valid resource references;
6. record aliases and exceptions that affect search or dispatch interpretation;
7. avoid copying third-party work without permission; and
8. never include private account, alliance, webhook, token, or personal data.

[Read the contribution requirements →](docs/contributing/index.md)  
[Read the verification workflow →](docs/contributing/verification-workflow.md)

---

# ⚖️ Independence and Attribution

This is an independent community project created and maintained by [Conroy1988](https://github.com/Conroy1988). It is **not operated by, endorsed by, or affiliated with SHPlay GmbH or the official MissionChief team**.

MissionChief names, trademarks, screenshots, game artwork, and third-party materials remain the property of their respective owners. Original project code and content are released under the [MIT Licence](LICENSE), unless a file states otherwise.

<div align="center">

## 🚨 **Build the knowledge. Verify the intelligence. Command the game.**

[![Enter Command Centre](https://img.shields.io/badge/ENTER_THE-COMMAND_CENTRE-1593D1?style=for-the-badge&logo=googlemaps&logoColor=white)](https://conroy1988.github.io/MissionChief-UK/)

<sub>MissionChief UK · Independent command knowledgebase · Maintained on GitHub</sub>

</div>
