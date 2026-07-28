# Search and Rescue HQ Operational Progression

Search and Rescue HQ provides the structured command, aerial-search, operational-support and specialist-personnel layer used by verified high-risk missing-person and major cross-service search incidents. The safe planning unit is a complete search system, not one active Drone or one SAR 4x4.

!!! info "Evidence boundary"
    Verified statements reproduce current canonical mission, vehicle, personnel and training records. Fleet sizes, reserve floors, placement patterns and commissioning sequences are recommendations. HQ economics, vehicle staffing, support-trailer towing, course durations and unlock details remain unknown where unpublished.

**Current evidence baseline:** 28 July 2026.

## Command doctrine

1. **Command before volume** — Control Van, SAR Commander and Search Advisor capability must exist before expanding search generators.
2. **Generation prerequisites remain separate** — an active Drone can be required before mission generation while a Police Helicopter may satisfy the incident aerial-search slot.
3. **Preserve alternative groups** — operational support and 4x4 rows require the published group quantity, not every listed resource.
4. **Personnel states before vehicle counts** — available, required and average-minimum fields must retain their semantics.
5. **Regional coverage before central storage** — off-road access, command and search support must reach the intended terrain.
6. **Recovery before further activation** — searches, patients and remote travel can keep resources unavailable after the visible phase completes.

[Open Mission Lookup](../tools/mission-lookup.md) · [Open Concurrent Fleet Planner](../tools/fleet-planner.md) · [Compare Resources](../tools/resource-comparison.md)

## Search system chain

```text
Search and Rescue HQ mission generation
                ↓
Active Drone prerequisite where published
                ↓
Control Van and command personnel
                ↓
Aerial-search alternative
                ↓
Operational-support alternative
                ↓
Mountain Rescue / SAR 4x4 alternatives
                ↓
Search personnel, patient handling and recovery
```

## Verified resources

| Resource | Verified role | Current evidence boundary |
|---|---|---|
| **Control Van** | Incident command and search coordination | Price, staffing, training and building relationship unpublished |
| **Drone** | Aerial search, reconnaissance and deployable equipment | 25,000 credits / 15 coins; Drone Operator education; Fire or Police equipment storage; course duration unpublished |
| **Police Helicopter** | Police air support and aerial search | Police Helicopter Station; Police aviation, 7 days |
| **Mountain Rescue 4x4** | Off-road Mountain Rescue response | Price, staffing and training unpublished |
| **SAR 4x4** | Off-road Search and Rescue response | Price, staffing and training unpublished |
| **Operational Support Van** | Search support and incident logistics | Economics, staffing and building relationship unpublished |
| **Operational Support Trailer** | Search support trailer | Compatible towing vehicle unpublished |
| **Personal SAR Vehicle** | Personnel transport and search support | Economics, staffing and building relationship unpublished |
| **Search Dog Unit** | Terrain and missing-person search | Economics, staffing, training and building relationship unpublished |

## Active Drone semantics

The verified High Risk and Very High Risk Missing Person missions require one **active Drone** before generation.

The same mission also publishes an incident response alternative:

```text
Police Helicopter OR Drone — quantity 1
```

These are separate concepts:

- the active Drone is a generation prerequisite;
- the aerial-response slot can be satisfied by either listed resource;
- the prerequisite does not automatically dispatch the Drone;
- a Police Helicopter does not remove the need for the active-Drone prerequisite.

## Operational-support alternatives

One qualifying resource satisfies the verified operational-support group:

- Operational Support Van;
- Operational Support Trailer;
- Personal SAR Vehicle.

Do not require all three simultaneously.

### Trailer boundary

The Operational Support Trailer is verified as a trailer, but its compatible towing vehicles remain unpublished. Do not count the trailer as independently dispatchable until its current game behaviour is directly reproduced.

## Off-road alternatives

Verified SAR missions require two qualifying vehicles in total from:

- Mountain Rescue 4x4;
- SAR 4x4.

Any valid combination may satisfy the group where supported. Do not require two of each.

