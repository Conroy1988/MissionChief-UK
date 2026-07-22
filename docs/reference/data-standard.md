# Data Standard

Structured records are authoritative only when they pass schema validation and meet the evidence requirements below.

## Required metadata

Each record should contain, where applicable:

```json
{
  "id": "stable-machine-id",
  "name": "UK display name",
  "aliases": [],
  "status": "verified",
  "last_verified": "YYYY-MM-DD",
  "sources": [],
  "notes": []
}
```

## Verification states

| Value | Use |
|---|---|
| `verified` | Reproduced in the current UK game or supported by a reliable primary source |
| `calculated` | Derived from verified records using a documented method |
| `community_reported` | Credible observation not yet independently reproduced |
| `review_required` | Potentially outdated, contradictory or incomplete |
| `deprecated` | No longer current but retained for migration or historical context |

## Source hierarchy

Prefer evidence in this order:

1. Current behaviour reproduced in MissionChief UK
2. Official UK game pages or announcements
3. Current game data exposed to the player/browser
4. Maintainer documentation for third-party tools
5. Multiple consistent community reports
6. Single unverified report

A lower-ranked source may identify a lead, but should not silently override stronger evidence.

## Naming and aliases

- `id` values use lowercase kebab-case and should not change after publication.
- `name` uses the current UK game label.
- `aliases` include common abbreviations, historical labels and predictable search terms.
- Do not merge two mechanically distinct resources merely because players use one informal name for both.

## Dates and units

- Dates use ISO 8601: `YYYY-MM-DD`.
- Credit values are stored as integers without punctuation.
- Durations must state their unit or use ISO 8601 duration format.
- Distances must identify the game measurement or real-world unit being represented.
- Percentages are stored consistently within each schema and documented explicitly.

## Contradictions

When reliable evidence conflicts:

1. mark the record `review_required`;
2. preserve both claims in the evidence notes;
3. identify version, date, account conditions and regional variant;
4. reproduce the behaviour where possible;
5. update dependent guides after resolution.
