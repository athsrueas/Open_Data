(function () {
  const data = window.EDU_VIEWER_DATA;
  if (!data) throw new Error("Viewer data not found.");

  const countries = data.countries;
  const countryByIso3 = Object.fromEntries(countries.map((country) => [country.iso3, country]));
  const metricCatalog = Object.fromEntries(data.metricCatalog.map((metric) => [metric.key, metric]));

  const state = {
    mapMetricKey: data.mapMetricKeys[0],
    primaryIso3: "KEN",
    secondaryIso3: "USA",
    activeTab: "overview",
  };

  const dom = {
    map: document.getElementById("map"),
    metricSelect: document.getElementById("metric-select"),
    primaryCountry: document.getElementById("primary-country"),
    secondaryCountry: document.getElementById("secondary-country"),
    compareContent: document.getElementById("compare-content"),
    graphExamples: document.getElementById("graph-examples"),
    sourceNotes: document.getElementById("source-notes"),
    heroStats: document.getElementById("hero-stats"),
    legendTitle: document.getElementById("legend-title"),
    legendUnit: document.getElementById("legend-unit"),
    legendRamp: document.getElementById("legend-ramp"),
    legendMin: document.getElementById("legend-min"),
    legendMax: document.getElementById("legend-max"),
    rankingList: document.getElementById("ranking-list"),
    tabButtons: Array.from(document.querySelectorAll(".tab-button")),
    tabPanels: Array.from(document.querySelectorAll(".tab-panel")),
  };

  let map = null;
  let popup;

  function renderMapFallback(message) {
    dom.map.innerHTML = `
      <div class="map-fallback">
        <div class="map-fallback-card">
          <p class="eyebrow">Map unavailable</p>
          <h2>The viewer data loaded, but the map library did not.</h2>
          <p>${message}</p>
          <p class="muted">The compare, ranking, and source-note panels still work below.</p>
        </div>
      </div>
    `;
  }

  function createMap() {
    if (!window.maplibregl) {
      renderMapFallback(
        "This page currently depends on the external MapLibre CDN. If that script is blocked, the rest of the viewer now falls back gracefully."
      );
      return null;
    }

    const instance = new maplibregl.Map({
      container: "map",
      style: {
        version: 8,
        sources: {
          osm: {
            type: "raster",
            tiles: [
              "https://a.tile.openstreetmap.org/{z}/{x}/{y}.png",
              "https://b.tile.openstreetmap.org/{z}/{x}/{y}.png",
            ],
            tileSize: 256,
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
          },
        },
        layers: [
          {
            id: "osm",
            type: "raster",
            source: "osm",
            paint: {
              "raster-opacity": 0.12,
              "raster-saturation": -1,
              "raster-brightness-max": 0.9,
            },
          },
        ],
      },
      center: [0, 8],
      zoom: 0.9,
      minZoom: 0.35,
      maxZoom: 7,
      attributionControl: false,
    });

    instance.addControl(new maplibregl.NavigationControl({ showCompass: false }), "top-right");
    instance.addControl(new maplibregl.AttributionControl({ compact: true }), "bottom-right");
    instance.touchZoomRotate.disableRotation();
    return instance;
  }

  function rampColors() {
    return ["#f2c572", "#e39a4f", "#cf6e34", "#9f4328", "#662317"];
  }

  function getMetricValues(metricKey) {
    return countries
      .map((country) => country.metrics[metricKey] && country.metrics[metricKey].value)
      .filter((value) => value != null && !Number.isNaN(value))
      .sort((a, b) => a - b);
  }

  function quantile(sortedValues, q) {
    if (!sortedValues.length) return null;
    const pos = (sortedValues.length - 1) * q;
    const base = Math.floor(pos);
    const rest = pos - base;
    if (sortedValues[base + 1] !== undefined) {
      return sortedValues[base] + rest * (sortedValues[base + 1] - sortedValues[base]);
    }
    return sortedValues[base];
  }

  function buildStops(metricKey) {
    const values = getMetricValues(metricKey);
    const colors = rampColors();
    const missingColor = "#9f9a92";
    if (!values.length) return { expression: missingColor, min: null, max: null };
    const breaks = [0, 0.25, 0.5, 0.75, 1].map((q) => quantile(values, q));
    const expression = [
      "case",
      ["==", ["get", metricKey], null],
      missingColor,
      ["step", ["get", metricKey], colors[0]],
    ];
    for (let index = 1; index < breaks.length; index += 1) {
      expression[3].push(breaks[index], colors[index]);
    }
    return { expression, min: values[0], max: values[values.length - 1] };
  }

  function hydrateGeojson(metricKey) {
    const geojson = JSON.parse(JSON.stringify(data.geojson));
    for (const feature of geojson.features) {
      const country = countryByIso3[feature.properties.iso3];
      const payload = country && country.metrics[metricKey];
      feature.properties[metricKey] = payload ? payload.value : null;
    }
    return geojson;
  }

  function formatCompactNumber(value, metricKey) {
    if (metricKey === "gdpPerCapita") return `$${Math.round(value).toLocaleString()}`;
    if (metricKey === "population" || metricKey === "schoolAvailabilityTotal") return Math.round(value).toLocaleString();
    return value.toFixed(1);
  }

  function formatValue(metricKey, payload) {
    if (!payload || payload.value == null || Number.isNaN(payload.value)) return "No data";
    const value = payload.value;
    if (metricKey === "gdpPerCapita") return `$${Math.round(value).toLocaleString()}`;
    if (metricKey === "population" || metricKey === "schoolAvailabilityTotal") return Math.round(value).toLocaleString();
    if (metricKey === "schoolAvailabilityPerMillion") return `${value.toFixed(1)} / 1M`;
    if (metricKey === "hloReadingScore") return value.toFixed(1);
    if (payload.unit === "%" || metricCatalog[metricKey]?.unit === "%") return `${value.toFixed(1)}%`;
    return `${value.toFixed(1)} ${payload.unit || ""}`.trim();
  }

  function updateLegend(metricKey, min, max) {
    const metric = metricCatalog[metricKey];
    dom.legendTitle.textContent = metric.label;
    dom.legendUnit.textContent = metric.unit;
    dom.legendMin.textContent = min == null ? "No data" : formatCompactNumber(min, metricKey);
    dom.legendMax.textContent = max == null ? "No data" : formatCompactNumber(max, metricKey);
    dom.legendRamp.innerHTML = rampColors().map((color) => `<span style="background:${color}"></span>`).join("");
  }

  function updateRankings(metricKey) {
    const ranked = countries
      .map((country) => ({ country, payload: country.metrics[metricKey] }))
      .filter((entry) => entry.payload && entry.payload.value != null)
      .sort((a, b) => b.payload.value - a.payload.value)
      .slice(0, 6);

    dom.rankingList.innerHTML = ranked
      .map(
        (entry, index) => `
          <article class="ranking-item">
            <strong>${String(index + 1).padStart(2, "0")}</strong>
            <div>
              <div>${entry.country.name}</div>
              <small>${entry.country.region}</small>
            </div>
            <strong>${formatValue(metricKey, entry.payload)}</strong>
          </article>
        `
      )
      .join("");
  }

  function updateHeroStats(metricKey) {
    const values = getMetricValues(metricKey);
    const withData = countries.filter((country) => {
      const payload = country.metrics[metricKey];
      return payload && payload.value != null;
    }).length;
    const topCountry = countries
      .filter((country) => country.metrics[metricKey] && country.metrics[metricKey].value != null)
      .sort((a, b) => b.metrics[metricKey].value - a.metrics[metricKey].value)[0];

    dom.heroStats.innerHTML = [
      { value: `${withData}`, label: "countries with usable values" },
      { value: values.length ? formatCompactNumber(values[values.length - 1], metricKey) : "n/a", label: "highest visible value" },
      { value: topCountry ? topCountry.name : "n/a", label: "current front-runner" },
      { value: metricCatalog[metricKey].category, label: "current lens" },
    ]
      .map(
        (item) => `
          <div class="hero-stat">
            <strong>${item.value}</strong>
            <span>${item.label}</span>
          </div>
        `
      )
      .join("");
  }

  function compareMetricRow(metricKey, leftCountry, rightCountry) {
    const left = leftCountry.metrics[metricKey];
    const right = rightCountry.metrics[metricKey];
    const leftSource = leftCountry.sources[metricKey];
    const rightSource = rightCountry.sources[metricKey];
    const values = getMetricValues(metricKey);
    const max = values.length ? values[values.length - 1] : 1;
    const leftWidth = left && left.value != null ? Math.max(4, (left.value / max) * 100) : 0;
    const rightWidth = right && right.value != null ? Math.max(4, (right.value / max) * 100) : 0;
    let label = metricCatalog[metricKey] ? metricCatalog[metricKey].label : metricKey;
    if ((leftSource && leftSource.displayNote) || (rightSource && rightSource.displayNote)) {
      label = `${label} / equivalent`;
    }

    const note = [leftSource && leftSource.displayNote, rightSource && rightSource.displayNote]
      .filter(Boolean)
      .filter((value, index, list) => list.indexOf(value) === index)
      .join(" ");
    return `
      <div class="metric-row">
        <header>
          <span>${label}</span>
          <span class="muted">${left ? formatValue(metricKey, left) : "No data"} / ${right ? formatValue(metricKey, right) : "No data"}</span>
        </header>
        <div class="metric-bar-track">
          <div class="metric-bar-fill" style="width:${leftWidth}%;"></div>
        </div>
        <div class="metric-bar-track">
          <div class="metric-bar-fill" style="width:${rightWidth}%; background:linear-gradient(90deg, #3c8f8d 0%, #8fd6d0 100%);"></div>
        </div>
        ${note ? `<small class="metric-note">${note}</small>` : ""}
      </div>
    `;
  }

  function updateComparePanel() {
    const left = countryByIso3[state.primaryIso3];
    const right = countryByIso3[state.secondaryIso3];
    const metricKeys = [
      "schoolAvailabilityPerMillion",
      "educationSpendPctGdp",
      "primaryCompletionRate",
      "literacyRate",
      "learningPovertyRate",
      "hloReadingScore",
      "gdpPerCapita",
    ];

    dom.compareContent.innerHTML = `
      <article class="country-card">
        <div class="country-head">
          <div>
            <h3>${left.name} vs ${right.name}</h3>
            <div class="country-meta">${left.region} and ${right.region}</div>
          </div>
        </div>
        <div class="metric-grid">
          ${metricKeys.map((metricKey) => compareMetricRow(metricKey, left, right)).join("")}
        </div>
      </article>
    `;
  }

  function updateGraphPanel() {
    const primary = countryByIso3[state.primaryIso3];
    dom.graphExamples.innerHTML = data.graphExamples
      .map(
        (edge) => `
          <article class="graph-edge">
            <div class="graph-path">
              <span class="graph-node">${edge.from}</span>
              <span class="graph-link">${edge.edge}</span>
              <span class="graph-node">${edge.to}</span>
            </div>
            <p class="muted">${edge.note.replace("Jurisdiction", primary.name)}</p>
          </article>
        `
      )
      .join("");
  }

  function updateSourceNotes() {
    dom.sourceNotes.innerHTML = data.sourceNotes.map((note) => `<article class="source-note"><p>${note}</p></article>`).join("");
  }

  function fillSelect(select, selectedIso3) {
    select.innerHTML = countries
      .map((country) => `<option value="${country.iso3}" ${country.iso3 === selectedIso3 ? "selected" : ""}>${country.name}</option>`)
      .join("");
  }

  function setActiveTab(tabName) {
    state.activeTab = tabName;
    dom.tabButtons.forEach((button) => {
      button.classList.toggle("is-active", button.dataset.tab === tabName);
    });
    dom.tabPanels.forEach((panel) => {
      panel.classList.toggle("is-active", panel.dataset.panel === tabName);
    });
  }

  function installControls() {
    dom.metricSelect.innerHTML = data.mapMetricKeys
      .map((metricKey) => `<option value="${metricKey}">${metricCatalog[metricKey].label}</option>`)
      .join("");
    dom.metricSelect.value = state.mapMetricKey;
    fillSelect(dom.primaryCountry, state.primaryIso3);
    fillSelect(dom.secondaryCountry, state.secondaryIso3);

    dom.metricSelect.addEventListener("change", (event) => {
      state.mapMetricKey = event.target.value;
      updateMapMetric();
    });
    dom.primaryCountry.addEventListener("change", (event) => {
      state.primaryIso3 = event.target.value;
      updateComparePanel();
      updateGraphPanel();
      highlightCountry(state.primaryIso3);
    });
    dom.secondaryCountry.addEventListener("change", (event) => {
      state.secondaryIso3 = event.target.value;
      updateComparePanel();
    });
    dom.tabButtons.forEach((button) => {
      button.addEventListener("click", () => setActiveTab(button.dataset.tab));
    });
  }

  function buildPopupHtml(feature) {
    const country = countryByIso3[feature.properties.iso3];
    const metricKey = state.mapMetricKey;
    const payload = country.metrics[metricKey];
    const source = country.sources[metricKey];
    return `
      <div>
        <strong>${country.name}</strong><br />
        <span>${country.region}</span><br />
        <span>${metricCatalog[metricKey].label}: ${payload ? formatValue(metricKey, payload) : "No data"}</span>
        ${source && source.displayNote ? `<br /><small>${source.displayNote}</small>` : ""}
      </div>
    `;
  }

  function highlightCountry(iso3) {
    if (map && map.getLayer("country-highlight")) {
      map.setFilter("country-highlight", ["==", ["get", "iso3"], iso3]);
    }
  }

  function walkCoordinates(value, visit) {
    if (!Array.isArray(value) || !value.length) return;
    if (typeof value[0] === "number" && typeof value[1] === "number") {
      visit(value[0], value[1]);
      return;
    }
    value.forEach((item) => walkCoordinates(item, visit));
  }

  function fitWorldToData() {
    const bounds = new maplibregl.LngLatBounds();
    let hasPoints = false;
    for (const feature of data.geojson.features) {
      const coords = feature.geometry && feature.geometry.coordinates;
      if (!coords) continue;
      walkCoordinates(coords, (lng, lat) => {
        bounds.extend([lng, lat]);
        hasPoints = true;
      });
    }
    if (hasPoints) {
      map.fitBounds(bounds, {
        padding: { top: 130, right: 40, bottom: 180, left: 40 },
        duration: 0,
      });
    }
  }

  function updateMapMetric() {
    const metricKey = state.mapMetricKey;
    const stops = buildStops(metricKey);
    if (map && map.getSource("countries")) {
      const hydrated = hydrateGeojson(metricKey);
      map.getSource("countries").setData(hydrated);
      map.setPaintProperty("country-fills", "fill-color", stops.expression);
    }
    updateLegend(metricKey, stops.min, stops.max);
    updateRankings(metricKey);
    updateHeroStats(metricKey);
  }

  function initializeMapLayers() {
    if (!map) return;
    map.addSource("countries", {
      type: "geojson",
      data: hydrateGeojson(state.mapMetricKey),
    });

    const stops = buildStops(state.mapMetricKey);
    map.addLayer({
      id: "country-fills",
      type: "fill",
      source: "countries",
      paint: {
        "fill-color": stops.expression,
        "fill-opacity": 0.82,
      },
    });

    map.addLayer({
      id: "country-borders",
      type: "line",
      source: "countries",
      paint: {
        "line-color": "rgba(50, 40, 32, 0.26)",
        "line-width": 0.55,
      },
    });

    map.addLayer({
      id: "country-highlight",
      type: "line",
      source: "countries",
      paint: {
        "line-color": "#fff9f2",
        "line-width": 2,
      },
      filter: ["==", ["get", "iso3"], state.primaryIso3],
    });

    popup = new maplibregl.Popup({
      closeButton: false,
      closeOnClick: false,
      offset: 10,
    });

    map.on("mousemove", "country-fills", (event) => {
      const feature = event.features && event.features[0];
      if (!feature) return;
      map.getCanvas().style.cursor = "pointer";
      popup.setLngLat(event.lngLat).setHTML(buildPopupHtml(feature)).addTo(map);
    });

    map.on("mouseleave", "country-fills", () => {
      map.getCanvas().style.cursor = "";
      popup.remove();
    });

    map.on("click", "country-fills", (event) => {
      const feature = event.features && event.features[0];
      if (!feature) return;
      state.primaryIso3 = feature.properties.iso3;
      dom.primaryCountry.value = state.primaryIso3;
      updateComparePanel();
      updateGraphPanel();
      highlightCountry(state.primaryIso3);
      setActiveTab("compare");
    });

    installControls();
    fitWorldToData();
    updateMapMetric();
    updateComparePanel();
    updateGraphPanel();
    updateSourceNotes();
    highlightCountry(state.primaryIso3);
  }

  installControls();
  updateMapMetric();
  updateComparePanel();
  updateGraphPanel();
  updateSourceNotes();

  map = createMap();
  if (map) {
    map.on("load", initializeMapLayers);
  }
})();
