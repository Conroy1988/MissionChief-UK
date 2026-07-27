# Fire Specialist Extensions and Container Logistics

Specialist fire expansion changes which missions an account can generate and which capabilities must be available to complete them. The safe sequence is:

1. verify what the extension unlocks or counts towards;
2. prepare the response vehicle and trained personnel;
3. place the capability within realistic travel time;
4. activate mission generation only when the complete chain is operational;
5. preserve frontline and specialist reserve after activation.

!!! info "Evidence boundary"
    The current repository verifies the mission-generation purpose of several extensions. Where compatible parent buildings, cost, build time or capacity are not published, this guide leaves them unknown. Strategic activation sequences are recommendations, not hidden game mechanics.

**Current evidence baseline:** 27 July 2026.

## Extension command table

| Extension | Verified capability | Current unknowns | Operational implication |
|---|---|---|---|
| **Technical Rescue Extension** | Counts as a precondition for technical-rescue mission generation | Compatible parent buildings, price, construction time and capacity | Prepare technical-rescue response before increasing the count of active generators. |
| **Foam Extension** | Counts as a precondition for foam-response mission generation | Compatible parent buildings, price, build time and capacity | Do not activate merely because one foam-capable vehicle exists; consider concurrency and travel time. |
| **Flood Rescue Extension** | Counts as a precondition for flood-rescue mission generation | Compatible parent buildings, price, build time and capacity | Flood capability should be positioned for the geography it serves, not only the station with spare space. |
| **Water Damage Pump Extension** | Counts as a precondition for water-damage-pump mission generation | Compatible parent buildings, price, build time and capacity | Treat pumping and flood rescue as separate operational capabilities unless a verified vehicle record states otherwise. |
| **Container Extension** | Enables Container Vehicle purchase and container storage at a Fire Station | Extension cost, construction time and storage capacity | Plan carriers, pods, crews and dispatch concurrency together before expanding the pod inventory. |

[Open the verified Buildings & Extensions reference](../reference/buildings-and-extensions.md)

## Extension activation gates

### Gate 1 — mission-generation readiness

Use [Mission Lookup](../tools/mission-lookup.md) to inspect missions associated with the specialist family. Identify guaranteed, alternative and probabilistic requirements separately.

Do not infer that an extension itself satisfies a vehicle requirement. An extension may enable or count towards mission generation while the response resource remains a separate dispatch need.

### Gate 2 — response-chain readiness

Confirm the complete response chain:

- compatible vehicle or container;
- required trained personnel;
- carrier or towing vehicle where applicable;
- enough frontline appliances to accompany the specialist response;
- geographic coverage for the generated mission family;
- reserve for a second incident.

### Gate 3 — personnel readiness

Training must be completed before the capability is counted as operational. The canonical HazMat record, for example, verifies a **three-day HazMat course at the Fire Academy**. Buying a HazMat resource before trained staff are available creates a visible fleet asset without reliable response capacity.

### Gate 4 — concurrent availability

Test more than one incident in the [Concurrent Fleet Planner](../tools/fleet-planner.md). An account may have every required specialist on paper but still fail when two missions need the same single unit, crew or carrier.

### Gate 5 — activation and observation

After activating an extension:

1. monitor the first specialist missions;
2. record response times and unavailable-resource messages;
3. identify whether the constraint is vehicle count, personnel, frontline escort or geography;
4. correct the constraint before activating another generator of the same family.

## Technical Rescue Extension playbook

### Before activation

- Confirm technical-rescue missions are appropriate for the account's current scale.
- Identify every specialist and frontline capability used by representative missions.
- Position the response resource where it can cover the extension's operating area.
- Keep trained personnel at the same operational base or within the game's supported staffing model.

### After activation

- Watch for long-distance specialist dispatches.
- Avoid making one technical-rescue unit the only solution for a wide network.
- Duplicate by response zone when travel time, not mission frequency, becomes the failure point.

!!! warning "Unknown building details"
    The canonical extension record does not currently publish compatible parent buildings, price, construction time or capacity. Do not convert those omissions into assumptions.

## Foam Extension playbook

Foam mission generation and foam response are distinct planning decisions.

The **Water Ladder with CAFS** is a verified foam-capable appliance with:

- **17,300 credits** or **10 coins**;
- minimum crew **2** and maximum crew **9**;
- a requirement for a **Fire Station with Fire Support**;
- firefighting, foam-response and compressed-air-foam capabilities.

Use [Resource Comparison](../tools/resource-comparison.md) to compare this with other foam resources in the canonical catalogue. Do not assume every foam vehicle also replaces every water, frontline or specialist requirement.

### Recommended activation sequence

1. secure at least one locally crewed foam capability;
2. verify that normal fire coverage remains intact when it dispatches;
3. test a second simultaneous foam demand in Fleet Planner;
4. activate the extension;
5. duplicate foam coverage when response distance or concurrency proves the need.

## Flood Rescue Extension playbook

Flood Rescue Extensions are verified mission-generation preconditions. Their current canonical record does not publish cost, parent-building compatibility, build time or capacity.

### Recommended placement logic

- Prioritise geographic access to likely flood-response areas.
- Keep the specialist unit separate from the frontline reserve calculation.
- Check cross-service requirements such as ambulance, HART, police or aviation through Mission Lookup rather than assuming a fire-only response.
- Do not treat a water-damage pump as equivalent to flood rescue unless an evidence-backed resource record explicitly supports that capability.

