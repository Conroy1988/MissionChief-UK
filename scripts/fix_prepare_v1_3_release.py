#!/usr/bin/env python3
from pathlib import Path

root = Path(__file__).resolve().parents[1]
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

runner = root / "scripts" / "run_public_verification_sync.py"
runner_text = runner.read_text(encoding="utf-8")
fixed_path = '    sync.RELEASE_PATH,\n'
dynamic_path = '    ROOT / "docs" / "releases" / f"v{sync.read_json(sync.VERSION_PATH)[\'version\']}.md",\n'
if fixed_path not in runner_text:
    raise SystemExit("Expected fixed release path is missing from synchronization runner")
runner.write_text(runner_text.replace(fixed_path, dynamic_path, 1), encoding="utf-8", newline="\n")

print("Corrected release preparation ordering, literal replacement handling and dynamic release synchronization.")
