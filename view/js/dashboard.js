import { loadDriverPerformanceChart } from "./charts/driverPerformance.js";
import { loadScatterChart } from "./charts/revenueVsDelay.js";
import { loadDelayRateChart } from "./charts/delayByRegion.js";
import { loadChart } from "./charts/freightByRegion.js";

Chart.defaults.font.family = "'Geist', sans-serif";
Chart.defaults.color = '#64748B';

const colorPalette = [
    '#6366F1', '#10B981', '#F59E0B', '#EC4899',
    '#3B82F6', '#8B5CF6', '#EF4444', '#06B6D4'
];

const legendPerPointConfig = {
    display: true,
    position: 'top',
    labels: {
        usePointStyle: true,
        boxWidth: 8,
        generateLabels: (chart) => {
            const data = chart.data;
            if (data.labels.length && data.datasets.length) {
                return data.labels.map((label, i) => {
                    const ds = data.datasets[0];
                    const color = Array.isArray(ds.backgroundColor)
                        ? ds.backgroundColor[i % ds.backgroundColor.length]
                        : ds.backgroundColor;

                    return {
                        text: label,
                        fillStyle: color,
                        strokeStyle: color,
                        hidden: !chart.getDataVisibility(i),
                        index: i
                    };
                });
            }
            return [];
        }
    },
    onClick: (evt, legendItem, legend) => {
        const index = legendItem.index;
        const chart = legend.chart;
        chart.toggleDataVisibility(index);
        chart.update();
    }
};

async function loadKPIs() {
    try {
        const kpis = await fetch("/api/dashboard/kpis").then(r => r.json());

        document.getElementById("kpiFreights").textContent = kpis.total_freights;
        document.getElementById("kpiDrivers").textContent = kpis.total_drivers;
        document.getElementById("kpiDelayed").textContent = kpis.delayed_freights;
        document.getElementById("kpiRevenue").textContent = `R$ ${kpis.total_revenue.toLocaleString("pt-BR")}`;
    } catch (err) {
        console.error("Error loading KPIs:", err);
    }
}

loadKPIs();
loadChart(colorPalette, legendPerPointConfig);
loadDelayRateChart(colorPalette);
loadDriverPerformanceChart(colorPalette, legendPerPointConfig);
loadScatterChart(colorPalette);
