document.getElementById("downloadBtn").addEventListener("click", function () {
    const url = document.getElementById("url").value.trim();
    const platform = document.getElementById("platform").value;

    if (!url) {
        alert("Please enter a valid URL.");
        return;
    }

    const messageDiv = document.getElementById('message');
    messageDiv.innerHTML = `
        <div class="spinner-container">
            <div class="spinner"></div>
            <p>Download in progress... Please wait.</p>
        </div>
    `; // Show the fancy spinner and message

    fetch(`/download`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ url, platform }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            messageDiv.innerHTML = `<p style="color: green;">${data.message}</p>`; // Success message
        } else {
            messageDiv.innerHTML = `<p style="color: red;">Error: ${data.error}</p>`; // Error message
        }
    })
    .catch(error => {
        messageDiv.innerHTML = `<p style="color: red;">An error occurred. Please try again later.</p>`;
        console.error(error);
    });
});