# MissionChief UK Static Data API

The MissionChief UK guide publishes a versioned, read-only JSON API generated from the same canonical records used by the documentation and browser tools.

## Production base

```text
https://conroy1988.github.io/MissionChief-UK/assets/data/v1/
```

## Endpoints

| Endpoint | Purpose |
|---|---|
| `manifest.json` | Version, status and collection counts |
| `missions.json` | Full mission records |
| `vehicles.json` | Full deployable-resource records |
| `infrastructure.json` | Full building and extension records |
| `training.json` | Full qualification and course records |
| `search-index.json` | Lightweight normalized search index |
| `faq.json` | Generated FAQ entries |
| `openapi.json` | OpenAPI 3.1 contract |

## Response envelope

Collection endpoints use:

```json
{
  "schema_version": "1",
  "data_version": "1.0.0",
  "released_at": "2026-07-22",
  "collection": "missions",
  "count": 0,
  "records": []
}
```

The deployed count and records are generated during the build.

## Versioning policy

- The URL segment `v1` identifies the API contract generation.
- `data_version` identifies the current data release.
- Additive records and optional fields may be published within v1.
- Breaking envelope or field changes require a new path such as `v2`.
- Previous API directories should remain available when practical so integrations can migrate deliberately.

## Availability and caching

The API is served as static GitHub Pages content. It has no authentication, write methods, query parameters or server-side filtering. Consumers should cache responses responsibly and use the manifest to detect data-version changes.

## Evidence contract

API consumers must preserve the repository’s evidence semantics:

- omitted fields are unknown, not zero;
- verified applies only to populated fields;
- empty mission requirement arrays may indicate unavailable response-table evidence;
- alternative groups require a total from any qualifying combination;
- towing is separate from dispatched emergency resources.

## Licence and attribution

Original project data and code are provided under the repository licence. MissionChief names and game-derived terminology remain the property of their respective owners.
