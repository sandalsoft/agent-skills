---
name: d3js
description: Creating interactive data visualisations using d3.js. Use this skill whenever building custom charts, graphs, network diagrams, geographic visualisations, dashboards, or any SVG-based data visualisation that needs fine-grained control over visual elements, transitions, or interactions. Applies to any JavaScript environment — vanilla JS, React, Vue, Svelte, or others. Trigger this skill when users mention d3, data visualisation, custom charts, SVG graphics, force-directed graphs, choropleth maps, interactive plots, or when they need bespoke visualisations beyond what standard charting libraries provide.
---

# D3.js Visualisation

D3.js (Data-Driven Documents) binds data to DOM elements and applies data-driven transformations, giving you precise control over every visual element. It works in any JavaScript environment.

## When to use d3.js

**Use d3.js for:**
- Custom visualisations with unique layouts or encodings
- Interactive explorations with pan, zoom, or brush
- Network/graph visualisations (force-directed, trees, chords)
- Geographic visualisations with custom projections
- Smooth, choreographed transitions
- Publication-quality graphics with fine-grained styling
- Novel chart types not in standard libraries

**Consider alternatives for:**
- 3D visualisations — use Three.js

## Setup

```javascript
import * as d3 from 'd3';
```

Or CDN (v7): `<script src="https://d3js.org/d3.v7.min.js"></script>`

## Core workflow

Every d3 visualisation follows this structure:

```javascript
function drawChart(data, container) {
  if (!data || data.length === 0) return;

  const svg = d3.select(container);
  svg.selectAll("*").remove();

  // 1. Dimensions and margins
  const width = 800, height = 400;
  const margin = { top: 20, right: 30, bottom: 40, left: 50 };
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;

  // 2. Main group with margin offset
  const g = svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

  // 3. Scales — map data domain to pixel range
  const xScale = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.x)])
    .range([0, innerWidth]);

  const yScale = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.y)])
    .range([innerHeight, 0]); // Inverted for SVG coordinates

  // 4. Axes
  g.append("g")
    .attr("transform", `translate(0,${innerHeight})`)
    .call(d3.axisBottom(xScale));
  g.append("g")
    .call(d3.axisLeft(yScale));

  // 5. Binddata and create elements
  g.selectAll("circle")
    .data(data)
    .join("circle")
    .attr("cx", d => xScale(d.x))
    .attr("cy", d => yScale(d.y))
    .attr("r", 5)
    .attr("fill", "steelblue");
}
```

### Integration patterns

**Pattern A: Direct DOM manipulation** (recommended for most cases)
Use d3 to select and manipulate DOM elements imperatively. Works everywhere.

**Pattern B: Declarative rendering** (for frameworks with templating)
Use d3 for calculations (scales, layouts) but render elements through your framework:

```javascript
function getBarPositions(data) {
  const xScale = d3.scaleBand()
    .domain(data.map(d => d.label))
    .range([0, 400]).padding(0.1);
  const yScale = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.value)])
    .range([300, 0]);

  return data.map(d => ({
    x: xScale(d.label),
    y: yScale(d.value),
    width: xScale.bandwidth(),
    height: 300 - yScale(d.value)
  }));
}
// Then render via JSX, Svelte template, Vue template, etc.
```

Use Pattern A for complex visualisations with transitions or interactions. Use Pattern B for simpler charts where your framework handles rendering.

### Responsive sizing

```javascript
function makeResponsive(container, data) {
  const observer = new ResizeObserver(() => {
    const { width, height } = container.getBoundingClientRect();
    drawChart(data, container, width, height);
  });
  observer.observe(container);
  return () => observer.disconnect();
}
```

## Interactivity

### Tooltips

```javascript
const tooltip = d3.select("body").append("div")
  .style("position", "absolute")
  .style("visibility", "hidden")
  .style("background", "white")
  .style("border", "1px solid #ddd")
  .style("padding", "10px")
  .style("border-radius", "4px")
  .style("pointer-events", "none");

elements
  .on("mouseover", (event, d) => {
    tooltip.style("visibility", "visible")
      .html(`<strong>${d.label}</strong><br/>Value: ${d.value}`);
  })
  .on("mousemove", (event) => {
    tooltip
      .style("top", (event.pageY - 10) + "px")
      .style("left", (event.pageX + 10) + "px");
  })
  .on("mouseout", () => tooltip.style("visibility", "hidden"));
```

### Zoom and pan

```javascript
const zoom = d3.zoom()
  .scaleExtent([0.5, 10])
  .on("zoom", (event) => g.attr("transform", event.transform));
svg.call(zoom);
```

### Transitions

```javascript
// Basic
elements.transition().duration(750).attr("r", 10);

// Staggered entrance
elements.transition()
  .delay((d, i) => i * 50)
  .duration(500)
  .attr("cy", d => yScale(d.value));

// Easing
elements.transition().duration(1000)
  .ease(d3.easeBounceOut).attr("r", 10);
```

## Data preparation

Always clean data before visualising:

```javascript
const clean = data.filter(d => d.value != null && !isNaN(d.value));
const sorted = [...data].sort((a, b) => b.value - a.value);
const parsed = data.map(d => ({ ...d, date: d3.timeParse("%Y-%m-%d")(d.date) }));
```

## Best practices

**Performance** — For >1000 elements, consider canvas instead of SVG. Use `.join()` over separate enter/update/exit. Debounce resize handlers.

**Accessibility** — Add `role="img"` and `aria-label` to the SVG. Include `<title>` and `<desc>` elements. Ensure sufficient colour contrast. Provide data table alternatives. Never rely on colour alone — use patterns, labels, or shapes as redundant encoding.

**Styling** — Define colour palettes upfront. Apply consistent typography. Use subtle grid lines with `stroke-dasharray`.

## Troubleshooting

- **Axes not appearing**: Check scales have valid domains (no NaN). Verify axis group transforms.
- **Transitions not working**: Call `.transition()` before the attribute changes, not after. Ensure unique data keys for proper binding.
- **Responsive sizing not working**: Use ResizeObserver. Ensure SVG has `width`/`height` or `viewBox`.
- **Performance problems**: Reduce DOM elements, use canvas, debounce resize.

## References

Read these for detailed patterns and guidance beyond the core workflow above:

- **`references/d3-patterns.md`** — Complete code for specific chart types: bar, line, scatter, pie, area, stacked bar, grouped bar, bubble, heatmap, chord diagram, tree, treemap, sunburst, force network, geographic maps, brush/zoom interactions, and animation patterns. Start here when building a specific visualisation type.
- **`references/scale-reference.md`** — Deep dive into every d3 scale type (linear, log, power, time, band, point, ordinal, sequential, diverging, quantize, quantile, threshold) with use cases, methods, and advanced patterns like adaptive scales and multi-stop gradients.
- **`references/colour-schemes.md`** — Colour palette recommendations: built-in categorical/sequential/diverging schemes, colour-blind safe palettes (Okabe-Ito, Viridis, Cividis), semantic colour associations, WCAG contrast guidelines, and professional palettes for journalism, science, and business.

## Assets

Starter templates you can copy and adapt:

- **`assets/chart-template.js`** — Basic chart scaffold with margins, scales, axes, and data binding
- **`assets/interactive-template.js`** — Full interactive scatter plot with tooltips, zoom, grid lines, click selection, and staggered entrance animation
- **`assets/sample-data.json`** — Example datasets (time series, categorical, scatter, hierarchical, network, stacked, geographic, diverging)
