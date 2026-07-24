#!/usr/bin/env python3

from pathlib import Path

path = Path("scripts/release_readiness.py")
text = path.read_text(encoding="utf-8")
replacements = {
    '        "data/sources/missionchief-uk \\",': '        "data/sources/missionchief-uk \\\\",',
    '        "docs/assets/data/official \\",': '        "docs/assets/data/official \\\\",',
}
for old, new in replacements.items():
    if old not in text:
        raise SystemExit(f"Expected malformed readiness literal not found: {old!r}")
    text = text.replace(old, new, 1)
path.write_text(text, encoding="utf-8", newline="\n")
