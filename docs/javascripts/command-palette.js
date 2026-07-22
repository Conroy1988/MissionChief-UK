(() => {
  "use strict";

  const script = document.currentScript;
  const siteRoot = script && script.src
    ? script.src.replace(/javascripts\/command-palette\.js(?:\?.*)?$/, "")
    : `${window.location.origin}/MissionChief-UK/`;
  const indexUrl = new URL("assets/data/v1/search-index.json", siteRoot);
  let indexPromise;
  let lastFocused;

  const collectionLabels = {
    missions: "Missions",
    vehicles: "Resources",
    infrastructure: "Infrastructure",
    training: "Qualifications",
  };

  const collectionCodes = {
    missions: "MIS",
    vehicles: "RES",
    infrastructure: "INF",
    training: "QLF",
  };

  const escapeHtml = (value) => String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");

  const resultHref = (item) => {
    const query = encodeURIComponent(item.name || item.id || "");
    if (item.collection === "missions") {
      return new URL(`tools/mission-lookup/?q=${query}`, siteRoot).href;
    }
    return new URL(`tools/query-catalogue/?q=${query}`, siteRoot).href;
  };

  const loadIndex = () => {
    if (!indexPromise) {
      indexPromise = fetch(indexUrl, { cache: "no-cache" })
        .then((response) => {
          if (!response.ok) throw new Error(`Search index request failed (${response.status})`);
          return response.json();
        })
        .then((payload) => payload.records || []);
    }
    return indexPromise;
  };

  function createPalette() {
    if (document.querySelector("[data-mcuk-palette]")) return;

    const palette = document.createElement("div");
    palette.className = "mcuk-palette";
    palette.dataset.mcukPalette = "";
    palette.dataset.open = "false";
    palette.innerHTML = `
      <section class="mcuk-palette__dialog" role="dialog" aria-modal="true" aria-labelledby="mcuk-palette-title">
        <div class="mcuk-palette__search">
          <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"></circle><path d="m20 20-3.5-3.5"></path></svg>
          <input id="mcuk-palette-title" type="search" autocomplete="off" spellcheck="false" placeholder="Search missions, resources, buildings or qualifications…" aria-label="Search verified MissionChief UK data">
          <button class="mcuk-palette__close" type="button" aria-label="Close command palette">ESC</button>
        </div>
        <div class="mcuk-palette__filters" role="group" aria-label="Filter command results">
          <button class="mcuk-palette__filter" type="button" data-filter="all" aria-pressed="true">All</button>
          <button class="mcuk-palette__filter" type="button" data-filter="missions" aria-pressed="false">Missions</button>
          <button class="mcuk-palette__filter" type="button" data-filter="vehicles" aria-pressed="false">Resources</button>
          <button class="mcuk-palette__filter" type="button" data-filter="infrastructure" aria-pressed="false">Infrastructure</button>
          <button class="mcuk-palette__filter" type="button" data-filter="training" aria-pressed="false">Qualifications</button>
        </div>
        <div class="mcuk-palette__status"><span data-palette-status>Loading verified index…</span><strong>Read-only intelligence</strong></div>
        <div class="mcuk-palette__results" role="listbox" aria-label="Verified data results" data-palette-results></div>
        <div class="mcuk-palette__footer"><span><kbd>↑</kbd><kbd>↓</kbd> move</span><span><kbd>Enter</kbd> open</span><span><kbd>Esc</kbd> close</span><span><kbd>Ctrl</kbd><kbd>K</kbd> toggle</span></div>
      </section>`;
    document.body.appendChild(palette);

    const launcher = document.createElement("button");
    launcher.className = "mcuk-command-launcher";
    launcher.type = "button";
    launcher.dataset.mcukPaletteOpen = "";
    launcher.setAttribute("aria-label", "Open MissionChief UK command palette");
    launcher.innerHTML = `<span>Search command data</span><kbd>${navigator.platform.includes("Mac") ? "⌘K" : "Ctrl K"}</kbd>`;

    const headerSource = document.querySelector(".md-header__source");
    if (headerSource) headerSource.before(launcher);
    else document.querySelector(".md-header__inner")?.appendChild(launcher);
  }

  function initPalette() {
    createPalette();
    const palette = document.querySelector("[data-mcuk-palette]");
    if (!palette || palette.dataset.ready === "true") return;
    palette.dataset.ready = "true";

    const input = palette.querySelector("input");
    const results = palette.querySelector("[data-palette-results]");
    const status = palette.querySelector("[data-palette-status]");
    const filters = [...palette.querySelectorAll("[data-filter]")];
    let records = [];
    let activeFilter = "all";
    let activeIndex = 0;

    const visibleResults = () => [...results.querySelectorAll(".mcuk-palette__result")];

    const setActive = (index) => {
      const items = visibleResults();
      if (!items.length) return;
      activeIndex = (index + items.length) % items.length;
      items.forEach((item, itemIndex) => {
        item.dataset.active = String(itemIndex === activeIndex);
        item.setAttribute("aria-selected", String(itemIndex === activeIndex));
      });
      items[activeIndex].scrollIntoView({ block: "nearest" });
    };

    const render = () => {
      const query = input.value.trim().toLowerCase();
      const tokens = query.match(/[a-z0-9]+/g) || [];
      const ranked = records
        .filter((item) => activeFilter === "all" || item.collection === activeFilter)
        .map((item) => {
          const haystack = `${item.name || ""} ${item.id || ""} ${item.service || ""} ${item.search_text || ""}`.toLowerCase();
          const score = tokens.length
            ? tokens.reduce((sum, token) => sum + (haystack.includes(token) ? 1 : 0), 0)
            : 1;
          const exactBoost = query && String(item.name || "").toLowerCase().startsWith(query) ? 3 : 0;
          return { item, score: score + exactBoost };
        })
        .filter(({ score }) => score > 0)
        .sort((a, b) => b.score - a.score || String(a.item.name).localeCompare(String(b.item.name)))
        .slice(0, 12);

      status.textContent = ranked.length
        ? `${ranked.length} result${ranked.length === 1 ? "" : "s"} shown from ${records.length} canonical records`
        : `No verified matches in ${activeFilter === "all" ? "the full estate" : collectionLabels[activeFilter]}`;

      if (!ranked.length) {
        results.innerHTML = `<div class="mcuk-palette__empty"><strong>No verified match</strong><span>Try a mission name, vehicle alias, service or qualification.</span></div>`;
        return;
      }

      results.innerHTML = ranked.map(({ item }, index) => `
        <a class="mcuk-palette__result" role="option" aria-selected="${index === 0}" data-active="${index === 0}" data-collection="${escapeHtml(item.collection)}" href="${escapeHtml(resultHref(item))}">
          <span class="mcuk-palette__badge">${escapeHtml(collectionCodes[item.collection] || "UK")}</span>
          <span class="mcuk-palette__copy"><strong>${escapeHtml(item.name || item.id)}</strong><span>${escapeHtml(collectionLabels[item.collection] || item.collection)} · ${escapeHtml(item.service || "Cross-service")} · ${escapeHtml(item.id || "No ID")}</span></span>
          <span class="mcuk-palette__arrow">→</span>
        </a>`).join("");
      activeIndex = 0;
    };

    const open = async () => {
      if (palette.dataset.open === "true") return;
      lastFocused = document.activeElement;
      palette.dataset.open = "true";
      document.body.classList.add("mcuk-palette-open");
      input.value = "";
      input.focus();
      if (!records.length) {
        try {
          records = await loadIndex();
          render();
        } catch (error) {
          status.textContent = "Verified search index unavailable";
          results.innerHTML = `<div class="mcuk-palette__empty"><strong>Command data unavailable</strong><span>${escapeHtml(error.message)}</span></div>`;
        }
      } else {
        render();
      }
    };

    const close = () => {
      palette.dataset.open = "false";
      document.body.classList.remove("mcuk-palette-open");
      if (lastFocused && typeof lastFocused.focus === "function") lastFocused.focus();
    };

    document.querySelectorAll("[data-mcuk-palette-open]").forEach((button) => button.addEventListener("click", open));
    palette.querySelector(".mcuk-palette__close").addEventListener("click", close);
    palette.addEventListener("click", (event) => { if (event.target === palette) close(); });
    input.addEventListener("input", render);

    filters.forEach((filter) => filter.addEventListener("click", () => {
      activeFilter = filter.dataset.filter;
      filters.forEach((item) => item.setAttribute("aria-pressed", String(item === filter)));
      render();
      input.focus();
    }));

    palette.addEventListener("keydown", (event) => {
      if (event.key === "Escape") { event.preventDefault(); close(); return; }
      if (event.key === "ArrowDown") { event.preventDefault(); setActive(activeIndex + 1); return; }
      if (event.key === "ArrowUp") { event.preventDefault(); setActive(activeIndex - 1); return; }
      if (event.key === "Enter" && event.target === input) {
        const item = visibleResults()[activeIndex];
        if (item) { event.preventDefault(); item.click(); }
      }
    });

    document.addEventListener("keydown", (event) => {
      const editable = event.target instanceof HTMLInputElement || event.target instanceof HTMLTextAreaElement || event.target?.isContentEditable;
      const shortcut = (event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "k";
      const slash = event.key === "/" && !editable && !event.ctrlKey && !event.metaKey && !event.altKey;
      if (!shortcut && !slash) return;
      event.preventDefault();
      if (palette.dataset.open === "true") close(); else open();
    });
  }

  if (typeof document$ !== "undefined") document$.subscribe(initPalette);
  else if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", initPalette, { once: true });
  else initPalette();
})();