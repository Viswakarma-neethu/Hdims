console.log("analytics_charts.js Loaded...");

// Initialize charts when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    const config = document.getElementById('chart-config');
    if (!config) {
        console.error("Configuration element not found");
        return;
    }

    const isAdmin = config.dataset.isAdmin === 'true';

    if (isAdmin) {
        initializeChart('diseaseChart', 'disease-data', 'pie');
        initializeChart('appointmentTrendChart', 'appointment-data', 'line');
        initializeChart('genderAgeChart', 'gender-data', 'bar');
    } else {
        initializeChart('personalHealthTrendChart', 'personal-data', 'line');
    }

    // Function to initialize Chart
    function initializeChart(canvasId, scriptId, chartType) {
        const container = document.querySelector(`#${canvasId}`).parentElement;
        const canvas = document.getElementById(canvasId);
        const loadingEl = container.querySelector('.chart-loading');

        try {
            const rawData = JSON.parse(document.getElementById(scriptId).textContent);

            new Chart(canvas, {
                type: chartType,
                data: rawData,
                options: getChartOptions(chartType, canvasId)
            });

            loadingEl.style.display = 'none';
            canvas.style.display = 'block';

        } catch (error) {
            console.error(`Error initializing ${canvasId}:`, error);
            showError(container, "Could not load chart data");
        }
    }

    // Chart Options
    function getChartOptions(type, id) {
        const baseOptions = {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'top' },
                tooltip: { mode: 'index', intersect: false }
            }
        };

        const titles = {
            'diseaseChart': 'Disease Distribution',
            'appointmentTrendChart': 'Appointment Trends',
            'genderAgeChart': 'Gender/Age Distribution',
            'personalHealthTrendChart': 'Your Health Trends'
        };

        return {
            ...baseOptions,
            plugins: {
                ...baseOptions.plugins,
                title: {
                    display: true,
                    text: titles[id],
                    font: { size: 16 }
                }
            }
        };
    }

    // Show Error if Data Not Available
    function showError(container, message) {
        const loadingEl = container.querySelector('.chart-loading');
        loadingEl.innerHTML = `
            <div class="chart-error">
                <i class="fas fa-exclamation-triangle"></i>
                ${message}
            </div>`;
    }
});
