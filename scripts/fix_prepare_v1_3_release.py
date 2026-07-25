#!/usr/bin/env python3
from pathlib import Path

root = Path(__file__).resolve().parents[1]
prepare = Path(__file__).with_name("prepare_v1_3_release.py")
prepare_text = prepare.read_text(encoding="utf-8")

ordering_line = '        r"\\[\\*\\*v1\\.2\\.0 Notes\\*\\*\\]\\(docs/releases/v1\\.2\\.0\\.md\\)": "[**v1.3.0 Notes**](docs/releases/v1.3.0.md)",\n'
if ordering_line in prepare_text:
    prepare_text = prepare_text.replace(ordering_line, "", 1)

replacement_call = '        replacement,\n        "generic release synchronization",'
replacement_fixed = '        lambda _match: replacement,\n        "generic release synchronization",'
if replacement_call in prepare_text:
    prepare_text = prepare_text.replace(replacement_call, replacement_fixed, 1)
elif replacement_fixed not in prepare_text:
    raise SystemExit("Generic release replacement call is not in an expected state")
prepare.write_text(prepare_text, encoding="utf-8", newline="\n")

runner = root / "scripts" / "run_public_verification_sync.py"
runner_text = runner.read_text(encoding="utf-8")
fixed_path = '    sync.RELEASE_PATH,\n'
dynamic_path = '    ROOT / "docs" / "releases" / f"v{sync.read_json(sync.VERSION_PATH)[\'version\']}.md",\n'
if fixed_path in runner_text:
    runner_text = runner_text.replace(fixed_path, dynamic_path, 1)
elif dynamic_path not in runner_text:
    raise SystemExit("Synchronization runner release path is not in an expected state")
runner.write_text(runner_text, encoding="utf-8", newline="\n")

sync_path = root / "scripts" / "sync_public_verification_metrics.py"
sync_text = sync_path.read_text(encoding="utf-8")
if 'VERSION_PATH = ROOT / "data" / "version.json"' in sync_text and "def current_release_path()" not in sync_text:
    read_json_block = '''def read_json(path: Path) -> object:\n    try:\n        return json.loads(path.read_text(encoding="utf-8"))\n    except (OSError, json.JSONDecodeError) as exc:\n        raise SyncFailure(f"Unable to read {path.relative_to(ROOT)}: {exc}") from exc\n\n\n'''
    compatibility = read_json_block + '''def current_release_path() -> Path:\n    document = read_json(VERSION_PATH)\n    if not isinstance(document, dict) or not isinstance(document.get("version"), str):\n        raise SyncFailure("Release metadata version is invalid")\n    return ROOT / "docs" / "releases" / f"v{document['version']}.md"\n\n\nRELEASE_PATH = current_release_path()\n\n\n'''
    if read_json_block not in sync_text:
        raise SystemExit("Synchronization module read_json block is missing")
    sync_text = sync_text.replace(read_json_block, compatibility, 1)
    sync_path.write_text(sync_text, encoding="utf-8", newline="\n")

print("Release preparation compatibility corrections are synchronized.")
