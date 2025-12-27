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

async function loadData() {
    const response = await fetch("data/freight_by_region.json");
    return response.json();
}

// Gráfico de Volume
async function loadChart() {
    const data = await loadData();

    const ctx = document.getElementById("chartRegion").getContext('2d');
    new Chart(ctx, {
        type: "bar",
        data: {
            labels: data.labels,
            datasets: [{
                label: "Quantidade",
                data: data.values,
                backgroundColor: colorPalette,
                borderRadius: 6,
                borderSkipped: false
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false,
            },
            plugins: {
                legend: legendPerPointConfig,
                tooltip: { enabled: true }
            },
            scales: {
                x: { grid: { display: false } },
                y: { grid: { color: '#F1F5F9' } }
            }
        }
    });
}

//Gráfico de Taxa de Atraso
async function loadDelayRateChart() {
    const response = await fetch("data/delay_rate_by_region.json");
    const data = await response.json();

    const ctx = document.getElementById("chartDelayRegion").getContext('2d');
    new Chart(ctx, {
        type: "doughnut", // Use "pie" se quiser fechado, "doughnut" é mais moderno
        data: {
            labels: data.labels,
            datasets: [{
                data: data.values,
                backgroundColor: colorPalette,
                borderColor: '#ffffff', // Borda branca para separar as fatias
                borderWidth: 2,
                hoverOffset: 10 // Efeito de expansão ao passar o mouse
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            layout: {
                padding: 20 // Um pouco de respiro
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'right', // Legenda na direita fica melhor em pizza
                    labels: {
                        usePointStyle: true,
                        boxWidth: 8,
                        padding: 20,
                        font: { size: 11 }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            const value = context.raw;
                            return ` ${context.label}: ${value.toFixed(1)}%`;
                        }
                    }
                }

            },
            // IMPORTANTE: Removemos o bloco 'scales' pois gráficos de pizza não têm eixos X/Y
        }
    });
}

//Gráfico Scatter
async function loadScatterChart() {
    const response = await fetch("data/revenue_vs_delay_by_freight_type.json");
    const rawData = await response.json();

    const datasets = rawData.map((item, index) => ({
        label: item.label,
        data: [{
            x: Number((item.x * 100).toFixed(1)),
            y: item.y
        }],
        pointRadius: 8,
        pointHoverRadius: 12,
        backgroundColor: colorPalette[index % colorPalette.length],
        borderColor: colorPalette[index % colorPalette.length],
    }));


    const ctx = document.getElementById("chartScatter").getContext('2d');
    new Chart(ctx, {
        type: "scatter",
        data: {
            datasets: datasets
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'nearest',
                intersect: true,
            },
            scales: {
                x: {
                    beginAtZero: true,
                    max: 100,
                    grid: { color: '#F1F5F9' },
                    title: { display: true, text: "Taxa de Atraso (%)" }
                },
                y: {
                    beginAtZero: true,
                    grid: { color: '#F1F5F9' },
                    title: { display: true, text: "Receita Total (R$)" }
                }
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'right',
                    labels: { usePointStyle: true }
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            const point = context.raw;
                            return `${context.dataset.label}: Atraso ${point.x}% | R$ ${point.y}`;
                        }
                    }
                }
            }
        }
    });
}

// Gráfico Performance
async function loadDriverPerformanceChart() {
    const response = await fetch("data/driver_performance.json");
    const data = await response.json();

    const ctx = document.getElementById("chartDrivers").getContext('2d');
    new Chart(ctx, {
        type: "bar",
        data: {
            labels: data.labels,
            datasets: [{
                label: "Desempenho",
                data: data.values,
                backgroundColor: colorPalette,
                borderRadius: 6,
                borderSkipped: false
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'nearest',
                axis: 'y',
                intersect: false
            },
            scales: {
                x: {
                    beginAtZero: true,
                    max: 100,
                    grid: { color: '#F1F5F9' },
                    title: { display: true, text: "Entregas no Prazo (%)" }
                },
                y: {
                    grid: { display: false }
                }
            },
            plugins: {
                legend: legendPerPointConfig,
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            return `Desempenho: ${context.raw}%`;
                        }
                    }
                }
            }
        }
    });
}

//Cards-KPI
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
loadChart();
loadDelayRateChart();
loadDriverPerformanceChart();
loadScatterChart();
