export async function loadScatterChart(colorPalette) {
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