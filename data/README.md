# MissionChief UK Structured Data

This directory contains machine-readable UK game records, validation schemas and contributor templates.

## Layout

```text
data/
├── schema/       # JSON Schema definitions
├── templates/    # Copy-ready starter records
└── uk/           # Published UK datasets
    ├── vehicles/
    ├── missions/
    ├── buildings/
    ├── training/
    └── aliases/
```

## Rules

- Use one stable canonical identifier per object.
- Keep exact UK game names separate from aliases.
- Do not guess missing values.
- Record verification status and check date.
- Use canonical identifiers for relationships.
- Run validation before proposing changes.

```bash
python scripts/validate_data.py
```

See `docs/reference/data-entry-guide.md` for the complete workflow.
