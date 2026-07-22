(() => {
  "use strict";

  const script = document.currentScript;
  const siteRoot = script && script.src
    ? script.src.replace(/javascripts\/official-mission-details\.js(?:\?.*)?$/, "")
    : `${window.location.origin}/MissionChief-UK/`;
  const catalogueUrl = new URL("assets/data/official/uk-missions.json", siteRoot);
  const CORE_FIELDS = new Set([
    "id",
    "name",
    "place",
    "place_array",
    "average_credits",
    "generated_by",
    "icons",
    "requirements",
    "chances",
    "additional",
    "prerequisites",
    "mission_categories",
    "official_url",
    "limited_availability",
    "availability"
  ]);
  let recordsPromise = null;

  const loadRecords = () => {
    if (!recordsPromise) {
      recordsPromise = fetch(catalogueUrl, { cache: "no-cache" })
        .then((response) => {
          if (!response.ok) throw new Error(`Unable to load official mission details (${response.status})`);
          return response.json();
        })
        .then((payload) => new Map((payload.records || []).map((record) => [String(record.id), record])));
    }
    return recordsPromise;
  };

  const missionIdFromCard = (card) => {
    const idText = card.querySelector("h3 small")?.textContent?.trim() || "";
    return idText.replace(/^#/, "");
  };

  const displayValue = (value) => {
    if (value === null) return "null";
    if (value === undefined) return "Not published";
    if (typeof value === "object") return JSON.stringify(value);
    return String(value);
  };

  const additionalEntries = (record) => {
    const entries = [];
    const additional = record.additional;
    if (additional && typeof additional === "object" && !Array.isArray(additional)) {
      Object.entries(additional).forEach(([key, value]) => {
        entries.push([`additional.${key}`, value]);
      });
    }
    Object.entries(record).forEach(([key, value]) => {
      if (!CORE_FIELDS.has(key)) entries.push([key, value]);
    });
    return entries
      .filter(([, value]) => value !== undefined)
      .sort(([left], [right]) => left.localeCompare(right));
  };

  const createAdditionalDetails = (record) => {
    const entries = additionalEntries(record);
    if (!entries.length) return null;

    const details = document.createElement("details");
    details.className = "mcuk-official-field-details";
    const summary = document.createElement("summary");
    summary.textContent = "Patients, personnel, variants and additional fields";
    const table = document.createElement("table");
    const thead = document.createElement("thead");
    thead.innerHTML = "<tr><th>Official field</th><th>Published value</th></tr>";
    const tbody = document.createElement("tbody");

    entries.forEach(([key, value]) => {
      const row = document.createElement("tr");
      const fieldCell = document.createElement("td");
      const code = document.createElement("code");
      code.textContent = key;
      fieldCell.append(code);
      const valueCell = document.createElement("td");
      valueCell.textContent = displayValue(value);
      row.append(fieldCell, valueCell);
      tbody.append(row);
    });

    table.append(thead, tbody);
    details.append(summary, table);
    return details;
  };

  const createCompleteRecordDetails = (record) => {
    const details = document.createElement("details");
    details.className = "mcuk-official-record-details";
    const summary = document.createElement("summary");
    summary.textContent = "Complete official catalogue record";
    const pre = document.createElement("pre");
    pre.textContent = "Open to load every official field…";
    details.append(summary, pre);
    details.addEventListener("toggle", () => {
      if (details.open && details.dataset.loaded !== "true") {
        pre.textContent = JSON.stringify(record, null, 2);
        details.dataset.loaded = "true";
      }
    });
    return details;
  };

  const addDetails = async (card) => {
    if (card.dataset.mcukOfficialDetails === "true") return;
    card.dataset.mcukOfficialDetails = "true";

    const missionId = missionIdFromCard(card);
    if (!missionId) return;

    try {
      const records = await loadRecords();
      const record = records.get(missionId);
      if (!record) return;

      const additional = createAdditionalDetails(record);
      if (additional) card.append(additional);
      card.append(createCompleteRecordDetails(record));
    } catch (error) {
      card.dataset.mcukOfficialDetails = "error";
    }
  };

  const enhance = (root) => {
    root.querySelectorAll("article.mcuk-mission-card").forEach((card) => addDetails(card));
  };

  const init = () => {
    const root = document.querySelector("[data-mcuk-tool='mission-lookup']");
    const results = root?.querySelector("[data-role='results']");
    if (!results || results.dataset.mcukOfficialObserver === "true") return;
    results.dataset.mcukOfficialObserver = "true";
    enhance(results);
    const observer = new MutationObserver(() => enhance(results));
    observer.observe(results, { childList: true, subtree: true });
  };

  if (typeof document$ !== "undefined") {
    document$.subscribe(init);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init, { once: true });
  } else {
    init();
  }
})();
