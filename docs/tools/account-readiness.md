# Account Readiness Planner

Build a local-only readiness scenario from the canonical UK mission catalogue, then compare the published requirements with the operational inventory and protected reserve that you enter.

!!! info "Privacy and evidence boundary"
    The planner runs entirely in your browser. It does not sign in to MissionChief, scrape an account, send inventory to this project or mutate game data. Saved scenarios use this browser's local storage. Blank inventory fields remain **unknown** rather than becoming zero. Recommendations and readiness labels are planning outputs, not hidden game rules.

<div class="mcuk-tool mcuk-readiness" data-mcuk-tool="account-readiness">
  <section class="mcuk-readiness-panel" aria-labelledby="readiness-scenario-heading">
    <h2 id="readiness-scenario-heading">1. Build the reference scenario</h2>
    <div class="mcuk-tool-controls mcuk-readiness-controls">
      <label>
        Canonical mission
        <select data-role="mission" aria-label="Canonical mission"></select>
      </label>
      <label>
        Concurrent copies
        <input data-role="concurrency" type="number" min="1" max="50" value="1" inputmode="numeric">
      </label>
      <button type="button" data-action="add-mission">Add mission</button>
      <button type="button" data-action="clear-current" class="md-button">Clear current</button>
    </div>
    <div data-role="scenario" aria-live="polite"><p>Loading canonical mission data…</p></div>
  </section>

  <section class="mcuk-readiness-panel" aria-labelledby="readiness-inventory-heading">
    <h2 id="readiness-inventory-heading">2. Enter deployable inventory</h2>
    <p><strong>Dispatchable units</strong> means correctly staffed, trained and usable units. Protected reserve defaults visibly to zero and is subtracted from incident cover. Leave dispatchable or personnel values blank when they are unknown.</p>
    <div data-role="inventory"><p>Add at least one mission to create the inventory worksheet.</p></div>
  </section>

  <section class="mcuk-readiness-panel" aria-labelledby="readiness-results-heading">
    <h2 id="readiness-results-heading">3. Review readiness</h2>
    <div data-role="summary" class="mcuk-readiness-summary" aria-live="polite"></div>
    <div data-role="results" aria-live="polite"><p>No scenario selected.</p></div>
  </section>

  <section class="mcuk-readiness-panel" aria-labelledby="readiness-storage-heading">
    <h2 id="readiness-storage-heading">4. Save or transfer the scenario</h2>
    <div class="mcuk-tool-controls mcuk-readiness-controls">
      <label>
        Scenario name
        <input data-role="scenario-name" type="text" value="My readiness scenario" maxlength="80">
      </label>
      <button type="button" data-action="save-local">Save in this browser</button>
      <label>
        Saved scenarios
        <select data-role="saved-scenarios" aria-label="Saved readiness scenarios">
          <option value="">No saved scenarios</option>
        </select>
      </label>
      <button type="button" data-action="load-local">Load</button>
      <button type="button" data-action="delete-local" class="md-button">Delete</button>
      <button type="button" data-action="export-json">Export JSON</button>
      <label class="mcuk-readiness-file">
        Import JSON
        <input data-role="import-json" type="file" accept="application/json,.json">
      </label>
    </div>
    <p data-role="storage-status" class="mcuk-evidence-note" role="status">Nothing leaves this browser unless you explicitly export a JSON file.</p>
  </section>
</div>

## What the planner checks

The calculation keeps each evidence type separate:

1. **Guaranteed resources** are added across selected missions and concurrency.
2. **Alternative groups** are allocated with a capacity-aware flow calculation, so one unit is not silently reused across several independent groups.
3. **Required incident personnel** are added across the scenario.
4. **Available-before-generation personnel** use the highest published threshold for each role rather than being added as dispatch demand.
5. **Trailers and containers** are checked against published compatible towing or carrier resources in a separate logistics calculation.
6. **Recovery assets** are reported as car or truck clearing workload, not converted into fictional emergency-vehicle rows.
7. Probabilistic, conditional, ranged and average-minimum fields remain advisory evidence and do not become exact gaps.

## Readiness states

| State | Meaning |
|---|---|
| **Ready** | Every exact requirement with relevant inventory data is covered after protected reserve |
| **Watch** | No definite exact gap is proven, but one or more inventory values or non-exact evidence fields remain unresolved |
| **Degraded** | At least one exact guaranteed, alternative, personnel or towing requirement has a definite shortfall |
| **Unavailable** | No mission scenario has been selected |

## Scope limitations

The planner does not model travel time, station routing, hospital or custody turnaround, incident duration, staff assignment rules, dispatch substitution that is not canonical, or whether a towing vehicle can simultaneously satisfy another response role. Use [Station Placement](../strategy/station-placement.md) for geography and the [Concurrent Fleet Planner](fleet-planner.md) for a simpler published-requirement multiplier.
