# Resource and Qualification Comparison

Compare two canonical deployable resources or two qualification records side by side.

<div class="mcuk-tool" data-mcuk-tool="comparison">
  <div class="mcuk-tool-controls">
    <label>
      Dataset
      <select data-role="kind">
        <option value="vehicles">Deployable resources</option>
        <option value="training">Qualifications</option>
      </select>
    </label>
    <label>
      First record
      <select data-role="first"></select>
    </label>
    <label>
      Second record
      <select data-role="second"></select>
    </label>
  </div>
  <div data-role="results" aria-live="polite">Loading comparison data…</div>
</div>

## Comparison rules

The table displays only fields contained in the canonical records. **Not verified** means that the value has not been reproduced; it does not mean zero, none or unrestricted.

Vehicle comparison covers:

- service and category;
- verified purchase cost;
- verified crew range;
- training labels;
- building requirements;
- capabilities.

Qualification comparison covers:

- service;
- role or course classification;
- supported operational roles;
- verified course name and duration;
- prerequisites.

## Data sources

This tool consumes the `vehicles.json` and `training.json` v1 exports generated during deployment.
