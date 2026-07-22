<div align="center">

<img src="assets/readme/mission-control-hero.svg" alt="MissionChief UK Command Knowledge Centre" width="100%">

<br>

[![Documentation](https://img.shields.io/badge/OPEN-DOCUMENTATION-1593D1?style=for-the-badge&logo=readthedocs&logoColor=white)](https://conroy1988.github.io/MissionChief-UK/)
[![MissionChief UK](https://img.shields.io/badge/REGION-UNITED_KINGDOM-0B1D31?style=for-the-badge)](https://www.missionchief.co.uk/)
[![Evidence Standard](https://img.shields.io/badge/INTELLIGENCE-EVIDENCE_LED-1675A9?style=for-the-badge&logo=databricks&logoColor=white)](docs/reference/data-standard.md)
[![Project Stage](https://img.shields.io/badge/STATUS-STAGE_15_COMPLETE-D63345?style=for-the-badge)](#current-operational-state)

[![Deploy MissionChief UK Guide](https://github.com/Conroy1988/MissionChief-UK/actions/workflows/deploy-pages.yml/badge.svg)](https://github.com/Conroy1988/MissionChief-UK/actions/workflows/deploy-pages.yml)
[![Validate guide](https://github.com/Conroy1988/MissionChief-UK/actions/workflows/validate.yml/badge.svg)](https://github.com/Conroy1988/MissionChief-UK/actions/workflows/validate.yml)
[![Last Commit](https://img.shields.io/github/last-commit/Conroy1988/MissionChief-UK?style=flat-square)](https://github.com/Conroy1988/MissionChief-UK/commits/main)
[![Issues](https://img.shields.io/github/issues/Conroy1988/MissionChief-UK?style=flat-square)](https://github.com/Conroy1988/MissionChief-UK/issues)
[![Licence](https://img.shields.io/github/license/Conroy1988/MissionChief-UK?style=flat-square)](LICENSE)

### The independent UK command knowledgebase for MissionChief

**Verified missions · Canonical vehicle data · Service guides · Strategy · Scripts · Structured data · Community verification**

[**Enter the Command Centre**](https://conroy1988.github.io/MissionChief-UK/) · [**Verified Vehicles**](docs/reference/verified-vehicle-records.md) · [**Verified Missions**](docs/reference/verified-mission-records.md) · [**Maritime Batch**](docs/reference/verified-mission-batch-4.md) · [**Contribute**](docs/contributing/index.md)

</div>

---

# 🚨 Mission Briefing

**MissionChief UK** is an independent, searchable knowledge centre for the United Kingdom version of MissionChief.

The project combines practical guides with machine-readable records and explicit evidence metadata. It is designed to answer operational questions without presenting assumptions, community shorthand or outdated values as verified facts.

> **Command principle:** useful information must be easy to find, current enough to trust and precise enough to act on.

---

# 📡 Current Operational State

Stage 15 is complete. The repository currently contains:

```text
16 verified mission records
12 canonical vehicle-resource records
5 represented operational service groups
4 published mission-data batches
```

| Domain | State | Delivered capability |
|---|---|---|
| **Command Centre** | Operational | MkDocs Material site, instant search, structured navigation and GitHub Pages deployment |
| **Vehicle reference** | Live | Canonical IDs, official labels, aliases, service roles, deployment metadata and evidence trails |
| **Mission reference** | Live | Guaranteed, probabilistic and alternative resources; patients; personnel; rewards; POIs and preconditions |
| **Fire and Rescue** | Populated baseline | First-response and specialist-resource records with verified missions |
| **Ambulance** | Populated baseline | RRV alternatives and structured patient mechanics |
| **Police** | Populated baseline | Public-order personnel, vehicles and prisoner data |
| **Coastguard and Lifeboat** | Populated baseline | Mud rescue, CRV, trailer boat, ILB/ALB, ocean restrictions and helicopter medivac |
| **Cross-reference integrity** | Operational | Every mission resource identifier is checked against the vehicle dataset |
| **Community verification** | Operational | Evidence submission, reproduction and editorial controls |

> [!IMPORTANT]
> The repository publishes only the fields supported by current UK-game evidence. A verified record may intentionally omit prices, staffing limits, training requirements or other attributes that have not yet been reproduced.

## Delivery progression

```text
STAGES 01–02  Foundation, identity and player journey
STAGES 03–07  Vehicle, mission, building, personnel and training frameworks
STAGES 08–10  Planning tools, verification, compatibility and recovery
STAGES 11–12  Contribution controls, schemas and first production records
STAGE 13      Referential integrity and expanded Fire data
STAGE 14      Ambulance and Police patient, personnel and alternative-resource models
STAGE 15      Coastguard, Lifeboat, trailer and ocean-rescue modelling
STAGE 16      Next: Mountain Rescue and specialist land-search operations
```

---

# 🗂️ Verified Data Programme

## Vehicle catalogue

The current catalogue covers Fire, Ambulance, Police, Coastguard and Lifeboat resources. Canonical identifiers are used by mission records and validation fails when a mission references an unknown resource.

[Open verified vehicle records →](docs/reference/verified-vehicle-records.md)

## Mission catalogue

Mission records can represent:

- guaranteed resources;
- probability-based resources;
- alternative groups where one qualifying resource satisfies the requirement;
- station and extension preconditions;
- points of interest and custom spawn areas;
- patient, prisoner and personnel behaviour;
- destination hand-offs and environment restrictions;
- base rewards and temporary event observations;
- verification dates and source trails.

[Open initial mission records →](docs/reference/verified-mission-records.md)  
[Open Fire expansion batch →](docs/reference/verified-mission-batch-2.md)  
[Open Ambulance and Police batch →](docs/reference/verified-mission-batch-3.md)  
[Open Coastguard and Lifeboat batch →](docs/reference/verified-mission-batch-4.md)

## Maritime modelling milestone

Stage 15 established the structured distinction between:

```text
Inland Rescue Boat (Trailer)
            ≠
ILB or ALB ocean-rescue vessel
```

It also introduced Coastguard and Lifeboat station preconditions, helicopter hangars, ocean-only restrictions, patient hand-offs and trailer deployment metadata without inventing towing compatibility.

---

# ⛰️ Stage 16 Target

The next controlled batch will model Mountain Rescue and specialist land-search operations.

The implementation target includes:

- Mountain Rescue Station preconditions;
- Mountain Rescue 4x4 and SAR 4x4 alternatives;
- Control Vans and Search Dog Units;
- Rescue Support Vehicles and ATV Carriers where evidenced;
- custom mission spawn areas;
- patient and critical-care probabilities;
- specialist personnel such as Search Advisors and Cave Rescue Specialists;
- explicit separation of base missions from HART, helicopter and drone overlays.

No vehicle name, staffing requirement or overlay value will be inferred from a neighbouring mission.

---

# ⚡ Rapid Access

| Route | Use it for | Access |
|---|---|---|
| **Start Here** | Account setup and early progression | [Open guide →](docs/getting-started/index.md) |
| **Emergency Services** | Service-specific vehicles, personnel and stations | [Browse services →](docs/services/index.md) |
| **Verified Vehicles** | Current canonical resource records | [Open records →](docs/reference/verified-vehicle-records.md) |
| **Verified Missions** | Current cross-service mission records | [Open records →](docs/reference/verified-mission-records.md) |
| **Maritime Operations** | Coastguard, Lifeboat and Ocean Rescue data | [Open Stage 15 batch →](docs/reference/verified-mission-batch-4.md) |
| **Scripts & Tools** | Compatibility, installation and recovery | [Inspect tools →](docs/scripts/index.md) |
| **Community Verification** | Submit and reproduce operational intelligence | [Open workflow →](docs/contributing/verification-workflow.md) |

---

# 🧠 Evidence Classification

| Marker | Classification | Definition |
|:---:|---|---|
| ✅ | **Verified** | Reproduced in the current UK game or confirmed through a reliable primary source |
| 🧮 | **Calculated** | Derived from verified values with the method documented |
| 🎯 | **Recommended** | Strategic guidance that can vary by account, geography or play style |
| ⚠️ | **Review required** | Potentially incomplete, contradictory, outdated or awaiting reproduction |

[Read the data and evidence standard →](docs/reference/data-standard.md)

---

# ✅ Validation and Delivery

Every push to `main` and every pull request is expected to pass:

```text
JSON syntax
    ↓
Draft 2020-12 schema validation
    ↓
Unique identifier checks
    ↓
Mission-to-vehicle reference validation
    ↓
Patient-range semantic validation
    ↓
MkDocs strict build
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

---

# 🤝 Contribute Operational Intelligence

Before submitting information:

1. distinguish observed fact from calculation or recommendation;
2. confirm the information belongs to the UK game;
3. provide a primary source or reproducible test where possible;
4. state when the information was last checked;
5. use canonical identifiers and valid resource references;
6. record aliases and dispatch-relevant exceptions;
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
