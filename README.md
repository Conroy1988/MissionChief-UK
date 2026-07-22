<div align="center">

<img src="assets/readme/mission-control-hero.svg" alt="MissionChief UK Command Knowledge Centre" width="100%">

<br>

[![Documentation](https://img.shields.io/badge/OPEN-DOCUMENTATION-1593D1?style=for-the-badge&logo=readthedocs&logoColor=white)](https://conroy1988.github.io/MissionChief-UK/)
[![MissionChief UK](https://img.shields.io/badge/REGION-UNITED_KINGDOM-0B1D31?style=for-the-badge)](https://www.missionchief.co.uk/)
[![Evidence Standard](https://img.shields.io/badge/INTELLIGENCE-EVIDENCE_LED-1675A9?style=for-the-badge&logo=databricks&logoColor=white)](docs/reference/data-standard.md)
[![Project Stage](https://img.shields.io/badge/STATUS-STAGE_18_BOMB_DISPOSAL-D63345?style=for-the-badge)](#current-operational-state)

[![Deploy MissionChief UK Guide](https://github.com/Conroy1988/MissionChief-UK/actions/workflows/deploy-pages.yml/badge.svg)](https://github.com/Conroy1988/MissionChief-UK/actions/workflows/deploy-pages.yml)
[![Validate guide](https://github.com/Conroy1988/MissionChief-UK/actions/workflows/validate.yml/badge.svg)](https://github.com/Conroy1988/MissionChief-UK/actions/workflows/validate.yml)
[![Last Commit](https://img.shields.io/github/last-commit/Conroy1988/MissionChief-UK?style=flat-square)](https://github.com/Conroy1988/MissionChief-UK/commits/main)
[![Issues](https://img.shields.io/github/issues/Conroy1988/MissionChief-UK?style=flat-square)](https://github.com/Conroy1988/MissionChief-UK/issues)
[![Licence](https://img.shields.io/github/license/Conroy1988/MissionChief-UK?style=flat-square)](LICENSE)

### The independent UK command knowledgebase for MissionChief

**Verified missions · Canonical resources · Infrastructure records · Emergency-service guides · Structured data · Community verification**

[**Enter Command Centre**](https://conroy1988.github.io/MissionChief-UK/) · [**Verified Vehicles**](docs/reference/verified-vehicle-records.md) · [**Verified Missions**](docs/reference/verified-mission-records.md) · [**Bomb Disposal**](docs/reference/verified-mission-batch-7.md) · [**Contribute**](docs/contributing/index.md)

</div>

---

# 🚨 Mission Briefing

**MissionChief UK** is an independent, searchable knowledge centre for the United Kingdom version of MissionChief.

The project combines practical guides with machine-readable records and explicit evidence metadata. Unsupported values are omitted rather than presented as facts.

> **Command principle:** useful information must be easy to find, current enough to trust and precise enough to act on.

---

# 📡 Current Operational State

Stage 18 has delivered the first Bomb Disposal and EOD mission-generation baseline:

```text
27 verified mission records
26 canonical vehicle-resource records
2 canonical infrastructure records
8 represented operational service groups
7 published mission-data batches
```

| Domain | State | Delivered capability |
|---|---|---|
| **Command Centre** | Operational | MkDocs Material site, instant search, structured navigation and GitHub Pages deployment |
| **Vehicle reference** | Live | Canonical IDs, official labels, aliases, deployment metadata and evidence trails |
| **Infrastructure reference** | Live baseline | Schema-controlled buildings and extensions with mission-precondition validation |
| **Mission reference** | Live | Guaranteed, probabilistic and alternative resources; variants; patients; personnel; rewards; POIs and preconditions |
| **Fire and Rescue** | Populated baseline | First-response and technical-rescue records |
| **Ambulance and HART** | Populated baseline | RRV alternatives, patient mechanics, ATV and specialist-response records |
| **Police** | Populated baseline | Public order, air support, prisoners and shared specialist response |
| **Coastguard and Lifeboat** | Populated baseline | Mud rescue, CRV, trailer boat, ILB/ALB, ocean restrictions and medivac |
| **Mountain Rescue** | Populated baseline | Alternative 4×4s, command, search dogs, cave rescue and overlays |
| **Search and Rescue HQ** | Populated baseline | Active-Drone preconditions, SAR command and aerial-search alternatives |
| **Bomb Disposal and EOD** | Populated precondition baseline | HQs, marine extensions, land/coastal missions and infrastructure integrity |

> [!IMPORTANT]
> A verified record applies that status only to populated fields. The first Bomb Disposal batch verifies mission-directory information; EOD response vehicles, personnel, training and costs remain unpublished until directly reproduced.

## Delivery progression

```text
STAGES 01–02  Foundation, identity and player journey
STAGES 03–07  Vehicle, mission, building, personnel and training frameworks
STAGES 08–10  Planning tools, verification, compatibility and recovery
STAGES 11–12  Contribution controls, schemas and first production records
STAGE 13      Referential integrity and expanded Fire data
STAGE 14      Ambulance and Police patient, personnel and alternative-resource models
STAGE 15      Coastguard, Lifeboat, trailer and ocean-rescue modelling
STAGE 16      Mountain Rescue, land search and explicit mission variants
STAGE 17      Search and Rescue HQ, active drones and missing-person operations
STAGE 18      Bomb Disposal infrastructure and unexploded-ordnance mission baseline
STAGE 19      Next: Airfield Operations
```

---

# 🗂️ Verified Data Programme

## Production collections

```text
data/uk/missions/         27 records
data/uk/vehicles/         26 records
data/uk/infrastructure/    2 records
```

The validator enforces:

- Draft 2020-12 schema conformance;
- unique record identifiers;
- mission-to-vehicle resource integrity;
- alternative-resource integrity;
- patient-range semantics;
- Bomb Disposal preconditions against canonical infrastructure IDs.

## Stage 18 infrastructure

```text
bomb_disposal_hq
bomb_disposal_marine_unit_extension
```

These are the first production building/extension records. Missions using `bomb_disposal_hqs` or `bomb_disposal_marine_unit_extensions` fail validation when the matching infrastructure record is absent.

## Stage 18 missions

| ID | Mission | Key Bomb Disposal preconditions | Credits |
|---:|---|---|---:|
| `829` | Unexploded WW2 Ordnance in Countryside | 1 HQ | 4,500 |
| `830` | Unexploded WW2 Ordnance on Quiet Beach | 1 HQ, 1 Marine Unit Extension | 5,500 |
| `832` | Unexploded WW2 Ordnance in Harbour | 3 HQs, 2 Marine Unit Extensions, active Drone | 15,000 |
| `839` | Unexploded WW2 Bomb Located at Building Site (Large) | 3 HQs, active Drone | 11,500 |

[Open the Bomb Disposal service guide →](docs/services/bomb-disposal.md)  
[Open verified Mission Batch 7 →](docs/reference/verified-mission-batch-7.md)

## Evidence boundary

The official directory confirmed IDs, names, POIs, rewards and infrastructure preconditions. Individual response tables were unavailable during verification, so the new records do not claim exact EOD vehicles or personnel.

An active Drone is recorded as a mission-generation precondition and is not automatically treated as a dispatch requirement.

---

# ⚡ Rapid Access

| Route | Use it for | Access |
|---|---|---|
| **Start Here** | Account setup and early progression | [Open guide →](docs/getting-started/index.md) |
| **Emergency Services** | Service-specific vehicles, personnel and stations | [Browse services →](docs/services/index.md) |
| **Verified Vehicles** | Current canonical deployable-resource records | [Open records →](docs/reference/verified-vehicle-records.md) |
| **Verified Missions** | Current cross-service mission records | [Open records →](docs/reference/verified-mission-records.md) |
| **Search and Rescue HQ** | Drone-enabled missing-person operations | [Open Stage 17 →](docs/reference/verified-mission-batch-6.md) |
| **Bomb Disposal and EOD** | HQ, marine-extension and unexploded-ordnance data | [Open Stage 18 →](docs/reference/verified-mission-batch-7.md) |
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

```text
JSON syntax
    ↓
Draft 2020-12 schema validation
    ↓
Unique identifier checks
    ↓
Mission-to-resource validation
    ↓
Infrastructure-precondition validation
    ↓
Patient-range semantic validation
    ↓
MkDocs strict build
```

Local validation:

```bash
pip install -r requirements.txt
python scripts/validate_data.py
mkdocs build --strict
```

---

# ⚖️ Independence and Attribution

This is an independent community project created and maintained by [Conroy1988](https://github.com/Conroy1988). It is **not operated by, endorsed by or affiliated with SHPlay GmbH or the official MissionChief team**.

MissionChief names, trademarks, screenshots, game artwork and third-party materials remain the property of their respective owners. Original project code and content are released under the [MIT Licence](LICENSE), unless a file states otherwise.

<div align="center">

## 🚨 **Build the knowledge. Verify the intelligence. Command the game.**

[![Enter Command Centre](https://img.shields.io/badge/ENTER_THE-COMMAND_CENTRE-1593D1?style=for-the-badge&logo=googlemaps&logoColor=white)](https://conroy1988.github.io/MissionChief-UK/)

</div>
