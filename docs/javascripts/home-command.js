(() => {
  "use strict";

  const script = document.currentScript;
  const siteRoot = script && script.src
    ? script.src.replace(/javascripts\/home-command\.js(?:\?.*)?$/, "")
    : `${window.location.origin}/MissionChief-UK/`;
  const manifestUrl = new URL("assets/data/v1/manifest.json", siteRoot);
  let manifestPromise;

  const text = (selector, value) => {
    document.querySelectorAll(selector).forEach((node) => {
      node.textContent = String(value);
    });
  };

  const collectionCount = (manifest, name, fallback = 0) => {
    const value = manifest?.collections?.[name]?.count;
    return Number.isFinite(value) ? value : fallback;
  };

  const releaseDate = (value) => {
    if (!value) return "Release date unavailable";
    const parsed = new Date(`${value}T00:00:00Z`);
    if (Number.isNaN(parsed.valueOf())) return `Released ${value}`;
    return `Released ${new Intl.DateTimeFormat("en-GB", {
      day: "numeric",
      month: "long",
      year: "numeric",
      timeZone: "UTC",
    }).format(parsed)}`;
  };

  const loadManifest = () => {
    if (!manifestPromise) {
      manifestPromise = fetch(manifestUrl, { cache: "no-cache" }).then((response) => {
        if (!response.ok) throw new Error(`Manifest request failed (${response.status})`);
        return response.json();
      });
    }
    return manifestPromise;
  };

  async function initHomeCommand() {
    const root = document.querySelector("[data-mcuk-home]");
    if (!root || root.dataset.mcukHomeReady === "true") return;
    root.dataset.mcukHomeReady = "true";

    const state = root.querySelector("[data-mcuk-live-state]");

    try {
      const manifest = await loadManifest();
      const missions = collectionCount(manifest, "missions", 62);
      const vehicles = collectionCount(manifest, "vehicles", 46);
      const infrastructure = collectionCount(manifest, "infrastructure", 18);
      const training = collectionCount(manifest, "training", 11);
      const searchable = Number.isFinite(manifest?.search_index?.count)
        ? manifest.search_index.count
        : missions + vehicles + infrastructure + training;

      text('[data-mcuk-metric="version"]', `v${manifest.data_version || "1.0.0"}`);
      text('[data-mcuk-metric="stage"]', `Stage ${manifest.stage ?? 34}`);
      text('[data-mcuk-metric="missions"]', missions);
      text('[data-mcuk-metric="resources"]', vehicles);
      text('[data-mcuk-metric="api"]', `API ${String(manifest.api_version || "v1").toUpperCase()}`);
      text('[data-mcuk-collection="missions"]', missions);
      text('[data-mcuk-collection="vehicles"]', vehicles);
      text('[data-mcuk-collection="infrastructure"]', infrastructure);
      text('[data-mcuk-collection="training"]', training);
      text("[data-mcuk-search-count]", searchable);
      text("[data-mcuk-status]", manifest.status || "production");
      text("[data-mcuk-release-date]", releaseDate(manifest.released_at));

      if (state) {
        state.dataset.state = "live";
        state.lastChild.textContent = ` Live ${manifest.status || "production"} manifest`;
      }
    } catch (error) {
      if (state) {
        state.dataset.state = "degraded";
        state.lastChild.textContent = " Static production baseline";
        state.title = error.message;
      }
    }
  }

  if (typeof document$ !== "undefined") {
    document$.subscribe(initHomeCommand);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initHomeCommand, { once: true });
  } else {
    initHomeCommand();
  }
})();
