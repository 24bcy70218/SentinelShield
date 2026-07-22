async function loadFileEvents() {

    try {

        const response = await fetch("/api/file-events");
        const data = await response.json();

        const table = document.getElementById("fileTable");

        table.innerHTML = "";

        let created = 0;
        let modified = 0;
        let deleted = 0;

        data.forEach(item => {

            if (item.event === "CREATED")
                created++;

            else if (item.event === "MODIFIED")
                modified++;

            else if (item.event === "DELETED")
                deleted++;

            let badge = "";

            switch (item.event) {

                case "CREATED":
                    badge = `<span class="badge bg-success">${item.event}</span>`;
                    break;

                case "MODIFIED":
                    badge = `<span class="badge bg-warning text-dark">${item.event}</span>`;
                    break;

                case "DELETED":
                    badge = `<span class="badge bg-danger">${item.event}</span>`;
                    break;

                case "MOVED":
                    badge = `<span class="badge bg-primary">${item.event}</span>`;
                    break;

                default:
                    badge = `<span class="badge bg-secondary">${item.event}</span>`;
            }

            table.innerHTML += `

                <tr>

                    <td>${item.time}</td>

                    <td>${badge}</td>

                    <td>${item.path}</td>

                </tr>

            `;
        });

        document.getElementById("totalEvents").innerText = data.length;
        document.getElementById("createdEvents").innerText = created;
        document.getElementById("modifiedEvents").innerText = modified;
        document.getElementById("deletedEvents").innerText = deleted;

    }

    catch (error) {

        console.error("Error loading file events:", error);

    }

}

document.getElementById("searchFile").addEventListener("keyup", function () {

    let filter = this.value.toLowerCase();

    let rows = document.querySelectorAll("#fileTable tr");

    rows.forEach(row => {

        row.style.display =
            row.innerText.toLowerCase().includes(filter)
            ? ""
            : "none";

    });

});

loadFileEvents();

setInterval(loadFileEvents, 5000);