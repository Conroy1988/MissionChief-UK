# Buildings and Extensions

Buildings create operating capacity and mission-generation relationships. Extensions activate specialist mission families or resource contracts. Neither should be treated as ready until the complete response chain is commissioned.

!!! info "Evidence boundary"
    Exact costs, build times, capacities, parent buildings and unlock conditions are published only where current evidence supports them. Missing values remain unknown. Activation sequences and reserve gates are recommendations.

## Infrastructure roles

| Role | Operational meaning |
|---|---|
| Routine station or base | Houses or generates the core service relationship |
| Specialist extension | Enables specialist mission generation, purchases or parking |
| Training facility | Produces verified qualifications where course evidence exists |
| Destination | Receives patients or prisoners where the game permits |
| Command or coordination building | Organises service generation or operational geography |
| Equipment storage | Makes supported equipment available when active and correctly assigned |
| Alliance infrastructure | Shared capability governed by alliance access and policy |

Review populated canonical fields in [Buildings and Extensions Reference](../reference/buildings-and-extensions.md).

## Generator versus responder

```text
Building or extension exists
            ↓
Mission family may generate
            ↓
Required vehicles / equipment / personnel are dispatched
            ↓
Cross-service partners and destinations complete the incident
```

The generator does not automatically provide the response. An active extension can therefore increase mission pressure before the necessary fleet, personnel or logistics are ready.

## Commissioning chain

Before activating a new building or extension, identify:

1. the mission families it can generate;
2. guaranteed and alternative resources used by representative missions;
3. verified training and personnel roles;
4. trailers, containers, towing vehicles, aircraft, boats or access equipment;
5. command and supervision;
6. patient, prisoner or recovery destinations;
7. other services required by the same mission family;
8. protected routine and specialist reserve;
9. geographic coverage and recovery-to-readiness.

Use [Mission Lookup](../tools/mission-lookup.md) and the relevant [service guide](../services/index.md) before activation.

## Extension activation gate

| Gate | Pass condition |
|---|---|
| Evidence | Representative missions and their semantics are understood |
| Response | The complete resource chain is operational, not merely owned |
| Personnel | Commissioning and replacement qualified cohorts are available |
| Logistics | Towing, carrier, launch, access or container chains are complete |
| Cross-service | Every hard partner service can respond independently |
| Geography | The capability can reach its intended POIs and access points |
| Concurrency | Two representative incidents do not reuse one scarce unit silently |
| Recovery | Useful routine and specialist cover can be restored afterwards |

## Small, standard and large infrastructure

Do not infer that larger buildings are always more efficient. Compare:

- confirmed vehicle or equipment capacity;
- extension availability;
- personnel and training access;
- geographic value;
- mission-generation effect;
- construction economics where verified;
- whether several smaller response clusters provide stronger reserve.

Unknown capacity or cost must remain a decision risk rather than being filled with a guessed number.

## Training facilities

Owning a training facility does not prove that:

- the required course exists there;
- its duration or class size is known;
- trained personnel can operate every related vehicle;
- one qualification transfers between service types;
- enough replacement personnel remain after dispatch.

Use [Training and Personnel](../reference/training-and-personnel.md) for verified course and role semantics.

## Hospitals, custody and destinations

Destination infrastructure affects how long resources remain committed after leaving the scene. When planning a building network, include:

- real route time from incident clusters;
- department or custody compatibility where verified;
- likely concurrent transports;
- return routes to useful coverage;
- alliance access assumptions;
- fallback destinations.

Do not treat a nearby destination as compatible without direct evidence.

## Dispatch and geographic organisation

Dispatch Centres and station grouping can help organise a large account, but visual organisation is not operational coverage. Use [Station Placement](../strategy/station-placement.md) for route, access, destination, specialist-hub and relief-base planning.

## Alliance infrastructure

Shared infrastructure should use explicit ownership, funding, access and review policies. It remains a contingency or shared service—not proof that every member has immediate local capability. See [Alliance Operations](../alliances/index.md).

## Change-control checklist

- [ ] Current canonical evidence reviewed.
- [ ] Unknown economics or capacities recorded.
- [ ] Mission-generation effect understood.
- [ ] Response fleet and equipment commissioned.
- [ ] Personnel and training ready.
- [ ] Logistics and destinations complete.
- [ ] Cross-service partners ready.
- [ ] Geography tested.
- [ ] Protected reserve preserved.
- [ ] One controlled activation observed before the next change.
