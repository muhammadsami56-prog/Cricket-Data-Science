
// Load dashboard data
async function loadDashboard() {
    try {
        const [optionsResponse, matchesResponse] = await Promise.all([
            fetch("/api/options"),
            fetch("/api/matches")
        ]);

        if (!optionsResponse.ok || !matchesResponse.ok) {
            throw new Error("Unable to load dashboard data.");
        }

        const options = await optionsResponse.json();
        const matches = await matchesResponse.json();

        document.getElementById("total-matches").textContent =
            options.total_matches.toLocaleString();

        document.getElementById("total-teams").textContent =
            options.teams.length;

        document.getElementById("total-venues").textContent =
            options.venues.length;

        fillDropdown("team1", options.teams);
        fillDropdown("team2", options.teams);
        fillDropdown("venue", options.venues);

        updateTossWinner();

        loadRecentMatches(matches);
        await loadPredictionHistory();

    } catch (error) {
        console.error("Dashboard error:", error);
    }
}


// Fill dropdowns
function fillDropdown(id, values) {
    const dropdown = document.getElementById(id);

    dropdown.innerHTML = '<option value="">Select an option</option>';

    values.forEach(value => {
        const option = document.createElement("option");
        option.value = value;
        option.textContent = value;
        dropdown.appendChild(option);
    });
}


// Update toss winner options
function updateTossWinner() {
    const team1 = document.getElementById("team1").value;
    const team2 = document.getElementById("team2").value;

    fillDropdown(
        "toss-winner",
        [team1, team2].filter(Boolean)
    );
}

document.getElementById("team1").addEventListener("change", updateTossWinner);
document.getElementById("team2").addEventListener("change", updateTossWinner);


// Show recent matches
function loadRecentMatches(matches) {
    const table = document.getElementById("matches-table");

    table.innerHTML = "";

    if (!matches.length) {
        table.innerHTML =
            '<tr><td colspan="4">No match records found.</td></tr>';
        return;
    }

    matches.forEach(match => {
        const row = document.createElement("tr");

        [
            match.team1,
            match.team2,
            match.venue,
            match.winner
        ].forEach(value => {
            const cell = document.createElement("td");
            cell.textContent = value || "N/A";
            row.appendChild(cell);
        });

        table.appendChild(row);
    });
}


// Load prediction history
async function loadPredictionHistory() {
    const table = document.getElementById("prediction-history-table");
    const counter = document.getElementById("total-predictions");

    try {
        const response = await fetch("/api/history");

        if (!response.ok) {
            throw new Error("Failed to load prediction history.");
        }

        const history = await response.json();

        // Update total prediction count
        counter.textContent = history.length;

        if (history.length === 0) {
            table.innerHTML =
                '<tr><td colspan="7">No predictions yet.</td></tr>';
            return;
        }

        table.innerHTML = "";

        history.forEach(item => {
            const row = document.createElement("tr");

            const values = [
                item.team1,
                item.team2,
                item.venue,
                item.toss_winner,
                item.toss_decision,
                item.predicted_winner,
                item.created_at
            ];

            values.forEach((value, index) => {
                const cell = document.createElement("td");

                if (index === 5) {
                    const badge = document.createElement("span");
                    badge.className = "winner-badge";
                    badge.textContent = "🏆 " + (value || "N/A");
                    cell.appendChild(badge);
                } else {
                    cell.textContent = value || "N/A";
                }

                row.appendChild(cell);
            });

            table.appendChild(row);
        });

    } catch (error) {
        console.error("Prediction history error:", error);

        counter.textContent = "—";

        table.innerHTML =
            '<tr><td colspan="7">Unable to load prediction history.</td></tr>';
    }
}


// Handle match prediction
document.getElementById("predict-btn").addEventListener("click", async () => {
    const resultBox = document.getElementById("prediction-result");
    const predictButton = document.getElementById("predict-btn");

    const data = {
        team1: document.getElementById("team1").value,
        team2: document.getElementById("team2").value,
        venue: document.getElementById("venue").value,
        toss_winner: document.getElementById("toss-winner").value,
        toss_decision: document.getElementById("toss-decision").value
    };

    if (!data.team1 || !data.team2 || !data.venue || !data.toss_winner) {
        resultBox.textContent = "Please select all match details.";
        return;
    }

    if (data.team1 === data.team2) {
        resultBox.textContent = "Please select two different teams.";
        return;
    }

    predictButton.disabled = true;
    predictButton.textContent = "Predicting...";

    resultBox.textContent = "Predicting match winner...";

    try {
        const response = await fetch("/api/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (!response.ok || result.error) {
            throw new Error(result.error || "Prediction failed.");
        }

        resultBox.innerHTML = "";

        const heading = document.createElement("h3");
        heading.textContent = "Predicted Winner";

        const winner = document.createElement("h2");
        winner.textContent = "🏆 " + result.predicted_winner;

        const message = document.createElement("p");
        message.textContent = result.message;

        resultBox.appendChild(heading);
        resultBox.appendChild(winner);
        resultBox.appendChild(message);

        // Refresh prediction history
        await loadPredictionHistory();

    } catch (error) {
        resultBox.textContent = error.message ||
            "Unable to connect to prediction server.";

    } finally {
        predictButton.disabled = false;
        predictButton.textContent = "Predict Match Winner";
    }
});


// Start dashboard
loadDashboard();
