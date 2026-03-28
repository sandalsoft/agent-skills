# D3.js Visualisation Patterns

Complete code patterns for common visualisation types. All examples use vanilla JavaScript with direct DOM manipulation (Pattern A from SKILL.md). Adapt for your framework as needed.

## Table of contents

- [Basic charts](#basic-charts): Bar, Line, Scatter, Pie
- [Stacked and grouped](#stacked-and-grouped): Stacked bar, Grouped bar, Area with gradient
- [Specialised charts](#specialised-charts): Bubble, Heatmap, Chord diagram
- [Hierarchical](#hierarchical): Tree, Treemap, Sunburst
- [Geographic](#geographic): Map with points, Choropleth
- [Network](#network): Force-directed graph
- [Interactions](#interactions): Brush and zoom, Linked brushing
- [Animation](#animation): Enter/update/exit, Path morphing

---

## Basic charts

### Bar chart

```javascript
function drawBarChart(data, container) {
  if (!data || data.length === 0) return;

  const svg = d3.select(container);
  svg.selectAll("*").remove();

  const width = 800, height = 400;
  const margin = { top: 20, right: 30, bottom: 40, left: 50 };
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;

  const g = svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

  const xScale = d3.scaleBand()
    .domain(data.map(d => d.category))
    .range([0, innerWidth])
    .padding(0.1);

  const yScale = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.value)])
    .range([innerHeight, 0]);

  g.append("g")
    .attr("transform", `translate(0,${innerHeight})`)
    .call(d3.axisBottom(xScale));
  g.append("g")
    .call(d3.axisLeft(yScale));

  g.selectAll("rect")
    .data(data)
    .join("rect")
    .attr("x", d => xScale(d.category))
    .attr("y", d => yScale(d.value))
    .attr("width", xScale.bandwidth())
    .attr("height", d => innerHeight - yScale(d.value))
    .attr("fill", "steelblue");
}
```

### Line chart

```javascript
function drawLineChart(data, container) {
  if (!data || data.length === 0) return;

  const svg = d3.select(container);
  svg.selectAll("*").remove();

  const width = 800, height = 400;
  const margin = { top: 20, right: 30, bottom: 40, left: 50 };
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;

  const g = svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

  const xScale = d3.scaleTime()
    .domain(d3.extent(data, d => d.date))
    .range([0, innerWidth]);

  const yScale = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.value)])
    .range([innerHeight, 0]);

  g.append("g")
    .attr("transform", `translate(0,${innerHeight})`)
    .call(d3.axisBottom(xScale));
  g.append("g")
    .call(d3.axisLeft(yScale));

  const line = d3.line()
    .x(d => xScale(d.date))
    .y(d => yScale(d.value))
    .curve(d3.curveMonotoneX);

  g.append("path")
    .datum(data)
    .attr("fill", "none")
    .attr("stroke", "steelblue")
    .attr("stroke-width", 2)
    .attr("d", line);
}
```

### Scatter plot

```javascript
function drawScatter(data, container) {
  if (!data || data.length === 0) return;

  const svg = d3.select(container);
  svg.selectAll("*").remove();

  const width = 800, height = 400;
  const margin = { top: 20, right: 30, bottom: 40, left: 50 };
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;

  const g = svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

  const xScale = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.x)]).range([0, innerWidth]);
  const yScale = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.y)]).range([innerHeight, 0]);
  const colourScale = d3.scaleOrdinal(d3.schemeCategory10);

  g.append("g").attr("transform", `translate(0,${innerHeight})`).call(d3.axisBottom(xScale));
  g.append("g").call(d3.axisLeft(yScale));

  g.selectAll("circle")
    .data(data)
    .join("circle")
    .attr("cx", d => xScale(d.x))
    .attr("cy", d => yScale(d.y))
    .attr("r", d => d.size ? d3.scaleSqrt().domain([0, d3.max(data, d => d.size)]).range([3, 20])(d.size) : 5)
    .attr("fill", d => colourScale(d.category))
    .attr("opacity", 0.7);
}
```

### Pie chart

```javascript
function drawPieChart(data, container) {
  if (!data || data.length === 0) return;

  const svg = d3.select(container);
  svg.selectAll("*").remove();

  const width = 400, height = 400;
  const radius = Math.min(width, height) / 2 - 20;

  const pie = d3.pie().value(d => d.value).sort(null);
  const arc = d3.arc().innerRadius(0).outerRadius(radius);
  const colourScale = d3.scaleOrdinal(d3.schemeCategory10);

  const g = svg.append("g")
    .attr("transform", `translate(${width / 2},${height / 2})`);

  g.selectAll("path")
    .data(pie(data))
    .join("path")
    .attr("d", arc)
    .attr("fill", (d, i) => colourScale(i))
    .attr("stroke", "white")
    .attr("stroke-width", 2);

  // Labels
  const labelArc = d3.arc().innerRadius(radius * 0.6).outerRadius(radius * 0.6);
  g.selectAll("text")
    .data(pie(data))
    .join("text")
    .attr("transform", d => `translate(${labelArc.centroid(d)})`)
    .attr("text-anchor", "middle")
    .attr("dy", "0.35em")
    .style("font-size", "12px")
    .text(d => d.data.label);
}
```

---

## Stacked and grouped

### Stacked bar chart

```javascript
function drawStackedBar(data, container) {
  // data: [{ group: 'Q1', seriesA: 30, seriesB: 40, seriesC: 25 }, ...]
  if (!data || data.length === 0) return;

  const svg = d3.select(container);
  svg.selectAll("*").remove();

  const width = 800, height = 400;
  const margin = { top: 20, right: 30, bottom: 40, left: 50 };
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;

  const g = svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

  const categories = Object.keys(data[0]).filter(k => k !== 'group');
  const stackedData = d3.stack().keys(categories)(data);

  const xScale = d3.scaleBand()
    .domain(data.map(d => d.group))
    .range([0, innerWidth]).padding(0.1);

  const yScale = d3.scaleLinear()
    .domain([0, d3.max(stackedData[stackedData.length - 1], d => d[1])])
    .range([innerHeight, 0]);

  const colourScale = d3.scaleOrdinal(d3.schemeCategory10);

  g.selectAll("g.series")
    .data(stackedData)
    .join("g")
    .attr("class", "series")
    .attr("fill", (d, i) => colourScale(i))
    .selectAll("rect")
    .data(d => d)
    .join("rect")
    .attr("x", d => xScale(d.data.group))
    .attr("y", d => yScale(d[1]))
    .attr("height", d => yScale(d[0]) - yScale(d[1]))
    .attr("width", xScale.bandwidth());

  g.append("g").attr("transform", `translate(0,${innerHeight})`).call(d3.axisBottom(xScale));
  g.append("g").call(d3.axisLeft(yScale));
}
```

### Grouped bar chart

```javascript
function drawGroupedBar(data, container) {
  // data: [{ group: 'Q1', seriesA: 30, seriesB: 40 }, ...]
  if (!data || data.length === 0) return;

  const svg = d3.select(container);
  svg.selectAll("*").remove();

  const width = 800, height = 400;
  const margin = { top: 20, right: 30, bottom: 40, left: 50 };
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;

  const g = svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

  const categories = Object.keys(data[0]).filter(k => k !== 'group');

  const x0 = d3.scaleBand().domain(data.map(d => d.group)).range([0, innerWidth]).padding(0.1);
  const x1 = d3.scaleBand().domain(categories).range([0, x0.bandwidth()]).padding(0.05);
  const yScale = d3.scaleLinear()
    .domain([0, d3.max(data, d => Math.max(...categories.map(c => d[c])))])
    .range([innerHeight, 0]);
  const colourScale = d3.scaleOrdinal(d3.schemeCategory10);

  g.selectAll("g.group")
    .data(data)
    .join("g")
    .attr("class", "group")
    .attr("transform", d => `translate(${x0(d.group)},0)`)
    .selectAll("rect")
    .data(d => categories.map(key => ({ key, value: d[key] })))
    .join("rect")
    .attr("x", d => x1(d.key))
    .attr("y", d => yScale(d.value))
    .attr("width", x1.bandwidth())
    .attr("height", d => innerHeight - yScale(d.value))
    .attr("fill", d => colourScale(d.key));

  g.append("g").attr("transform", `translate(0,${innerHeight})`).call(d3.axisBottom(x0));
  g.append("g").call(d3.axisLeft(yScale));
}
```

### Area chart with gradient

```javascript
function drawAreaChart(data, container) {
  if (!data || data.length === 0) return;

  const svg = d3.select(container);
  svg.selectAll("*").remove();

  const width = 800, height = 400;
  const margin = { top: 20, right: 30, bottom: 40, left: 50 };
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;

  // Gradient definition
  const defs = svg.append("defs");
  const gradient = defs.append("linearGradient")
    .attr("id", "areaGradient")
    .attr("x1", "0%").attr("x2", "0%")
    .attr("y1", "0%").attr("y2", "100%");
  gradient.append("stop").attr("offset", "0%")
    .attr("stop-color", "steelblue").attr("stop-opacity", 0.8);
  gradient.append("stop").attr("offset", "100%")
    .attr("stop-color", "steelblue").attr("stop-opacity", 0.1);

  const g = svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

  const xScale = d3.scaleTime()
    .domain(d3.extent(data, d => d.date)).range([0, innerWidth]);
  const yScale = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.value)]).range([innerHeight, 0]);

  const area = d3.area()
    .x(d => xScale(d.date))
    .y0(innerHeight)
    .y1(d => yScale(d.value))
    .curve(d3.curveMonotoneX);

  g.append("path").datum(data).attr("fill", "url(#areaGradient)").attr("d", area);

  const line = d3.line()
    .x(d => xScale(d.date))
    .y(d => yScale(d.value))
    .curve(d3.curveMonotoneX);

  g.append("path").datum(data)
    .attr("fill", "none").attr("stroke", "steelblue").attr("stroke-width", 2).attr("d", line);

  g.append("g").attr("transform", `translate(0,${innerHeight})`).call(d3.axisBottom(xScale));
  g.append("g").call(d3.axisLeft(yScale));
}
```

---

## Specialised charts

### Bubble chart

```javascript
function drawBubbleChart(data, container) {
  if (!data || data.length === 0) return;

  const svg = d3.select(container);
  svg.selectAll("*").remove();

  const width = 800, height = 600;
  const margin = { top: 20, right: 30, bottom: 40, left: 50 };
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;

  const g = svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

  const xScale = d3.scaleLinear().domain([0, d3.max(data, d => d.x)]).range([0, innerWidth]);
  const yScale = d3.scaleLinear().domain([0, d3.max(data, d => d.y)]).range([innerHeight, 0]);
  const sizeScale = d3.scaleSqrt().domain([0, d3.max(data, d => d.size)]).range([0, 50]);
  const colourScale = d3.scaleOrdinal(d3.schemeCategory10);

  g.selectAll("circle")
    .data(data)
    .join("circle")
    .attr("cx", d => xScale(d.x))
    .attr("cy", d => yScale(d.y))
    .attr("r", d => sizeScale(d.size))
    .attr("fill", d => colourScale(d.category))
    .attr("opacity", 0.6)
    .attr("stroke", "white")
    .attr("stroke-width", 2);

  g.append("g").attr("transform", `translate(0,${innerHeight})`).call(d3.axisBottom(xScale));
  g.append("g").call(d3.axisLeft(yScale));
}
```

### Heatmap

```javascript
function drawHeatmap(data, container) {
  // data: [{ row: 'Monday', column: 'Morning', value: 42 }, ...]
  if (!data || data.length === 0) return;

  const svg = d3.select(container);
  svg.selectAll("*").remove();

  const width = 800, height = 600;
  const margin = { top: 100, right: 60, bottom: 30, left: 100 };
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;

  const rows = Array.from(new Set(data.map(d => d.row)));
  const columns = Array.from(new Set(data.map(d => d.column)));

  const g = svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

  const xScale = d3.scaleBand().domain(columns).range([0, innerWidth]).padding(0.01);
  const yScale = d3.scaleBand().domain(rows).range([0, innerHeight]).padding(0.01);
  const colourScale = d3.scaleSequential(d3.interpolateYlOrRd)
    .domain([0, d3.max(data, d => d.value)]);

  g.selectAll("rect")
    .data(data)
    .join("rect")
    .attr("x", d => xScale(d.column))
    .attr("y", d => yScale(d.row))
    .attr("width", xScale.bandwidth())
    .attr("height", yScale.bandwidth())
    .attr("fill", d => colourScale(d.value));

  // Column labels
  g.selectAll(".col-label")
    .data(columns)
    .join("text")
    .attr("class", "col-label")
    .attr("x", d => xScale(d) + xScale.bandwidth() / 2)
    .attr("y", -10)
    .attr("text-anchor", "middle")
    .style("font-size", "12px")
    .text(d => d);

  // Row labels
  g.selectAll(".row-label")
    .data(rows)
    .join("text")
    .attr("class", "row-label")
    .attr("x", -10)
    .attr("y", d => yScale(d) + yScale.bandwidth() / 2)
    .attr("dy", "0.35em")
    .attr("text-anchor", "end")
    .style("font-size", "12px")
    .text(d => d);

  // Colour legend
  const legendHeight = 200, legendWidth = 20;
  const legend = svg.append("g")
    .attr("transform", `translate(${width - 50},${margin.top})`);
  const legendScale = d3.scaleLinear().domain(colourScale.domain()).range([legendHeight, 0]);

  for (let i = 0; i < legendHeight; i++) {
    legend.append("rect")
      .attr("y", i).attr("width", legendWidth).attr("height", 1)
      .attr("fill", colourScale(legendScale.invert(i)));
  }
  legend.append("g")
    .attr("transform", `translate(${legendWidth},0)`)
    .call(d3.axisRight(legendScale).ticks(5));
}
```

### Chord diagram

```javascript
function drawChordDiagram(data, container) {
  // data: [{ source: 'A', target: 'B', value: 10 }, ...]
  if (!data || data.length === 0) return;

  const svg = d3.select(container);
  svg.selectAll("*").remove();

  const width = 600, height = 600;
  const innerRadius = Math.min(width, height) * 0.3;
  const outerRadius = innerRadius + 30;

  const nodes = Array.from(new Set(data.flatMap(d => [d.source, d.target])));
  const matrix = Array.from({ length: nodes.length }, () => Array(nodes.length).fill(0));
  data.forEach(d => {
    const i = nodes.indexOf(d.source), j = nodes.indexOf(d.target);
    matrix[i][j] += d.value;
    matrix[j][i] += d.value;
  });

  const chord = d3.chord().padAngle(0.05).sortSubgroups(d3.descending);
  const arc = d3.arc().innerRadius(innerRadius).outerRadius(outerRadius);
  const ribbon = d3.ribbon().source(d => d.source).target(d => d.target);
  const colourScale = d3.scaleOrdinal(d3.schemeCategory10).domain(nodes);

  const g = svg.append("g")
    .attr("transform", `translate(${width / 2},${height / 2})`);
  const chords = chord(matrix);

  // Ribbons
  g.append("g").attr("fill-opacity", 0.67)
    .selectAll("path").data(chords).join("path")
    .attr("d", ribbon)
    .attr("fill", d => colourScale(nodes[d.source.index]))
    .attr("stroke", d => d3.rgb(colourScale(nodes[d.source.index])).darker());

  // Arcs
  const group = g.append("g").selectAll("g").data(chords.groups).join("g");
  group.append("path")
    .attr("d", arc)
    .attr("fill", d => colourScale(nodes[d.index]))
    .attr("stroke", d => d3.rgb(colourScale(nodes[d.index])).darker());

  // Labels
  group.append("text")
    .each(d => { d.angle = (d.startAngle + d.endAngle) / 2; })
    .attr("dy", "0.31em")
    .attr("transform", d =>
      `rotate(${(d.angle * 180 / Math.PI) - 90})translate(${outerRadius + 30})${d.angle > Math.PI ? "rotate(180)" : ""}`)
    .attr("text-anchor", d => d.angle > Math.PI ? "end" : null)
    .text((d, i) => nodes[i])
    .style("font-size", "12px");
}
```

---

## Hierarchical

### Tree diagram

```javascript
function drawTree(data, container) {
  if (!data) return;

  const svg = d3.select(container);
  svg.selectAll("*").remove();

  const width = 800, height = 600;
  const tree = d3.tree().size([height - 100, width - 200]);
  const root = d3.hierarchy(data);
  tree(root);

  const g = svg.append("g").attr("transform", "translate(100,50)");

  // Links
  g.selectAll("path")
    .data(root.links())
    .join("path")
    .attr("d", d3.linkHorizontal().x(d => d.y).y(d => d.x))
    .attr("fill", "none")
    .attr("stroke", "#555")
    .attr("stroke-width", 2);

  // Nodes
  const node = g.selectAll("g.node")
    .data(root.descendants())
    .join("g")
    .attr("class", "node")
    .attr("transform", d => `translate(${d.y},${d.x})`);

  node.append("circle")
    .attr("r", 6)
    .attr("fill", d => d.children ? "#555" : "#999");

  node.append("text")
    .attr("dy", "0.31em")
    .attr("x", d => d.children ? -8 : 8)
    .attr("text-anchor", d => d.children ? "end" : "start")
    .text(d => d.data.name)
    .style("font-size", "12px");
}
```

### Treemap

```javascript
function drawTreemap(data, container) {
  if (!data) return;

  const svg = d3.select(container);
  svg.selectAll("*").remove();

  const width = 800, height = 600;
  const root = d3.hierarchy(data).sum(d => d.value).sort((a, b) => b.value - a.value);

  d3.treemap().size([width, height]).padding(2).round(true)(root);

  const colourScale = d3.scaleOrdinal(d3.schemeCategory10);

  const cell = svg.selectAll("g")
    .data(root.leaves())
    .join("g")
    .attr("transform", d => `translate(${d.x0},${d.y0})`);

  cell.append("rect")
    .attr("width", d => d.x1 - d.x0)
    .attr("height", d => d.y1 - d.y0)
    .attr("fill", d => colourScale(d.parent.data.name))
    .attr("stroke", "white")
    .attr("stroke-width", 2);

  cell.append("text")
    .attr("x", 4).attr("y", 16)
    .text(d => d.data.name)
    .style("font-size", "12px")
    .style("fill", "white");
}
```

### Sunburst diagram

```javascript
function drawSunburst(data, container) {
  if (!data) return;

  const svg = d3.select(container);
  svg.selectAll("*").remove();

  const width = 600, height = 600;
  const radius = Math.min(width, height) / 2;

  const root = d3.hierarchy(data).sum(d => d.value).sort((a, b) => b.value - a.value);
  d3.partition().size([2 * Math.PI, radius])(root);

  const arc = d3.arc()
    .startAngle(d => d.x0).endAngle(d => d.x1)
    .innerRadius(d => d.y0).outerRadius(d => d.y1);

  const colourScale = d3.scaleOrdinal(d3.schemeCategory10);

  svg.append("g")
    .attr("transform", `translate(${width / 2},${height / 2})`)
    .selectAll("path")
    .data(root.descendants())
    .join("path")
    .attr("d", arc)
    .attr("fill", d => colourScale(d.depth))
    .attr("stroke", "white")
    .attr("stroke-width", 1);
}
```

---

## Geographic

### Map with points

```javascript
function drawMapWithPoints(geoData, pointData, container) {
  if (!geoData || !pointData) return;

  const svg = d3.select(container);
  svg.selectAll("*").remove();

  const width = 800, height = 600;
  const projection = d3.geoMercator().fitSize([width, height], geoData);
  const pathGenerator = d3.geoPath().projection(projection);

  svg.selectAll("path")
    .data(geoData.features)
    .join("path")
    .attr("d", pathGenerator)
    .attr("fill", "#e0e0e0")
    .attr("stroke", "#999")
    .attr("stroke-width", 0.5);

  svg.selectAll("circle")
    .data(pointData)
    .join("circle")
    .attr("cx", d => projection([d.longitude, d.latitude])[0])
    .attr("cy", d => projection([d.longitude, d.latitude])[1])
    .attr("r", 5)
    .attr("fill", "steelblue")
    .attr("opacity", 0.7);
}
```

### Choropleth map

```javascript
function drawChoropleth(geoData, valueData, container) {
  if (!geoData || !valueData) return;

  const svg = d3.select(container);
  svg.selectAll("*").remove();

  const width = 800, height = 600;
  const projection = d3.geoMercator().fitSize([width, height], geoData);
  const pathGenerator = d3.geoPath().projection(projection);

  const valueLookup = new Map(valueData.map(d => [d.id, d.value]));
  const colourScale = d3.scaleSequential(d3.interpolateBlues)
    .domain([0, d3.max(valueData, d => d.value)]);

  svg.selectAll("path")
    .data(geoData.features)
    .join("path")
    .attr("d", pathGenerator)
    .attr("fill", d => {
      const value = valueLookup.get(d.id);
      return value ? colourScale(value) : "#e0e0e0";
    })
    .attr("stroke", "#999")
    .attr("stroke-width", 0.5);
}
```

---

## Network

### Force-directed graph

```javascript
function drawForceGraph(nodes, links, container) {
  if (!nodes || !links) return;

  const svg = d3.select(container);
  svg.selectAll("*").remove();

  const width = 800, height = 600;

  const simulation = d3.forceSimulation(nodes)
    .force("link", d3.forceLink(links).id(d => d.id).distance(100))
    .force("charge", d3.forceManyBody().strength(-300))
    .force("center", d3.forceCenter(width / 2, height / 2));

  const link = svg.selectAll("line")
    .data(links)
    .join("line")
    .attr("stroke", "#999")
    .attr("stroke-width", 1);

  const node = svg.selectAll("circle")
    .data(nodes)
    .join("circle")
    .attr("r", 8)
    .attr("fill", "steelblue")
    .call(d3.drag()
      .on("start", (event) => {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        event.subject.fx = event.subject.x;
        event.subject.fy = event.subject.y;
      })
      .on("drag", (event) => {
        event.subject.fx = event.x;
        event.subject.fy = event.y;
      })
      .on("end", (event) => {
        if (!event.active) simulation.alphaTarget(0);
        event.subject.fx = null;
        event.subject.fy = null;
      }));

  simulation.on("tick", () => {
    link
      .attr("x1", d => d.source.x).attr("y1", d => d.source.y)
      .attr("x2", d => d.target.x).attr("y2", d => d.target.y);
    node.attr("cx", d => d.x).attr("cy", d => d.y);
  });
}
```

---

## Interactions

### Brush and zoom

```javascript
function drawBrushableScatter(data, container) {
  if (!data || data.length === 0) return;

  const svg = d3.select(container);
  svg.selectAll("*").remove();

  const width = 800, height = 400;
  const margin = { top: 20, right: 30, bottom: 40, left: 50 };
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;

  const g = svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

  const xScale = d3.scaleLinear().domain([0, d3.max(data, d => d.x)]).range([0, innerWidth]);
  const yScale = d3.scaleLinear().domain([0, d3.max(data, d => d.y)]).range([innerHeight, 0]);

  const circles = g.selectAll("circle")
    .data(data)
    .join("circle")
    .attr("cx", d => xScale(d.x))
    .attr("cy", d => yScale(d.y))
    .attr("r", 5)
    .attr("fill", "steelblue");

  const brush = d3.brush()
    .extent([[0, 0], [innerWidth, innerHeight]])
    .on("start brush", (event) => {
      if (!event.selection) return;
      const [[x0, y0], [x1, y1]] = event.selection;
      circles.attr("fill", d => {
        const cx = xScale(d.x), cy = yScale(d.y);
        return (cx >= x0 && cx <= x1 && cy >= y0 && cy <= y1) ? "orange" : "steelblue";
      });
    });

  g.append("g").attr("class", "brush").call(brush);
}
```

### Linked brushing between charts

Use a shared selection state and redraw both charts when the brush changes. Each chart reads the same `selectedIds` set to determine highlight colour.

```javascript
function drawLinkedCharts(data, container1, container2) {
  let selectedIds = new Set();

  function drawScatter() {
    const svg = d3.select(container1);
    // ... scales, axes ...
    svg.selectAll("circle").data(data).join("circle")
      .attr("fill", d => selectedIds.has(d.id) ? "orange" : "steelblue");
  }

  function drawBars() {
    const svg = d3.select(container2);
    // ... scales, axes ...
    svg.selectAll("rect").data(data).join("rect")
      .attr("fill", d => selectedIds.has(d.id) ? "orange" : "steelblue");
  }

  // Brush on scatter updates selectedIds, then redraws both
  const brush = d3.brush().on("brush end", (event) => {
    if (!event.selection) { selectedIds.clear(); }
    else {
      const [[x0, y0], [x1, y1]] = event.selection;
      selectedIds = new Set(data.filter(d => {
        const cx = xScale(d.x), cy = yScale(d.y);
        return cx >= x0 && cx <= x1 && cy >= y0 && cy <= y1;
      }).map(d => d.id));
    }
    drawScatter();
    drawBars();
  });
}
```

---

## Animation

### Enter, update, exit with transitions

Use a key function for object constancy so d3 can track which elements are new, updated, or removed:

```javascript
function updateChart(data, container) {
  const svg = d3.select(container);

  const circles = svg.selectAll("circle")
    .data(data, d => d.id); // Key function

  // EXIT
  circles.exit()
    .transition().duration(500)
    .attr("r", 0)
    .remove();

  // UPDATE
  circles
    .transition().duration(500)
    .attr("cx", d => xScale(d.x))
    .attr("cy", d => yScale(d.y));

  // ENTER
  circles.enter()
    .append("circle")
    .attr("cx", d => xScale(d.x))
    .attr("cy", d => yScale(d.y))
    .attr("r", 0)
    .attr("fill", "steelblue")
    .transition().duration(500)
    .attr("r", 5);
}
```

### Path morphing

```javascript
function morphPath(data1, data2, container) {
  const svg = d3.select(container);
  const line = d3.line()
    .x(d => xScale(d.x))
    .y(d => yScale(d.y))
    .curve(d3.curveMonotoneX);

  svg.select("path")
    .datum(data1)
    .attr("d", line)
    .transition().duration(1000)
    .attrTween("d", function () {
      const previous = d3.select(this).attr("d");
      const current = line(data2);
      return d3.interpolatePath(previous, current);
    });
}
```
