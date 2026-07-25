#!/usr/bin/env python3
from pathlib import Path

path = Path(__file__).with_name("prepare_v1_3_release.py")
text = path.read_text(encoding="utf-8")
line = '        r"\\[\\*\\*v1\\.2\\.0 Notes\\*\\*\\]\\(docs/releases/v1\\.2\\.0\\.md\\)": "[**v1.3.0 Notes**](docs/releases/v1.3.0.md)",\n'
if line not in text:
    raise SystemExit("Expected README ordering line is missing")
path.write_text(text.replace(line, "", 1), encoding="utf-8", newline="\n")
print("Corrected release preparation ordering.")
