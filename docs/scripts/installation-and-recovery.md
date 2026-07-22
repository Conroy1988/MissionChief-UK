# Installation, Updates and Recovery

This guide defines the standard installation and recovery content required for every documented MissionChief tool.

## Before installation

- Confirm the tool's canonical source.
- Review its requested browser or userscript permissions.
- Record the currently installed version.
- Export settings where the tool supports it.
- Disable overlapping tools before the first test.

## Standard installation flow

1. Install a supported browser extension or userscript manager.
2. Open the tool's canonical distribution page.
3. Review the source and requested permissions.
4. Install the script or extension.
5. Reload MissionChief UK.
6. Confirm that the tool is active only on the expected game domain.
7. Test one feature at a time before enabling optional modules.

## Update discipline

Automatic updates are convenient but can introduce breaking changes. Compatibility records should therefore state:

- where updates are downloaded from;
- whether updates are automatic;
- how to inspect the installed version;
- how to temporarily disable updates;
- how to return to a known working version when permitted by the project.

## Fault isolation

When a page behaves incorrectly:

1. reproduce the problem with all optional modules disabled;
2. test the affected tool alone;
3. re-enable other scripts individually;
4. record browser, device, tool versions and affected page;
5. inspect the browser console only when technically appropriate;
6. report the smallest reproducible conflict.

## Recovery

A complete tool record should explain how to:

- disable the tool;
- remove it;
- clear only its own stored settings where possible;
- restore an exported configuration;
- confirm that the base game works without the tool.

Never instruct users to erase all browser storage as the first recovery action.
