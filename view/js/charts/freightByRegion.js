export async function loadChart(colorPalette, legendPerPointConfig) {
    const response = await fetch("/api/dashboard/freight_by_region");
    const data = await response.json();

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
