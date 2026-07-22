<div class="mcuk-home" data-mcuk-home markdown>

<section class="mcuk-home-hero" markdown>

<div class="mcuk-hero-topline">
  <span class="mcuk-kicker">United Kingdom Operations Intelligence</span>
  <span class="mcuk-live-state" data-mcuk-live-state><i></i> Production baseline</span>
</div>

# MissionChief UK

<p class="mcuk-hero-lead">A verified command platform for searching incidents, understanding requirements, planning fleets and consuming structured UK game data.</p>

<div class="mcuk-actions" markdown>
[Search mission requirements](tools/mission-lookup.md){ .md-button .md-button--primary }
[Plan concurrent incidents](tools/fleet-planner.md){ .md-button }
[Open the static API](api/index.md){ .md-button }
</div>

<div class="mcuk-hero-telemetry">
  <div><strong data-mcuk-metric="version">v1.0.0</strong><span>Data release</span></div>
  <div><strong data-mcuk-metric="stage">Stage 34</strong><span>Core programme</span></div>
  <div><strong data-mcuk-metric="missions">62</strong><span>Verified missions</span></div>
  <div><strong data-mcuk-metric="resources">46</strong><span>Canonical resources</span></div>
  <div><strong data-mcuk-metric="api">API v1</strong><span>Public interface</span></div>
</div>

<div class="mcuk-radar" aria-hidden="true">
  <span class="mcuk-radar-ring mcuk-radar-ring--one"></span>
  <span class="mcuk-radar-ring mcuk-radar-ring--two"></span>
  <span class="mcuk-radar-sweep"></span>
  <span class="mcuk-radar-core">UK</span>
  <i class="mcuk-radar-node mcuk-radar-node--one"></i>
  <i class="mcuk-radar-node mcuk-radar-node--two"></i>
  <i class="mcuk-radar-node mcuk-radar-node--three"></i>
</div>

</section>

<section class="mcuk-command-strip">
  <span><b>SEARCH</b> Find the exact incident or resource</span>
  <span><b>ASSESS</b> Separate guaranteed and uncertain demand</span>
  <span><b>PLAN</b> Model simultaneous operational pressure</span>
  <span><b>VERIFY</b> Trace populated facts to evidence</span>
</section>

## Choose a command route

<div class="mcuk-command-grid">

<a class="mcuk-command-card mcuk-command-card--blue" href="tools/mission-lookup/">
  <span class="mcuk-command-icon">01</span>
  <small>MISSION INTELLIGENCE</small>
  <strong>Mission Lookup</strong>
  <p>Search IDs, names, aliases, POIs, service groups, patient profiles and requirement types.</p>
  <em>Launch lookup →</em>
</a>

<a class="mcuk-command-card mcuk-command-card--red" href="tools/fleet-planner/">
  <span class="mcuk-command-icon">02</span>
  <small>RESOURCE PLANNING</small>
  <strong>Concurrent Fleet Planner</strong>
  <p>Multiply guaranteed requirements across several incidents without flattening alternative groups.</p>
  <em>Open planner →</em>
</a>

<a class="mcuk-command-card mcuk-command-card--cyan" href="tools/resource-comparison/">
  <span class="mcuk-command-icon">03</span>
  <small>CAPABILITY ANALYSIS</small>
  <strong>Resource Comparison</strong>
  <p>Compare vehicles and qualifications while keeping unsupported values visibly unknown.</p>
  <em>Compare records →</em>
</a>

<a class="mcuk-command-card mcuk-command-card--steel" href="services/">
  <span class="mcuk-command-icon">04</span>
  <small>SERVICE DOCTRINE</small>
  <strong>Emergency Services</strong>
  <p>Navigate operational guidance across core, remote, maritime, specialist and railway response.</p>
  <em>Browse services →</em>
</a>

<a class="mcuk-command-card mcuk-command-card--violet" href="tools/query-catalogue/">
  <span class="mcuk-command-icon">05</span>
  <small>NATURAL-LANGUAGE SEARCH</small>
  <strong>Query Catalogue</strong>
  <p>Use ordinary words or a short question against the generated cross-collection evidence index.</p>
  <em>Ask the catalogue →</em>
</a>

<a class="mcuk-command-card mcuk-command-card--gold" href="api/">
  <span class="mcuk-command-icon">06</span>
  <small>MACHINE-READABLE DATA</small>
  <strong>Static Data API</strong>
  <p>Consume versioned JSON collections, the manifest, search index, FAQ and OpenAPI contract.</p>
  <em>Read API contract →</em>
</a>

</div>

## Live intelligence estate

<div class="mcuk-operations-board">
  <div class="mcuk-board-header">
    <div>
      <small>PRODUCTION POSTURE</small>
      <h3>Validated UK data, one controlled source</h3>
    </div>
    <span data-mcuk-release-date>Released 22 July 2026</span>
  </div>
  <div class="mcuk-board-metrics">
    <div><strong data-mcuk-collection="missions">62</strong><span>Mission records</span><i>Requirements, outcomes and generation</i></div>
    <div><strong data-mcuk-collection="vehicles">46</strong><span>Deployable resources</span><i>Vehicles, trailers, boats and equipment</i></div>
    <div><strong data-mcuk-collection="infrastructure">18</strong><span>Infrastructure records</span><i>Buildings and extensions</i></div>
    <div><strong data-mcuk-collection="training">11</strong><span>Qualification records</span><i>Roles and verified course fields</i></div>
  </div>
  <div class="mcuk-board-footer">
    <span><b data-mcuk-search-count>137</b> searchable canonical entities</span>
    <span><b data-mcuk-status>production</b> release status</span>
    <a href="reference/data-exports/">Inspect generated exports →</a>
  </div>
