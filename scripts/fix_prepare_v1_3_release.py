#!/usr/bin/env python3
from pathlib import Path

path = Path(__file__).with_name("prepare_v1_3_release.py")
text = path.read_text(encoding="utf-8")

ordering_line = '        r"\\[\\*\\*v1\\.2\\.0 Notes\\*\\*\\]\\(docs/releases/v1\\.2\\.0\\.md\\)": "[**v1.3.0 Notes**](docs/releases/v1.3.0.md)",\n'
if ordering_line not in text:
    raise SystemExit("Expected README ordering line is missing")
text = text.replace(ordering_line, "", 1)

replacement_call = '        replacement,\n        "generic release synchronization",'
if replacement_call not in text:
    raise SystemExit("Expected generic release replacement call is missing")
text = text.replace(
    replacement_call,
    '        lambda _match: replacement,\n        "generic release synchronization",',
    1,
)

path.write_text(text, encoding="utf-8", newline="\n")
print("Corrected release preparation ordering and literal replacement handling.")
