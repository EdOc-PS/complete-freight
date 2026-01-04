export async function loadDelayRateChart(colorPalette) {
    const response = await fetch("/api/dashboard/delay_by_region");
    const data = await response.json();

    const ctx = document.getElementById("chartDelayRegion").getContext('2d');
    new Chart(ctx, {
        type: "doughnut", 
        data: {
            labels: data.labels,
            datasets: [{
                data: data.values,
                backgroundColor: colorPalette,
                borderColor: '#ffffff', 
                borderWidth: 2,
                hoverOffset: 10 
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            layout: {
                padding: 20
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'right',
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
        }
    });
}