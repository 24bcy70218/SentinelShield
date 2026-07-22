// ===============================
// SentinelShield Dashboard
// ===============================

// ----------- Charts -----------

let labels = [];

let cpuData = [];
let ramData = [];
let diskData = [];

function createChart(id, label, data, color) {

    return new Chart(document.getElementById(id), {

        type: "line",

        data: {

            labels: labels,

            datasets: [
                {
                    label: label,
                    data: data,
                    borderColor: color,
                    borderWidth: 2,
                    fill: false,
                    tension: 0.3
                }
            ]

        },

        options: {

            responsive: true,

            animation: false,

            scales: {

                y: {
                    min: 0,
                    max: 100
                }

            }

        }

    });

}

const cpuChart = createChart("cpuChart", "CPU %", cpuData, "red");
const ramChart = createChart("ramChart", "RAM %", ramData, "blue");
const diskChart = createChart("diskChart", "Disk %", diskData, "green");

function updateCharts(system) {

    const time = new Date().toLocaleTimeString();

    labels.push(time);

    cpuData.push(system.cpu);
    ramData.push(system.memory);
    diskData.push(system.disk);

    if (labels.length > 20) {

        labels.shift();

        cpuData.shift();
        ramData.shift();
        diskData.shift();

    }

    cpuChart.update();
    ramChart.update();
    diskChart.update();

}


// ===============================
// Alert Pie Chart
// ===============================

const pieData = {
    labels: ["Critical", "Warning", "Info"],
    datasets: [
        {
            data: [0, 0, 0]
        }
    ]
};

const alertPieChart = new Chart(
    document.getElementById("alertPieChart"),
    {
        type: "pie",
        data: pieData,
        options: {
            responsive: true
        }
    }
);

// ==============================
// Alert Timeline Chart
// ==============================

