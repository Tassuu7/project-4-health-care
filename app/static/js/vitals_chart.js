/**
 * AegisCare Enterprise - Interactive SVG Vitals Trend Visualizer
 */

function renderVitalsChart(containerId, vitalsData) {
  const container = document.getElementById(containerId);
  if (!container) return;

  if (!vitalsData || vitalsData.length === 0) {
    container.innerHTML = "<p class='text-muted text-center p-4'>No historical vitals recorded.</p>";
    return;
  }

  const width = container.clientWidth || 600;
  const height = 240;
  const padding = 40;

  // Extract BP and Pulse points
  const points = vitalsData.map((v, i) => {
    const x = padding + (i / Math.max(1, vitalsData.length - 1)) * (width - 2 * padding);
    const sysY = height - padding - ((v.systolic_bp - 60) / 140) * (height - 2 * padding);
    const hrY = height - padding - ((v.heart_rate - 40) / 120) * (height - 2 * padding);
    return { x, sysY, hrY, sys: v.systolic_bp, hr: v.heart_rate };
  });

  const sysPath = points.map((p, i) => `${i === 0 ? "M" : "L"} ${p.x} ${p.sysY}`).join(" ");
  const hrPath = points.map((p, i) => `${i === 0 ? "M" : "L"} ${p.x} ${p.hrY}`).join(" ");

  const svg = `
    <svg class="svg-chart" viewBox="0 0 ${width} ${height}">
      <!-- Grid lines -->
      <line x1="${padding}" y1="${padding}" x2="${width - padding}" y2="${padding}" class="chart-grid-line" />
      <line x1="${padding}" y1="${height / 2}" x2="${width - padding}" y2="${height / 2}" class="chart-grid-line" />
      <line x1="${padding}" y1="${height - padding}" x2="${width - padding}" y2="${height - padding}" class="chart-grid-line" />
      
      <!-- Axis Labels -->
      <text x="10" y="${padding + 4}" class="chart-axis-text">200 mmHg</text>
      <text x="10" y="${height / 2 + 4}" class="chart-axis-text">130 mmHg</text>
      <text x="10" y="${height - padding + 4}" class="chart-axis-text">60 mmHg</text>
      
      <!-- Trend lines -->
      <path d="${sysPath}" class="vitals-trend-line" />
      <path d="${hrPath}" class="vitals-pulse-line" />
      
      <!-- Data points -->
      ${points.map(p => `<circle cx="${p.x}" cy="${p.sysY}" r="4" fill="#2563eb" />`).join("")}
      ${points.map(p => `<circle cx="${p.x}" cy="${p.hrY}" r="4" fill="#dc2626" />`).join("")}
    </svg>
  `;
  container.innerHTML = svg;
}
