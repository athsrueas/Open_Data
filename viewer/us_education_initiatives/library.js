(function () {
  const US_STATES_GEOJSON_URL = "https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json";
  const LOWER_48 = new Set([
    "AL", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME",
    "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK",
    "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY",
  ]);
  const STATE_CODE_BY_NAME = {
    Alabama: "AL", Alaska: "AK", Arizona: "AZ", Arkansas: "AR", California: "CA", Colorado: "CO",
    Connecticut: "CT", Delaware: "DE", Florida: "FL", Georgia: "GA", Hawaii: "HI", Idaho: "ID",
    Illinois: "IL", Indiana: "IN", Iowa: "IA", Kansas: "KS", Kentucky: "KY", Louisiana: "LA",
    Maine: "ME", Maryland: "MD", Massachusetts: "MA", Michigan: "MI", Minnesota: "MN", Mississippi: "MS",
    Missouri: "MO", Montana: "MT", Nebraska: "NE", Nevada: "NV", "New Hampshire": "NH", "New Jersey": "NJ",
    "New Mexico": "NM", "New York": "NY", "North Carolina": "NC", "North Dakota": "ND", Ohio: "OH",
    Oklahoma: "OK", Oregon: "OR", Pennsylvania: "PA", "Rhode Island": "RI", "South Carolina": "SC",
    "South Dakota": "SD", Tennessee: "TN", Texas: "TX", Utah: "UT", Vermont: "VT", Virginia: "VA",
    Washington: "WA", "West Virginia": "WV", Wisconsin: "WI", Wyoming: "WY",
  };

  let geojsonPromise = null;
  let mapViews = [];

  const PUBLIC_METRIC_LABELS = {
    continuumBalanceScore: "Continuum score (low-tech to high-tech)",
    directAnchorCount: "State-linked initiatives",
    testingAnchorCount: "Testing-focused initiatives",
    workBasedAnchorCount: "Work-based learning initiatives",
    outdoorAnchorCount: "Outdoor learning initiatives",
    reducedTechnologyAnchorCount: "Low-tech policy initiatives",
    combinedCount: "State-linked + nationwide initiatives",
  };

  function createInitiativeAtlas(root, data) {
    if (!root) throw new Error("Root element is required.");
    if (!data || !Array.isArray(data.initiatives)) throw new Error("Atlas data not found.");

    const state = {
      search: "",
      category: "all",
      scope: "all",
      sort: "featured",
      selectedId: data.featuredInitiativeIds[0] || data.initiatives[0]?.id || null,
      selectedStateCode: data.stateMap?.states?.find((item) => item.directAnchorCount > 0)?.code || data.stateMap?.states?.[0]?.code || null,
      mapMetric: data.stateMap?.metrics?.[0]?.key || "directAnchorCount",
    };

    function matchesSearch(item, search) {
      if (!search) return true;
      const haystack = [
        item.initiative, item.category, item.locationLabel, item.coreFocus, item.outcomeSummary,
        item.keyFigures.join(" "), item.policies.join(" "),
      ].join(" ").toLowerCase();
      return haystack.includes(search);
    }

    function filteredInitiatives() {
      const search = state.search.trim().toLowerCase();
      let items = data.initiatives.filter((item) => {
        if (state.category !== "all" && item.category !== state.category) return false;
        if (state.scope !== "all" && item.locationScope !== state.scope) return false;
        return matchesSearch(item, search);
      });
      if (state.sort === "timeline") {
        items = items.slice().sort((a, b) => (b.timeline.startYear || 0) - (a.timeline.startYear || 0) || a.initiative.localeCompare(b.initiative));
      } else if (state.sort === "alphabetical") {
        items = items.slice().sort((a, b) => a.initiative.localeCompare(b.initiative));
      } else {
        items = items.slice().sort((a, b) => b.score - a.score || a.initiative.localeCompare(b.initiative));
      }
      return items;
    }

    function selectedInitiative(items) {
      return items.find((item) => item.id === state.selectedId) || data.initiatives.find((item) => item.id === state.selectedId) || items[0] || data.initiatives[0] || null;
    }

    function selectedStateRecord() {
      const states = data.stateMap?.states || [];
      return states.find((item) => item.code === state.selectedStateCode) || states[0] || null;
    }

    function statCards(items) {
      const activeNowCount = items.filter((item) => item.timeline.isOngoing).length;
      return [
        { value: String(items.length), label: "Visible initiatives" },
        { value: String(activeNowCount), label: "Still active" },
        { value: String(new Set(items.map((item) => item.category)).size), label: "Category lenses" },
        { value: String(new Set(items.map((item) => item.locationScope)).size), label: "Geography modes" },
      ];
    }

    function histogram(items) {
      const counts = new Map();
      items.forEach((item) => counts.set(item.timeline.era || "Unknown", (counts.get(item.timeline.era || "Unknown") || 0) + 1));
      return Array.from(counts.entries()).map(([era, count]) => ({ era, count })).sort((a, b) => a.era.localeCompare(b.era));
    }

    function scopeBars(items) {
      const counts = new Map();
      items.forEach((item) => counts.set(item.locationScope, (counts.get(item.locationScope) || 0) + 1));
      const max = Math.max(...Array.from(counts.values()), 1);
      return Array.from(counts.entries()).map(([scope, count]) => ({ scope, count, width: (count / max) * 100 })).sort((a, b) => b.count - a.count || a.scope.localeCompare(b.scope));
    }

    function metricBreaks(values) {
      const sorted = values.filter((v) => Number.isFinite(v)).sort((a, b) => a - b);
      if (!sorted.length) return { min: 0, max: 0, q1: 0, q2: 0, q3: 0 };
      const at = (q) => {
        const p = (sorted.length - 1) * q;
        const i = Math.floor(p);
        const f = p - i;
        return sorted[i + 1] != null ? sorted[i] + f * (sorted[i + 1] - sorted[i]) : sorted[i];
      };
      return { min: sorted[0], max: sorted[sorted.length - 1], q1: at(0.25), q2: at(0.5), q3: at(0.75) };
    }

    function destroyMaps() {
      mapViews.forEach((entry) => entry.map.remove());
      mapViews = [];
    }

    function mapStyle() {
      return {
        version: 8,
        sources: {
          osm: {
            type: "raster",
            tiles: ["https://a.tile.openstreetmap.org/{z}/{x}/{y}.png", "https://b.tile.openstreetmap.org/{z}/{x}/{y}.png"],
            tileSize: 256,
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
          },
        },
        layers: [{ id: "osm", type: "raster", source: "osm", paint: { "raster-opacity": 0.2, "raster-saturation": -1, "raster-brightness-max": 0.92 } }],
      };
    }

    function loadStateGeojson(metricKey) {
      if (!geojsonPromise) {
        geojsonPromise = fetch(US_STATES_GEOJSON_URL).then((res) => {
          if (!res.ok) throw new Error("Failed to load U.S. state geometry.");
          return res.json();
        });
      }
      return geojsonPromise.then((geojson) => {
        const byCode = Object.fromEntries((data.stateMap?.states || []).map((s) => [s.code, s]));
        const values = (data.stateMap?.states || []).map((s) => Number(s[metricKey] || 0));
        const breaks = metricBreaks(values);
        const features = (geojson.features || [])
          .map((feature) => {
            const name = feature?.properties?.name;
            const code = STATE_CODE_BY_NAME[name];
            if (!code || !byCode[code]) return null;
            return {
              ...feature,
              properties: {
                ...feature.properties,
                state_code: code,
                state_name: name,
                metric_value: Number(byCode[code][metricKey] || 0),
              },
            };
          })
          .filter(Boolean);
        return { geojson: { type: "FeatureCollection", features }, breaks };
      });
    }

    function mapPane(containerId, filterCodes, bounds, zoom) {
      return { containerId, filterCodes, bounds, zoom };
    }

    function initStateMaps() {
      const mainContainer = root.querySelector("#map-main");
      const akContainer = root.querySelector("#map-ak");
      const hiContainer = root.querySelector("#map-hi");
      if (!mainContainer || !window.maplibregl || !data.stateMap) return;

      loadStateGeojson(state.mapMetric)
        .then(({ geojson, breaks }) => {
          const panes = [
            mapPane("map-main", Array.from(LOWER_48), [[-125.0, 24.0], [-66.0, 49.8]], 3.1),
            mapPane("map-ak", ["AK"], [[-179.5, 51.2], [-129.8, 71.8]], 2.2),
            mapPane("map-hi", ["HI"], [[-160.9, 18.8], [-154.6, 22.5]], 5.2),
          ];

          panes.forEach((pane) => {
            if (!root.querySelector(`#${pane.containerId}`)) return;
            const map = new maplibregl.Map({
              container: pane.containerId,
              style: mapStyle(),
              interactive: true,
              attributionControl: false,
              dragRotate: false,
              touchZoomRotate: false,
              minZoom: 1.5,
              maxZoom: 8,
            });
            map.on("load", () => {
              map.addSource("states", { type: "geojson", data: geojson });
              const filter = ["in", ["get", "state_code"], ["literal", pane.filterCodes]];
              map.addLayer({
                id: `fill-${pane.containerId}`,
                type: "fill",
                source: "states",
                filter,
                paint: {
                  "fill-color": [
                    "interpolate",
                    ["linear"],
                    ["coalesce", ["get", "metric_value"], 0],
                    breaks.min, "#f3f4f7",
                    breaks.q1, "#c5dceb",
                    breaks.q2, "#79b1ce",
                    breaks.q3, "#3f7fa9",
                    breaks.max, "#1f4f72",
                  ],
                  "fill-opacity": 0.96,
                },
              });
              map.addLayer({
                id: `line-${pane.containerId}`,
                type: "line",
                source: "states",
                filter,
                paint: { "line-color": "rgba(22,22,22,0.55)", "line-width": 1.1 },
              });
              map.addLayer({
                id: `selected-${pane.containerId}`,
                type: "line",
                source: "states",
                filter: ["all", filter, ["==", ["get", "state_code"], state.selectedStateCode || ""]],
                paint: { "line-color": "#b65431", "line-width": 3 },
              });

              map.fitBounds(pane.bounds, { padding: pane.containerId === "map-main" ? 20 : 10, duration: 0 });
              map.on("click", `fill-${pane.containerId}`, (event) => {
                const code = event.features?.[0]?.properties?.state_code;
                if (!code) return;
                state.selectedStateCode = code;
                const picked = (data.stateMap?.states || []).find((entry) => entry.code === code);
                if (picked?.anchorInitiativeIds?.length) {
                  state.selectedId = picked.anchorInitiativeIds[0];
                }
                render();
              });
              map.on("mouseenter", `fill-${pane.containerId}`, () => { map.getCanvas().style.cursor = "pointer"; });
              map.on("mouseleave", `fill-${pane.containerId}`, () => { map.getCanvas().style.cursor = ""; });
            });
            mapViews.push({ map, pane });
          });
        })
        .catch(() => {
          const fallback = root.querySelector(".map-fallback-note");
          if (fallback) fallback.textContent = "State geometry could not be loaded. Map panel is currently unavailable.";
        });
    }

    function render() {
      destroyMaps();
      const items = filteredInitiatives();
      const selected = selectedInitiative(items);
      if (selected) state.selectedId = selected.id;

      const cards = statCards(items);
      const timeline = histogram(items);
      const scopes = scopeBars(items);
      const selectedState = selectedStateRecord();
      const stateOptions = (data.stateMap?.states || []).slice().sort((a, b) => a.name.localeCompare(b.name));

      root.innerHTML = `
        <main class="atlas-shell">
          <section class="hero">
            <div class="hero-copy">
              <p class="eyebrow">U.S. Education Initiatives Atlas</p>
              <h1>U.S. Education Initiatives by State</h1>
              <p class="lede">${data.subtitle}</p>
              <div class="hero-stats">
                ${cards.map((card) => `<div class="hero-stat"><strong>${card.value}</strong><span>${card.label}</span></div>`).join("")}
              </div>
            </div>
            <div class="hero-rail">
              <p class="panel-label">Featured</p>
              ${data.featuredInitiativeIds
                .map((id) => data.initiatives.find((item) => item.id === id))
                .filter(Boolean)
                .map((item) => `<button class="feature-button ${state.selectedId === item.id ? "is-active" : ""}" data-select-id="${item.id}"><span>${item.initiative}</span><small>${item.locationLabel}</small></button>`)
                .join("")}
            </div>
          </section>

          <section class="workspace">
            <div class="controls">
              <label class="control search-control"><span>Search</span><input id="search-input" type="search" placeholder="Policy, person, state, outcome" value="${escapeHtml(state.search)}" /></label>
              <label class="control"><span>Category</span><select id="category-select"><option value="all">All categories</option>${Array.from(new Set(data.initiatives.map((item) => item.category))).sort((a, b) => a.localeCompare(b)).map((category) => `<option value="${escapeAttr(category)}" ${state.category === category ? "selected" : ""}>${category}</option>`).join("")}</select></label>
              <label class="control"><span>Geography</span><select id="scope-select"><option value="all">All scopes</option><option value="national" ${state.scope === "national" ? "selected" : ""}>National</option><option value="state" ${state.scope === "state" ? "selected" : ""}>State</option><option value="region" ${state.scope === "region" ? "selected" : ""}>Region</option><option value="multi_state" ${state.scope === "multi_state" ? "selected" : ""}>Multi-state</option><option value="mixed" ${state.scope === "mixed" ? "selected" : ""}>Mixed</option><option value="other" ${state.scope === "other" ? "selected" : ""}>Other</option></select></label>
              <label class="control"><span>Sort</span><select id="sort-select"><option value="featured" ${state.sort === "featured" ? "selected" : ""}>Editorial relevance</option><option value="timeline" ${state.sort === "timeline" ? "selected" : ""}>Latest start year</option><option value="alphabetical" ${state.sort === "alphabetical" ? "selected" : ""}>Alphabetical</option></select></label>
            </div>

            <section class="map-panel">
              <div class="map-panel-head">
                <div>
                  <p class="panel-label">Geographic view</p>
                </div>
                <label class="control metric-control">
                  <span>Map metric</span>
                  <select id="map-metric-select">${(data.stateMap?.metrics || []).map((metric) => `<option value="${escapeAttr(metric.key)}" ${state.mapMetric === metric.key ? "selected" : ""}>${PUBLIC_METRIC_LABELS[metric.key] || metric.label}</option>`).join("")}</select>
                </label>
                <label class="control metric-control">
                  <span>State</span>
                  <select id="state-select">
                    ${stateOptions
                      .map(
                        (item) =>
                          `<option value="${item.code}" ${state.selectedStateCode === item.code ? "selected" : ""}>${item.name}</option>`
                      )
                      .join("")}
                  </select>
                </label>
              </div>
              <div class="map-layout">
                <div class="geo-map-shell">
                  <div id="map-main" class="geo-map main"></div>
                  <div class="map-insets">
                    <div class="inset-wrap"><span>Alaska</span><div id="map-ak" class="geo-map inset"></div></div>
                    <div class="inset-wrap"><span>Hawaii</span><div id="map-hi" class="geo-map inset"></div></div>
                  </div>
                  <p class="map-fallback-note"></p>
                </div>
                <aside class="state-detail-panel">
                  ${selectedState ? `
                    <p class="panel-label">State detail</p>
                    <h3>${selectedState.name}</h3>
                    <div class="state-metrics">
                      <div><span class="detail-label">State-linked initiatives</span><strong>${selectedState.directAnchorCount}</strong></div>
                      <div><span class="detail-label">Nationwide initiatives</span><strong>${selectedState.nationalContextCount}</strong></div>
                      <div><span class="detail-label">Strongest evidence</span><strong>${selectedState.strongestEvidenceScore}/5</strong></div>
                    </div>
                    <section class="detail-section">
                      <span class="detail-label">Documented initiatives in this state</span>
                      <div class="state-anchor-list">
                        ${selectedState.anchorDetails.length
                          ? selectedState.anchorDetails.map((anchor) => `<button class="state-anchor-button" data-select-id="${anchor.initiativeId}"><strong>${anchor.initiative}</strong><small>${anchor.anchorType.replaceAll("_", " ")}</small></button>`).join("")
                          : `<p class="detail-summary">No state-specific initiative links are loaded yet for this state.</p>`}
                      </div>
                    </section>` : ""}
                </aside>
              </div>
            </section>

            <div class="insights">
              <article class="insight-panel">
                <p class="panel-label">Timeline spread</p>
                <div class="histogram">
                  ${timeline.map((item) => {
                    const max = Math.max(...timeline.map((entry) => entry.count), 1);
                    return `<div class="histogram-row"><span>${item.era}</span><div class="bar-track"><div class="bar-fill" style="width:${(item.count / max) * 100}%"></div></div><strong>${item.count}</strong></div>`;
                  }).join("")}
                </div>
              </article>
              <article class="insight-panel">
                <p class="panel-label">Geography mix</p>
                <div class="scope-list">
                  ${scopes.map((item) => `<div class="scope-row"><span>${formatScope(item.scope)}</span><div class="bar-track"><div class="bar-fill alt" style="width:${item.width}%"></div></div><strong>${item.count}</strong></div>`).join("")}
                </div>
              </article>
            </div>

            <div class="content-grid">
              <section class="initiative-list">
                <div class="list-head"><p class="panel-label">Explorer</p><span>${items.length} shown</span></div>
                <div class="initiative-items">
                  ${items.map((item) => `<button class="initiative-item ${state.selectedId === item.id ? "is-active" : ""}" data-select-id="${item.id}"><div class="initiative-item-top"><span class="category-chip">${item.category}</span><span class="scope-chip">${formatScope(item.locationScope)}</span></div><h2>${item.initiative}</h2><p>${item.coreFocus}</p><div class="initiative-meta"><span>${item.timeline.label}</span><span>${item.locationLabel}</span></div></button>`).join("")}
                </div>
              </section>
              <aside class="detail-panel">
                ${selected ? `
                  <p class="panel-label">Detail</p>
                  <h2>${selected.initiative}</h2>
                  <p class="detail-summary">${selected.coreFocus}</p>
                  <div class="detail-grid">
                    <div><span class="detail-label">Category</span><strong>${selected.category}</strong></div>
                    <div><span class="detail-label">Location</span><strong>${selected.locationLabel}</strong></div>
                    <div><span class="detail-label">Timeline</span><strong>${selected.timeline.label}</strong></div>
                    <div><span class="detail-label">Source</span><strong>${selected.sourceHost}</strong></div>
                  </div>
                  <section class="detail-section">
                    <span class="detail-label">Research status</span>
                    <div class="evidence-strip">
                      <span class="tag">${selected.evidence.researchStatus || "seed"}</span>
                      ${selected.evidence.consensusDirection ? `<span class="tag">${selected.evidence.consensusDirection}</span>` : ""}
                      ${selected.evidence.confidenceLabel ? `<span class="tag">${selected.evidence.confidenceLabel}</span>` : ""}
                      ${selected.evidence.evidenceScore ? `<span class="tag">evidence ${selected.evidence.evidenceScore}/5</span>` : ""}
                    </div>
                    ${selected.evidence.qualityNotes ? `<p class="detail-summary">${selected.evidence.qualityNotes}</p>` : `<p class="detail-summary">No structured evidence review has been attached yet.</p>`}
                  </section>
                  <section class="detail-section"><span class="detail-label">Policies and mechanisms</span><ul class="detail-list">${selected.policies.map((value) => `<li>${value}</li>`).join("")}</ul></section>
                  <section class="detail-section"><span class="detail-label">Observed outcomes</span><ul class="detail-list">${selected.outcomes.map((value) => `<li>${value}</li>`).join("")}</ul></section>
                  <a class="source-link" href="${selected.source}" target="_blank" rel="noreferrer">Open source reference</a>
                ` : `<p>No initiatives match the current filters.</p>`}
              </aside>
            </div>
          </section>
        </main>
      `;

      bindEvents();
      initStateMaps();
    }

    function bindEvents() {
      const searchInput = root.querySelector("#search-input");
      const categorySelect = root.querySelector("#category-select");
      const scopeSelect = root.querySelector("#scope-select");
      const sortSelect = root.querySelector("#sort-select");
      const mapMetricSelect = root.querySelector("#map-metric-select");
      const stateSelect = root.querySelector("#state-select");
      if (searchInput) searchInput.addEventListener("input", (event) => { state.search = event.target.value; render(); });
      if (categorySelect) categorySelect.addEventListener("change", (event) => { state.category = event.target.value; render(); });
      if (scopeSelect) scopeSelect.addEventListener("change", (event) => { state.scope = event.target.value; render(); });
      if (sortSelect) sortSelect.addEventListener("change", (event) => { state.sort = event.target.value; render(); });
      if (mapMetricSelect) mapMetricSelect.addEventListener("change", (event) => { state.mapMetric = event.target.value; render(); });
      if (stateSelect) {
        stateSelect.addEventListener("change", (event) => {
          state.selectedStateCode = event.target.value;
          render();
        });
      }
      root.querySelectorAll("[data-select-id]").forEach((button) => {
        button.addEventListener("click", () => { state.selectedId = button.dataset.selectId; render(); });
      });
    }

    render();
    return {
      setSearch(value) { state.search = value || ""; render(); },
      setCategory(value) { state.category = value || "all"; render(); },
      setScope(value) { state.scope = value || "all"; render(); },
      select(id) { state.selectedId = id; render(); },
    };
  }

  function formatScope(scope) {
    return scope.replace("_", " ");
  }

  function escapeHtml(value) {
    return String(value).replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;").replaceAll('"', "&quot;");
  }

  function escapeAttr(value) {
    return escapeHtml(value);
  }

  window.InitiativeAtlas = { create: createInitiativeAtlas };
})();
