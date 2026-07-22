<div align="center">

<img src="assets/readme/mission-control-hero.svg" alt="MissionChief UK Command Knowledge Centre" width="100%">

<br>

[![Documentation](https://img.shields.io/badge/OPEN-DOCUMENTATION-1593D1?style=for-the-badge&logo=readthedocs&logoColor=white)](https://conroy1988.github.io/MissionChief-UK/)
[![MissionChief UK](https://img.shields.io/badge/REGION-UNITED_KINGDOM-0B1D31?style=for-the-badge)](https://www.missionchief.co.uk/)
[![Evidence Standard](https://img.shields.io/badge/INTELLIGENCE-EVIDENCE_LED-1675A9?style=for-the-badge&logo=databricks&logoColor=white)](docs/reference/data-standard.md)
[![Project Stage](https://img.shields.io/badge/STATUS-STAGE_17_SAR_HQ-D63345?style=for-the-badge)](#current-operational-state)

[![Deploy MissionChief UK Guide](https://github.com/Conroy1988/MissionChief-UK/actions/workflows/deploy-pages.yml/badge.svg)](https://github.com/Conroy1988/MissionChief-UK/actions/workflows/deploy-pages.yml)
[![Validate guide](https://github.com/Conroy1988/MissionChief-UK/actions/workflows/validate.yml/badge.svg)](https://github.com/Conroy1988/MissionChief-UK/actions/workflows/validate.yml)
[![Last Commit](https://img.shields.io/github/last-commit/Conroy1988/MissionChief-UK?style=flat-square)](https://github.com/Conroy1988/MissionChief-UK/commits/main)
[![Issues](https://img.shields.io/github/issues/Conroy1988/MissionChief-UK?style=flat-square)](https://github.com/Conroy1988/MissionChief-UK/issues)
[![Licence](https://img.shields.io/github/license/Conroy1988/MissionChief-UK?style=flat-square)](LICENSE)

### The independent UK command knowledgebase for MissionChief

**Verified missions · Canonical resources · Emergency-service guides · Strategy · Scripts · Structured data · Community verification**

[**Enter Command Centre**](https://conroy1988.github.io/MissionChief-UK/) · [**Verified Vehicles**](docs/reference/verified-vehicle-records.md) · [**Verified Missions**](docs/reference/verified-mission-records.md) · [**Search & Rescue HQ**](docs/reference/verified-mission-batch-6.md) · [**Contribute**](docs/contributing/index.md)

</div>

---

# 🚨 Mission Briefing

**MissionChief UK** is an independent, searchable knowledge centre for the United Kingdom version of MissionChief.

The project combines practical guides with machine-readable records and explicit evidence metadata. It is designed to answer operational questions without presenting assumptions, community shorthand or outdated values as verified facts.

> **Command principle:** useful information must be easy to find, current enough to trust and precise enough to act on.

---

# 📡 Current Operational State

Stage 17 is complete. The production dataset now contains:

```text
23 verified mission records
26 canonical vehicle-resource records
7 represented operational service groups
6 published mission-data batches
```

| Domain | State | Delivered capability |
|---|---|---|
| **Command Centre** | Operational | MkDocs Material site, instant search, structured navigation and GitHub Pages deployment |
| **Vehicle reference** | Live | Canonical IDs, official labels, aliases, deployment metadata and evidence trails |
| **Mission reference** | Live | Guaranteed, probabilistic and alternative resources; variants; patients; personnel; rewards; POIs and preconditions |
| **Fire and Rescue** | Populated baseline | First-response and technical-rescue records |
| **Ambulance and HART** | Populated baseline | RRV alternatives, patient mechanics, ATV and specialist-response records |
| **Police** | Populated baseline | Public-order personnel, vehicles, air support and prisoner data |
| **Coastguard and Lifeboat** | Populated baseline | Mud rescue, CRV, trailer boat, ILB/ALB, ocean restrictions and helicopter medivac |
| **Mountain Rescue** | Populated baseline | Alternative 4×4s, command, search dogs, cave rescue and additive overlays |
| **Search and Rescue HQ** | Populated baseline | Active-Drone preconditions, SAR command personnel, operational support and aerial-search alternatives |
| **Cross-reference integrity** | Operational | Mission resource identifiers are checked against the canonical resource dataset |
| **Community verification** | Operational | Evidence submission, reproduction and editorial controls |

> [!IMPORTANT]
> A verified record applies that status only to its populated fields. Prices, staffing limits, training requirements and unlock rules remain omitted where the current UK interfaces have not yet been reproduced.

## Delivery progression

```text
STAGES 01–02  Foundation, identity and player journey
STAGES 03–07  Vehicle, mission, building, personnel and training frameworks
STAGES 08–10  Planning tools, verification, compatibility and recovery
STAGES 11–12  Contribution controls, schemas and first production records
STAGE 13      Referential integrity and expanded Fire data
STAGE 14      Ambulance and Police patient, personnel and alternative-resource models
STAGE 15      Coastguard, Lifeboat, trailer and ocean-rescue modelling
STAGE 16      Mountain Rescue, land-search resources and additive mission variants
STAGE 17      Search and Rescue HQ, active drones and missing-person operations
STAGE 18      Next: Bomb Disposal and EOD operations
```

---

# 🗂️ Verified Data Programme

## Vehicle catalogue

The canonical resource dataset now contains 26 records across Fire, Ambulance, HART support, Police, Coastguard, Lifeboat, Mountain Rescue and Search and Rescue.

Stage 17 adds:

- Operational Support Van;
- Operational Support Trailer;
- Personal SAR Vehicle;
- Police Helicopter;
- Drone.

Official labels remain canonical. Trailer status is recorded without inventing towing compatibility, and the generic Drone record remains shared because official missions use it across more than one specialist service.

[Open verified vehicle records →](docs/reference/verified-vehicle-records.md)

## Mission catalogue

Mission records can represent:

- guaranteed vehicle requirements;
- probability-based vehicles and personnel;
- alternative groups where one qualifying resource satisfies the requirement;
- building, extension, hangar, HQ and active-equipment preconditions;
- points of interest and custom spawn areas;
- patient, prisoner and personnel behaviour;
- exact required, available, average-minimum and probabilistic personnel states;
- environment restrictions and destination hand-offs;
- base missions, additive overlays and mission variations;
- base rewards and temporary multiplier observations;
- verification dates and source trails.

[Open initial mission records →](docs/reference/verified-mission-records.md)  
[Open Fire expansion batch →](docs/reference/verified-mission-batch-2.md)  
[Open Ambulance and Police batch →](docs/reference/verified-mission-batch-3.md)  
[Open Coastguard and Lifeboat batch →](docs/reference/verified-mission-batch-4.md)  
[Open Mountain Rescue batch →](docs/reference/verified-mission-batch-5.md)  
[Open Search and Rescue HQ batch →](docs/reference/verified-mission-batch-6.md)

---

# 🔎 Stage 17 Search and Rescue HQ Milestone

Stage 17 introduces the first structured Search and Rescue HQ service model.

## Three independent alternative groups

The verified missing-person missions require:

```text
1 Operational Support Van
OR Operational Support Trailer
OR Personal SAR Vehicle

1 Police Helicopter
OR Drone

2 Mountain Rescue 4x4s
OR SAR 4x4s
OR a valid mixture
```

Each group satisfies a different operational function. They must not be merged or treated as requiring every listed resource.

## Active Drone precondition

The missions require one active Drone before generation. This is separate from the incident aerial-search requirement, which can be satisfied by a Police Helicopter or Drone.

## Personnel states

The verified records distinguish:

- 2 Search Advisors available;
- 4 SAR Commanders available;
- 1 Search Advisor required;
- 2 SAR Commanders required;
- average minimum 10 Search Technicians.

The Search Technician value is stored as `average_minimum`; it is not presented as an exact guaranteed incident headcount.

## Verified missions

| ID | Mission | Police Cars | Average reward |
|---:|---|---:|---:|
| `635` | High Risk Missing Person | 3 | 15,275 |
| `636` | Very High Risk Missing Person | 5 | 18,750 |

[Open the Search and Rescue HQ guide →](docs/services/search-and-rescue.md)

---

# ⚡ Rapid Access

| Route | Use it for | Access |
|---|---|---|
| **Start Here** | Account setup and early progression | [Open guide →](docs/getting-started/index.md) |
| **Emergency Services** | Service-specific vehicles, personnel and stations | [Browse services →](docs/services/index.md) |
| **Verified Vehicles** | Current canonical resource records | [Open records →](docs/reference/verified-vehicle-records.md) |
| **Verified Missions** | Current cross-service mission records | [Open records →](docs/reference/verified-mission-records.md) |
| **Maritime Operations** | Coastguard, Lifeboat and Ocean Rescue | [Open Stage 15 batch →](docs/reference/verified-mission-batch-4.md) |
| **Mountain Rescue** | 4×4 alternatives, search resources and cave rescue | [Open Stage 16 batch →](docs/reference/verified-mission-batch-5.md) |
| **Search and Rescue HQ** | Drone-enabled missing-person operations | [Open Stage 17 batch →](docs/reference/verified-mission-batch-6.md) |
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
Mission-to-resource reference validation
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
