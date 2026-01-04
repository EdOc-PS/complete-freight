export async function loadDriverPerformanceChart(colorPalette, legendPerPointConfig) {
    const response = await fetch("/api/dashboard/driver_performance");
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
