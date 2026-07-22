# Concurrent Fleet Planner

Select a verified mission and estimate the published guaranteed-resource requirement for several simultaneous incidents.

<div class="mcuk-tool" data-mcuk-tool="fleet-planner">
  <div class="mcuk-tool-controls">
    <label>
      Mission
      <select data-role="mission"></select>
    </label>
    <label>
      Concurrent incidents
      <input data-role="concurrency" type="number" min="1" max="50" value="1">
    </label>
  </div>
  <div data-role="results" aria-live="polite">Loading mission data…</div>
</div>

## Calculation method

For guaranteed resources:

```text
published quantity × concurrent incident count
```

Alternative groups are shown independently as a total number of qualifying resources. The planner does not choose an allocation between alternatives.

## Scope limitations

This is a requirement multiplier, not a complete cover model. It does not account for:

- travel time or station geography;
- vehicles already committed elsewhere;
- personnel availability or qualifications;
- reserve-cover policy;
- alliance support;
- probabilistic or conditionally triggered resources;
- whether one resource can satisfy overlapping alternative rows.

Use the result as a verified lower-level planning input, not as a guarantee of operational readiness.
