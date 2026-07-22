let chart;

let labels = [];

let uploadData = [];

let downloadData = [];


function createChart() {

    const ctx = document.getElementById("networkChart");

    chart = new Chart(ctx, {

        type: "line",

        data: {

            labels: labels,

            datasets: [

                {
                    label: "Upload (KB/s)",
                    data: uploadData,
                    borderWidth: 2,
                    tension: 0.3
                },

                {
                    label: "Download (KB/s)",
                    data: downloadData,
                    borderWidth: 2,
                    tension: 0.3
                }

            ]

        },

        options: {

            responsive: true,

            animation: false,

            scales: {

                y: {

                    beginAtZero: true

                }

            }

        }

    });

}

async function loadStatus() {

    const response = await fetch("/api/network-status");

    const data = await response.json();

    document.getElementById("activeConnections").innerText =
        data.active_connections;

    document.getElementById("listeningPorts").innerText =
        data.listening_ports;

    document.getElementById("uploadSpeed").innerText =
        data.upload_speed + " KB/s";

    document.getElementById("downloadSpeed").innerText =
        data.download_speed + " KB/s";

    labels.push(new Date().toLocaleTimeString());

    uploadData.push(data.upload_speed);

    downloadData.push(data.download_speed);

    if (labels.length > 20) {

        labels.shift();

        uploadData.shift();

        downloadData.shift();

    }

chart.update();    

}

async function loadConnections() {

    const response = await fetch("/api/network-connections");

    const data = await response.json();

    const table = document.getElementById("connectionTable");

    table.innerHTML = "";

    data.forEach(conn => {

        let badge = `<span class="badge bg-secondary">${conn.status}</span>`;

        if (conn.status === "ESTABLISHED")
            badge = `<span class="badge bg-success">${conn.status}</span>`;

        if (conn.status === "LISTEN")
            badge = `<span class="badge bg-primary">${conn.status}</span>`;

        table.innerHTML += `

            <tr>

                <td>${conn.pid}</td>

                <td>${conn.process}</td>

                <td>${conn.local}</td>

                <td>${conn.remote}</td>

                <td>${badge}</td>

            </tr>

        `;

    });

}

document.getElementById("searchConnection").addEventListener("keyup", function () {

    const filter = this.value.toLowerCase();

    document.querySelectorAll("#connectionTable tr").forEach(row => {

        row.style.display = row.innerText.toLowerCase().includes(filter)
            ? ""
            : "none";

    });

});

createChart();

loadStatus();

loadConnections();

setInterval(loadStatus, 5000);
setInterval(loadConnections, 5000);