(() => {
  "use strict";

  const script = document.currentScript;
  const siteRoot = script && script.src
    ? script.src.replace(/javascripts\/official-mission-details\.js(?:\?.*)?$/, "")
    : `${window.location.origin}/MissionChief-UK/`;
  const catalogueUrl = new URL("assets/data/official/uk-missions.json", siteRoot);
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

  const addDetails = async (card) => {
    if (card.dataset.mcukOfficialDetails === "true") return;
    card.dataset.mcukOfficialDetails = "true";

    const missionId = missionIdFromCard(card);
    if (!missionId) return;

    try {
      const records = await loadRecords();
      const record = records.get(missionId);
      if (!record) return;

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
      card.append(details);
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
