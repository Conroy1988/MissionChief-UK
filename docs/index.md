<div class="mcuk-hero" markdown>

<span class="mcuk-kicker">UK Operations Intelligence Platform</span>

# MissionChief UK Command Centre

The independent, evidence-led guide for MissionChief UK—combining operational references, verified structured data, interactive planning tools and a versioned public API.

<div class="mcuk-actions" markdown>
[Search mission requirements](tools/mission-lookup.md){ .md-button .md-button--primary }
[Plan concurrent resources](tools/fleet-planner.md){ .md-button }
[Open the static API](api/index.md){ .md-button }
</div>

</div>

<div class="mcuk-status-grid">
  <div class="mcuk-status"><strong>Stage 34</strong>Core programme complete</div>
  <div class="mcuk-status"><strong>62 missions</strong>Verified production records</div>
  <div class="mcuk-status"><strong>75 entities</strong>Resources, infrastructure and qualifications</div>
  <div class="mcuk-status"><strong>API v1</strong>Versioned public exports</div>
</div>

## Select an operational route

<div class="grid cards" markdown>

-   :material-database-search: **Mission intelligence**

    ---

    Search mission IDs, names, POIs, preconditions, patients and requirement groups.

    [:octicons-arrow-right-24: Open Mission Lookup](tools/mission-lookup.md)

-   :material-fire-truck: **Emergency services**

    ---

    Navigate Fire, Ambulance, Police, Coastguard, Lifeboat, Mountain Rescue, SAR, EOD, Airfield, Recovery and Railway response.

    [:octicons-arrow-right-24: Browse services](services/index.md)

-   :material-compare: **Compare resources**

    ---

    Compare canonical vehicles or qualifications while keeping unknown values visible.

    [:octicons-arrow-right-24: Open comparison](tools/resource-comparison.md)

-   :material-calculator-variant: **Plan concurrent incidents**

    ---

    Multiply guaranteed requirements and preserve independent alternative groups.

    [:octicons-arrow-right-24: Open Fleet Planner](tools/fleet-planner.md)

-   :material-message-question: **Ask the catalogue**

    ---

    Use ordinary words or a short question to search the generated cross-collection evidence index.

    [:octicons-arrow-right-24: Open Query Catalogue](tools/query-catalogue.md)

-   :material-database-export: **Use the data API**

    ---

    Consume versioned mission, resource, infrastructure, training, search and FAQ exports.

    [:octicons-arrow-right-24: Read API guide](api/index.md)

-   :material-rocket-launch: **Start and progress**

    ---

    Build correctly, avoid early waste and understand the initial expansion path.

    [:octicons-arrow-right-24: Begin here](getting-started/index.md)

-   :material-source-branch: **Contribute intelligence**

    ---

    Submit corrections, reproducible UK evidence and new mission or resource data.

    [:octicons-arrow-right-24: Contribution standard](contributing/index.md)

</div>

## Production state

```text
62 mission records
46 deployable resources
18 infrastructure records
11 qualification records
13 verified mission batches
```

Every production build validates JSON schemas, resource and infrastructure relationships, patient/towing/personnel ranges, generated exports and the strict documentation build before Pages deployment.

## Intelligence standard

| Classification | Operational meaning |
|---|---|
| **Verified** | Reproduced in the current UK game or supported by a suitable primary source |
| **Calculated** | Derived transparently from verified values |
| **Recommended** | Strategy that may vary by account, geography or play style |
| **Review required** | Incomplete, contradictory, outdated or awaiting reproduction |

!!! info "Evidence boundary"
    Verified applies only to populated fields. Missing data remains unknown rather than being converted into a zero or an assumption.

The [roadmap](ROADMAP.md) records the completed Stages 1–34 programme and the remaining continuous evidence-maintenance priorities.

---

> **Independent project:** This guide is not operated by or affiliated with SHPlay GmbH or the official MissionChief team. MissionChief names, screenshots and game assets remain the property of their respective owners.
