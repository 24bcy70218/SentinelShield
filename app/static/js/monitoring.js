let cpuChart;
let memoryChart;

// ------------------------
// Create Charts
// ------------------------

function createCharts() {

    const cpuCtx = document.getElementById("cpuChart").getContext("2d");

    cpuChart = new Chart(cpuCtx, {
        type: "doughnut",
        data: {
            labels: ["Used", "Free"],
            datasets: [{
                data: [0, 100],
                backgroundColor: [
                    "#0d6efd",
                    "#dee2e6"
                ]
            }]
        }
    });

    const memCtx = document.getElementById("memoryChart").getContext("2d");

    memoryChart = new Chart(memCtx, {
        type: "doughnut",
        data: {
            labels: ["Used", "Free"],
            datasets: [{
                data: [0, 100],
                backgroundColor: [
                    "#198754",
                    "#dee2e6"
                ]
            }]
        }
    });

}

createCharts();

// ------------------------
// Load System Status
// ------------------------

async function loadStatus(){

    const res = await fetch("/api/system-status");
    const data = await res.json();

    document.getElementById("cpu").innerHTML = data.cpu + "%";
    document.getElementById("memory").innerHTML = data.memory + "%";
    document.getElementById("disk").innerHTML = data.disk + "%";
    document.getElementById("processes").innerHTML = data.processes;

    document.getElementById("upload").innerHTML =
        data.upload + " MB";

    document.getElementById("download").innerHTML =
        data.download + " MB";

    document.getElementById("hostname").innerHTML =
        data.hostname;

    document.getElementById("uptime").innerHTML =
        data.uptime;

    // CPU Progress Bar

    const bar = document.getElementById("cpu-bar");

    bar.style.width = data.cpu + "%";

    bar.innerHTML = data.cpu + "%";

    // Charts

    cpuChart.data.datasets[0].data = [
        data.cpu,
        100 - data.cpu
    ];

    cpuChart.update();

    memoryChart.data.datasets[0].data = [
        data.memory,
        100 - data.memory
    ];

    memoryChart.update();

}

// ------------------------
// Load Processes
// ------------------------

async function loadProcesses(){

    const res = await fetch("/api/processes");

    const processes = await res.json();

    let html = "";

    processes.forEach(proc=>{

        html += `
        <tr>
            <td>${proc.pid}</td>
            <td>${proc.name}</td>
            <td>${proc.cpu}</td>
            <td>${proc.memory}</td>
        </tr>
        `;

    });

    document.getElementById("processTable").innerHTML = html;

}

// ------------------------

function updateClock(){

    document.getElementById("monitorTime").innerHTML =
        new Date().toLocaleString();

}

updateClock();
loadStatus();
loadProcesses();

setInterval(updateClock,1000);

setInterval(loadStatus,5000);

setInterval(loadProcesses,5000);