# Fire Mission-Family Pressure Analysis

Stage 37A closes by converting the complete canonical Fire mission estate into a live, evidence-labelled demand profile. The analysis below reads the same versioned `missions.json` export used by Mission Lookup and the public API, then reports only transparent counts and sums from published fields.

!!! info "Evidence boundary"
    Mission counts, guaranteed quantities, alternative-group quantities, patient maxima and personnel-field presence are calculated directly from canonical records in the current export. Family tags are deterministic analytical labels and may overlap. They are not official MissionChief categories, mission frequencies, dispatch recommendations or hidden unlock rules.

**Current evidence baseline:** 28 July 2026.

## What this analysis answers

Use the dashboard to identify:

- which capability families occupy the largest part of the Fire catalogue;
- which guaranteed resources accumulate the greatest catalogue-wide demand;
- which missions create the highest single-incident unit load;
- where independent alternative groups create command or specialist bottlenecks;
- where patient and personnel fields add pressure beyond vehicle quantities;
- which family should drive the next fleet, training or geographic investment.

It does **not** estimate how often a mission will spawn. A quantity summed across the catalogue is a **catalogue pressure indicator**, not an expected daily dispatch total.

## Deterministic family tags

A mission can belong to several families because operational capabilities overlap. For example, a railway incident may also be technical rescue, mass casualty, HazMat and foam response.

| Family | Tagging evidence |
|---|---|
| Airfield and airport | Airport category, airfield extensions or dedicated airfield resources |
| Railway and tunnel | Railway categories, Railway Fire Response or Road Rail capability |
| Flood and water damage | Flood/pump extensions, water-damage category or Flood Rescue Units |
| Wildfire and forest fire | Published mission name contains forest fire or wildfire |
| HazMat and CBRN | HazMat, CBRN or HazMat-container alternatives |
| Foam and fire support | Fire-support category, Foam Extensions or verified foam resources |
| Technical rescue | Technical Rescue Extensions, Rescue Support Vehicles or rescue containers |
| Mass casualty and high patient load | Mass-casualty category/equipment or patient maximum of at least 20 |
| Rural fire | Official rural category |
| Urban and structural fire | Official urban category |
| General fire | No specialist analytical tag applies |

!!! warning "Overlapping rows"
    Do not add family mission counts together to produce a Fire total. One mission can appear in multiple family rows by design.

<style>
.fire-pressure-controls {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: .8rem;
  margin: 1rem 0;
}
.fire-pressure-controls label {
  display: grid;
  gap: .35rem;
  font-weight: 600;
}
.fire-pressure-controls input,
.fire-pressure-controls select {
  width: 100%;
  padding: .55rem .65rem;
  border: 1px solid var(--md-default-fg-color--lightest);
  border-radius: .3rem;
  background: var(--md-default-bg-color);
  color: var(--md-default-fg-color);
}
.fire-pressure-history {
  align-content: end;
  grid-template-columns: auto 1fr !important;
  align-items: center;
}
.fire-pressure-history input {
  width: auto;
}
.fire-pressure-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: .75rem;
  margin: 1rem 0 1.25rem;
}
.fire-pressure-card {
  display: grid;
  gap: .2rem;
  padding: .85rem;
  border: 1px solid var(--md-default-fg-color--lightest);
  border-radius: .35rem;
  background: var(--md-code-bg-color);
}
.fire-pressure-card strong {
  font-size: 1.35rem;
}
.fire-pressure-card span {
  font-size: .78rem;
  color: var(--md-default-fg-color--light);
}
.fire-pressure-table-wrap {
  overflow-x: auto;
  margin-bottom: 1.25rem;
}
.fire-pressure-table-wrap table {
  min-width: 680px;
}
#fire-pressure-status {
  padding: .7rem .8rem;
  border-left: .2rem solid var(--md-accent-fg-color);
  background: var(--md-code-bg-color);
}
.fire-pressure-error #fire-pressure-status {
  border-left-color: #d32f2f;
}
</style>

## Live canonical pressure dashboard