const timelineChart = new Chart(
    document.getElementById("timelineChart"),
    {
        type: "line",
        data: {
            labels: [],
            datasets: [
                {
                    label: "Alerts",
                    data: [],
                    tension: 0.3,
                    fill: false
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: true
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    }
);

async function loadAlertTimeline() {

    const response = await fetch("/alert-timeline");

    const data = await response.json();

    timelineChart.data.labels = data.map(item => item.time);

    timelineChart.data.datasets[0].data =
        data.map(item => item.count);

    timelineChart.update();

}

async function loadAlertStatistics() {

    const response = await fetch("/alert-stats");

    const stats = await response.json();

    document.getElementById("totalAlerts").innerText =
        stats.total;

    document.getElementById("criticalAlerts").innerText =
        stats.critical;

    document.getElementById("warningAlerts").innerText =
        stats.warning;

    document.getElementById("infoAlerts").innerText =
        stats.info;

    alertPieChart.data.datasets[0].data = [
        stats.critical,
        stats.warning,
        stats.info
    ];

    alertPieChart.update();

}

// ----------- System Info -----------

async function updateSystemInfo() {

    const response = await fetch("/system-info");
    const data = await response.json();

    document.getElementById("cpu").innerText = data.cpu + "%";
    document.getElementById("ram").innerText = data.memory + "%";
    document.getElementById("disk").innerText = data.disk + "%";
    document.getElementById("process").innerText = data.processes;

    const cpuBar = document.getElementById("cpu-bar");

    if (cpuBar) {

        cpuBar.style.width = data.cpu + "%";
        cpuBar.innerText = data.cpu + "%";

    }

    updateCharts(data);

}

// ----------- Recent Events -----------

async function loadRecentEvents() {

    const response = await fetch("/recent-events");
    const events = await response.json();

    const list = document.getElementById("recent-events");

    list.innerHTML = "";

    events.forEach(event => {

        list.innerHTML += `
            <li class="list-group-item">
                ${event}
            </li>
        `;

    });

}

// ----------- Alert Count -----------

async function loadAlertCount() {

    const response = await fetch("/alert-count");
    const data = await response.json();

    document.getElementById("alert-count").innerText = data.count;

}

// ----------- Alert History -----------

async function loadRecentAlerts() {

    const response = await fetch("/recent-alerts");
    const alerts = await response.json();

    const list = document.getElementById("recent-alerts");

    list.innerHTML = "";

    if (alerts.length === 0) {

        list.innerHTML = `
            <li class="list-group-item">
                No alerts found.
            </li>
        `;

        return;
    }

    alerts.forEach(alert => {

        list.innerHTML += `
            <li class="list-group-item">
                <strong>${alert.level}</strong> - ${alert.title}<br>
                ${escapeHTML(alert.message)}
            </li>
        `;

    });

}

// ===============================
// System Health
// ===============================

async function loadHealthScore() {

    const response = await fetch("/health-score");

    const health = await response.json();

    document.getElementById("healthScore").innerText =
        health.score + "/100";

    const status = document.getElementById("healthStatus");

    status.innerText = health.status;

    // Remove previous Bootstrap text colors
    status.classList.remove(
        "text-success",
        "text-primary",
        "text-warning",
        "text-danger"
    );

    // Add new color
    status.classList.add("text-" + health.color);

}

// ===============================
// Threat Level
// ===============================

async function loadThreatLevel() {

    const response = await fetch("/threat-level");

    const threat = await response.json();

    document.getElementById("threatIcon").innerText =
        threat.icon;

    document.getElementById("threatLevel").innerText =
        threat.level;

    document.getElementById("threatMessage").innerText =
        threat.message;

    const level = document.getElementById("threatLevel");

    level.classList.remove(
        "text-success",
        "text-primary",
        "text-warning",
        "text-danger"
    );

    level.classList.add("text-" + threat.color);

}

// ===============================
// Top Alert Types Chart
// ===============================

const alertTypeChart = new Chart(
    document.getElementById("alertTypeChart"),
    {
        type: "bar",

        data: {

            labels: [],

            datasets: [

                {

                    label: "Number of Alerts",

                    data: []

                }

            ]

        },

        options: {

            responsive: true,

            indexAxis: "y",

            scales: {

                x: {

                    beginAtZero: true

                }

            }

        }

    }
);

async function loadAlertTypes() {

    const response = await fetch("/alert-types");

    const data = await response.json();

    alertTypeChart.data.labels =
        Object.keys(data);

    alertTypeChart.data.datasets[0].data =
        Object.values(data);

    alertTypeChart.update();

}

// ----------- Toast Notification -----------

let lastAlert = "";

async function checkLatestAlert() {

    const response = await fetch("/latest-alert");
    const alert = await response.json();

    if (!alert.message)
        return;

    if (alert.message === lastAlert)
        return;

    lastAlert = alert.message;

    document.getElementById("toast-message").innerHTML =
        `<strong>${escapeHTML(alert.title)}</strong><br>${alert.message}`;

    const toast = new bootstrap.Toast(
        document.getElementById("alertToast")
    );

    toast.show();

}

// ===============================
// Alert Search
// ===============================

document.addEventListener("DOMContentLoaded", () => {

    const searchBox = document.getElementById("alertSearch");

    if (!searchBox) return;

    searchBox.addEventListener("keyup", function () {

        const value = this.value.toLowerCase();

        const alerts =
            document.querySelectorAll("#recent-alerts li");

        alerts.forEach(alert => {

            if (alert.innerText.toLowerCase().includes(value)) {

                alert.style.display = "";

            } else {

                alert.style.display = "none";

            }

        });

    });

});


function updateLastUpdated() {

    const element = document.getElementById("lastUpdated");

    if (!element) return;

    const now = new Date();

    element.innerHTML =
        "🟢 " + now.toLocaleTimeString();

}

// ----------- Refresh Dashboard -----------

// ----------- Refresh Dashboard -----------

async function refreshDashboard() {

    try {

        await updateSystemInfo();

        await loadRecentEvents();

        await loadAlertCount();

        await loadRecentAlerts();

        await loadAlertStatistics();

        await loadAlertTimeline();

        await loadHealthScore();

        await loadThreatLevel();

        await loadAlertTypes();

        await checkLatestAlert();

        // Update Last Refreshed Time
        updateLastUpdated();

    }
    catch (error) {

        console.error("Dashboard Refresh Error:", error);

    }

}

function escapeHTML(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}

// Initial Load
refreshDashboard();

// Refresh every 5 seconds
setInterval(refreshDashboard, 5000);

