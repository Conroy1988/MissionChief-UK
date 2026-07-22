(() => {
  "use strict";

  function applyDeepLink() {
    const query = new URLSearchParams(window.location.search).get("q");
    if (!query) return;

    const root = document.querySelector("[data-mcuk-tool='mission-lookup'], [data-mcuk-tool='query-catalogue']");
    const input = root?.querySelector("[data-role='query']");
    if (!input || input.dataset.mcukDeepLinkApplied === "true") return;

    input.dataset.mcukDeepLinkApplied = "true";
    input.value = query;
    input.dispatchEvent(new Event("input", { bubbles: true }));
    input.focus({ preventScroll: true });
    root.scrollIntoView({ behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth", block: "start" });
  }

  const schedule = () => {
    applyDeepLink();
    window.setTimeout(applyDeepLink, 100);
  };

  if (typeof document$ !== "undefined") document$.subscribe(schedule);
  else if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", schedule, { once: true });
  else schedule();
})();