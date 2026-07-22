(() => {
  "use strict";

  const existing = window.MCUKOfficialCatalogue;
  if (existing && typeof existing.load === "function") return;

  const script = document.currentScript;
  const siteRoot = script && script.src
    ? script.src.replace(/javascripts\/official-catalogue-loader\.js(?:\?.*)?$/, "")
    : `${window.location.origin}/MissionChief-UK/`;
  const catalogueUrl = new URL("assets/data/official/uk-missions.json", siteRoot);
  let payloadPromise = null;

  const load = () => {
    if (!payloadPromise) {
      payloadPromise = fetch(catalogueUrl, { cache: "no-cache" })
        .then((response) => {
          if (response.status === 404) {
            return { records: [], count: 0, source: null };
          }
          if (!response.ok) {
            throw new Error(`Unable to load official UK mission catalogue (${response.status})`);
          }
          return response.json();
        })
        .then((payload) => ({
          records: Array.isArray(payload.records) ? payload.records : [],
          count: Number(payload.count) || 0,
          source: payload.source || null
        }));
    }
    return payloadPromise;
  };

  const reset = () => {
    payloadPromise = null;
  };

  window.MCUKOfficialCatalogue = Object.freeze({
    load,
    reset,
    url: catalogueUrl.toString()
  });
})();
