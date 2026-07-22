<div align="center">

<img src="assets/readme/mission-control-hero.svg" alt="MissionChief UK Command Knowledge Centre" width="100%">

<br>

[![Documentation](https://img.shields.io/badge/OPEN-DOCUMENTATION-1593D1?style=for-the-badge&logo=readthedocs&logoColor=white)](https://conroy1988.github.io/MissionChief-UK/)
[![MissionChief UK](https://img.shields.io/badge/REGION-UNITED_KINGDOM-0B1D31?style=for-the-badge)](https://www.missionchief.co.uk/)
[![Evidence Standard](https://img.shields.io/badge/INTELLIGENCE-EVIDENCE_LED-1675A9?style=for-the-badge&logo=databricks&logoColor=white)](docs/reference/data-standard.md)
[![Project Phase](https://img.shields.io/badge/STATUS-FOUNDATION_PHASE-D63345?style=for-the-badge)](docs/ROADMAP.md)

[![Deploy MissionChief UK Guide](https://github.com/Conroy1988/MissionChief-UK/actions/workflows/deploy-pages.yml/badge.svg)](https://github.com/Conroy1988/MissionChief-UK/actions/workflows/deploy-pages.yml)
[![Last Commit](https://img.shields.io/github/last-commit/Conroy1988/MissionChief-UK?style=flat-square)](https://github.com/Conroy1988/MissionChief-UK/commits/main)
[![Issues](https://img.shields.io/github/issues/Conroy1988/MissionChief-UK?style=flat-square)](https://github.com/Conroy1988/MissionChief-UK/issues)
[![Licence](https://img.shields.io/github/license/Conroy1988/MissionChief-UK?style=flat-square)](LICENSE)

### The independent UK command knowledgebase for MissionChief

**Game intelligence · Service references · Strategy · Scripts · Structured data · Community knowledge**

[Enter the Command Centre](https://conroy1988.github.io/MissionChief-UK/) · [Start Here](docs/getting-started/index.md) · [Search the Database](docs/reference/index.md) · [View the Roadmap](docs/ROADMAP.md) · [Contribute](docs/contributing/index.md)

</div>

---

## 🚨 Mission Briefing

**MissionChief UK** is being built as the definitive, searchable knowledge centre for the United Kingdom version of MissionChief.

The objective is not another partial wiki or loose collection of tips. The objective is a maintained operational reference capable of answering practical questions across the entire game:

- What should I build next?
- Which vehicles, extensions and training courses does a mission require?
- How should a station or specialist fleet be configured?
- Which scripts are useful, safe and compatible with the UK game?
- How do alliance systems, transport, patients, prisoners and credits actually work?
- Which information is verified fact, calculated guidance, strategic recommendation or still awaiting confirmation?

> **Command principle:** useful information must be easy to find, current enough to trust and precise enough to act on.

---

## 🛰️ Command Network

<table>
<tr>
<td width="25%" align="center"><h3>🚒</h3><strong>Fire & Rescue</strong><br><sub>Stations, appliances, specialist units, extensions and staffing.</sub></td>
<td width="25%" align="center"><h3>🚑</h3><strong>Ambulance</strong><br><sub>Patients, transport, hospitals, response assets and clinical resources.</sub></td>
<td width="25%" align="center"><h3>🚓</h3><strong>Police</strong><br><sub>Custody, prisoners, public order, investigation and specialist policing.</sub></td>
<td width="25%" align="center"><h3>🚁</h3><strong>Air Operations</strong><br><sub>Helicopters, aircraft, bases, roles and deployment requirements.</sub></td>
</tr>
<tr>
<td align="center"><h3>🚤</h3><strong>Maritime</strong><br><sub>Coastguard, lifeboat, inland rescue and seagoing operations.</sub></td>
<td align="center"><h3>⛰️</h3><strong>Specialist Rescue</strong><br><sub>Mountain rescue, technical capability and cross-service response.</sub></td>
<td align="center"><h3>🏗️</h3><strong>Infrastructure</strong><br><sub>Buildings, extensions, classrooms, hospitals and dispatch centres.</sub></td>
<td align="center"><h3>📡</h3><strong>Command Systems</strong><br><sub>Dispatching, missions, finance, alliances and account progression.</sub></td>
</tr>
</table>

---

## ⚡ Rapid Access

| Operational route | Use it for | Access |
|---|---|---|
| **New Player Control** | Account setup, first buildings, early fleets and expansion order | [Deploy guide →](docs/getting-started/index.md) |
| **Game Systems** | Credits, coins, missions, patients, prisoners, transport and dispatching | [Open systems →](docs/systems/index.md) |
| **Emergency Services** | Vehicles, personnel, training, stations and specialist resources | [Browse services →](docs/services/index.md) |
| **Strategy Room** | Placement, staffing, fleet composition, coverage and financial efficiency | [Open strategy →](docs/strategy/index.md) |
| **Alliance Operations** | Roles, funds, events, shared buildings, rules and coordination | [Open alliance guides →](docs/alliances/index.md) |
| **Scripts & Tools** | LSSM, userscripts, browser tools, installation and recommended settings | [Inspect tools →](docs/scripts/index.md) |
| **Reference Database** | Structured records, aliases, requirements and future calculator data | [Search records →](docs/reference/index.md) |

---

## 🧠 Intelligence Classification

This project deliberately separates evidence from opinion.

| Marker | Classification | Definition |
|:---:|---|---|
| ✅ | **Verified** | Reproduced in the current UK game or confirmed through a reliable primary source |
| 🧮 | **Calculated** | Derived from verified values with the method documented |
| 🎯 | **Recommended** | Operational guidance that can vary by account, geography or play style |
| ⚠️ | **Review required** | Potentially outdated, incomplete or awaiting reproduction |

Every mature record should include a verification date and source trail wherever practical. MissionChief changes over time; undocumented assumptions are not treated as facts.

[Read the full data and evidence standard →](docs/reference/data-standard.md)

---

## 🗃️ Knowledgebase Architecture

```text
MISSIONCHIEF UK COMMAND CENTRE
│
├── Human-readable intelligence
│   ├── Getting started and progression
│   ├── Game systems and mechanics
│   ├── Emergency-service references
│   ├── Strategy and fleet planning
│   ├── Alliance operations
│   └── Scripts, tools and configuration
│
├── Structured reference data
│   ├── Vehicles and trailers
│   ├── Buildings and extensions
│   ├── Personnel and training
│   ├── Missions and requirements
│   ├── Aliases and terminology
│   └── Future calculators and APIs
│
└── Delivery platform
    ├── GitHub repository
    ├── MkDocs Material website
    ├── Instant full-text search
    └── Automated GitHub Pages deployment
```

<details>
<summary><strong>View the repository structure</strong></summary>

```text
.
├── .github/
│   └── workflows/
│       └── deploy-pages.yml
├── assets/
│   └── readme/
├── docs/
│   ├── getting-started/
│   ├── systems/
│   ├── services/
│   ├── strategy/
│   ├── alliances/
│   ├── scripts/
│   ├── reference/
│   ├── contributing/
│   └── stylesheets/
├── data/
│   ├── schema/
│   └── uk/
├── mkdocs.yml
├── requirements.txt
└── README.md
```

</details>

---

## 📊 Operational Roadmap

```text
PHASE 01  ████████████████████  Foundation and standards
PHASE 02  ███░░░░░░░░░░░░░░░░  Core systems and progression
PHASE 03  ██░░░░░░░░░░░░░░░░░  Emergency-service references
PHASE 04  █░░░░░░░░░░░░░░░░░░  Searchable structured database
PHASE 05  ░░░░░░░░░░░░░░░░░░░  Scripts and recommended setups
PHASE 06  ░░░░░░░░░░░░░░░░░░░  Calculators and planning tools
PHASE 07  ░░░░░░░░░░░░░░░░░░░  Community intelligence network
PHASE 08  ░░░░░░░░░░░░░░░░░░░  Public data services and API
```

### Current deployment state

- [x] Repository and documentation architecture
- [x] Evidence and editorial standards
- [x] Search-ready MkDocs Material platform
- [x] Custom MissionChief UK visual identity
- [x] Automated GitHub Pages deployment workflow
- [ ] Core game-system publication
- [ ] Service-by-service reference population
- [ ] Comprehensive missions and requirements database
- [ ] Script catalogue and compatibility matrix
- [ ] Interactive calculators and planning tools

[Open the complete roadmap →](docs/ROADMAP.md)

---

## 🧩 Scripts & Tools Doctrine

Scripts will not be listed merely because they exist. Each documented tool should explain:

- what it changes;
- how it is installed;
- which browsers and devices it supports;
- whether it is actively maintained;
- which permissions it requests;
- whether it conflicts with other tools;
- the recommended MissionChief UK configuration;
- known limitations, risks and recovery steps.

This area is intended to become a practical compatibility and configuration centre for LSSM, userscripts, browser extensions and community tooling.

[Enter Scripts & Tools →](docs/scripts/index.md)

---

## 🛠️ Run the Command Centre Locally

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate

pip install -r requirements.txt
mkdocs serve
```

Open `http://127.0.0.1:8000`.

For a production-equivalent validation build:

```bash
mkdocs build --strict
```

---

## 🤝 Contribute Operational Intelligence

Corrections, verified values, screenshots, reproducible observations, strategy analysis and tool documentation are welcome.

Before submitting information:

1. distinguish observed fact from recommendation;
2. include the UK game context;
3. provide a source or reproducible test where possible;
4. note when the information was last verified;
5. avoid copying third-party work without permission and appropriate treatment.

[Read the contribution and editorial requirements →](docs/contributing/index.md)

---

## ⚖️ Independence & Attribution

This is an independent community project. It is **not operated by, endorsed by or affiliated with SHPlay GmbH or the official MissionChief team**.

MissionChief names, trademarks, screenshots, game artwork and third-party materials remain the property of their respective owners. Original project code and content are released under the [MIT Licence](LICENSE), unless a file states otherwise.

---

<div align="center">

### 🚨 Build the knowledge. Improve the response. Command the game.

[![Enter Command Centre](https://img.shields.io/badge/ENTER_THE-COMMAND_CENTRE-1593D1?style=for-the-badge&logo=googlemaps&logoColor=white)](https://conroy1988.github.io/MissionChief-UK/)

<sub>MissionChief UK · Independent command knowledgebase · Maintained on GitHub</sub>

</div>
