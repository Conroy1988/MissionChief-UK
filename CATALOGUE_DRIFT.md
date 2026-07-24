# Official catalogue drift control

MissionChief UK treats the official `einsaetze.json` feed as an external source that can change without notice. Production remains at 100% verified coverage only while every official mission identity and operational field matches the evidence-controlled canonical model.

## Fail-closed refresh model

The scheduled catalogue workflow downloads a candidate feed into an isolated runner directory. It does **not** overwrite tracked production data before comparison.

The drift detector compares the candidate records with the committed official snapshot and classifies:

- new official mission IDs;
- removed official mission IDs;
- mission identity changes;
- nested requirement, chance and prerequisite changes;
- patient and personnel changes;
- relationships, durations, seasonal windows, generator rules and other operational metadata changes.

A semantically identical feed is a successful no-op. Wrapper timestamps and source metadata do not create false drift because comparison is performed on the mission records themselves.

## Evidence invalidation

A modified or removed mission that is currently marked `fully-canonical` is listed as **invalidated pending review**. The production record is not silently deleted or rewritten. Its previous evidence remains available, but it cannot be assumed to describe the candidate official mission until the changed fields have been reconciled.

New official IDs are listed as uncovered identities unless a matching canonical record already exists.

The report calculates projected verified coverage using the candidate official count and the currently valid fully canonical IDs.

## Review queue

Each unique drift state receives a deterministic SHA-256 fingerprint.

The scheduled workflow retains:

- the complete JSON drift report;
- a reviewer-readable Markdown report;
- the candidate official source files;
- an Actions artifact containing the evidence.

For a new fingerprint, it pushes a dedicated `automation/official-catalogue-drift-*` branch and attempts to open a draft pull request. It also creates or updates a GitHub issue so the change remains visible even when automated pull-request creation is unavailable.

The scheduled workflow then fails intentionally. This makes an external catalogue change visible and prevents it from being mistaken for a successful 100% refresh.

## Resolution requirements

A drift branch may only be merged after:

1. every added or changed field has reproducible official evidence;
2. owned mapping contracts are updated without guessing semantics;
3. affected canonical mission records are generated or amended;
4. invalidated verification decisions are re-established;
5. strict official equivalence returns to zero failures;
6. the candidate backlog returns to zero;
7. exact-head CI, MkDocs and browser acceptance pass;
8. the deployed site and immutable release are verified when a release is required.

## Local use

Generate a report without failing:

```bash
python scripts/detect_official_mission_drift.py \
  --baseline data/sources/missionchief-uk/einsaetze.raw.json \
  --candidate /path/to/candidate/einsaetze.raw.json \
  --json-output /tmp/official-catalogue-drift.json \
  --markdown-output /tmp/official-catalogue-drift.md
```

Add `--fail-on-drift` when the caller should receive exit code `2` for a valid but changed candidate feed.
