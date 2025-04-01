function analyzePassword() {
    let password = document.getElementById("passwordInput").value;

    fetch("/analyze", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ password: password })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("strength").textContent = data.strength;
        document.getElementById("timeToCrack").textContent = data.time_to_crack;
        
        let leakedElement = document.getElementById("leaked");
        leakedElement.textContent = data.leaked ? "Yes" : "No";
        leakedElement.className = data.leaked ? "leaked-true" : "leaked-false";

        document.getElementById("suggestion").textContent = data.suggestion || "N/A";
    })
    .catch(error => console.error("Error:", error));
}