## Water Damage Pump Extension playbook

Water Damage Pump Extensions generate their own mission family. The extension record verifies that purpose but leaves building and economic fields unknown.

### Recommended activation sequence

- verify a suitable pumping resource exists and is crewed;
- preserve a transport or carrier path when the resource is container-based;
- confirm that the station can still dispatch ordinary fire resources;
- activate one generator first and observe mission pressure before adding more;
- distribute additional capability when the first unit becomes a travel-time or concurrency bottleneck.

## Container Extension system

The Container Extension is verified for **Fire Stations** and enables both container storage and purchase of the Container Vehicle and published UK container pods.

### Verified Container Vehicle contract

| Field | Verified value |
|---|---|
| Cost | **10,000 credits** or **10 coins** |
| Staffing | Minimum **1**, maximum **2** |
| Building | Fire Station with Container Extension |
| Capability | Container transport |
| Published compatible pods | Water, Bulk Foam, Rescue, Command, Welfare, BASU, Misting, HazMat, Operational Support Unit and High Volume Pump containers |

The official UK container contract identifies the Container Vehicle as the towing vehicle for every published pod in the canonical fleet.

[Review the complete UK Container Fleet evidence](../reference/verified-vehicle-container-fleet-batch-4.md)

## Container planning doctrine

A container estate contains at least four separate operational resources:

1. **the extension** — permits the system to exist at the station;
2. **the pod** — supplies the specialist capability;
3. **the Container Vehicle** — transports the selected pod;
4. **the crew** — makes the carrier dispatchable.

!!! tip "Recommended readiness rule"
    Do not count a stored pod as immediately available unless a compatible, staffed carrier is also available to move it. This is an operational inference from the verified towing contract, not a claim about undocumented game internals.

### Carrier-to-pod pressure

One carrier serving many pods can become a transport bottleneck during simultaneous incidents. Use the Fleet Planner and actual dispatch behaviour to decide when another carrier is justified.

A second carrier is usually more valuable when:

- two container capabilities are regularly needed at once;
- one carrier is committed for long travel times;
- several stations depend on the same central container base;
- the carrier's crew is also being used by other vehicles;
- alliance support is not consistently available.

### Recommended container base patterns

=== "Single specialist base"

    Appropriate for an early compact network with rare container demand.

    - one Container Extension;
    - one staffed Container Vehicle;
    - a limited pod set matched to current missions;
    - alliance fallback for unusual simultaneous demand.

    The risk is a single carrier or station becoming the failure point.

=== "Regional container bases"

    Appropriate when the account covers several distant response zones.

    - distribute carriers by travel-time region;
    - place high-frequency pods near their mission geography;
    - avoid duplicating every pod automatically;
    - keep enough trained staff for simultaneous carrier dispatches.

=== "Major-incident logistics network"

    Appropriate for established accounts with sustained concurrency.

    - multiple carriers across the network;
    - duplicate critical pods based on measured demand;
    - separate welfare, command and operational-support planning from suppression capability;
    - maintain frontline and command reserve while container resources are committed.

## Container acquisition order

There is no universal mandatory pod order. Use this evidence-led sequence:

1. search recent and unlocked missions for container requirements;
2. classify the requirement as guaranteed, alternative or probabilistic;
3. confirm the pod's crew and carrier path;
4. buy the highest-pressure capability first;
5. test simultaneous demand before adding lower-frequency pods;
6. duplicate only when geography or concurrency demonstrates the need.

## Common specialist-expansion failures

| Failure | Symptom | Correction |
|---|---|---|
| Activating generators before response readiness | New specialist missions wait for unavailable units | Pause further activation and complete the response chain |
| Treating extension count as response capability | Missions generate correctly but no vehicle can satisfy them | Add and staff the actual response resource |
| Owning pods without carrier capacity | Specialist pods remain stored while the carrier is committed | Increase carrier availability or distribute pod bases |
| Training after purchase | New vehicles cannot be reliably crewed | Run the training pipeline before operational activation |
| Centralising every specialist | Long travel times block distant incidents | Duplicate by response zone |
| Assuming missing cost or capacity is zero | Expansion planning uses unsupported values | Keep the field unknown until direct evidence is added |
| Confusing flood rescue with water pumping | The wrong specialist is dispatched or purchased | Check each mission and resource capability separately |

## Specialist activation checklist

- [ ] the extension's verified mission-generation purpose is understood;
- [ ] compatible-building and economic fields are not being guessed;
- [ ] every required vehicle, pod and carrier is available;
- [ ] required training is complete;
- [ ] the specialist can reach the intended area in reasonable time;
- [ ] normal frontline and command reserve remains available;
- [ ] simultaneous specialist demand has been tested;
- [ ] container pods have staffed carrier capacity;
- [ ] the first activation will be observed before another generator is added;
- [ ] alliance assistance is treated as support rather than guaranteed capacity.

## Continue Stage 37A

Return to [Fire & Rescue progression and fleet planning](fire-and-rescue.md) for the core network doctrine. Later Stage 37A batches will cover specialist training pipelines, airfield and railway fire-response planning, wildfire and water rescue, and mission-family pressure analysis derived from the complete canonical catalogue.
