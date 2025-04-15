document.getElementById("doctor-select").addEventListener("change", function () {
    const doctorId = this.value;
    const dateInput = document.getElementById("appointment-date");
    const dateListContainer = document.getElementById("available-dates-list");
    const submitBtn = document.querySelector("button[type='submit']");

    fetch(`/api/doctors/by_user/${doctorId}/available_dates/`)
        .then(response => response.json())
        .then(data => {
            // Clear previous options
            dateListContainer.innerHTML = "";
            dateInput.value = "";

            if (data.available_dates && data.available_dates.length > 0) {
                submitBtn.disabled = false;

                data.available_dates.forEach(dateStr => {
                    const dateObj = new Date(dateStr);
                    const readable = dateObj.toLocaleDateString('en-US', {
                        year: 'numeric',
                        month: 'long',
                        day: 'numeric',
                        weekday: 'long'
                    });

                    const dateDiv = document.createElement("div");
                    dateDiv.textContent = readable;
                    dateDiv.style.display = "inline-block"
                    dateDiv.style.cursor = "pointer";
                    dateDiv.style.padding = "6px 12px";
                    dateDiv.style.marginBottom = "5px";
                    dateDiv.style.border = "1px solid #ccc";
                    dateDiv.style.borderRadius = "5px";
                    dateDiv.style.backgroundColor = "#f9f9f9";

                    // Set date input when clicked
                    dateDiv.addEventListener("click", function () {
                        dateInput.value = dateStr;
                        // Optional: highlight the selected date
                        Array.from(dateListContainer.children).forEach(child => {
                            child.style.backgroundColor = "#f9f9f9";
                        });
                        dateDiv.style.backgroundColor = "#d0ebff";
                    });

                    dateListContainer.appendChild(dateDiv);
                });

            } else {
                const noDateMsg = document.createElement("div");
                noDateMsg.textContent = "No available dates";
                noDateMsg.style.color = "red";
                dateListContainer.appendChild(noDateMsg);
                submitBtn.disabled = true;
            }
        })
        .catch(error => {
            console.error("Error fetching dates:", error);
            submitBtn.disabled = true;
        });
});
