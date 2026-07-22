(() => {
  "use strict";

  const script = document.currentScript;
  const siteRoot = script && script.src
    ? script.src.replace(/javascripts\/intelligence-tools\.js(?:\?.*)?$/, "")
    : `${window.location.origin}/MissionChief-UK/`;
  const apiRoot = new URL("assets/data/v1/", siteRoot);
  const officialDataRoot = new URL("assets/data/official/", siteRoot);
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

  const displayValue = (value) => {
    if (value === null || value === undefined || value === "") return "Not published";
    if (typeof value === "object") return JSON.stringify(value);
    return String(value);
  };

  async function collection(name) {
    if (!cache.has(name)) {
      cache.set(name, fetch(new URL(`${name}.json`, apiRoot), { cache: "no-cache" })
        .then((response) => {
          if (!response.ok) throw new Error(`Unable to load ${name} data (${response.status})`);
          return response.json();
        })
        .then((payload) => payload.records || []));
    }
    return cache.get(name);
  }

  async function officialCatalogue() {
    const cacheKey = "official-uk-missions";
    if (!cache.has(cacheKey)) {
      cache.set(cacheKey, fetch(new URL("uk-missions.json", officialDataRoot), { cache: "no-cache" })
        .then((response) => {
          if (response.status === 404) return { records: [], count: 0, source: null };
          if (!response.ok) throw new Error(`Unable to load official UK mission catalogue (${response.status})`);
          return response.json();
        })
        .then((payload) => ({
          records: Array.isArray(payload.records) ? payload.records : [],
          count: Number(payload.count) || 0,
          source: payload.source || null
        })));
    }
    return cache.get(cacheKey);
  }

  function claimRoot(selector) {
    const root = document.querySelector(selector);
    if (!root || root.dataset.mcukReady === "true") return null;
    root.dataset.mcukReady = "true";
    return root;
  }

  function requirementRows(mission) {
    const requirements = mission.requirements || {};
    const rows = [];
    for (const item of requirements.guaranteed || []) {
      rows.push({ type: "Guaranteed", resource: item.resource, quantity: item.quantity });
    }
    for (const item of requirements.probabilistic || []) {
      rows.push({ type: `${Math.round(item.probability * 100)}% probability`, resource: item.resource, quantity: item.quantity });
    }
    for (const item of requirements.conditional || []) {
      const probability = typeof item.probability === "number" ? ` · ${Math.round(item.probability * 100)}%` : "";
      rows.push({ type: `${label(item.condition)}${probability}`, resource: item.resource, quantity: item.quantity });
    }
    for (const item of requirements.alternatives || []) {
      rows.push({ type: "Alternative group", resource: item.resources.map(label).join(" OR "), quantity: item.quantity });
    }
    return rows;
  }

  function missionCard(mission, officialRecord = null) {
    const rows = requirementRows(mission);
    const resourceTable = rows.length
      ? `<table><thead><tr><th>Requirement</th><th>Resource</th><th>Qty</th></tr></thead><tbody>${rows.map((row) => `<tr><td>${escapeHtml(row.type)}</td><td>${escapeHtml(label(row.resource))}</td><td>${escapeHtml(row.quantity)}</td></tr>`).join("")}</tbody></table>`
      : "<p><em>No dispatch-level resources are published for this evidence state.</em></p>";
    const preconditions = Object.entries(mission.preconditions || {}).filter(([, value]) => value && (!Array.isArray(value) || value.length));
    const patient = mission.patients
      ? `<p><strong>Patients:</strong> ${escapeHtml(mission.patients.minimum ?? 0)}–${escapeHtml(mission.patients.maximum ?? 0)}</p>`
      : "";
    const officialLink = officialRecord?.official_url
      ? `<a class="mcuk-catalogue-link" href="${escapeHtml(officialRecord.official_url)}" target="_blank" rel="noopener">Open official mission page ↗</a>`
      : "";
    return `<article class="mcuk-tool-card mcuk-mission-card mcuk-mission-card--canonical">
      <div class="mcuk-catalogue-badges"><span class="mcuk-catalogue-badge mcuk-catalogue-badge--canonical">Canonical mapped</span>${officialRecord ? '<span class="mcuk-catalogue-badge">Official ID matched</span>' : ""}</div>
      <h3>${escapeHtml(mission.name)} <small>#${escapeHtml(mission.id)}</small></h3>
      <p><strong>Service:</strong> ${escapeHtml(label(mission.service))}</p>
      <p><strong>Average credits:</strong> ${escapeHtml(mission.reward?.average_credits ?? "Not published")}</p>
      ${patient}
      ${preconditions.length ? `<details><summary>Generation preconditions</summary><ul>${preconditions.map(([key, value]) => `<li>${escapeHtml(label(key))}: ${escapeHtml(Array.isArray(value) ? value.join(", ") : value)}</li>`).join("")}</ul></details>` : ""}
      ${resourceTable}
      <p class="mcuk-evidence-note">Evidence status: ${escapeHtml(label(mission.verification?.status || "unknown"))}; checked ${escapeHtml(mission.verification?.checked_at || "unknown")}.</p>
      ${officialLink}
    </article>`;
  }

  function officialRequirementTable(mission) {
    const requirements = mission.requirements && typeof mission.requirements === "object" ? mission.requirements : {};
    const chances = mission.chances && typeof mission.chances === "object" ? mission.chances : {};
    const keys = [...new Set([...Object.keys(requirements), ...Object.keys(chances)])].sort();
    if (!keys.length) return "<p><em>The official catalogue does not publish requirement keys for this mission.</em></p>";
    return `<table><thead><tr><th>Official requirement key</th><th>Published value</th><th>Chance field</th></tr></thead><tbody>${keys.map((key) => `<tr><td><code>${escapeHtml(key)}</code></td><td>${escapeHtml(displayValue(requirements[key]))}</td><td>${escapeHtml(displayValue(chances[key]))}</td></tr>`).join("")}</tbody></table>`;
  }

  function officialMissionCard(mission) {
    const places = Array.isArray(mission.place_array) && mission.place_array.length
      ? mission.place_array
      : mission.place ? [mission.place] : [];
    const prerequisites = mission.prerequisites && typeof mission.prerequisites === "object"
      ? Object.entries(mission.prerequisites)
      : [];
    const availability = mission.availability || {};
    const categories = Array.isArray(mission.mission_categories) ? mission.mission_categories : [];
    const availabilityText = mission.limited_availability
      ? `<p><strong>Availability:</strong> ${escapeHtml(availability.starts_at || "Unspecified start")} → ${escapeHtml(availability.ends_at || "Unspecified end")}</p>`
      : "";
    return `<article class="mcuk-tool-card mcuk-mission-card mcuk-mission-card--official">
      <div class="mcuk-catalogue-badges"><span class="mcuk-catalogue-badge mcuk-catalogue-badge--official">Official UK catalogue</span><span class="mcuk-catalogue-badge mcuk-catalogue-badge--pending">Canonical mapping pending</span></div>
      <h3>${escapeHtml(mission.name)} <small>#${escapeHtml(mission.id)}</small></h3>
      <p><strong>Generated by:</strong> ${escapeHtml(label(mission.generated_by || "Not published"))}</p>
      <p><strong>Average credits:</strong> ${escapeHtml(mission.average_credits ?? "Not published")}</p>
      ${places.length ? `<p><strong>POI:</strong> ${escapeHtml(places.join(", "))}</p>` : ""}
      ${categories.length ? `<p><strong>Mission categories:</strong> ${escapeHtml(categories.map(label).join(", "))}</p>` : ""}
      ${availabilityText}
      ${prerequisites.length ? `<details><summary>Official generation prerequisites</summary><ul>${prerequisites.map(([key, value]) => `<li><code>${escapeHtml(key)}</code>: ${escapeHtml(displayValue(value))}</li>`).join("")}</ul></details>` : ""}
      ${officialRequirementTable(mission)}
      <p class="mcuk-evidence-note">This is a current official catalogue record. Requirement keys are displayed verbatim and have not been guessed into canonical vehicle resources.</p>
      <a class="mcuk-catalogue-link" href="${escapeHtml(mission.official_url)}" target="_blank" rel="noopener">Open official mission page ↗</a>
    </article>`;
  }

  function missionSearchText(mission) {
    const values = [
      mission.id,
      mission.name,
      mission.generated_by,
      mission.place,
      ...(mission.aliases || []),
      ...(mission.poi || []),
      ...(mission.place_array || []),
      ...(mission.mission_types || []),
      ...(mission.mission_categories || []),
      ...Object.keys(mission.requirements || {}),
      ...Object.keys(mission.prerequisites || {})
    ];
    return values.filter((value) => value !== null && value !== undefined).join(" ").toLowerCase();
  }

  async function initMissionLookup() {
    const root = claimRoot("[data-mcuk-tool='mission-lookup']");
    if (!root) return;
    const input = root.querySelector("[data-role='query']");
    const service = root.querySelector("[data-role='service']");
    const sourceFilter = root.querySelector("[data-role='source']");
    const summary = root.querySelector("[data-role='summary']");
    const results = root.querySelector("[data-role='results']");
    try {
      const [canonicalMissions, officialPayload] = await Promise.all([collection("missions"), officialCatalogue()]);
      const officialMissions = officialPayload.records;
      const officialById = new Map(officialMissions.map((mission) => [String(mission.id), mission]));
      const canonicalIds = new Set(canonicalMissions.map((mission) => String(mission.id)));
      const entries = [
        ...canonicalMissions.map((mission) => ({
          kind: "canonical",
          mission,
          official: officialById.get(String(mission.id)) || null,
          category: mission.service || "canonical",
          searchText: missionSearchText(mission)
        })),
        ...officialMissions
          .filter((mission) => !canonicalIds.has(String(mission.id)))
          .map((mission) => ({
            kind: "official",
            mission,
            official: mission,
            category: mission.generated_by || mission.additional?.filter_id || "official catalogue",
            searchText: missionSearchText(mission)
          }))
      ];
      entries.sort((a, b) => {
        const aNumber = Number(a.mission.id);
        const bNumber = Number(b.mission.id);
        if (Number.isFinite(aNumber) && Number.isFinite(bNumber)) return aNumber - bNumber;
        return String(a.mission.id).localeCompare(String(b.mission.id));
      });

      const categories = [...new Set(entries.map((entry) => entry.category).filter(Boolean))]
        .sort((a, b) => label(a).localeCompare(label(b)));
      service.innerHTML = `<option value="">All services and generators</option>${categories.map((item) => `<option value="${escapeHtml(item)}">${escapeHtml(label(item))}</option>`).join("")}`;

      const render = () => {
        const query = input.value.trim().toLowerCase();
        const selectedService = service.value;
        const selectedSource = sourceFilter?.value || "";
        const filtered = entries.filter((entry) => {
          return (!query || entry.searchText.includes(query))
            && (!selectedService || entry.category === selectedService)
            && (!selectedSource || entry.kind === selectedSource);
        });
        const visible = filtered.slice(0, 100);
        if (summary) {
          const mappedCount = canonicalMissions.length;
          const officialOnlyCount = Math.max(0, officialMissions.length - [...canonicalIds].filter((id) => officialById.has(id)).length);
          summary.innerHTML = `<strong>${escapeHtml(filtered.length)}</strong> matching mission${filtered.length === 1 ? "" : "s"}; showing ${escapeHtml(visible.length)}. Catalogue coverage: <strong>${escapeHtml(mappedCount)}</strong> canonical mapped and <strong>${escapeHtml(officialOnlyCount)}</strong> official records awaiting full mapping.`;
        }
        results.innerHTML = visible.length
          ? visible.map((entry) => entry.kind === "canonical" ? missionCard(entry.mission, entry.official) : officialMissionCard(entry.mission)).join("")
          : "<p>No matching UK mission records.</p>";
      };
      input.addEventListener("input", render);
      service.addEventListener("change", render);
      sourceFilter?.addEventListener("change", render);
      render();
    } catch (error) {
      results.innerHTML = `<p class="mcuk-tool-error">${escapeHtml(error.message)}</p>`;
    }
  }

  async function initComparison() {
    const root = claimRoot("[data-mcuk-tool='comparison']");
    if (!root) return;
    const kind = root.querySelector("[data-role='kind']");
    const first = root.querySelector("[data-role='first']");
    const second = root.querySelector("[data-role='second']");
    const results = root.querySelector("[data-role='results']");
    let records = [];
    const render = () => {
      const selected = [first.value, second.value].map((id) => records.find((record) => String(record.id) === String(id))).filter(Boolean);
      const fields = kind.value === "vehicles"
        ? ["service", "category", "cost", "staffing", "training", "building_requirements", "capabilities"]
        : ["service", "qualification_type", "roles", "course_name", "duration_hours", "prerequisites"];
      results.innerHTML = selected.length === 2 ? `<table><thead><tr><th>Field</th>${selected.map((record) => `<th>${escapeHtml(record.name)}</th>`).join("")}</tr></thead><tbody>${fields.map((field) => `<tr><th>${escapeHtml(label(field))}</th>${selected.map((record) => `<td><pre>${escapeHtml(typeof record[field] === "object" ? JSON.stringify(record[field], null, 2) : record[field] ?? "Not verified")}</pre></td>`).join("")}</tr>`).join("")}</tbody></table>` : "";
    };
    const loadOptions = async () => {
      records = await collection(kind.value);
      const options = records.map((record) => `<option value="${escapeHtml(record.id)}">${escapeHtml(record.name)} (${escapeHtml(record.id)})</option>`).join("");
      first.innerHTML = options;
      second.innerHTML = options;
      if (second.options.length > 1) second.selectedIndex = 1;
      render();
    };
    kind.addEventListener("change", () => loadOptions().catch((error) => { results.textContent = error.message; }));
    first.addEventListener("change", render);
    second.addEventListener("change", render);
    try { await loadOptions(); } catch (error) { results.textContent = error.message; }
  }

  async function initPlanner() {
    const root = claimRoot("[data-mcuk-tool='fleet-planner']");
    if (!root) return;
    const missionSelect = root.querySelector("[data-role='mission']");
    const concurrency = root.querySelector("[data-role='concurrency']");
    const results = root.querySelector("[data-role='results']");
    try {
      const missions = await collection("missions");
      missionSelect.innerHTML = missions.map((mission) => `<option value="${escapeHtml(mission.id)}">${escapeHtml(mission.name)} (#${escapeHtml(mission.id)})</option>`).join("");
      const render = () => {
        const mission = missions.find((item) => String(item.id) === String(missionSelect.value));
        if (!mission) return;
        const multiplier = Math.max(1, Number.parseInt(concurrency.value, 10) || 1);
        const guaranteed = (mission.requirements?.guaranteed || []).map((item) => `<tr><td>${escapeHtml(label(item.resource))}</td><td>${escapeHtml(item.quantity)}</td><td>${escapeHtml(item.quantity * multiplier)}</td></tr>`).join("");
        const alternatives = (mission.requirements?.alternatives || []).map((item) => `<li>${escapeHtml(item.quantity * multiplier)} total from: ${escapeHtml(item.resources.map(label).join(" OR "))}</li>`).join("");
        results.innerHTML = `<h3>${escapeHtml(mission.name)}</h3><table><thead><tr><th>Guaranteed resource</th><th>One mission</th><th>${multiplier} concurrent</th></tr></thead><tbody>${guaranteed || "<tr><td colspan='3'>No guaranteed resources published.</td></tr>"}</tbody></table>${alternatives ? `<h4>Alternative groups</h4><ul>${alternatives}</ul>` : ""}<p class="mcuk-evidence-note">This multiplies published requirements; it does not model travel time, cover, staffing availability or overlapping alternative allocation.</p>`;
      };
      missionSelect.addEventListener("change", render);
      concurrency.addEventListener("input", render);
      render();
    } catch (error) { results.textContent = error.message; }
  }

  async function initQueryCatalogue() {
    const root = claimRoot("[data-mcuk-tool='query-catalogue']");
    if (!root) return;
    const input = root.querySelector("[data-role='query']");
    const results = root.querySelector("[data-role='results']");
    try {
      const index = await collection("search-index");
      const render = () => {
        const tokens = input.value.toLowerCase().match(/[a-z0-9]+/g) || [];
        if (!tokens.length) { results.innerHTML = "<p>Enter a question or keywords.</p>"; return; }
        const ranked = index.map((item) => ({ item, score: tokens.reduce((sum, token) => sum + (item.search_text.includes(token) ? 1 : 0), 0) }))
          .filter(({ score }) => score > 0)
          .sort((a, b) => b.score - a.score || String(a.item.name).localeCompare(String(b.item.name)))
          .slice(0, 30);
        results.innerHTML = ranked.length ? `<ol>${ranked.map(({ item, score }) => `<li><strong>${escapeHtml(item.name)}</strong> <code>${escapeHtml(item.collection)}</code> — score ${score}</li>`).join("")}</ol>` : "<p>No evidence-backed matches.</p>";
      };
      input.addEventListener("input", render);
      render();
    } catch (error) { results.textContent = error.message; }
  }

  function initAll() {
    initMissionLookup();
    initComparison();
    initPlanner();
    initQueryCatalogue();
  }

  if (typeof document$ !== "undefined") {
    document$.subscribe(initAll);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initAll, { once: true });
  } else {
    initAll();
  }
})();
