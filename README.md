<div align="center">

<img src="assets/readme/mission-control-hero.svg" alt="MissionChief UK Command Knowledge Centre" width="100%">

<br>

[![Documentation](https://img.shields.io/badge/OPEN-DOCUMENTATION-1593D1?style=for-the-badge&logo=readthedocs&logoColor=white)](https://conroy1988.github.io/MissionChief-UK/)
[![MissionChief UK](https://img.shields.io/badge/REGION-UNITED_KINGDOM-0B1D31?style=for-the-badge)](https://www.missionchief.co.uk/)
[![Evidence Standard](https://img.shields.io/badge/INTELLIGENCE-EVIDENCE_LED-1675A9?style=for-the-badge&logo=databricks&logoColor=white)](docs/reference/data-standard.md)
[![Project Stage](https://img.shields.io/badge/STATUS-STAGE_15_MARITIME_DATA-D63345?style=for-the-badge)](#current-operational-state)

[![Deploy MissionChief UK Guide](https://github.com/Conroy1988/MissionChief-UK/actions/workflows/deploy-pages.yml/badge.svg)](https://github.com/Conroy1988/MissionChief-UK/actions/workflows/deploy-pages.yml)
[![Validate guide](https://github.com/Conroy1988/MissionChief-UK/actions/workflows/validate.yml/badge.svg)](https://github.com/Conroy1988/MissionChief-UK/actions/workflows/validate.yml)
[![Last Commit](https://img.shields.io/github/last-commit/Conroy1988/MissionChief-UK?style=flat-square)](https://github.com/Conroy1988/MissionChief-UK/commits/main)
[![Issues](https://img.shields.io/github/issues/Conroy1988/MissionChief-UK?style=flat-square)](https://github.com/Conroy1988/MissionChief-UK/issues)
[![Licence](https://img.shields.io/github/license/Conroy1988/MissionChief-UK?style=flat-square)](LICENSE)

### The independent UK command knowledgebase for MissionChief

**Game intelligence · Verified missions · Vehicle records · Maritime operations · Strategy · Scripts · Structured data · Community verification**

[**Enter the Command Centre**](https://conroy1988.github.io/MissionChief-UK/) · [**Verified Vehicles**](docs/reference/verified-vehicle-records.md) · [**Verified Missions**](docs/reference/verified-mission-records.md) · [**Maritime Batch**](docs/reference/verified-mission-batch-4.md) · [**Compatibility**](docs/scripts/compatibility-centre.md) · [**Contribute**](docs/contributing/index.md)

</div>

---

# 🚨 Mission Briefing

**MissionChief UK** is an independent, searchable command knowledge centre for the United Kingdom version of MissionChief.

It is being built as a maintained information system rather than another partial wiki or loose collection of tips. Practical guides, structured records and evidence metadata are kept together so players can understand both the operational answer and the basis for trusting it.

The knowledgebase is designed to answer questions such as:

- What should I build next?
- Which vehicles, extensions, stations and trained personnel does a mission require?
- Which requirements are guaranteed, probabilistic or satisfied by alternatives?
- How should a specialist fleet be configured?
- Which scripts are maintained, compatible and recoverable?
- Which values are verified facts, calculations, recommendations or still awaiting reproduction?

> **Command principle:** useful information must be easy to find, current enough to trust and precise enough to act on.

<table>
<tr>
<td width="25%" align="center"><strong>🔎 FIND</strong><br><sub>Search missions, vehicles, aliases, services and systems.</sub></td>
<td width="25%" align="center"><strong>✅ VERIFY</strong><br><sub>Separate reproduced facts from assumptions and advice.</sub></td>
<td width="25%" align="center"><strong>🧭 PLAN</strong><br><sub>Connect fleet, staffing, geography, progression and cost.</sub></td>
<td width="25%" align="center"><strong>🛡️ RECOVER</strong><br><sub>Document compatibility, troubleshooting and rollback.</sub></td>
</tr>
</table>

---

# 📡 Current Operational State

The project has progressed beyond its Stage 10 architecture milestone into **Stage 15 verified maritime-data expansion**.

The documentation and schema architecture is established, while the production dataset now contains:

```text
16 verified mission records
12 canonical vehicle-resource records
5 represented operational service groups
```

| Domain | Current state | Delivered capability |
|---|---|---|
| **Command Centre** | Operational | MkDocs Material site, custom identity, instant search, structured navigation and GitHub Pages deployment |
| **Vehicle reference** | Verified records live | Canonical IDs, official labels, aliases, service roles, deployment metadata and evidence trails |
| **Mission reference** | Four verified batches live | Guaranteed, probabilistic and alternative resources; patients; personnel; rewards; POIs and preconditions |
| **Fire and Rescue** | Populated baseline | First response and specialist-resource records with verified missions |
| **Ambulance** | Populated baseline | RRV alternatives and structured patient mechanics |
| **Police** | Populated baseline | Public-order personnel, vehicles and prisoner data |
| **Coastguard and Lifeboat** | Populated baseline | Mud rescue, CRV, trailer boat, ILB/ALB, ocean restrictions and helicopter medivac |
| **Cross-reference integrity** | Operational | Mission resources are validated against canonical vehicle records |
| **Dataset manifest** | Operational | Explicit inventory and bounded publication posture |
| **Buildings, personnel and training** | Framework delivered | Database specifications ready for controlled population |
| **Planning tools** | Programme established | Future calculators and decision-support tools based on verified data |
| **Scripts and compatibility** | Operational framework | Tool catalogue, device posture, installation, troubleshooting and recovery standards |
| **Community verification** | Operational framework | Evidence submission, reproduction and editorial controls |

> [!IMPORTANT]
> Stage 15 means verified cross-service data is being published through the live reference pages. It does **not** claim that every UK mission, vehicle, building, training course, price or edge case has already been catalogued.

## Delivery progression

```text
STAGES 01–02  Foundation, scope, identity and player journey
STAGES 03–07  Vehicle, mission, building, personnel and training frameworks
STAGES 08–10  Planning tools, community verification, compatibility and recovery
STAGES 11–12  Contribution controls, schemas and first production records
STAGE 13      Referential integrity and expanded Fire mission data
STAGE 14      Ambulance and Police alternative, patient and personnel models
STAGE 15      Coastguard, Lifeboat, trailer and ocean-rescue modelling
```

---

# 🗂️ Verified Data Programme

## Current vehicle catalogue

The live dataset contains 12 canonical vehicle-resource records across Fire, Ambulance, Police, Coastguard and Lifeboat operations.

Stage 15 adds:

- CRV;
- Coastguard Mud Rescue Unit;
- Mud Decontamination Unit;
- Coastguard Rescue Helicopter;
- Inland Rescue Boat (Trailer);
- ILB; and
- ALB.

Official abbreviations remain canonical where that is how the mission page presents the requirement. Expanded terms are stored as searchable aliases rather than silently replacing the game terminology.

[Open verified vehicle records →](docs/reference/verified-vehicle-records.md)

## Current mission catalogue

Mission records distinguish:

- guaranteed resource requirements;
- chance-based requirements with explicit probabilities;
- alternative groups where one qualifying vehicle satisfies the requirement;
- station and extension preconditions;
- POIs and mission groups;
- patient, prisoner, personnel and hand-off behaviour;
- ocean-only vehicle restrictions and custom spawn areas;
- base rewards and observed temporary multipliers; and
- source and verification metadata.

[Open initial verified mission records →](docs/reference/verified-mission-records.md)  
[Open Fire expansion batch →](docs/reference/verified-mission-batch-2.md)  
[Open Ambulance and Police batch →](docs/reference/verified-mission-batch-3.md)  
[Open Coastguard and Lifeboat batch →](docs/reference/verified-mission-batch-4.md)

## Maritime modelling milestone

Stage 15 establishes the first structured distinction between:

```text
Inland Rescue Boat (Trailer)
            ≠
ILB or ALB ocean-rescue vessel
```

It also records:

- Coastguard Rescue Stations and Lifeboat Stations separately;
- helicopter and specialist-extension preconditions;
- trailer status without guessing towing compatibility;
- ILB-or-ALB alternative requirements;
- ocean vehicle restrictions;
- Lifeboat Station patient hand-offs; and
- temporary reward multipliers without overwriting base rewards.

## Referential integrity

Structured validation checks every guaranteed, probabilistic and alternative mission resource against the canonical vehicle dataset. A misspelled, missing or invented resource ID cannot silently pass the repository contract.

---

# 🛰️ Command Network

<table>
<tr>
<td width="25%" align="center"><h3>🚒</h3><strong>Fire & Rescue</strong><br><sub>Stations, appliances, specialist units, extensions and staffing.</sub></td>
<td width="25%" align="center"><h3>🚑</h3><strong>Ambulance</strong><br><sub>Patients, transport, response assets and specialist care.</sub></td>
<td width="25%" align="center"><h3>🚓</h3><strong>Police</strong><br><sub>Custody, public order, investigation and specialist policing.</sub></td>
<td width="25%" align="center"><h3>🚁</h3><strong>Air Operations</strong><br><sub>Helicopters, aircraft, bases and deployment requirements.</sub></td>
</tr>
<tr>
<td align="center"><h3>🚤</h3><strong>Maritime</strong><br><sub>Coastguard, lifeboat, mud rescue, trailers and ocean operations.</sub></td>
<td align="center"><h3>⛰️</h3><strong>Specialist Rescue</strong><br><sub>Mountain, technical and cross-service response.</sub></td>
<td align="center"><h3>🏗️</h3><strong>Infrastructure</strong><br><sub>Buildings, extensions, hospitals, classrooms and dispatch centres.</sub></td>
<td align="center"><h3>📡</h3><strong>Command Systems</strong><br><sub>Dispatching, missions, finance, alliances and tooling.</sub></td>
</tr>
</table>

---

# ⚡ Rapid Access

| Operational route | Use it for | Access |
|---|---|---|
| **New Player Control** | Account setup, first buildings and expansion order | [Deploy guide →](docs/getting-started/index.md) |
| **Game Systems** | Missions, patients, prisoners, transport, buildings and dispatching | [Open systems →](docs/systems/index.md) |
| **Emergency Services** | Vehicles, personnel, training and specialist resources | [Browse services →](docs/services/index.md) |
| **Verified Vehicles** | Current schema-backed resource records | [Open records →](docs/reference/verified-vehicle-records.md) |
| **Verified Missions** | Current cross-service mission records | [Open records →](docs/reference/verified-mission-records.md) |
| **Maritime Operations** | Coastguard, Lifeboat and Ocean Rescue data | [Open Stage 15 batch →](docs/reference/verified-mission-batch-4.md) |
| **Strategy Room** | Progression, placement, staffing and fleet composition | [Open strategy →](docs/strategy/index.md) |
| **Scripts & Tools** | LSSM, userscripts, browsers, compatibility and recovery | [Inspect tools →](docs/scripts/index.md) |
| **Planning Tools** | Future verified-data calculators and comparisons | [Open programme →](docs/tools/planning-tools.md) |
| **Community Verification** | Submit, reproduce and review operational intelligence | [Open workflow →](docs/contributing/verification-workflow.md) |

---

# 🧠 Intelligence Classification

| Marker | Classification | Definition |
|:---:|---|---|
| ✅ | **Verified** | Reproduced in the current UK game or confirmed through a reliable primary source |
| 🧮 | **Calculated** | Derived from verified values with the method documented |
| 🎯 | **Recommended** | Operational guidance that can vary by account, geography, alliance or play style |
| ⚠️ | **Review required** | Potentially outdated, incomplete, contradictory or awaiting reproduction |

Mature records include verification dates and source trails wherever practical. MissionChief changes over time; undocumented assumptions are not promoted to facts.

[Read the data and evidence standard →](docs/reference/data-standard.md)

---

# 🗃️ Knowledgebase Architecture

```text
MISSIONCHIEF UK COMMAND CENTRE
│
├── Human-readable operational intelligence
│   ├── Getting started and progression
│   ├── Game systems and emergency-service guides
│   ├── Strategy and alliance operations
│   └── Scripts, compatibility and recovery
│
├── Structured reference data
│   ├── Verified vehicles and aliases
│   ├── Verified missions and requirements
│   ├── Buildings, extensions, personnel and training
│   └── Future calculators, exports and APIs
│
├── Evidence and governance
│   ├── Verification classifications
│   ├── Source and last-verified metadata
│   ├── Community reproduction workflow
│   └── Schema and referential-integrity validation
│
└── Delivery platform
    ├── GitHub repository
    ├── MkDocs Material website
    ├── Instant full-text search
    ├── Automated GitHub Pages deployment
    └── Pull-request validation gates
```

---

# 🧩 Scripts, Devices and Compatibility

Tool entries should identify:

- what the tool changes;
- how it is installed and updated;
- supported browsers and devices;
- maintenance status;
- permissions and data access;
- conflicts with other tools;
- recommended UK configuration;
- known limitations; and
- safe disable, recovery and rollback procedures.

The compatibility centre covers LSSM, userscripts, browser extensions, MissionChief Map Command Toolkit, MissionChief Command Nexus and other community tooling without treating inclusion as endorsement.

[Open the compatibility centre →](docs/scripts/compatibility-centre.md)  
[Open installation and recovery →](docs/scripts/installation-and-recovery.md)

---

# ✅ Validation and Delivery

Every push to `main` and every pull request is expected to pass:

```text
Checkout
   ↓
Python 3.12
   ↓
Install dependencies
   ↓
Validate JSON against Draft 2020-12 schemas
   ↓
Validate mission resource references
   ↓
Validate patient ranges
   ↓
Build MkDocs with --strict
```

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

Before submitting information:

1. distinguish observed fact from calculation or recommendation;
2. include the MissionChief UK context;
3. provide a source or reproducible test where possible;
4. state when the information was last verified;
5. use canonical identifiers and valid resource references;
6. record aliases and exceptions affecting search or dispatch interpretation;
7. avoid copying third-party work without permission; and
8. never include private account, alliance, webhook, token or personal data.

[Read the contribution requirements →](docs/contributing/index.md)  
[Read the verification workflow →](docs/contributing/verification-workflow.md)

---

# ⚖️ Independence and Attribution

This is an independent community project created and maintained by [Conroy1988](https://github.com/Conroy1988). It is **not operated by, endorsed by or affiliated with SHPlay GmbH or the official MissionChief team**.

MissionChief names, trademarks, screenshots, game artwork and third-party materials remain the property of their respective owners. Original project code and content are released under the [MIT Licence](LICENSE), unless a file states otherwise.

<div align="center">

## 🚨 **Build the knowledge. Verify the intelligence. Command the game.**

[![Enter Command Centre](https://img.shields.io/badge/ENTER_THE-COMMAND_CENTRE-1593D1?style=for-the-badge&logo=googlemaps&logoColor=white)](https://conroy1988.github.io/MissionChief-UK/)

<sub>MissionChief UK · Independent command knowledgebase · Maintained on GitHub</sub>

</div>
