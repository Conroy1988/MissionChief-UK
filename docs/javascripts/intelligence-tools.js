(() => {
  "use strict";

  const script = document.currentScript;
  const siteRoot = script && script.src
    ? script.src.replace(/javascripts\/intelligence-tools\.js(?:\?.*)?$/, "")
    : `${window.location.origin}/MissionChief-UK/`;
  const apiRoot = new URL("assets/data/v1/", siteRoot);
  const cache = new Map();

  const escapeHtml = (value) => String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");

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

  const label = (value) => String(value || "")
    .replaceAll("_", " ")
    .replace(/\b\w/g, (character) => character.toUpperCase());

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

  function missionCard(mission) {
    const rows = requirementRows(mission);
    const resourceTable = rows.length
      ? `<table><thead><tr><th>Requirement</th><th>Resource</th><th>Qty</th></tr></thead><tbody>${rows.map((row) => `<tr><td>${escapeHtml(row.type)}</td><td>${escapeHtml(label(row.resource))}</td><td>${escapeHtml(row.quantity)}</td></tr>`).join("")}</tbody></table>`
      : "<p><em>No dispatch-level resources are published for this evidence state.</em></p>";
    const preconditions = Object.entries(mission.preconditions || {}).filter(([, value]) => value && (!Array.isArray(value) || value.length));
    const patient = mission.patients
      ? `<p><strong>Patients:</strong> ${escapeHtml(mission.patients.minimum ?? 0)}–${escapeHtml(mission.patients.maximum ?? 0)}</p>`
      : "";
    return `<article class="mcuk-tool-card">
      <h3>${escapeHtml(mission.name)} <small>#${escapeHtml(mission.id)}</small></h3>
      <p><strong>Service:</strong> ${escapeHtml(label(mission.service))}</p>
      <p><strong>Average credits:</strong> ${escapeHtml(mission.reward?.average_credits ?? "Not published")}</p>
      ${patient}
      ${preconditions.length ? `<details><summary>Generation preconditions</summary><ul>${preconditions.map(([key, value]) => `<li>${escapeHtml(label(key))}: ${escapeHtml(Array.isArray(value) ? value.join(", ") : value)}</li>`).join("")}</ul></details>` : ""}
      ${resourceTable}
      <p class="mcuk-evidence-note">Evidence status: ${escapeHtml(label(mission.verification?.status || "unknown"))}; checked ${escapeHtml(mission.verification?.checked_at || "unknown")}.</p>
    </article>`;
  }

  async function initMissionLookup() {
    const root = document.querySelector("[data-mcuk-tool='mission-lookup']");
    if (!root) return;
    const input = root.querySelector("[data-role='query']");
    const service = root.querySelector("[data-role='service']");
    const results = root.querySelector("[data-role='results']");
    try {
      const missions = await collection("missions");
      const services = [...new Set(missions.map((mission) => mission.service).filter(Boolean))].sort();
      service.innerHTML = `<option value="">All services</option>${services.map((item) => `<option value="${escapeHtml(item)}">${escapeHtml(label(item))}</option>`).join("")}`;
      const render = () => {
        const query = input.value.trim().toLowerCase();
        const selectedService = service.value;
        const filtered = missions.filter((mission) => {
          const haystack = [mission.id, mission.name, ...(mission.aliases || []), ...(mission.poi || []), ...(mission.mission_types || [])].join(" ").toLowerCase();
          return (!query || haystack.includes(query)) && (!selectedService || mission.service === selectedService);
        }).slice(0, 50);
        results.innerHTML = filtered.length ? filtered.map(missionCard).join("") : "<p>No matching verified records.</p>";
      };
      input.addEventListener("input", render);
      service.addEventListener("change", render);
      render();
    } catch (error) {
      results.innerHTML = `<p class="mcuk-tool-error">${escapeHtml(error.message)}</p>`;
    }
  }

  async function initComparison() {
    const root = document.querySelector("[data-mcuk-tool='comparison']");
    if (!root) return;
    const kind = root.querySelector("[data-role='kind']");
    const first = root.querySelector("[data-role='first']");
    const second = root.querySelector("[data-role='second']");
    const results = root.querySelector("[data-role='results']");
    const loadOptions = async () => {
      const records = await collection(kind.value);
      const options = records.map((record) => `<option value="${escapeHtml(record.id)}">${escapeHtml(record.name)} (${escapeHtml(record.id)})</option>`).join("");
      first.innerHTML = options;
      second.innerHTML = options;
      if (second.options.length > 1) second.selectedIndex = 1;
      render(records);
    };
    const render = (records) => {
      const selected = [first.value, second.value].map((id) => records.find((record) => String(record.id) === String(id))).filter(Boolean);
      const fields = kind.value === "vehicles"
        ? ["service", "category", "cost", "staffing", "training", "building_requirements", "capabilities"]
        : ["service", "qualification_type", "roles", "course_name", "duration_hours", "prerequisites"];
      results.innerHTML = selected.length === 2 ? `<table><thead><tr><th>Field</th>${selected.map((record) => `<th>${escapeHtml(record.name)}</th>`).join("")}</tr></thead><tbody>${fields.map((field) => `<tr><th>${escapeHtml(label(field))}</th>${selected.map((record) => `<td><pre>${escapeHtml(typeof record[field] === "object" ? JSON.stringify(record[field], null, 2) : record[field] ?? "Not verified")}</pre></td>`).join("")}</tr>`).join("")}</tbody></table>` : "";
    };
    let records = [];
    kind.addEventListener("change", async () => { records = await collection(kind.value); await loadOptions(); });
    first.addEventListener("change", () => render(records));
    second.addEventListener("change", () => render(records));
    try { records = await collection(kind.value); await loadOptions(); } catch (error) { results.textContent = error.message; }
  }

  async function initPlanner() {
    const root = document.querySelector("[data-mcuk-tool='fleet-planner']");
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
    const root = document.querySelector("[data-mcuk-tool='query-catalogue']");
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

  document.addEventListener("DOMContentLoaded", () => {
    initMissionLookup();
    initComparison();
    initPlanner();
    initQueryCatalogue();
  });
})();
