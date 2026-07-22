# 🚨 MissionChief UK — The Complete Guide

**MissionChief UK** is an independent, searchable knowledge base for the UK version of MissionChief.

The objective is comprehensive coverage: every service, mission, vehicle, building, extension, training requirement, game system, strategy, alliance workflow, useful script and recurring player question—documented in one maintainable project.

> This project is independent and is not operated by or affiliated with SHPlay GmbH or the official MissionChief team.

## Project scope

| Area | Coverage |
|---|---|
| Core game | Credits, coins, missions, dispatching, patients, prisoners and transport |
| Emergency services | Fire, Ambulance, Police, Coastguard, Lifeboat, Mountain Rescue and specialist resources |
| Infrastructure | Stations, extensions, classrooms, hospitals, prisons and dispatch centres |
| Resources | Vehicles, trailers, aircraft, boats, personnel, qualifications and equipment |
| Strategy | Progression, placement, staffing, fleet composition, coverage and finance |
| Alliances | Roles, funds, shared buildings, events, rules and operational coordination |
| Scripts and tools | LSSM, userscripts, browser tools, installation and recommended settings |
| Reference data | Structured game records designed for site search and future API use |

## Repository structure

```text
.
├── docs/                 # Human-readable guides
│   ├── getting-started/
│   ├── systems/
│   ├── services/
│   ├── strategy/
│   ├── alliances/
│   ├── scripts/
│   ├── reference/
│   └── contributing/
├── data/                 # Structured searchable game data
│   ├── schema/
│   └── uk/
├── mkdocs.yml            # Documentation site and navigation
└── requirements.txt      # Local documentation dependencies
```

## Local preview

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
mkdocs serve
```

Open `http://127.0.0.1:8000`.

## Information standard

Content must distinguish between:

- **Verified facts** — confirmed against the current UK game, official material or reproducible behaviour
- **Calculated guidance** — derived from verified values and explained
- **Operational recommendations** — strategy that can vary by account, geography or play style
- **Unverified observations** — community reports awaiting confirmation

Records should include verification dates and sources wherever practical. MissionChief changes over time; undocumented assumptions will not be treated as facts.

## Current status

The project is in its **foundation phase**. The site framework, content taxonomy, data model and contribution standards are being established before systematic population of the knowledge base.

See [`docs/ROADMAP.md`](docs/ROADMAP.md).

## Contributing

Corrections, verified data, screenshots, guide improvements and tool documentation are welcome. Read [`docs/contributing/index.md`](docs/contributing/index.md) before submitting changes.

## Licence

Original project code and content are released under the [MIT Licence](LICENSE), unless a file states otherwise. Third-party names, screenshots, game assets and quoted material remain the property of their respective owners.