</div>

!!! important "Evidence boundary"
    **Verified applies only to populated fields.** An omitted value is unknown, not zero. Empty response arrays may represent directory-level evidence where the individual response table was unavailable.

## Operational coverage

<div class="mcuk-theatre-grid">
  <article>
    <small>CORE RESPONSE</small>
    <h3>Everyday command</h3>
    <div class="mcuk-chip-row">
      <a href="services/fire-and-rescue/">Fire &amp; Rescue</a>
      <a href="services/ambulance/">Ambulance &amp; HART</a>
      <a href="services/police/">Police &amp; Public Order</a>
    </div>
    <p>Core buildings, deployable resources, common incidents and progression dependencies.</p>
  </article>
  <article>
    <small>MARITIME &amp; REMOTE</small>
    <h3>Special geography</h3>
    <div class="mcuk-chip-row">
      <a href="services/coastguard-and-lifeboat/">Coastguard &amp; Lifeboat</a>
      <a href="services/mountain-rescue/">Mountain Rescue</a>
      <a href="services/search-and-rescue/">Search &amp; Rescue HQ</a>
    </div>
    <p>Coastal, offshore, mountain and search operations with specialist infrastructure.</p>
  </article>
  <article>
    <small>SPECIALIST OPERATIONS</small>
    <h3>High-complexity response</h3>
    <div class="mcuk-chip-row">
      <a href="services/bomb-disposal/">Bomb Disposal &amp; EOD</a>
      <a href="services/airfield-operations/">Airfield Operations</a>
      <a href="services/recovery/">Recovery &amp; HGV</a>
      <a href="services/railway-response/">Railway Response</a>
    </div>
    <p>Specialist mission chains, qualifications, resource dependencies and infrastructure.</p>
  </article>
</div>

## From evidence to command decision

<div class="mcuk-pipeline">
  <div><span>01</span><strong>Capture</strong><p>Record reproducible UK evidence and source context.</p></div>
  <i></i>
  <div><span>02</span><strong>Model</strong><p>Represent missions, resources and qualifications as canonical JSON.</p></div>
  <i></i>
  <div><span>03</span><strong>Validate</strong><p>Enforce schemas, identifiers, ranges and cross-record relationships.</p></div>
  <i></i>
  <div><span>04</span><strong>Publish</strong><p>Generate documentation, intelligence tools, FAQ and static API exports.</p></div>
  <i></i>
  <div><span>05</span><strong>Verify live</strong><p>Smoke-test the deployed Pages site and public API before release.</p></div>
</div>

## Intelligence standard

<div class="mcuk-evidence-grid">
  <article class="mcuk-evidence mcuk-evidence--verified"><b>✅</b><strong>Verified</strong><p>Reproduced in the current UK game or supported by a suitable primary source.</p></article>
  <article class="mcuk-evidence mcuk-evidence--calculated"><b>🧮</b><strong>Calculated</strong><p>Derived transparently from verified values with the method retained.</p></article>
  <article class="mcuk-evidence mcuk-evidence--recommended"><b>🎯</b><strong>Recommended</strong><p>Strategic guidance that may vary by account, geography or play style.</p></article>
  <article class="mcuk-evidence mcuk-evidence--review"><b>⚠️</b><strong>Review required</strong><p>Incomplete, contradictory, outdated or awaiting reproduction.</p></article>
</div>

[Read the complete data and evidence standard →](reference/data-standard.md)

## Start from your operating position

<div class="mcuk-role-grid">
  <a href="getting-started/"><span>NEW COMMANDER</span><strong>Build the right foundation</strong><p>Start the account, understand the interface and avoid expensive early mistakes.</p></a>
  <a href="strategy/account-progression/"><span>GROWING ACCOUNT</span><strong>Plan expansion deliberately</strong><p>Balance service growth, station placement and specialist capability.</p></a>
  <a href="alliances/"><span>ALLIANCE OPERATIONS</span><strong>Coordinate at scale</strong><p>Use shared knowledge for transport, event and major-incident workflows.</p></a>
  <a href="api/"><span>DEVELOPER / RESEARCHER</span><strong>Consume the canonical data</strong><p>Build read-only tools against the versioned JSON and OpenAPI interface.</p></a>
</div>

<section class="mcuk-final-cta" markdown>

<div>
  <small>COMMUNITY INTELLIGENCE</small>
  <h2>Found a gap, contradiction or new UK mission?</h2>
  <p>Submit reproducible evidence. Every accepted contribution should make the platform more precise—not merely larger.</p>
</div>

<div class="mcuk-actions" markdown>
[Contribute evidence](contributing/index.md){ .md-button .md-button--primary }
[Open an issue](https://github.com/Conroy1988/MissionChief-UK/issues/new/choose){ .md-button }
</div>

</section>

---

> **Independent project:** MissionChief UK is not operated by, endorsed by or affiliated with SHPlay GmbH or the official MissionChief team. MissionChief names, screenshots, game artwork and related assets remain the property of their respective owners.

</div>
