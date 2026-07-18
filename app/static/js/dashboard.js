async function updateDashboard() {

    const response = await fetch("/system-info");
    const data = await response.json();

    // Numbers
    document.getElementById("cpu").innerText = data.cpu + "%";
    document.getElementById("ram").innerText = data.memory + "%";
    document.getElementById("disk").innerText = data.disk + "%";
    document.getElementById("process").innerText = data.processes;

    // CPU Progress Bar
    let cpuBar = document.getElementById("cpu-bar");

    cpuBar.style.width = data.cpu + "%";
    cpuBar.innerText = data.cpu + "%";

    cpuBar.classList.remove(
        "bg-success",
        "bg-warning",
        "bg-danger"
    );

    if (data.cpu < 50)
        cpuBar.classList.add("bg-success");
    else if (data.cpu < 80)
        cpuBar.classList.add("bg-warning");
    else
        cpuBar.classList.add("bg-danger");
}

async function updateRecentEvents() {

    const response = await fetch("/recent-events");
    const events = await response.json();

    let html = "";

    events.forEach(event => {
        html += `
            <li class="list-group-item">
                ${event}
            </li>
        `;
    });

    document.getElementById("recent-events").innerHTML = html;
}

updateDashboard();
updateRecentEvents();

setInterval(updateDashboard, 5000);
setInterval(updateRecentEvents, 5000);