## Personnel model

Verified SAR roles include:

- SAR Commander;
- Search Advisor;
- Search Technician.

### Available before generation

The verified High Risk and Very High Risk Missing Person records publish:

- 4 SAR Commanders available;
- 2 Search Advisors available.

### Required at the incident

The same missions publish:

- 2 SAR Commanders required;
- 1 Search Advisor required.

### Average-minimum semantics

Where Search Technician demand is published as `average_minimum`, it must not be represented as an exact guaranteed count. Use Mission Lookup to inspect the current mission field rather than converting the role into a fixed dispatch rule.

## Representative mission pressure

### High Risk Missing Person

Verified response:

- 1 Control Van;
- 3 Police Cars;
- 1 Police Helicopter **or** Drone;
- 2 Mountain Rescue 4x4s and/or SAR 4x4s;
- 1 Operational Support Van, Trailer or Personal SAR Vehicle;
- 2 required SAR Commanders;
- 1 required Search Advisor;
- 1 patient generated at mission end;
- 40% transport probability and 5% critical-care probability;
- 2 Search and Rescue HQs and 1 active Drone as preconditions.

### Very High Risk Missing Person

The verified structure is the same, with 5 Police Cars rather than 3 and a higher average reward. It remains a one-patient mission with the same transport and critical-care probabilities.

### Transparent concurrency calculation

Running both verified missing-person missions together creates:

- 2 Control Vans;
- 8 Police Cars;
- 2 independent aerial-search slots;
- 4 qualifying Mountain Rescue/SAR 4x4 slots;
- 2 operational-support slots;
- 4 required SAR Commanders;
- 2 required Search Advisors;
- up to 2 patients generated at mission end.

This is a calculation from two verified missions, not an official combined mission. Active-Drone preconditions are generation conditions rather than dispatch quantities and are not converted into two guaranteed Drone responses.

## Major cross-service searches

Large railway, cave and remote incidents may add:

- Search Dog Units;
- several operational-support alternatives;
- Police Helicopter or Drone capability;
- Railway Police and EIU;
- Fire, HART, Welfare and mass-casualty resources;
- Cave Rescue Specialist and Operational Team Leader roles.

Use Mission Lookup for each incident rather than applying the two missing-person templates universally.

## Six commissioning gates

| Gate | Question | Recommended pass condition |
|---|---|---|
| HQ readiness | Are command, support and off-road systems available? | The HQ creates an operational chain rather than only a generator |
| Drone prerequisite | Is the required active equipment present? | Generation prerequisites are met without confusing them with response rows |
| Command personnel | Are SAR Commander and Search Advisor states ready? | Available and required values are both supported |
| Alternative groups | Can one valid resource satisfy each published group? | No group is multiplied into every listed option |
| Geography | Can resources reach the search area and patient access point? | Route-based coverage is practical |
| Recovery | Can a second search begin after the first? | Command, support, aerial and off-road reserve returns to useful positions |

## Recommended fleet templates

These are strategy recommendations, not official requirements.

### Foundation SAR network

| Capability | Recommended position |
|---|---|
| Search and Rescue HQ | Build only when the complete command/support chain can be commissioned |
| Control Van | 1 local unit with trained/assigned command personnel |
| Drone | 1 active item with Drone Operator capability where required |
| Off-road response | 3–4 qualifying Mountain Rescue/SAR 4x4s across the first region |
| Operational support | 1 verified option; avoid trailer dependence until towing is understood |
| Protected reserve | Alliance support for rare second incidents while local depth develops |

### Developing network

| Capability | Recommended position |
|---|---|
| HQs | Two operational HQ regions where current mission preconditions require them |
| Control Vans | One per main response region plus replacement staffing |
| Aerial search | Drone route plus Police Helicopter fallback or alliance support |
| Off-road response | 6–8 qualifying 4x4s across two search zones |
| Operational support | Two independently dispatchable support options |
| Personnel | Required and replacement SAR Commander/Search Advisor cohorts |

### Established network

