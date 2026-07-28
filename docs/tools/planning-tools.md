# Intelligence Tools Programme

Stages 29–32 established deterministic browser-side evidence lookup and comparison. Stage 40 adds local-only account readiness modelling without connecting to or mutating a MissionChief account.

## Live tools

### Account Readiness Planner

Combines selected canonical missions, concurrency, user-entered operational inventory and protected reserve. It checks guaranteed resources, capacity-aware alternative allocation, exact personnel, generation thresholds, towing/carrier compatibility and recovery workloads while preserving unknown and non-exact evidence states.

[Open Account Readiness Planner](account-readiness.md)

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
- Account-readiness scenarios remain local unless the user explicitly exports JSON.

## Data flow

```text
Canonical JSON records + user-entered local inventory
                    ↓
Schema-controlled evidence interpretation
                    ↓
Browser-side allocation and gap calculations
                    ↓
Ready / Watch / Degraded / Unavailable planning state
```

## Privacy model

The readiness planner uses browser local storage for optional saved scenarios. It does not authenticate against MissionChief, scrape account pages or upload inventory to this project. Export and import are explicit user-controlled JSON actions.

## Future enhancement boundary

Authenticated account integration, automatic inventory scraping, server-side scenario storage and hidden dispatch inference are outside the current evidence and privacy model. Routing and geographic optimisation remain separate future work because they require map, travel-time and account-location inputs.
