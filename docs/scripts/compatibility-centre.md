# Script and Tool Compatibility Centre

Stage 10 creates a UK-focused reference for MissionChief browser tooling, userscripts and supporting utilities.

## Catalogue record

Every tool entry should document:

- public name and canonical project link;
- developer or maintaining organisation;
- purpose and affected game areas;
- installation method;
- supported browsers and devices;
- required userscript manager or extension;
- permissions requested;
- update channel and maintenance status;
- known conflicts;
- recovery and uninstall steps;
- UK-specific configuration guidance;
- last compatibility verification date.

## Compatibility states

| State | Meaning |
|---|---|
| Supported | Verified working in the named environment |
| Partial | Core functionality works with documented limitations |
| Experimental | Early or incomplete verification |
| Incompatible | Confirmed conflict or unsupported environment |
| Unknown | Not yet tested |

## Test matrix

Testing should cover, where relevant:

- Chrome and Chromium-based browsers;
- Firefox;
- desktop Safari;
- iPhone and iPad Safari userscript environments;
- Android browser environments;
- Tampermonkey;
- Violentmonkey;
- Safari-compatible userscript managers;
- simultaneous use with LSSM and other major scripts.

## Conflict records

A conflict entry must identify:

1. the exact tools and versions involved;
2. the affected page or feature;
3. the visible symptom;
4. reproduction steps;
5. available workaround;
6. whether the conflict has been reported upstream.

## Security standard

The catalogue must not describe a script as safe merely because it is popular. Reviews should inspect requested permissions, update sources, external network access, credential handling and the consequences of automatic updates.
