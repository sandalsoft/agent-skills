/**
 * Interactive D3.js Chart Template
 *
 * Framework-agnostic scatter plot with tooltips, zoom, grid lines,
 * click selection, and staggered entrance animation.
 *
 * Usage (vanilla JS):
 *   const svg = document.querySelector('#chart');
 *   drawInteractiveChart(sampleData, svg);
 */
import * as d3 from 'd3';

function drawInteractiveChart(data, container) {
  if (!data || data.length === 0) return;

  const svg = d3.select(container);
  svg.selectAll("*").remove();

  // Dimensions
  const width = 800;
  const height = 500;
  const margin = { top: 20, right: 30, bottom: 40, left: 50 };
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;

  svg.attr("width", width).attr("height", height);

  // Main group
  const g = svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

  // Scales
  const xScale = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.x)])
    .range([0, innerWidth]).nice();

  const yScale = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.y)])
    .range([innerHeight, 0]).nice();

  const sizeScale = d3.scaleSqrt()
    .domain([0, d3.max(data, d => d.size || 10)])
    .range([3, 20]);

  const colourScale = d3.scaleOrdinal(d3.schemeCategory10);

  // Zoom
  const zoom = d3.zoom()
    .scaleExtent([0.5, 10])
    .on("zoom", (event) => {
      g.attr("transform",
        `translate(${margin.left + event.transform.x},${margin.top + event.transform.y}) scale(${event.transform.k})`);
    });
  svg.call(zoom);

  // Axes
  g.append("g")
    .attr("class", "x-axis")
    .attr("transform", `translate(0,${innerHeight})`)
    .call(d3.axisBottom(xScale));

  g.append("g")
    .attr("class", "y-axis")
    .call(d3.axisLeft(yScale));

  // Grid lines
  g.append("g")
    .attr("class", "grid")
    .attr("opacity", 0.1)
    .call(d3.axisLeft(yScale).tickSize(-innerWidth).tickFormat(""));

  g.append("g")
    .attr("class", "grid")
    .attr("opacity", 0.1)
    .attr("transform", `translate(0,${innerHeight})`)
    .call(d3.axisBottom(xScale).tickSize(-innerHeight).tickFormat(""));

  // Tooltip
  const tooltip = d3.select("body").append("div")
    .style("position", "absolute")
    .style("display", "none")
    .style("padding", "10px")
    .style("background", "white")
    .style("border", "1px solid #ddd")
    .style("border-radius", "4px")
    .style("pointer-events", "none")
    .style("box-shadow", "0 2px 4px rgba(0,0,0,0.1)")
    .style("font-size", "13px")
    .style("z-index", "1000");

  // Data points
  const circles = g.selectAll("circle")
    .data(data)
    .join("circle")
    .attr("cx", d => xScale(d.x))
    .attr("cy", d => yScale(d.y))
    .attr("r", 0) // Start at 0 for entrance animation
    .attr("fill", d => colourScale(d.category || 'default'))
    .attr("stroke", "#fff")
    .attr("stroke-width", 2)
    .attr("opacity", 0.7)
    .style("cursor", "pointer");

  // Hover
  circles
    .on("mouseover", function (event, d) {
      d3.select(this).transition().duration(200)
        .attr("opacity", 1).attr("stroke-width", 3);
      tooltip.style("display", "block")
        .html(`<strong>${d.label || 'Point'}</strong><br/>
               X: ${d.x.toFixed(2)}<br/>
               Y: ${d.y.toFixed(2)}
               ${d.category ? `<br/>Category: ${d.category}` : ''}
               ${d.size ? `<br/>Size: ${d.size.toFixed(2)}` : ''}`);
    })
    .on("mousemove", function (event) {
      tooltip
        .style("left", (event.pageX + 10) + "px")
        .style("top", (event.pageY - 10) + "px");
    })
    .on("mouseout", function () {
      d3.select(this).transition().duration(200)
        .attr("opacity", 0.7).attr("stroke-width", 2);
      tooltip.style("display", "none");
    })
    .on("click", function (event, d) {
      circles.attr("stroke", "#fff").attr("stroke-width", 2);
      d3.select(this).attr("stroke", "#000").attr("stroke-width", 3);
      // Emit selection — wire into your app's state as needed
      svg.dispatch("point-selected", { detail: d, bubbles: true });
    });

  // Staggered entrance animation
  circles.transition()
    .duration(800)
    .delay((d, i) => i * 20)
    .attr("r", d => sizeScale(d.size || 10));

  // Axis labels
  g.append("text")
    .attr("x", innerWidth / 2)
    .attr("y", innerHeight + margin.bottom - 5)
    .attr("text-anchor", "middle")
    .style("font-size", "14px")
    .text("X Axis");

  g.append("text")
    .attr("transform", "rotate(-90)")
    .attr("x", -innerHeight / 2)
    .attr("y", -margin.left + 15)
    .attr("text-anchor", "middle")
    .style("font-size", "14px")
    .text("Y Axis");

  // Return cleanup function (removes tooltip)
  return () => tooltip.remove();
}

// Sample data
const sampleData = Array.from({ length: 50 }, (_, i) => ({
  id: i,
  label: `Point ${i + 1}`,
  x: Math.random() * 100,
  y: Math.random() * 100,
  size: Math.random() * 30 + 5,
  category: ['A', 'B', 'C', 'D'][Math.floor(Math.random() * 4)]
}));

export { drawInteractiveChart, sampleData };
