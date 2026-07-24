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

## Current coverage

```text
1,062 official UK missions
284 canonical mission records
267 direct official/canonical ID matches
226 fully canonical missions
795 official missions awaiting direct canonical records
```

The full five-gate position and per-mission blockers are published on the [Mission Verification Status](../reference/mission-verification-status.md) page.

## Evidence levels

The lookup deliberately distinguishes the source and normalized evidence tiers:

- **Official catalogue** — the mission exists in the current public MissionChief UK catalogue and its official raw requirement keys are shown verbatim.
- **Canonical mapped** — a project record has been normalized into verified resources, probabilities, alternatives, personnel, patients and preconditions where those fields have been reproduced.
- **Fully canonical** — the record has passed identity, official-key mapping, operational and final evidence-completeness gates in the verification programme.

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

## Verification programme

Every mission progresses through:

1. captured;
2. identity verified;
3. requirements mapped;
4. operationally verified; and
5. fully canonical.

The machine-readable status exposes every mission’s current stage, canonical path, blocking reasons and next action. A mission can only enter a mapped stage when every official requirement, chance and prerequisite key it uses is present in the verified key registry.

## Data sources

The tool and supporting verification pages consume:

```text
assets/data/v1/missions.json
assets/data/official/uk-missions.json
assets/data/official/uk-mission-coverage.json
assets/data/official/uk-mission-verification.json
```

The official catalogue is refreshed from `https://www.missionchief.co.uk/einsaetze.json`, checksummed, reconciled against canonical IDs and committed through an isolated ingestion workflow. Every complete raw official object remains retained under `data/sources/missionchief-uk/` for audit and future mapping.
