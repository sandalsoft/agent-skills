/**
 * Basic D3.js Chart Template
 *
 * Framework-agnostic scaffold with margins, scales, axes, and data binding.
 * Adapt for React (useEffect + ref), Svelte ($effect + bind:this), Vue (onMounted + ref), etc.
 *
 * Usage (vanilla JS):
 *   const svg = document.querySelector('#chart');
 *   drawBarChart(sampleData, svg);
 */
import * as d3 from 'd3';

function drawBarChart(data, container) {
  if (!data || data.length === 0) return;

  const svg = d3.select(container);
  svg.selectAll("*").remove();

  // 1. Dimensions and margins
  const width = 800;
  const height = 400;
  const margin = { top: 20, right: 30, bottom: 40, left: 50 };
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;

  // 2. Main group offset by margins
  const g = svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

  // 3. Scales
  const xScale = d3.scaleBand()
    .domain(data.map(d => d.label))
    .range([0, innerWidth])
    .padding(0.1);

  const yScale = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.value)])
    .range([innerHeight, 0])
    .nice();

  // 4. Axes
  g.append("g")
    .attr("class", "x-axis")
    .attr("transform", `translate(0,${innerHeight})`)
    .call(d3.axisBottom(xScale));

  g.append("g")
    .attr("class", "y-axis")
    .call(d3.axisLeft(yScale));

  // 5. Data binding
  g.selectAll("rect")
    .data(data)
    .join("rect")
    .attr("x", d => xScale(d.label))
    .attr("y", d => yScale(d.value))
    .attr("width", xScale.bandwidth())
    .attr("height", d => innerHeight - yScale(d.value))
    .attr("fill", "steelblue");

  // 6. Axis labels
  g.append("text")
    .attr("class", "axis-label")
    .attr("x", innerWidth / 2)
    .attr("y", innerHeight + margin.bottom - 5)
    .attr("text-anchor", "middle")
    .text("Category");

  g.append("text")
    .attr("class", "axis-label")
    .attr("transform", "rotate(-90)")
    .attr("x", -innerHeight / 2)
    .attr("y", -margin.left + 15)
    .attr("text-anchor", "middle")
    .text("Value");
}

// Sample data
const sampleData = [
  { label: 'A', value: 30 },
  { label: 'B', value: 80 },
  { label: 'C', value: 45 },
  { label: 'D', value: 60 },
  { label: 'E', value: 20 },
  { label: 'F', value: 90 }
];

export { drawBarChart, sampleData };
