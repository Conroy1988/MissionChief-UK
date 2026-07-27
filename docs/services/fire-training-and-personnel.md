# Fire Training and Personnel Planning

Vehicles create capability only when the correct personnel can crew them at the time they are needed. Fire expansion therefore has two separate inventories:

- **physical resources** — stations, appliances, specialists, carriers and containers;
- **operational personnel** — available staff, qualified staff, assigned crews and reserve depth.

A fleet can look complete in the vehicle market and still be operationally incomplete when specialist training, local staffing or simultaneous dispatches are not covered.

!!! info "Evidence boundary"
    The guide distinguishes verified course records from strategic personnel recommendations. Course name, duration and academy are stated only where the current UK training matrix has been reproduced. Class sizes, prerequisites and transferability remain unknown unless explicitly verified.

**Current evidence baseline:** 27 July 2026.

## The personnel dependency chain

Use this model for every specialist purchase:

```text
Mission pressure
      ↓
Required capability
      ↓
Vehicle or container
      ↓
Minimum operational crew
      ↓
Required qualification
      ↓
Academy and course lead time
      ↓
Local trained reserve
```

Owning the vehicle proves only one step of the chain.

## Personnel states in the mission data

Official mission records use several personnel semantics. Do not flatten them into one guaranteed number.

| State | Meaning | Planning consequence |
|---|---|---|
| `available` | Qualified personnel must exist before the mission can generate | Maintain the qualification before activating related mission generation. |
| `required` | An exact personnel requirement applies at the incident | Confirm the dispatched vehicles can deliver the required people. |
| `average_minimum` | The source publishes an average-minimum value | Treat it as the source's stated average boundary, not a guaranteed exact count. |
| `range` | The source publishes an explicit minimum and maximum | Plan for the upper end when resilience matters. |
| `probabilistic` | Personnel may be required according to a chance value | Preserve the probability rather than permanently dispatching the unit as guaranteed. |

[Review the Training and Personnel database](../reference/training-and-personnel.md) · [Search personnel requirements in Mission Lookup](../tools/mission-lookup.md)

## Verified Fire Academy courses

### HazMat

The current canonical HazMat Unit and CBRN Vehicle records verify:

| Field | Verified value |
|---|---|
| Course | **HazMat** |
| Duration | **3 days** |
| School | **Fire Academy** |
| Operational use | HazMat vehicles and units |

The course lead time is part of the vehicle acquisition decision. A newly purchased HazMat resource should not be counted as available until its trained crew can be assigned without removing another required capability.

### ARFF-Training

Airfield firefighting vehicles such as the RIV verify:

| Field | Verified value |
|---|---|
| Course | **ARFF-Training** |
| Duration | **3 days** |
| School | **Fire Academy** |
| Operational use | Airport-specific firefighting vehicles |

ARFF is a cross-service specialist dependency rather than a general Fire appliance qualification. Keep its personnel pool distinct when planning airfield capability.

[Open Airfield Operations](airfield-operations.md)

## Training gates before purchase

### Gate 1 — requirement verification

Use Mission Lookup to confirm whether the qualification is tied to:

- mission generation;
- vehicle operation;
- personnel availability;
- incident attendance;
- an alternative or probabilistic requirement.

Do not start a training programme from an assumed relationship.

### Gate 2 — course lead time

Count the full verified course duration before the planned operational date. Vehicle purchase, extension completion and course completion should converge rather than occur as disconnected events.

### Gate 3 — local assignment

Place trained staff where the specialist vehicle is expected to operate. A qualification held elsewhere in the account may not solve local travel, assignment or concurrency problems.

### Gate 4 — reserve depth

A single minimum crew creates a single point of failure. Staff may already be assigned, dispatched or needed by another vehicle.

!!! tip "Recommended reserve rule"
    For each critical specialist response zone, train enough people to crew the expected first dispatch **plus one replacement crew**. This is a resilience recommendation, not a published MissionChief minimum.

### Gate 5 — simultaneous demand

Test the intended crew plan against two or more incidents. A vehicle-level fleet plan can pass while the personnel plan fails because the same trained people are implicitly assigned twice.

## Cohort-based training plan

Train specialists in cohorts tied to an operational deployment rather than sending isolated personnel without a fleet plan.

### Cohort 1 — commissioning crew

The first cohort should make the new vehicle genuinely dispatchable when it enters service.

- cover the intended operational crew;
- keep the trainees assigned to the correct station or response cluster;
- complete training before activating related mission generation;
- verify the vehicle does not borrow the only crew from another specialist.

### Cohort 2 — replacement crew

