async function loadIPStatistics() {

    const response = await fetch("/ip-statistics");

    const data = await response.json();

    let totalAttacks = 0;

    let topIP = "-";
    let highestCount = 0;

    const table = document.getElementById("ipTable");

    table.innerHTML = "";

    const labels = [];
    const counts = [];
    const attackTypes = {};


    data.forEach(item => {

        totalAttacks += item.count;

        labels.push(item.ip);
        counts.push(item.count);

        for (const type in item.types) {

              attackTypes[type] =
                (attackTypes[type] || 0) + item.types[type];

        }

        if (item.count > highestCount) {

            highestCount = item.count;
            topIP = item.ip;

        }

        let attackTypeHTML = "";

        for (const type in item.types) {

            attackTypeHTML +=
                `${type} (${item.types[type]})<br>`;

        }

        let badgeColor = "success";

        if (item.risk === "Medium") {

           badgeColor = "warning";

        }

        else if (item.risk === "High") {

            badgeColor = "danger";

        }

        else if (item.risk === "Critical") {

            badgeColor = "dark";

        }
        
        let blockedBadge = item.blocked
            ? `<button class="btn btn-danger btn-sm"
                       onclick="unblockIP('${item.ip}')">
                    Unblock
                </button>`
            : `<span class="badge bg-success">
                  Active
                </span>`;
            


        table.innerHTML += `
        <tr>

            <td>${item.ip}</td>

            <td>${item.count}</td>

            <td>${item.last_seen}</td>

            <td>${attackTypeHTML}</td>

            <td>${item.threat_score}</td>

            <td>
                <span class="badge bg-${badgeColor}">
                   ${item.risk}
                </span>
            </td>

            <td>
                ${blockedBadge}
            </td>

        </tr> 
        `;

    });

    document.getElementById("totalAttacks").innerText =
        totalAttacks;

    document.getElementById("uniqueAttackers").innerText =
        data.length;

    document.getElementById("topAttacker").innerText =
        topIP;

    document.getElementById("highestCount").innerText =
        highestCount;

    drawChart(labels, counts);
    drawAttackTypes(attackTypes);

}

let chart = null;

function drawChart(labels, counts) {

    const canvas = document.getElementById("attackChart");

    if (!canvas) {
        console.error("Canvas with id 'attackChart' not found.");
        return;
    }

    if (chart) {
        chart.destroy();
    }

    chart = new Chart(canvas.getContext("2d"), {
        type: "bar",
        data: {
            labels: labels,
            datasets: [{
                label: "Attack Count",
                data: counts
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

let attackPie = null;

function drawAttackTypes(typeData) {

    if (attackPie) {

        attackPie.destroy();

    }

    attackPie = new Chart(

        document.getElementById("attackTypeChart"),

        {

            type: "pie",

            data: {

                labels: Object.keys(typeData),

                datasets: [

                    {

                        data: Object.values(typeData)

                    }

                ]

            },

            options: {

                responsive: true

            }

        }

    );

}

async function unblockIP(ip) {

    const response = await fetch("/unblock/" + ip, {
        method: "POST"
    });

    if (response.ok) {
        loadIPStatistics();
    } else {
        alert("Failed to unblock IP.");
    }
}


loadIPStatistics();

setInterval(loadIPStatistics, 5000);