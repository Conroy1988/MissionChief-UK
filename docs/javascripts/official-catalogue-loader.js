(() => {
  "use strict";

  const existing = window.MCUKOfficialCatalogue;
  if (existing && typeof existing.load === "function") return;

  const script = document.currentScript;
  const siteRoot = script && script.src
    ? script.src.replace(/javascripts\/official-catalogue-loader\.js(?:\?.*)?$/, "")
    : `${window.location.origin}/MissionChief-UK/`;
  const catalogueUrl = new URL("assets/data/official/uk-missions.json", siteRoot);
  const catalogueHref = catalogueUrl.toString();
  const nativeFetch = window.fetch.bind(window);
  let responsePromise = null;
  let payloadPromise = null;

  const requestUrl = (input) => {
    try {
      if (input instanceof Request) return new URL(input.url, document.baseURI).toString();
      return new URL(String(input), document.baseURI).toString();
    } catch {
      return "";
    }
  };

  const fetchCatalogueResponse = (init = { cache: "no-cache" }) => {
    if (!responsePromise) {
      responsePromise = nativeFetch(catalogueUrl, init)
        .catch((error) => {
          responsePromise = null;
          throw error;
        });
    }
    return responsePromise.then((response) => response.clone());
  };

  window.fetch = (input, init) => {
    if (requestUrl(input) === catalogueHref) {
      return fetchCatalogueResponse(init);
    }
    return nativeFetch(input, init);
  };

  const load = () => {
    if (!payloadPromise) {
      payloadPromise = fetchCatalogueResponse({ cache: "no-cache" })
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
        }))
        .catch((error) => {
          payloadPromise = null;
          throw error;
        });
    }
    return payloadPromise;
  };

  const reset = () => {
    responsePromise = null;
    payloadPromise = null;
  };

  window.MCUKOfficialCatalogue = Object.freeze({
    load,
    reset,
    url: catalogueHref
  });
})();
