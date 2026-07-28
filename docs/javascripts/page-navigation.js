(() => {
  "use strict";

  const MIN_SECTIONS = 4;

  function labelTaskListControls(content) {
    for (const input of content.querySelectorAll(".task-list-item input[type='checkbox']")) {
      if (input.hasAttribute("aria-label") || input.hasAttribute("aria-labelledby")) continue;
      const item = input.closest(".task-list-item");
      const labelText = (item?.textContent || "")
        .replace(/\s+/g, " ")
        .trim();
      input.setAttribute("aria-label", labelText || "Checklist item");
    }
  }

  function initContentEnhancements() {
    const content = document.querySelector(".md-content .md-typeset");
    if (!content) return;

    labelTaskListControls(content);

    if (content.querySelector(".mcuk-home") || content.querySelector("[data-mcuk-page-sections]")) return;

    const heading = content.querySelector("h1");
    const sections = [...content.querySelectorAll("h2[id]")]
      .filter((section) => section.textContent.trim());
    if (!heading || sections.length < MIN_SECTIONS) return;

    const details = document.createElement("details");
    details.className = "mcuk-page-sections";
    details.dataset.mcukPageSections = "true";

    const summary = document.createElement("summary");
    summary.textContent = `Page sections (${sections.length})`;
    details.append(summary);

    const nav = document.createElement("nav");
    nav.setAttribute("aria-label", "Page sections");
    const list = document.createElement("ol");

    for (const section of sections) {
      const item = document.createElement("li");
      const link = document.createElement("a");
      link.href = `#${encodeURIComponent(section.id)}`;
      link.textContent = section.textContent.replace(/¶\s*$/, "").trim();
      item.append(link);
      list.append(item);
    }

    nav.append(list);
    details.append(nav);
    heading.insertAdjacentElement("afterend", details);
  }

  if (typeof document$ !== "undefined") {
    document$.subscribe(initContentEnhancements);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initContentEnhancements, { once: true });
  } else {
    initContentEnhancements();
  }
})();
