(() => {
  "use strict";

  const FAMILY_RULES = [
    {
      id: "airfield",
      label: "Airfield and airport",
      test: ({ categories, preconditions, resources }) =>
        categories.has("airport") ||
        Boolean(preconditions.aviation_firefighting_extensions) ||
        Boolean(preconditions.airfield_operations_extensions) ||
        resources.has("airfield_firefighting_command_vehicle") ||
        resources.has("airfield_operations_vehicle") ||
        resources.has("major_foam_tender") ||
        resources.has("riv"),
    },
    {
      id: "railway",
      label: "Railway and tunnel",
      test: ({ categories, preconditions, resources }) =>
        categories.has("railway_fire") ||
        categories.has("railway_police") ||
        Boolean(preconditions.railway_fire_responses) ||
        resources.has("road_rail_unit"),
    },
    {
      id: "flood",
      label: "Flood and water damage",
      test: ({ categories, preconditions, resources }) =>
        categories.has("water_damage_and_flood") ||
        Boolean(preconditions.flood_rescue_extensions) ||
        Boolean(preconditions.water_damage_pump_extensions) ||
        resources.has("flood_rescue_unit"),
    },
    {
      id: "wildfire",
      label: "Wildfire and forest fire",
      test: ({ mission }) => /(?:forest fire|wildfire)/i.test(mission.name || ""),
    },
    {
      id: "hazmat",
      label: "HazMat and CBRN",
      test: ({ resources }) =>
        resources.has("hazmat_unit") ||
        resources.has("cbrn_vehicle") ||
        resources.has("hazmat_container"),
    },
    {
      id: "foam",
      label: "Foam and fire support",
      test: ({ categories, preconditions, resources }) =>
        categories.has("fire_support_specialization") ||
        Boolean(preconditions.foam_extensions) ||
        [
          "foam_unit",
          "bulk_foam_unit",
          "major_foam_tender",
          "bulk_foam_container",
          "foam_container",
          "water_foam_carrier",
          "water_ladder_with_cafs",
          "rescue_pump_with_cafs",
        ].some((resource) => resources.has(resource)),
    },
    {
      id: "technical",
      label: "Technical rescue",
      test: ({ preconditions, resources }) =>
        Boolean(preconditions.technical_rescue_extensions) ||
        resources.has("rescue_support_vehicle") ||
        resources.has("rescue_container"),
    },
    {
      id: "mass-casualty",
      label: "Mass casualty and high patient load",
      test: ({ categories, resources, mission }) =>
        categories.has("mass_casualty_ambulance_specialization") ||
        resources.has("mass_casualty_equipment") ||
        Number(mission.patients?.maximum || 0) >= 20,
    },
    {
      id: "rural",
      label: "Rural fire",
      test: ({ categories }) => categories.has("rural"),
    },
    {
      id: "urban",
      label: "Urban and structural fire",
      test: ({ categories }) => categories.has("urban"),
    },
  ];

  const numberFormatter = new Intl.NumberFormat("en-GB");

  const escapeHtml = (value) =>
    String(value ?? "")
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");

  const guaranteedRows = (mission) => mission.requirements?.guaranteed || [];
  const alternativeRows = (mission) => mission.requirements?.alternatives || [];

  const guaranteedUnits = (mission) =>
    guaranteedRows(mission).reduce((total, row) => total + Number(row.quantity || 0), 0);

  const alternativeSlots = (mission) =>
    alternativeRows(mission).reduce((total, row) => total + Number(row.quantity || 0), 0);

  const resourceSet = (mission) => {
    const resources = new Set();
    guaranteedRows(mission).forEach((row) => resources.add(row.resource));
    alternativeRows(mission).forEach((row) =>
      (row.resources || []).forEach((resource) => resources.add(resource)),
    );
    return resources;
  };

  const classifyMission = (mission) => {
    const context = {
      mission,
      categories: new Set(mission.official_metadata?.mission_categories || []),
      preconditions: mission.preconditions || {},
      resources: resourceSet(mission),
    };
    const families = FAMILY_RULES.filter((rule) => rule.test(context)).map((rule) => rule.id);
    return families.length ? families : ["general"];
  };

  const isHistorical = (mission) => {
    const end = mission.availability_window?.ends_at;
    if (!end) return false;
    const timestamp = Date.parse(end);
    return Number.isFinite(timestamp) && timestamp < Date.now();
  };

  const familyLabel = (id) =>
    FAMILY_RULES.find((rule) => rule.id === id)?.label || "General fire";

  const setTableBody = (element, rows, columnCount) => {
    element.innerHTML = rows.length
      ? rows.join("")
      : `<tr><td colspan="${columnCount}">No matching canonical missions.</td></tr>`;
  };

  const initialise = async () => {
    const root = document.getElementById("fire-pressure-dashboard");
    if (!root || root.dataset.initialised === "true") return;
    root.dataset.initialised = "true";

    const status = document.getElementById("fire-pressure-status");
    const familySelect = document.getElementById("fire-pressure-family");
    const searchInput = document.getElementById("fire-pressure-search");
    const includeHistorical = document.getElementById("fire-pressure-history");
    const familyBody = document.getElementById("fire-pressure-family-body");
    const resourceBody = document.getElementById("fire-pressure-resource-body");
    const missionBody = document.getElementById("fire-pressure-mission-body");
    const summary = document.getElementById("fire-pressure-summary");

    try {
      const response = await fetch(root.dataset.source, { cache: "no-store" });
      if (!response.ok) throw new Error(`Mission export returned HTTP ${response.status}`);
      const payload = await response.json();
      const fireMissions = (payload.records || [])
        .filter((mission) => mission.service === "fire")
        .map((mission) => ({ ...mission, pressureFamilies: classifyMission(mission) }));

      const options = [
        '<option value="all">All Fire mission families</option>',
        ...FAMILY_RULES.map(
          (rule) => `<option value="${rule.id}">${escapeHtml(rule.label)}</option>`,
        ),
        '<option value="general">General fire</option>',
      ];
      familySelect.innerHTML = options.join("");

      const render = () => {
        const query = searchInput.value.trim().toLowerCase();
        const selectedFamily = familySelect.value;
        const historicalAllowed = includeHistorical.checked;

        const baseRecords = fireMissions.filter((mission) => {
          if (!historicalAllowed && isHistorical(mission)) return false;
          if (!query) return true;
          const searchText = [
            mission.name,
            ...(mission.aliases || []),
            ...(mission.pressureFamilies || []).map(familyLabel),
          ]
            .join(" ")
            .toLowerCase();
          return searchText.includes(query);
        });

        const records = baseRecords.filter(
          (mission) =>
            selectedFamily === "all" || mission.pressureFamilies.includes(selectedFamily),
        );

        const totalGuaranteed = records.reduce(
          (total, mission) => total + guaranteedUnits(mission),
          0,
        );
        const totalAlternativeSlots = records.reduce(
          (total, mission) => total + alternativeSlots(mission),
          0,
        );
        const highestPatients = records.reduce(
          (maximum, mission) => Math.max(maximum, Number(mission.patients?.maximum || 0)),
          0,
        );
        const personnelMissions = records.filter(
          (mission) =>
            (mission.personnel?.required || []).length ||
            (mission.personnel?.available || []).length ||
            (mission.personnel?.ranges || []).length,
        ).length;

        summary.innerHTML = [
          ["Matching missions", records.length],
          ["Guaranteed resource units", totalGuaranteed],
          ["Independent alternative slots", totalAlternativeSlots],
          ["Highest patient maximum", highestPatients],
          ["Missions with personnel fields", personnelMissions],
        ]
          .map(
            ([label, value]) =>
              `<div class="fire-pressure-card"><strong>${numberFormatter.format(value)}</strong><span>${escapeHtml(label)}</span></div>`,
          )
          .join("");

        const familyRows = [...FAMILY_RULES.map((rule) => rule.id), "general"].map((id) => {
          const familyRecords = baseRecords.filter((mission) =>
            mission.pressureFamilies.includes(id),
          );
          const guaranteed = familyRecords.reduce(
            (total, mission) => total + guaranteedUnits(mission),
            0,
          );
          const fireEngines = familyRecords.reduce(
            (total, mission) =>
              total +
              guaranteedRows(mission)
                .filter((row) => row.resource === "fire_engine")
                .reduce((rowTotal, row) => rowTotal + Number(row.quantity || 0), 0),
            0,
          );
          const highest = familyRecords
            .slice()
            .sort((a, b) => guaranteedUnits(b) - guaranteedUnits(a))[0];
          return `<tr>
            <td>${escapeHtml(familyLabel(id))}</td>
            <td>${numberFormatter.format(familyRecords.length)}</td>
            <td>${numberFormatter.format(guaranteed)}</td>
            <td>${numberFormatter.format(fireEngines)}</td>
            <td>${highest ? `${numberFormatter.format(guaranteedUnits(highest))} — ${escapeHtml(highest.name)}` : "—"}</td>
          </tr>`;
        });
        setTableBody(familyBody, familyRows, 5);

        const resources = new Map();
        records.forEach((mission) => {
          guaranteedRows(mission).forEach((row) => {
            const current = resources.get(row.resource) || { quantity: 0, missions: 0 };
            current.quantity += Number(row.quantity || 0);
            current.missions += 1;
            resources.set(row.resource, current);
          });
        });
        const resourceRows = [...resources.entries()]
          .sort((a, b) => b[1].quantity - a[1].quantity || a[0].localeCompare(b[0]))
          .slice(0, 15)
          .map(
            ([resource, values]) => `<tr>
              <td><code>${escapeHtml(resource)}</code></td>
              <td>${numberFormatter.format(values.quantity)}</td>
              <td>${numberFormatter.format(values.missions)}</td>
            </tr>`,
          );
        setTableBody(resourceBody, resourceRows, 3);

        const missionRows = records
          .slice()
          .sort(
            (a, b) =>
              guaranteedUnits(b) - guaranteedUnits(a) ||
              Number(b.patients?.maximum || 0) - Number(a.patients?.maximum || 0) ||
              String(a.name).localeCompare(String(b.name)),
          )
          .slice(0, 20)
          .map(
            (mission) => `<tr>
              <td>${escapeHtml(mission.name)}</td>
              <td>${mission.pressureFamilies.map((id) => escapeHtml(familyLabel(id))).join(", ")}</td>
              <td>${numberFormatter.format(guaranteedUnits(mission))}</td>
              <td>${numberFormatter.format(alternativeSlots(mission))}</td>
              <td>${numberFormatter.format(Number(mission.patients?.maximum || 0))}</td>
            </tr>`,
          );
        setTableBody(missionBody, missionRows, 5);

        status.textContent = `Analysing ${numberFormatter.format(records.length)} of ${numberFormatter.format(fireMissions.length)} canonical Fire mission records from data version ${payload.data_version || "unknown"}. Family rows overlap by design.`;
      };

      [familySelect, searchInput, includeHistorical].forEach((control) =>
        control.addEventListener("input", render),
      );
      render();
    } catch (error) {
      status.textContent = `Pressure analysis unavailable: ${error.message}`;
      root.classList.add("fire-pressure-error");
    }
  };

  if (window.document$?.subscribe) {
    window.document$.subscribe(initialise);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initialise, { once: true });
  } else {
    initialise();
  }
})();
