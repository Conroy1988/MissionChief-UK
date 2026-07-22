# Intelligence Tools Programme

Stages 29–32 convert the structured reference database into practical browser-side decision support.

## Live tools

### Mission Requirement Lookup

Searches missions by ID, name, alias, POI and mission type. It renders guaranteed, probabilistic, conditional and alternative resources without merging their meanings.

[Open Mission Lookup](mission-lookup.md)

### Resource and Qualification Comparison

Compares two deployable resources or qualification records using only populated canonical fields. Unknown costs, staffing or course details remain visibly unverified.

[Open Comparison Tool](resource-comparison.md)

### Concurrent Fleet Planner

Multiplies published guaranteed requirements for several simultaneous incidents and preserves alternative groups independently.

[Open Fleet Planner](fleet-planner.md)

### Natural-Language Query Catalogue

Matches ordinary questions and keywords against the generated cross-collection search index. It is deterministic evidence retrieval, not generative inference.

[Open Query Catalogue](query-catalogue.md)

## Engineering principles

- Structured data is the single source of truth.
- Calculations are reproducible in the browser.
- Assumptions and scope limits are displayed beside results.
- Unknown values never silently become zero.
- Recommendations remain distinct from verified game mechanics.
- Tools fail visibly when versioned exports cannot be loaded.
- No tool mutates a MissionChief account or repository record.

## Data flow

```text
Canonical JSON records
        ↓
Schema and relationship validation
        ↓
Versioned v1 exports
        ↓
Browser-side lookup and calculations
```

## Future enhancement

The delivered tools establish a stable read-only layer. Saved scenarios, account inventory import, routing, geographic optimisation and authenticated account integration remain optional future features and would require separate privacy and evidence controls.
