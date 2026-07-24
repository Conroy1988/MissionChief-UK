# Fully Canonical Mission Batch 1

This page records the first mission batch promoted through all five evidence gates in the MissionChief UK 100% verification programme.

## Batch result

```text
11 fully canonical missions
11 direct official/canonical ID matches
1 verified requirement-key mapping
2 verified or narrowly classified prerequisite-key mappings
0 unmapped official keys in the promoted records
```

## Included missions

| ID | Mission | Fire Stations | Fire engines | Base average credits | Published relationships |
|---:|---|---:|---:|---:|---|
| `0` | Bin fire | 1 | 1 | 110 | Follow-ups retained |
| `1` | Container fire | 1 | 1 | 170 | None published in the retained record |
| `2` | Burning car | 1 | 1 | 370 | Expansions and follow-ups retained; Recovery overlay remains separate |
| `3` | Burning motorbike | 1 | 1 | 340 | Expansion and follow-ups retained; Recovery overlay remains separate |
| `4` | Burning grass | 1 | 1 | 200 | Expansion retained |
| `6` | Garden shed fire | 2 | 2 | 600 | Follow-ups retained |
| `7` | Burning leaves | 1 | 1 | 210 | Expansion retained |
| `8` | Bulk rubbish fire | 1 | 1 | 220 | Expansions and follow-ups retained |
| `9` | Bale of straw fire | 1 | 1 | 250 | Expansions retained |
| `10` | Tractor fire | 1 | 1 | 600 | None published in the retained record |
| `11` | Phonebox on fire | 1 | 1 | 240 | Follow-ups retained |

## Evidence gates completed

Every mission in this batch passed:

1. **Captured** — the complete official record is retained in the checksummed UK source snapshot.
2. **Identity verified** — the official mission ID and exact UK name match the canonical record.
3. **Requirements mapped** — every published requirement, chance and prerequisite key is explicitly mapped or narrowly classified.
4. **Operationally verified** — published rewards and mission relationships are represented; base records remain separate from additive overlays.
5. **Fully canonical** — strict key equivalence and final evidence-completeness auditing passed.

## Verified official-key mappings

| Official field | Classification | Canonical meaning |
|---|---|---|
| `requirements.firetrucks` | Verified | Guaranteed `fire_engine` quantity |
| `prerequisites.fire_stations` | Verified | Minimum `fire_stations` count |
| `prerequisites.main_building` | Not operational only for value `0` | No canonical prerequisite is emitted; any non-zero value fails validation |

The mappings are stored in:

```text
data/uk/official-key-mappings.json
```

## Enforcement

The batch is not accepted through documentation alone. CI validates:

- every promoted mission exists in both official and canonical collections;
- exact UK names match;
- canonical records remain classified as verified;
- every official requirement, chance and prerequisite key is mapped;
- official mapped quantities equal canonical quantities;
- strict promoted records contain no extra guaranteed requirement or precondition outside the official mapping result;
- no official chance is silently ignored; and
- the verification registry explicitly records evidence sources and the completed stage.

Relevant machine-readable controls:

```text
data/uk/mission-verification-registry.json
data/uk/official-key-mappings.json
scripts/validate_official_key_mappings.py
scripts/generate_mission_verification_status.py
```

## Programme position after this batch

```text
Official missions captured:        1,062 / 1,062
Direct canonical ID matches:          52 / 1,062
Fully canonical missions:             11 / 1,062
Remaining to fully canonical:      1,051
```

The next batches should continue through low-complexity Fire and Rescue missions before introducing probability keys, alternatives, specialist resources and patient mechanics.
