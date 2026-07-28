# Missions and Dispatching

Mission planning requires four separate questions: **why the mission can generate, what the mission publishes, what is currently responding or on scene, and what work remains after response**.

## Mission lifecycle

```text
Generation preconditions satisfied
              ↓
Mission appears
              ↓
Guaranteed / alternative / conditional / probabilistic requirements
              ↓
Resources dispatch and travel
              ↓
On-scene personnel and capability checks
              ↓
Patients / prisoners / recovery / follow-up outcomes
              ↓
Resources return to useful operational geography
```

Do not flatten these stages into one vehicle count.

## Generation preconditions

Canonical mission records may publish counts or states such as:

- buildings and stations;
- specialist extensions;
- active equipment;
- available qualified personnel;
- points of interest;
- custom spawn areas;
- availability windows.

A precondition explains why a mission may appear. It does not necessarily create a dispatch requirement.

## Requirement types

### Guaranteed

A guaranteed row publishes an exact resource and quantity for that mission record.

```json
{
  "resource": "fire_engine",
  "quantity": 2
}
```

For several selected incidents, guaranteed quantities can be added transparently.

### Alternative group

An alternative group publishes a quantity that may be satisfied from any listed qualifying resource.

```json
{
  "resources": ["police_helicopter", "drone"],
  "quantity": 1
}
```

This means one qualifying resource, not one of each. Every displayed alternative row remains independent. A resource appearing in several groups must not be reused silently.

### Probabilistic

A probabilistic row has a published chance. It is not guaranteed and should not be treated as a permanent exact fleet requirement.

### Conditional

A conditional row applies only when its stated condition is met, such as `only_when_available`. A probability can also be attached to a conditional row; both semantics must remain visible.

## Personnel states

Canonical records distinguish:

| State | Meaning |
|---|---|
| `available` | Qualified personnel must exist before generation |
| `required` | Exact personnel required at the incident |
| `average_minimum` | Published average-minimum indicator, not an exact headcount |
| `ranges` | Explicit minimum-to-maximum requirement |
| `probabilistic` | Personnel requirement with a published chance |

The [Account Readiness Planner](../tools/account-readiness.md) uses the highest available-before-generation threshold for each role and adds exact incident-required personnel across selected missions. Non-exact personnel remains advisory.

## Responding, on scene and still required

A live mission interface can distinguish resources that are:

- requested but not dispatched;
- travelling;
- on scene;
- transporting or otherwise committed;
- still required by the incident.

The canonical database publishes mission requirements, not a live account dispatch state. Browser tools in this project therefore do not claim to know which owned vehicle is currently responding or whether a live mission has already satisfied a row.

## Patients

Patient fields can include:

- minimum and maximum count;
- generated-at-end state;
- treatment codes;
- hospital specialisation;
- transport probability;
- critical-care probability.

A patient maximum is not automatically an ambulance quantity. Travel, treatment, critical care, transport probability, hospital capacity and handoff time remain separate constraints.

## Prisoners

A published prisoner maximum describes custody workload. Do not assume every Police resource has identical prisoner capacity or that scene vehicles return immediately after transport. Use the [Police guide](../services/police.md) for verified custody contracts.

## Recovery assets

Recovery records publish cars, trucks or other assets to clear under `recovery.assets`. These are post-response outcomes and remain separate from emergency-resource requirements.

## Follow-up and variation records

The catalogue preserves:

- follow-up mission relationships;
- additive overlays;
- mission variations;
- historical or limited-availability records;
- base mission IDs and canonical string variant IDs.

An overlay requirement applies only to that variant. It must not be merged into every base mission with the same name.

## Dispatch planning workflow

1. Open the mission in [Mission Lookup](../tools/mission-lookup.md).
2. Separate preconditions from dispatch requirements.
3. Separate guaranteed, alternative, conditional and probabilistic rows.
4. Review exact and non-exact personnel states.
5. Identify patient, prisoner, recovery and follow-up outcomes.
6. Check vehicle training, towing, carrier and building relationships.
7. Test current inventory and protected reserve in [Account Readiness](../tools/account-readiness.md).
8. Add geography, destinations and return time using [Station Placement](../strategy/station-placement.md).
9. Dispatch or expand only against the measured bottleneck.

## Common modelling errors

- adding every member of an alternative group;
- treating a precondition as a dispatched vehicle;
- converting probability into certainty;
- dropping an `only_when_available` condition;
- using `average_minimum` as an exact count;
- converting patient or prisoner maxima into guessed vehicles;
- applying an overlay to its base mission;
- using one command or specialist unit across independent rows;
- counting an unstaffed or untrained vehicle as deployable;
- assuming a live account state from static canonical data.
