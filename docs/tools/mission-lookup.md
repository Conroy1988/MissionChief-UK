# Mission Requirement Lookup

Search the production MissionChief UK mission dataset by ID, name, alias, POI or mission type. Results are loaded from the versioned JSON export generated during deployment.

<div class="mcuk-tool" data-mcuk-tool="mission-lookup">
  <div class="mcuk-tool-controls">
    <label>
      Search
      <input data-role="query" type="search" placeholder="e.g. train derailment, 588, harbour">
    </label>
    <label>
      Service
      <select data-role="service"></select>
    </label>
  </div>
  <div data-role="results" aria-live="polite">Loading verified mission data…</div>
</div>

## Interpretation

The lookup distinguishes:

- guaranteed resources;
- probability-based resources;
- conditional resources;
- independent alternative groups;
- generation preconditions;
- patient ranges;
- evidence status and verification date.

An empty dispatch table means that dispatch-level evidence is not published for that record. It does not mean that no response is required.

## Data source

This tool consumes `assets/data/v1/missions.json`. It performs no independent scraping and cannot override the canonical repository records.
