<div align="center">

<img src="assets/readme/mission-control-hero.svg" alt="MissionChief UK Command Knowledge Centre" width="100%">

<br>

[![Documentation](https://img.shields.io/badge/OPEN-DOCUMENTATION-1593D1?style=for-the-badge&logo=readthedocs&logoColor=white)](https://conroy1988.github.io/MissionChief-UK/)
[![MissionChief UK](https://img.shields.io/badge/REGION-UNITED_KINGDOM-0B1D31?style=for-the-badge)](https://www.missionchief.co.uk/)
[![Evidence Standard](https://img.shields.io/badge/INTELLIGENCE-EVIDENCE_LED-1675A9?style=for-the-badge&logo=databricks&logoColor=white)](docs/reference/data-standard.md)
[![Project Stage](https://img.shields.io/badge/STATUS-STAGE_20_RECOVERY-D63345?style=for-the-badge)](#current-operational-state)

[![Deploy MissionChief UK Guide](https://github.com/Conroy1988/MissionChief-UK/actions/workflows/deploy-pages.yml/badge.svg)](https://github.com/Conroy1988/MissionChief-UK/actions/workflows/deploy-pages.yml)
[![Validate guide](https://github.com/Conroy1988/MissionChief-UK/actions/workflows/validate.yml/badge.svg)](https://github.com/Conroy1988/MissionChief-UK/actions/workflows/validate.yml)
[![Last Commit](https://img.shields.io/github/last-commit/Conroy1988/MissionChief-UK?style=flat-square)](https://github.com/Conroy1988/MissionChief-UK/commits/main)
[![Issues](https://img.shields.io/github/issues/Conroy1988/MissionChief-UK?style=flat-square)](https://github.com/Conroy1988/MissionChief-UK/issues)
[![Licence](https://img.shields.io/github/license/Conroy1988/MissionChief-UK?style=flat-square)](LICENSE)

### The independent UK command knowledgebase for MissionChief

**Verified missions · Canonical resources · Infrastructure records · Emergency-service guides · Structured data · Community verification**

[**Enter Command Centre**](https://conroy1988.github.io/MissionChief-UK/) · [**Verified Vehicles**](docs/reference/verified-vehicle-records.md) · [**Verified Missions**](docs/reference/verified-mission-records.md) · [**Recovery Operations**](docs/reference/verified-mission-batch-9.md) · [**Contribute**](docs/contributing/index.md)

</div>

---

# 🚨 Mission Briefing

**MissionChief UK** is an independent, searchable knowledge centre for the United Kingdom version of MissionChief.

The project combines practical guides with machine-readable records and explicit evidence metadata. Unsupported values are omitted rather than presented as facts.

> **Command principle:** useful information must be easy to find, current enough to trust and precise enough to act on.

---

# 📡 Current Operational State

Stage 20 delivers the first production Recovery and HGV recovery model:

```text
36 verified mission records
39 canonical vehicle-resource records
8 canonical infrastructure records
10 represented operational service groups
9 published mission-data batches
```

| Domain | State | Delivered capability |
|---|---|---|
| **Command Centre** | Operational | MkDocs Material site, instant search, structured navigation and GitHub Pages deployment |
| **Vehicle reference** | Live | Canonical IDs, official labels, aliases, deployment metadata and evidence trails |
| **Infrastructure reference** | Live | Schema-controlled buildings and extensions with mission-precondition validation |
| **Mission reference** | Live | Guaranteed, probabilistic, conditional and alternative resources; variants; patients; personnel; towing; rewards; POIs and preconditions |
| **Fire and Rescue** | Populated baseline | First response, technical rescue, hazardous materials, airport and recovery variations |
| **Ambulance and HART** | Populated baseline | Patient mechanics, command, mass-casualty and specialist response |
| **Police** | Populated baseline | Public order, air support, traffic policing, prisoners and recovery-linked incidents |
| **Coastguard and Lifeboat** | Populated baseline | Mud rescue, CRV, trailer boat, ILB/ALB, ocean restrictions and medivac |
| **Mountain Rescue** | Populated baseline | Alternative 4×4s, command, search dogs, cave rescue and overlays |
| **Search and Rescue HQ** | Populated baseline | Active-Drone preconditions, SAR command and aerial-search alternatives |
| **Bomb Disposal and EOD** | Populated precondition baseline | HQs, marine extensions, land/coastal missions and infrastructure integrity |
| **Airfield Operations** | Populated baseline | Airport extensions, RIV/foam fleet, airfield command and Code C/F incidents |
| **Recovery and HGV Recovery** | Populated baseline | Recovery Centres, HGV extensions, towing ranges and recovery-enabled variants |

> [!IMPORTANT]
> A verified record applies only to populated fields. Recovery infrastructure costs, capacity, staffing and vehicle inventory remain unpublished until directly reproduced.

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
STAGE 18      Bomb Disposal infrastructure and unexploded-ordnance baseline
STAGE 19      Airfield Operations and code-based aircraft incidents
STAGE 20      Recovery Centres, HGV extensions and structured towing outcomes
STAGE 21      Next: Railway Police and railway fire response
```

---

# 🗂️ Verified Data Programme

## Production collections

```text
data/uk/missions/         36 records
data/uk/vehicles/         39 records
data/uk/infrastructure/    8 records
```

The validator enforces:

- Draft 2020-12 schema conformance;
- unique record identifiers;
- guaranteed, probabilistic and conditional resource integrity;
- every resource inside alternative groups;
- patient-range semantics;
- towing-range semantics;
- mapped infrastructure-precondition integrity.

## Stage 20 infrastructure

```text
recovery_centre
hgv_recovery_extension
```

These join the Bomb Disposal and Airfield infrastructure records. Missions using `recovery_centres` or `hgv_recovery_extensions` fail validation when the matching canonical infrastructure record is absent.

## Stage 20 missions

| Dataset ID | Mission | Towing | Credits |
|---|---|---|---:|
| `784` | Abandoned Car Obstructing Road | Response page unavailable | 400 |
| `785` | Broken Down Car Obstructing Road | Response page unavailable | 400 |
| `2-recovery-overlay` | Burning car | 1 car | 670 |
| `13-hgv-recovery-overlay` | Burning truck | 1 truck | 1,280 |
| `129-recovery-overlay` | Multi vehicle RTC | 2–4 cars | 1,900 |
| `782-recovery-overlay` | Non-Injury RTC with Police Car | 1 car | 4,800 |

[Open the Recovery service guide →](docs/services/recovery.md)  
[Open verified Mission Batch 9 →](docs/reference/verified-mission-batch-9.md)

## Towing is separate from dispatch

Official pages list towing under **Other information**, not Vehicle and Personnel Requirements. The dataset therefore stores towing under `recovery.assets` rather than inventing a Recovery Vehicle dispatch row.

## Conditional probability

Multi vehicle RTC records one Traffic Car with both:

- a 50% requirement probability;
- the condition `only_when_available`.

The schema preserves both facts in one conditional requirement.

---

# ⚡ Rapid Access

| Route | Use it for | Access |
|---|---|---|
| **Start Here** | Account setup and early progression | [Open guide →](docs/getting-started/index.md) |
| **Emergency Services** | Service-specific vehicles, personnel and stations | [Browse services →](docs/services/index.md) |
| **Verified Vehicles** | Current canonical deployable-resource records | [Open records →](docs/reference/verified-vehicle-records.md) |
| **Verified Missions** | Current cross-service mission records | [Open records →](docs/reference/verified-mission-records.md) |
| **Airfield Operations** | Airport fleet, extensions and aircraft incidents | [Open Stage 19 →](docs/reference/verified-mission-batch-8.md) |
| **Recovery Operations** | Recovery Centres, towing and HGV variations | [Open Stage 20 →](docs/reference/verified-mission-batch-9.md) |
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
Patient and towing range validation
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
