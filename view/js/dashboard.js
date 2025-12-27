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
    const freights = await fetch("/data/freights.json").then(r => r.json());
    const drivers = await fetch("/data/drivers.json").then(r => r.json());

    const totalFreights = freights.length;
    const totalDrivers = drivers.length;

    const delayedFreights = freights.filter(
        f => new Date(f.delivery_date) > new Date(f.expected_date)
    ).length;

    const totalRevenue = freights.reduce(
        (sum, f) => sum + f.value, 0
    );

    document.getElementById("kpiFreights").textContent = totalFreights;
    document.getElementById("kpiDrivers").textContent = totalDrivers;
    document.getElementById("kpiDelayed").textContent = delayedFreights;
    document.getElementById("kpiRevenue").textContent = `R$ ${totalRevenue.toLocaleString("pt-BR")}`;
}

loadKPIs();
loadChart(colorPalette, legendPerPointConfig);
loadDelayRateChart(colorPalette);
loadDriverPerformanceChart(colorPalette, legendPerPointConfig);
loadScatterChart(colorPalette);