<div id="fire-pressure-dashboard" data-source="../../assets/data/v1/missions.json">
  <div class="fire-pressure-controls">
    <label>
      Mission family
      <select id="fire-pressure-family" aria-label="Select Fire mission family">
        <option>Loading canonical families…</option>
      </select>
    </label>
    <label>
      Search missions
      <input id="fire-pressure-search" type="search" placeholder="Example: hotel, railway, flood" aria-label="Search Fire missions">
    </label>
    <label class="fire-pressure-history">
      <input id="fire-pressure-history" type="checkbox" checked>
      Include historical and event-window records
    </label>
  </div>

  <p id="fire-pressure-status" role="status">Loading the canonical Fire mission export…</p>

  <div id="fire-pressure-summary" class="fire-pressure-summary" aria-live="polite"></div>

  <h3>Family profile</h3>
  <div class="fire-pressure-table-wrap">
    <table>
      <thead>
        <tr>
          <th>Analytical family</th>
          <th>Missions</th>
          <th>Guaranteed units across catalogue</th>
          <th>Fire Engine units</th>
          <th>Highest single mission</th>
        </tr>
      </thead>
      <tbody id="fire-pressure-family-body">
        <tr><td colspan="5">Loading…</td></tr>
      </tbody>
    </table>
  </div>

  <h3>Highest accumulated guaranteed-resource demand</h3>
  <p>This table sums only guaranteed resource rows in the current filter. Alternatives remain separate because selecting one valid option is a dispatch decision.</p>
  <div class="fire-pressure-table-wrap">
    <table>
      <thead>
        <tr>
          <th>Canonical resource ID</th>
          <th>Guaranteed quantity across catalogue</th>
          <th>Missions containing the guaranteed row</th>
        </tr>
      </thead>
      <tbody id="fire-pressure-resource-body">
        <tr><td colspan="3">Loading…</td></tr>
      </tbody>
    </table>
  </div>

  <h3>Highest single-mission guaranteed load</h3>
  <div class="fire-pressure-table-wrap">
    <table>
      <thead>
        <tr>
          <th>Mission</th>
          <th>Analytical families</th>
          <th>Guaranteed units</th>
          <th>Independent alternative slots</th>
          <th>Patient maximum</th>
        </tr>
      </thead>
      <tbody id="fire-pressure-mission-body">
        <tr><td colspan="5">Loading…</td></tr>
      </tbody>
    </table>
  </div>
</div>

## Reading the metrics safely

### Guaranteed resource units

This is the arithmetic sum of all quantities in `requirements.guaranteed`. It provides a reproducible measure of visible vehicle/resource pressure. It does not account for journey time, treatment duration, crew availability or whether one vehicle can satisfy another capability through verified substitution.

### Independent alternative slots

This sums the quantity attached to every alternative group. Each group must be treated independently. A single ICCU, Ambulance Control Unit or specialist vehicle must not be reused across several slots unless dispatch behaviour explicitly proves that reuse.

### Patient maximum

The dashboard reports the published maximum patient field. It does not convert patients into a guessed ambulance requirement. Treatment, transport probability, critical-care probability, hospital availability and handoff time remain separate operational constraints.

### Personnel-field presence

A mission is counted when it publishes required, available or ranged personnel data. The count indicates where vehicle-only fleet planning is insufficient; it does not flatten different personnel semantics into one number.

## Operational decision sequence

1. Select the family currently generating delays or alliance dependence.
2. Review its accumulated guaranteed-resource table.
3. Inspect the highest single-mission loads.
4. Open representative missions in [Mission Lookup](../tools/mission-lookup.md).
5. Test two or more incidents in the [Concurrent Fleet Planner](../tools/fleet-planner.md).
6. Compare candidate resources in [Resource Comparison](../tools/resource-comparison.md).
7. Identify whether the deficit is quantity, geography, training, command, towing, carrier capacity or another service.
8. Correct the measured bottleneck before activating more generators.

## Progression implications

| Pressure pattern | Recommended interpretation |
|---|---|
| High mission count, low single-mission load | Prioritise geographic frontline coverage and routine concurrency |
| Low mission count, high specialist load | Protect rare specialists and use regional reserve planning |
| High alternative-slot pressure | Increase independently crewed command or substitution options |
| High patient maxima | Audit ambulance command, transport, critical care and hospitals separately |
| High Fire Engine accumulation | Expand staffed frontline depth before adding another specialist generator |
| High technical-rescue accumulation | Distribute Rescue Support and trained crews by response zone |
| High railway/airfield/flood pressure | Commission the complete cross-service chain rather than Fire assets alone |

## Stage 37A completion

Batch 7 completes the Fire & Rescue operational-guide programme:

1. progression foundation;
2. specialist extensions and container logistics;
3. training and personnel planning;
4. airfield and railway response;
5. wildfire, flood and water rescue;
6. major-incident resilience;
7. live mission-family pressure analysis.

The Fire programme now moves into evidence maintenance. The next service programme is **Stage 37B — Ambulance & HART operational progression**.
