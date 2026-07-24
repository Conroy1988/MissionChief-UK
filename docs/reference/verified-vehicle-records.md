# Verified Vehicle Records

The canonical deployable-resource collection is stored under `data/uk/vehicles/` and exported through the versioned static API.

The authoritative live counts and evidence gaps are no longer maintained manually on this page. See [UK Vehicle Coverage Status](vehicle-coverage-status.md) for the generated comparison between the source ledger and canonical records.

## Evidence model

A canonical record verifies only the attributes it contains:

- omitted prices, crew limits, training and building restrictions remain unknown rather than zero;
- official MissionChief UK pages and official Help Centre articles are primary sources;
- authenticated current-game observations may verify market IDs and purchase details;
- community userscripts may identify candidates, but cannot independently verify market values;
- abbreviations remain unexpanded until a primary source supplies the exact name.

## Machine-readable records

- canonical records: `data/uk/vehicles/*.json`
- source ledger: `data/sources/missionchief-uk/vehicle-type-inventory.json`
- generated coverage: `data/sources/missionchief-uk/vehicle-coverage.json`
- public coverage endpoint: `assets/data/official/uk-vehicle-coverage.json`

Every vehicle change must keep the source ledger, generated coverage and canonical records deterministic under the Stage 36A validation workflow.
