# Mission Requirement Lookup

Search the complete official MissionChief UK mission catalogue alongside the higher-trust canonical records maintained by this project. The lookup covers mission IDs, names, aliases, POIs, categories, generating services, official requirement keys and generation prerequisites.

<div class="mcuk-tool" data-mcuk-tool="mission-lookup">
  <div class="mcuk-tool-controls mcuk-mission-lookup-controls">
    <label>
      Search
      <input data-role="query" type="search" placeholder="e.g. train derailment, 588, harbour, HART">
    </label>
    <label>
      Service or generator
      <select data-role="service"></select>
    </label>
    <label>
      Evidence coverage
      <select data-role="source">
        <option value="">All official UK missions</option>
        <option value="canonical">Canonical mapped records</option>
        <option value="official">Official catalogue awaiting full mapping</option>
      </select>
    </label>
  </div>
  <div class="mcuk-catalogue-summary" data-role="summary" aria-live="polite"></div>
  <div data-role="results" aria-live="polite">Loading the official UK mission catalogue…</div>
</div>

## Evidence levels

The lookup deliberately distinguishes two evidence states:

- **Canonical mapped** — a project record has been normalized into verified resources, probabilities, alternatives, personnel, patients and preconditions where those fields have been reproduced.
- **Official catalogue** — the mission exists in the current public MissionChief UK catalogue and its official raw requirement keys are shown verbatim, but every key has not yet been promoted into the canonical resource model.

An official catalogue record is authoritative evidence that the mission and displayed official fields exist. It is not automatically a verified dispatch recommendation. Unknown internal keys are never guessed into vehicle types.

## Canonical interpretation

Canonical records distinguish:

- guaranteed resources;
- probability-based resources;
- conditional resources;
- independent alternative groups;
- generation preconditions;
- patient and prisoner ranges;
- personnel requirements;
- evidence status and verification date.

An empty dispatch table means that dispatch-level evidence is not published for that canonical record. It does not mean that no response is required.

## Data sources

The tool consumes:

```text
assets/data/v1/missions.json
assets/data/official/uk-missions.json
assets/data/official/uk-mission-coverage.json
```

The official catalogue is refreshed from `https://www.missionchief.co.uk/einsaetze.json`, checksummed, reconciled against canonical IDs and committed through an isolated ingestion workflow. Every complete raw official object remains retained under `data/sources/missionchief-uk/` for audit and future mapping.