| Capability | Recommended position |
|---|---|
| HQ and command | Independently dispatchable regional search groups |
| Aerial search | Multiple active and response-capable options without one trained-person failure point |
| Off-road response | Sized from measured simultaneous searches and remote return times |
| Operational support | Vehicle/trailer/personal options distributed by geography and towing certainty |
| Dogs and specialists | Regional Search Dog and specialist-personnel reserve |
| Cross-service resilience | Police, Mountain Rescue, HART, Railway and medical dependencies tested together |

## Placement doctrine

### Urban/peri-urban missing-person network

- Position Control Vans and Police support near population and transport corridors.
- Keep off-road vehicles close enough for woodland, river and edge-of-city searches.
- Use Drone equipment where it adds genuine coverage rather than replacing ground teams.
- Preserve Police Car and patient-transport reserve.

### Rural and upland network

- Align HQ command with Mountain Rescue 4x4/SAR 4x4 geography.
- Distribute operational support by travel-time zone.
- Maintain aerial-search alternatives for distant searches.
- Include custom spawn areas and road access.

### Railway and major-incident network

- Position search command near railway corridors and major cross-service risks.
- Preserve EIU, Railway Police, dogs and operational support independently.
- Test multiple command and support slots without reusing one unit.
- Include mass-casualty, welfare and patient handling where published.

## Recovery-to-readiness

After a search incident:

1. record Control Vans, off-road resources, aerial assets and support units still committed;
2. restore one command and off-road response route in each exposed region;
3. confirm active Drone equipment and operators remain ready;
4. return SAR Commander and Search Advisor cohorts to useful geography;
5. review patients and cross-service missions still active;
6. rerun the selected dual-search scenario;
7. correct repeated command, support, aerial or personnel shortages before more HQ expansion.

## Common failures

| Failure | Operational symptom | Correction |
|---|---|---|
| Dispatching the active Drone prerequisite | The generation field is treated as a guaranteed response | Keep prerequisite and response alternative separate |
| Requiring every support option | Fleet plan demands Van, Trailer and Personal SAR Vehicle simultaneously | Apply the quantity to the alternative group |
| Requiring both 4x4 types | Off-road demand is doubled incorrectly | Use any valid combination across the group |
| Treating average minimum as exact | Search Technician planning becomes a false fixed rule | Preserve the published personnel semantic |
| Counting a trailer without towing | Operational Support appears available but may not dispatch | Leave towing unknown until reproduced |
| Centralising Control Vans | One search removes regional command | Duplicate by travel-time zone |
| Ignoring personnel availability | Vehicles attend while SAR Commander or Search Advisor requirements remain open | Audit roles separately |
| Expanding HQs before reserve | New searches generate without a second command/support chain | Commission complete regional readiness first |

## Operational readiness checklist

- [ ] Control Van, off-road and operational-support systems are complete;
- [ ] active Drone prerequisites are separate from aerial-response slots;
- [ ] Drone Operator education is available where required;
- [ ] Mountain Rescue/SAR 4x4 alternative quantities are interpreted correctly;
- [ ] Operational Support alternatives are not multiplied;
- [ ] trailer towing remains unknown where unpublished;
- [ ] SAR Commander and Search Advisor available/required states are supported;
- [ ] Search Technician semantics are not converted into an exact count;
- [ ] patient generation, transport and critical care are included;
- [ ] geography and custom spawn areas are tested;
- [ ] two searches have been tested together;
- [ ] cross-service dependencies and recovery reserve are ready;
- [ ] unpublished values remain unknown rather than zero.

## Stage 37E completion

Together with [Mountain Rescue progression](mountain-rescue.md), this guide completes:

- off-road and remote-area response;
- command, dogs and operational support;
- active Drone and aerial-search semantics;
- SAR Commander, Search Advisor and specialist-personnel planning;
- HART and helicopter overlays;
- scalable regional fleet templates;
- concurrency and recovery-to-readiness.

The next service programme is **Stage 37F — Bomb Disposal and EOD operational progression**.
