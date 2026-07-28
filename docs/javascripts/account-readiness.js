(() => {
  "use strict";

  const STORAGE_KEY = "mcuk-account-readiness-v1";
  const EXPORT_VERSION = 1;
  const script = document.currentScript;
  const siteRoot = script && script.src
    ? script.src.replace(/javascripts\/account-readiness\.js(?:\?.*)?$/, "")
    : `${window.location.origin}/MissionChief-UK/`;
  const apiRoot = new URL("assets/data/v1/", siteRoot);
  const cache = new Map();

  const escapeHtml = (value) => String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");

  const label = (value) => String(value || "")
    .replaceAll("_", " ")
    .replace(/\b\w/g, (character) => character.toUpperCase());

  const finiteNumber = (value) => {
    if (value === "" || value === null || value === undefined) return null;
    const parsed = Number(value);
    return Number.isFinite(parsed) && parsed >= 0 ? parsed : null;
  };

  const addToMap = (map, key, quantity) => {
    const value = Number(quantity);
    if (!key || !Number.isFinite(value)) return;
    map.set(key, (map.get(key) || 0) + value);
  };

  const maxInMap = (map, key, quantity) => {
    const value = Number(quantity);
    if (!key || !Number.isFinite(value)) return;
    map.set(key, Math.max(map.get(key) || 0, value));
  };

  async function collection(name) {
    if (!cache.has(name)) {
      cache.set(name, fetch(new URL(`${name}.json`, apiRoot), { cache: "no-cache" })
        .then((response) => {
          if (!response.ok) throw new Error(`Unable to load ${name} data (${response.status})`);
          return response.json();
        })
        .then((payload) => Array.isArray(payload.records) ? payload.records : []));
    }
    return cache.get(name);
  }

  function claimRoot() {
    const root = document.querySelector("[data-mcuk-tool='account-readiness']");
    if (!root || root.dataset.mcukReady === "true") return null;
    root.dataset.mcukReady = "true";
    return root;
  }

  function emptyState() {
    return {
      scenario: [],
      resources: {},
      personnel: {}
    };
  }

  function sanitiseState(candidate) {
    const clean = emptyState();
    if (!candidate || typeof candidate !== "object") return clean;
    if (Array.isArray(candidate.scenario)) {
      clean.scenario = candidate.scenario
        .map((item) => ({
          missionId: String(item?.missionId ?? ""),
          concurrency: Math.min(50, Math.max(1, Number.parseInt(item?.concurrency, 10) || 1))
        }))
        .filter((item) => item.missionId);
    }
    for (const [key, value] of Object.entries(candidate.resources || {})) {
      clean.resources[String(key)] = {
        dispatchable: value?.dispatchable === "" ? "" : String(value?.dispatchable ?? ""),
        reserve: value?.reserve === "" ? "0" : String(value?.reserve ?? "0")
      };
    }
    for (const [key, value] of Object.entries(candidate.personnel || {})) {
      clean.personnel[String(key)] = {
        available: value?.available === "" ? "" : String(value?.available ?? ""),
        reserve: value?.reserve === "" ? "0" : String(value?.reserve ?? "0")
      };
    }
    return clean;
  }

  function aggregateScenario(state, missionById) {
    const guaranteed = new Map();
    const alternatives = [];
    const personnelRequired = new Map();
    const personnelAvailable = new Map();
    const advisoryPersonnel = [];
    const recovery = new Map();
    const selected = [];

    for (const entry of state.scenario) {
      const mission = missionById.get(String(entry.missionId));
      if (!mission) continue;
      const concurrency = Math.min(50, Math.max(1, Number(entry.concurrency) || 1));
      selected.push({ mission, concurrency });

      for (const item of mission.requirements?.guaranteed || []) {
        addToMap(guaranteed, item.resource, Number(item.quantity) * concurrency);
      }
      for (const [index, item] of (mission.requirements?.alternatives || []).entries()) {
        alternatives.push({
          id: `${mission.id}:${index}`,
          label: `${mission.name} — alternative ${index + 1}`,
          resources: [...new Set(item.resources || [])],
          quantity: Number(item.quantity) * concurrency
        });
      }
      for (const item of mission.personnel?.required || []) {
        addToMap(personnelRequired, item.role, Number(item.quantity) * concurrency);
      }
      for (const item of mission.personnel?.available || []) {
        maxInMap(personnelAvailable, item.role, item.quantity);
      }
      for (const type of ["average_minimum", "probabilistic", "ranges"]) {
        for (const item of mission.personnel?.[type] || []) {
          advisoryPersonnel.push({ mission: mission.name, type, item, concurrency });
        }
      }
      for (const item of mission.requirements?.probabilistic || []) {
        advisoryPersonnel.push({ mission: mission.name, type: "probabilistic_resource", item, concurrency });
      }
      for (const item of mission.requirements?.conditional || []) {
        advisoryPersonnel.push({ mission: mission.name, type: "conditional_resource", item, concurrency });
      }
      for (const asset of mission.recovery?.assets || []) {
        const current = recovery.get(asset.asset_type) || { minimum: 0, maximum: 0 };
        current.minimum += Number(asset.minimum || 0) * concurrency;
        current.maximum += Number(asset.maximum ?? asset.minimum ?? 0) * concurrency;
        recovery.set(asset.asset_type, current);
      }
    }

    return {
      selected,
      guaranteed,
      alternatives,
      personnelRequired,
      personnelAvailable,
      advisoryPersonnel,
      recovery
    };
  }

  function addEdge(graph, from, to, capacity) {
    if (!graph.has(from)) graph.set(from, []);
    if (!graph.has(to)) graph.set(to, []);
    const forward = { to, capacity, flow: 0, reverse: graph.get(to).length };
    const backward = { to: from, capacity: 0, flow: 0, reverse: graph.get(from).length };
    graph.get(from).push(forward);
    graph.get(to).push(backward);
  }

  function solveAllocation(groups, capacities) {
    const graph = new Map();
    const source = "source";
    const sink = "sink";
    const resourceKeys = new Set();
    const allocation = new Map();
    const required = groups.reduce((sum, group) => sum + Math.max(0, Number(group.quantity) || 0), 0);

    for (const group of groups) {
      for (const resource of group.resources || []) resourceKeys.add(resource);
    }
    for (const resource of resourceKeys) {
      addEdge(graph, source, `resource:${resource}`, Math.max(0, capacities.get(resource) || 0));
    }
    groups.forEach((group, index) => {
      const groupNode = `group:${index}`;
      addEdge(graph, groupNode, sink, Math.max(0, Number(group.quantity) || 0));
      for (const resource of group.resources || []) {
        addEdge(graph, `resource:${resource}`, groupNode, Number.MAX_SAFE_INTEGER);
      }
    });

    let totalFlow = 0;
    while (true) {
      const queue = [source];
      const parents = new Map([[source, null]]);
      while (queue.length && !parents.has(sink)) {
        const node = queue.shift();
        for (let index = 0; index < (graph.get(node) || []).length; index += 1) {
          const edge = graph.get(node)[index];
          if (edge.capacity - edge.flow <= 0 || parents.has(edge.to)) continue;
          parents.set(edge.to, { node, index });
          queue.push(edge.to);
          if (edge.to === sink) break;
        }
      }
      if (!parents.has(sink)) break;
      let increment = Number.MAX_SAFE_INTEGER;
      for (let node = sink; node !== source;) {
        const parent = parents.get(node);
        const edge = graph.get(parent.node)[parent.index];
        increment = Math.min(increment, edge.capacity - edge.flow);
        node = parent.node;
      }
      for (let node = sink; node !== source;) {
        const parent = parents.get(node);
        const edge = graph.get(parent.node)[parent.index];
        edge.flow += increment;
        graph.get(edge.to)[edge.reverse].flow -= increment;
        node = parent.node;
      }
      totalFlow += increment;
    }

    groups.forEach((group, index) => {
      const groupNode = `group:${index}`;
      const rows = [];
      for (const resource of group.resources || []) {
        const edge = (graph.get(`resource:${resource}`) || []).find((candidate) => candidate.to === groupNode);
        if (edge && edge.flow > 0) rows.push({ resource, quantity: edge.flow });
      }
      allocation.set(group.id, rows);
    });

    return { totalFlow, required, allocation };
  }

  function buildInventoryModel(aggregate, vehicleById) {
    const resources = new Set(aggregate.guaranteed.keys());
    for (const group of aggregate.alternatives) {
      for (const resource of group.resources) resources.add(resource);
    }
    const towableAssets = new Set();
    for (const resource of resources) {
      const vehicle = vehicleById.get(resource);
      if ((vehicle?.towing?.towable_by || []).length) {
        towableAssets.add(resource);
        for (const towingResource of vehicle.towing.towable_by) resources.add(towingResource);
      }
    }
    return { resources, towableAssets };
  }

  function inputValue(record, field, fallback = "") {
    const value = record?.[field];
    return value === undefined || value === null ? fallback : String(value);
  }

  function statusBadge(status, text = null) {
    return `<span class="mcuk-readiness-badge mcuk-readiness-badge--${escapeHtml(status)}">${escapeHtml(text || label(status))}</span>`;
  }

  function advisoryLabel(entry) {
    if (entry.type === "average_minimum") {
      return `${entry.mission}: average-minimum ${entry.item.role || "personnel"} ${entry.item.quantity ?? "not published"}`;
    }
    if (entry.type === "ranges") {
      return `${entry.mission}: ${entry.item.role || "personnel"} range ${entry.item.minimum ?? "?"}–${entry.item.maximum ?? "?"}`;
    }
    if (entry.type === "probabilistic") {
      return `${entry.mission}: ${entry.item.role || "personnel"} ${entry.item.quantity ?? "?"} at ${Math.round(Number(entry.item.probability || 0) * 100)}%`;
    }
    if (entry.type === "probabilistic_resource") {
      return `${entry.mission}: ${label(entry.item.resource)} ${entry.item.quantity ?? "?"} at ${Math.round(Number(entry.item.probability || 0) * 100)}%`;
    }
    const probability = Number.isFinite(Number(entry.item.probability))
      ? ` at ${Math.round(Number(entry.item.probability) * 100)}%`
      : "";
    return `${entry.mission}: ${label(entry.item.resource)} ${entry.item.quantity ?? "?"}, ${label(entry.item.condition)}${probability}`;
  }

  function initAccountReadiness() {
    const root = claimRoot();
    if (!root) return;

    const missionSelect = root.querySelector("[data-role='mission']");
    const concurrencyInput = root.querySelector("[data-role='concurrency']");
    const scenarioRoot = root.querySelector("[data-role='scenario']");
    const inventoryRoot = root.querySelector("[data-role='inventory']");
    const summaryRoot = root.querySelector("[data-role='summary']");
    const resultsRoot = root.querySelector("[data-role='results']");
    const scenarioName = root.querySelector("[data-role='scenario-name']");
    const savedSelect = root.querySelector("[data-role='saved-scenarios']");
    const importInput = root.querySelector("[data-role='import-json']");
    const storageStatus = root.querySelector("[data-role='storage-status']");

    let missions = [];
    let missionById = new Map();
    let vehicleById = new Map();
    let state = emptyState();

    const readSaved = () => {
      try {
        const parsed = JSON.parse(localStorage.getItem(STORAGE_KEY) || "{}");
        return parsed && typeof parsed === "object" ? parsed : {};
      } catch {
        return {};
      }
    };

    const writeSaved = (saved) => {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(saved));
    };

    const renderSavedOptions = () => {
      const saved = readSaved();
      const names = Object.keys(saved).sort((a, b) => a.localeCompare(b));
      savedSelect.innerHTML = names.length
        ? `<option value="">Select a saved scenario</option>${names.map((name) => `<option value="${escapeHtml(name)}">${escapeHtml(name)}</option>`).join("")}`
        : '<option value="">No saved scenarios</option>';
    };

    const renderScenario = () => {
      if (!state.scenario.length) {
        scenarioRoot.innerHTML = "<p>No missions selected. Add a canonical mission to begin.</p>";
        return;
      }
      const rows = state.scenario.map((entry, index) => {
        const mission = missionById.get(String(entry.missionId));
        return `<tr>
          <td>${escapeHtml(mission?.name || `Mission #${entry.missionId}`)}</td>
          <td>${escapeHtml(entry.concurrency)}</td>
          <td><button type="button" data-action="remove-mission" data-index="${index}" class="md-button">Remove</button></td>
        </tr>`;
      }).join("");
      scenarioRoot.innerHTML = `<div class="mcuk-readiness-table"><table><thead><tr><th>Mission</th><th>Concurrent copies</th><th>Action</th></tr></thead><tbody>${rows}</tbody></table></div>`;
    };

    const renderInventory = (aggregate) => {
      if (!aggregate.selected.length) {
        inventoryRoot.innerHTML = "<p>Add at least one mission to create the inventory worksheet.</p>";
        return;
      }
      const model = buildInventoryModel(aggregate, vehicleById);
      for (const resource of model.resources) {
        if (!state.resources[resource]) state.resources[resource] = { dispatchable: "", reserve: "0" };
      }
      for (const role of new Set([...aggregate.personnelRequired.keys(), ...aggregate.personnelAvailable.keys()])) {
        if (!state.personnel[role]) state.personnel[role] = { available: "", reserve: "0" };
      }

      const resourceRows = [...model.resources]
        .sort((a, b) => label(a).localeCompare(label(b)))
        .map((resource) => {
          const record = state.resources[resource];
          const vehicle = vehicleById.get(resource);
          const note = vehicle?.name && vehicle.name !== label(resource) ? vehicle.name : label(resource);
          return `<tr data-resource-id="${escapeHtml(resource)}">
            <th scope="row"><span>${escapeHtml(note)}</span><code>${escapeHtml(resource)}</code></th>
            <td><input data-inventory="resource" data-id="${escapeHtml(resource)}" data-field="dispatchable" type="number" min="0" inputmode="numeric" value="${escapeHtml(inputValue(record, "dispatchable"))}" aria-label="Dispatchable ${escapeHtml(note)}"></td>
            <td><input data-inventory="resource" data-id="${escapeHtml(resource)}" data-field="reserve" type="number" min="0" inputmode="numeric" value="${escapeHtml(inputValue(record, "reserve", "0"))}" aria-label="Protected reserve ${escapeHtml(note)}"></td>
          </tr>`;
        }).join("");

      const roles = [...new Set([...aggregate.personnelRequired.keys(), ...aggregate.personnelAvailable.keys()])]
        .sort((a, b) => a.localeCompare(b));
      const personnelTable = roles.length ? `<h3>Qualified personnel</h3>
        <p>Available personnel is used for generation thresholds. Incident cover subtracts the protected personnel reserve.</p>
        <div class="mcuk-readiness-table"><table><thead><tr><th>Role</th><th>Available qualified personnel</th><th>Protected reserve</th></tr></thead><tbody>${roles.map((role) => {
          const record = state.personnel[role];
          return `<tr data-personnel-role="${escapeHtml(role)}"><th scope="row">${escapeHtml(role)}</th><td><input data-inventory="personnel" data-id="${escapeHtml(role)}" data-field="available" type="number" min="0" inputmode="numeric" value="${escapeHtml(inputValue(record, "available"))}" aria-label="Available ${escapeHtml(role)}"></td><td><input data-inventory="personnel" data-id="${escapeHtml(role)}" data-field="reserve" type="number" min="0" inputmode="numeric" value="${escapeHtml(inputValue(record, "reserve", "0"))}" aria-label="Protected reserve ${escapeHtml(role)}"></td></tr>`;
        }).join("")}</tbody></table></div>` : "";

      inventoryRoot.innerHTML = `<h3>Operational resources</h3>
        <div class="mcuk-readiness-table"><table><thead><tr><th>Canonical resource</th><th>Dispatchable and correctly crewed</th><th>Protected reserve</th></tr></thead><tbody>${resourceRows}</tbody></table></div>${personnelTable}`;
    };

    const renderResults = (aggregate) => {
      if (!aggregate.selected.length) {
        summaryRoot.innerHTML = `${statusBadge("unavailable")}<p>Add a mission to begin.</p>`;
        resultsRoot.innerHTML = "<p>No scenario selected.</p>";
        return;
      }

      const knownCapacity = new Map();
      const unknownResources = new Set();
      for (const resource of buildInventoryModel(aggregate, vehicleById).resources) {
        const record = state.resources[resource] || {};
        const dispatchable = finiteNumber(record.dispatchable);
        const reserve = finiteNumber(record.reserve) ?? 0;
        if (dispatchable === null) unknownResources.add(resource);
        else knownCapacity.set(resource, Math.max(0, dispatchable - reserve));
      }

      const residual = new Map(knownCapacity);
      const guaranteedRows = [];
      let gaps = 0;
      let unknowns = 0;
      for (const [resource, demand] of [...aggregate.guaranteed.entries()].sort((a, b) => label(a[0]).localeCompare(label(b[0])))) {
        const known = knownCapacity.get(resource);
        let status;
        let detail;
        if (known === undefined) {
          status = "unknown";
          detail = "Dispatchable inventory not entered";
          unknowns += 1;
        } else if (known >= demand) {
          status = "ready";
          detail = `${known} usable after reserve`;
        } else {
          status = "degraded";
          detail = `${known} usable; short by ${demand - known}`;
          gaps += 1;
        }
        residual.set(resource, Math.max(0, (known || 0) - demand));
        guaranteedRows.push(`<tr><td>${escapeHtml(label(resource))}<br><code>${escapeHtml(resource)}</code></td><td>${escapeHtml(demand)}</td><td>${escapeHtml(detail)}</td><td>${statusBadge(status)}</td></tr>`);
      }

      const alternativeSolution = solveAllocation(aggregate.alternatives, residual);
      const alternativeRows = aggregate.alternatives.map((group) => {
        const allocations = alternativeSolution.allocation.get(group.id) || [];
        const allocated = allocations.reduce((sum, item) => sum + item.quantity, 0);
        const hasUnknown = group.resources.some((resource) => unknownResources.has(resource));
        let status;
        let detail;
        if (allocated >= group.quantity) {
          status = "ready";
          detail = allocations.map((item) => `${item.quantity} ${label(item.resource)}`).join(" + ") || "Covered";
        } else if (hasUnknown) {
          status = "unknown";
          detail = `${allocated}/${group.quantity} covered by known inventory; unknown accepted resources remain`;
          unknowns += 1;
        } else {
          status = "degraded";
          detail = `${allocated}/${group.quantity} allocatable; short by ${group.quantity - allocated}`;
          gaps += 1;
        }
        return `<tr><td>${escapeHtml(group.label)}</td><td>${escapeHtml(group.quantity)}</td><td>${escapeHtml(group.resources.map(label).join(" OR "))}</td><td>${escapeHtml(detail)}</td><td>${statusBadge(status)}</td></tr>`;
      });

      const personnelRows = [];
      const roles = [...new Set([...aggregate.personnelRequired.keys(), ...aggregate.personnelAvailable.keys()])]
        .sort((a, b) => a.localeCompare(b));
      for (const role of roles) {
        const required = aggregate.personnelRequired.get(role) || 0;
        const generation = aggregate.personnelAvailable.get(role) || 0;
        const record = state.personnel[role] || {};
        const available = finiteNumber(record.available);
        const reserve = finiteNumber(record.reserve) ?? 0;
        const usable = available === null ? null : Math.max(0, available - reserve);
        const generationStatus = available === null ? "unknown" : available >= generation ? "ready" : "degraded";
        const incidentStatus = usable === null ? "unknown" : usable >= required ? "ready" : "degraded";
        const status = generationStatus === "degraded" || incidentStatus === "degraded"
          ? "degraded"
          : generationStatus === "unknown" || incidentStatus === "unknown" ? "unknown" : "ready";
        if (status === "degraded") gaps += 1;
        if (status === "unknown") unknowns += 1;
        const detail = available === null
          ? "Qualified personnel not entered"
          : `${available} available; ${usable} usable after reserve`;
        personnelRows.push(`<tr><td>${escapeHtml(role)}</td><td>${escapeHtml(required || "—")}</td><td>${escapeHtml(generation || "—")}</td><td>${escapeHtml(detail)}</td><td>${statusBadge(status)}</td></tr>`);
      }

      const demandedTowables = new Map();
      for (const [resource, quantity] of aggregate.guaranteed) {
        if ((vehicleById.get(resource)?.towing?.towable_by || []).length) addToMap(demandedTowables, resource, quantity);
      }
      for (const group of aggregate.alternatives) {
        for (const item of alternativeSolution.allocation.get(group.id) || []) {
          if ((vehicleById.get(item.resource)?.towing?.towable_by || []).length) addToMap(demandedTowables, item.resource, item.quantity);
        }
      }
      const towingGroups = [...demandedTowables.entries()].map(([resource, quantity]) => ({
        id: `tow:${resource}`,
        label: label(resource),
        resources: vehicleById.get(resource)?.towing?.towable_by || [],
        quantity
      }));
      const towingSolution = solveAllocation(towingGroups, knownCapacity);
      const towingRows = towingGroups.map((group) => {
        const allocations = towingSolution.allocation.get(group.id) || [];
        const allocated = allocations.reduce((sum, item) => sum + item.quantity, 0);
        const hasUnknown = group.resources.some((resource) => unknownResources.has(resource));
        let status;
        let detail;
        if (allocated >= group.quantity) {
          status = "ready";
          detail = allocations.map((item) => `${item.quantity} ${label(item.resource)}`).join(" + ");
        } else if (hasUnknown) {
          status = "unknown";
          detail = `${allocated}/${group.quantity} covered by known towing inventory`;
          unknowns += 1;
        } else {
          status = "degraded";
          detail = `${allocated}/${group.quantity} compatible towing routes; short by ${group.quantity - allocated}`;
          gaps += 1;
        }
        return `<tr><td>${escapeHtml(group.label)}</td><td>${escapeHtml(group.quantity)}</td><td>${escapeHtml(group.resources.map(label).join(" OR "))}</td><td>${escapeHtml(detail)}</td><td>${statusBadge(status)}</td></tr>`;
      });

      const relevantResources = new Set([
        ...aggregate.guaranteed.keys(),
        ...aggregate.alternatives.flatMap((group) => group.resources)
      ]);
      const qualifications = [];
      const seenQualifications = new Set();
      for (const resource of relevantResources) {
        for (const training of vehicleById.get(resource)?.training_requirements || []) {
          const key = `${resource}:${training.course}:${training.duration_days}:${training.school}`;
          if (seenQualifications.has(key)) continue;
          seenQualifications.add(key);
          qualifications.push({ resource, ...training });
        }
      }

      const finalState = gaps > 0 ? "degraded" : unknowns > 0 || aggregate.advisoryPersonnel.length > 0 ? "watch" : "ready";
      summaryRoot.innerHTML = `${statusBadge(finalState)}<div><strong>${escapeHtml(aggregate.selected.length)}</strong> mission row${aggregate.selected.length === 1 ? "" : "s"}; <strong>${gaps}</strong> definite gap${gaps === 1 ? "" : "s"}; <strong>${unknowns}</strong> unresolved inventory check${unknowns === 1 ? "" : "s"}.</div>`;

      const guaranteedTable = `<h3>Guaranteed resources</h3><div class="mcuk-readiness-table"><table><thead><tr><th>Resource</th><th>Required</th><th>Inventory result</th><th>Status</th></tr></thead><tbody>${guaranteedRows.join("") || '<tr><td colspan="4">No guaranteed resource rows are published.</td></tr>'}</tbody></table></div>`;
      const alternativesTable = aggregate.alternatives.length
        ? `<h3>Independent alternative groups</h3><p>The allocator prevents known inventory from being reused across several groups.</p><div class="mcuk-readiness-table"><table><thead><tr><th>Group</th><th>Required</th><th>Accepted resources</th><th>Allocation</th><th>Status</th></tr></thead><tbody>${alternativeRows.join("")}</tbody></table></div>`
        : "";
      const personnelTable = roles.length
        ? `<h3>Personnel</h3><div class="mcuk-readiness-table"><table><thead><tr><th>Role</th><th>Required at incidents</th><th>Available-before-generation threshold</th><th>Inventory result</th><th>Status</th></tr></thead><tbody>${personnelRows.join("")}</tbody></table></div>`
        : "";
      const towingTable = towingGroups.length
        ? `<h3>Towing and carrier compatibility</h3><p>This is a separate logistics check. It does not assume that a towing vehicle can also satisfy another response row at the same time.</p><div class="mcuk-readiness-table"><table><thead><tr><th>Trailer or container</th><th>Required</th><th>Compatible towing resources</th><th>Allocation</th><th>Status</th></tr></thead><tbody>${towingRows.join("")}</tbody></table></div>`
        : "";
      const qualificationTable = qualifications.length
        ? `<h3>Published qualification contracts</h3><p>Resource inventory should include only correctly staffed and trained units. These rows are advisory because the canonical records do not prove a universal crew-to-unit conversion.</p><div class="mcuk-readiness-table"><table><thead><tr><th>Resource</th><th>Course</th><th>Duration</th><th>School</th></tr></thead><tbody>${qualifications.map((item) => `<tr><td>${escapeHtml(label(item.resource))}</td><td>${escapeHtml(item.course || "Not published")}</td><td>${escapeHtml(item.duration_days === undefined ? "Not published" : `${item.duration_days} day${item.duration_days === 1 ? "" : "s"}`)}</td><td>${escapeHtml(item.school || "Not published")}</td></tr>`).join("")}</tbody></table></div>`
        : "";
      const recoveryTable = aggregate.recovery.size
        ? `<h3>Recovery workload</h3><p>These are post-response assets to clear, not fictional emergency-resource requirements.</p><div class="mcuk-readiness-table"><table><thead><tr><th>Asset type</th><th>Minimum</th><th>Maximum</th></tr></thead><tbody>${[...aggregate.recovery.entries()].map(([asset, range]) => `<tr><td>${escapeHtml(label(asset))}</td><td>${escapeHtml(range.minimum)}</td><td>${escapeHtml(range.maximum)}</td></tr>`).join("")}</tbody></table></div>`
        : "";
      const advisory = aggregate.advisoryPersonnel.length
        ? `<h3>Non-exact evidence</h3><p>These fields are displayed for attention but do not become exact readiness gaps.</p><ul>${aggregate.advisoryPersonnel.map((entry) => `<li>${escapeHtml(advisoryLabel(entry))}</li>`).join("")}</ul>`
        : "";

      resultsRoot.innerHTML = `${guaranteedTable}${alternativesTable}${personnelTable}${towingTable}${qualificationTable}${recoveryTable}${advisory}`;
    };

    const renderAll = () => {
      renderScenario();
      const aggregate = aggregateScenario(state, missionById);
      renderInventory(aggregate);
      renderResults(aggregate);
    };

    root.addEventListener("input", (event) => {
      const input = event.target.closest("[data-inventory]");
      if (!input) return;
      const collectionName = input.dataset.inventory === "personnel" ? "personnel" : "resources";
      if (!state[collectionName][input.dataset.id]) state[collectionName][input.dataset.id] = {};
      state[collectionName][input.dataset.id][input.dataset.field] = input.value;
      renderResults(aggregateScenario(state, missionById));
    });

    root.addEventListener("click", (event) => {
      const button = event.target.closest("button[data-action]");
      if (!button) return;
      const action = button.dataset.action;
      if (action === "add-mission") {
        const missionId = String(missionSelect.value || "");
        if (!missionId) return;
        const concurrency = Math.min(50, Math.max(1, Number.parseInt(concurrencyInput.value, 10) || 1));
        const existing = state.scenario.find((item) => item.missionId === missionId);
        if (existing) existing.concurrency = Math.min(50, existing.concurrency + concurrency);
        else state.scenario.push({ missionId, concurrency });
        renderAll();
      }
      if (action === "remove-mission") {
        state.scenario.splice(Number(button.dataset.index), 1);
        renderAll();
      }
      if (action === "clear-current") {
        state = emptyState();
        renderAll();
        storageStatus.textContent = "Current scenario cleared. Saved scenarios were not changed.";
      }
      if (action === "save-local") {
        const name = scenarioName.value.trim();
        if (!name) {
          storageStatus.textContent = "Enter a scenario name before saving.";
          return;
        }
        try {
          const saved = readSaved();
          saved[name] = { version: EXPORT_VERSION, savedAt: new Date().toISOString(), state };
          writeSaved(saved);
          renderSavedOptions();
          savedSelect.value = name;
          storageStatus.textContent = `Saved “${name}” in this browser.`;
        } catch (error) {
          storageStatus.textContent = `Unable to save locally: ${error.message}`;
        }
      }
      if (action === "load-local") {
        const name = savedSelect.value;
        const saved = readSaved()[name];
        if (!saved) {
          storageStatus.textContent = "Select a saved scenario to load.";
          return;
        }
        state = sanitiseState(saved.state);
        scenarioName.value = name;
        renderAll();
        storageStatus.textContent = `Loaded “${name}” from this browser.`;
      }
      if (action === "delete-local") {
        const name = savedSelect.value;
        if (!name) {
          storageStatus.textContent = "Select a saved scenario to delete.";
          return;
        }
        try {
          const saved = readSaved();
          delete saved[name];
          writeSaved(saved);
          renderSavedOptions();
          storageStatus.textContent = `Deleted “${name}” from this browser.`;
        } catch (error) {
          storageStatus.textContent = `Unable to delete the saved scenario: ${error.message}`;
        }
      }
      if (action === "export-json") {
        const payload = {
          format: "missionchief-uk-account-readiness",
          version: EXPORT_VERSION,
          exportedAt: new Date().toISOString(),
          name: scenarioName.value.trim() || "Readiness scenario",
          state
        };
        const blob = new Blob([JSON.stringify(payload, null, 2)], { type: "application/json" });
        const url = URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = url;
        link.download = "missionchief-uk-readiness-scenario.json";
        link.click();
        URL.revokeObjectURL(url);
        storageStatus.textContent = "Exported the current scenario as JSON.";
      }
    });

    importInput.addEventListener("change", async () => {
      const file = importInput.files?.[0];
      if (!file) return;
      try {
        const payload = JSON.parse(await file.text());
        if (payload.format !== "missionchief-uk-account-readiness" || Number(payload.version) !== EXPORT_VERSION) {
          throw new Error("Unsupported readiness scenario format");
        }
        state = sanitiseState(payload.state);
        scenarioName.value = String(payload.name || "Imported readiness scenario").slice(0, 80);
        renderAll();
        storageStatus.textContent = `Imported “${scenarioName.value}”. It has not been saved locally.`;
      } catch (error) {
        storageStatus.textContent = `Unable to import JSON: ${error.message}`;
      } finally {
        importInput.value = "";
      }
    });

    Promise.all([collection("missions"), collection("vehicles")])
      .then(([missionRecords, vehicleRecords]) => {
        missions = missionRecords.slice().sort((a, b) => {
          const aNumber = Number(a.id);
          const bNumber = Number(b.id);
          if (Number.isFinite(aNumber) && Number.isFinite(bNumber)) return aNumber - bNumber;
          return String(a.id).localeCompare(String(b.id));
        });
        missionById = new Map(missions.map((mission) => [String(mission.id), mission]));
        vehicleById = new Map(vehicleRecords.map((vehicle) => [String(vehicle.id), vehicle]));
        missionSelect.innerHTML = missions.map((mission) => `<option value="${escapeHtml(mission.id)}">${escapeHtml(mission.name)} (#${escapeHtml(mission.id)})</option>`).join("");
        renderSavedOptions();
        renderAll();
      })
      .catch((error) => {
        scenarioRoot.innerHTML = `<p class="mcuk-tool-error">${escapeHtml(error.message)}</p>`;
        inventoryRoot.innerHTML = "";
        resultsRoot.innerHTML = "";
      });
  }

  function initAll() {
    initAccountReadiness();
  }

  if (typeof document$ !== "undefined") {
    document$.subscribe(initAll);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initAll, { once: true });
  } else {
    initAll();
  }
})();