The second cohort protects the capability when the first crew is committed or unavailable.

- size it for the same vehicle or another unit with the same verified qualification;
- distribute it where travel and assignment rules permit practical use;
- avoid counting untrained general personnel as qualified reserve.

### Cohort 3 — expansion reserve

Train ahead of the next confirmed vehicle only when the expansion is part of the current plan. Unallocated specialist training can be useful, but it should not consume academy capacity needed by a nearer operational dependency.

## Recommended personnel depth by network stage

These are strategy recommendations, not game requirements.

| Network stage | Recommended posture |
|---|---|
| Foundation | One commissioning crew for each active specialist; alliance support may cover rare second incidents. |
| Developing | One commissioning crew plus one replacement crew for critical specialists in each main response cluster. |
| Established | Multiple independently dispatchable crews across geographic zones, with academy throughput planned for replacements and new vehicles. |

## Station and cluster planning

### Keep qualifications near the vehicle

The operational value of trained personnel falls when they are stored at a distant station from the specialist they are intended to crew. Use response clusters to align:

- specialist vehicles;
- trained personnel;
- frontline escort capacity;
- command support;
- extension-driven mission geography.

### Avoid hidden personnel sharing

A plan may accidentally use the same people for:

- a frontline appliance;
- a HazMat Unit;
- a Container Vehicle;
- an airfield vehicle;
- another specialist unit.

Document the normal assignment of each trained cohort. A parked vehicle should not be shown as available in the operating plan when its crew is normally committed elsewhere.

### Separate rare qualifications from core staffing

Specialist training should not reduce routine frontline crewing below the account's reserve target. Train additional personnel where possible rather than moving the only available frontline crew into a specialist role.

## Personnel audit workflow

Run this audit before every specialist activation.

1. List every vehicle and container capability in the response zone.
2. Record its verified minimum crew and training requirement where published.
3. Identify the normal assigned cohort.
4. Identify a replacement cohort for critical capabilities.
5. Simulate simultaneous incidents in Fleet Planner.
6. Check whether any person or cohort is counted twice.
7. Correct the staffing gap before activating another extension or purchasing another specialist.

## Expansion timing matrix

| Situation | Recommended action |
|---|---|
| Vehicle available, course incomplete | Delay operational activation; complete the commissioning cohort. |
| Course complete, vehicle not yet required | Retain the cohort for the planned deployment, but review whether academy capacity has a nearer priority. |
| One trained crew, repeated simultaneous demand | Train a replacement cohort before buying another vehicle that uses the same qualification. |
| Several trained crews, long response times | Distribute qualified staff and vehicles by response zone. |
| Specialist crew taken from frontline appliances | Increase personnel depth or revise assignments before further specialist expansion. |
| Extension ready, response staff incomplete | Keep mission generation inactive until the full response chain is staffed. |

## Common training failures

| Failure | Symptom | Correction |
|---|---|---|
| Buying before training | The specialist exists but cannot be counted as reliable response capacity | Complete the commissioning cohort first |
| Training exactly the minimum | One dispatch removes all qualified availability | Add a replacement cohort |
| Storing trained staff centrally | Distant stations cannot crew local specialists efficiently | Align cohorts with response zones |
| Sharing one cohort across several vehicles | Multiple vehicles appear available but only one can dispatch | Give each operational plan explicit crew ownership |
| Guessing course transferability | Staff are assumed qualified for vehicles not covered by reproduced evidence | Keep qualifications vehicle-specific until verified |
| Confusing mission personnel with vehicle crew | Incident personnel requirements are treated as vehicle staffing | Preserve the source semantics separately |
| Activating extensions before staffing | New missions appear before qualified response exists | Delay activation until training and assignment are complete |

## Fire training readiness checklist

- [ ] the course relationship is verified rather than assumed;
- [ ] published course duration and academy are recorded where known;
- [ ] class size, prerequisites and transferability remain unknown when unpublished;
- [ ] a commissioning crew is trained before the vehicle becomes operational;
- [ ] critical specialists have a replacement crew;
- [ ] trained personnel are assigned near the intended vehicle;
- [ ] no cohort is counted simultaneously on multiple vehicles;
- [ ] frontline reserve remains staffed after specialist assignment;
- [ ] extension activation waits for the complete response chain;
- [ ] future training is tied to an actual expansion plan.

## Continue Stage 37A

Return to [Fire & Rescue progression](fire-and-rescue.md) or the [specialist extension and container playbooks](fire-and-rescue-specialists.md). Later Stage 37A batches will cover airfield and railway fire response, wildfire and water rescue, and mission-family pressure analysis.
