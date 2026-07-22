# Structured Data Entry Guide

This guide defines how MissionChief UK records move from observation into the repository's structured datasets.

## Core rule

A record must not present an uncertain value as verified. Unknown fields should be omitted where the schema permits, or explicitly marked through the record's verification metadata.

## Record lifecycle

1. **Identify the canonical object** — determine whether the subject is a vehicle, mission, building, extension, course, personnel type or alias.
2. **Capture evidence** — retain the source, screenshot context, reproducible game path and observation date.
3. **Normalise terminology** — use the exact UK game label as the canonical name and place alternatives in `aliases`.
4. **Create the record** — copy the relevant file from `data/templates/` and replace every placeholder.
5. **Validate locally** — run `python scripts/validate_data.py` and `mkdocs build --strict`.
6. **Review relationships** — confirm every referenced identifier exists or is deliberately pending.
7. **Publish with classification** — use `verified`, `calculated`, `community-tested`, `review-required` or `obsolete` accurately.

## Identifier conventions

Identifiers are lowercase kebab-case and remain stable after publication.

```text
fire-engine
major-fire-at-industrial-site
police-station
public-order
```

Do not encode mutable values, costs or dates in identifiers.

## Evidence requirements

A mature record should include:

- verification classification;
- date last checked;
- source type;
- source description or reproducible method;
- notes explaining regional or account-specific conditions.

## Numeric values

Keep numbers machine-readable. Do not place currency symbols, commas or explanatory words inside numeric fields.

```json
{
  "cost_credits": 100000,
  "minimum_staff": 2
}
```

Explanatory qualifications belong in notes.

## Probabilities

Only record a probability when the game or repeatable evidence supports the exact value. Otherwise describe the requirement as conditional or mark it for review.

## Relationships

Use canonical identifiers when linking records. Aliases exist for search and display; they must not become foreign keys.

## File placement

```text
data/uk/vehicles/
data/uk/missions/
data/uk/buildings/
data/uk/training/
data/uk/aliases/
```

One canonical object per file is preferred. Collections may be used for compact controlled vocabularies where the schema explicitly supports them.

## Publication threshold

A record may enter the repository as `review-required` when it is useful but incomplete. It must not be promoted to `verified` without reproducible evidence.