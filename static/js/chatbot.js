
function toggleChatbot() {
    const body = document.getElementById("chatbot-body");
    body.style.display = body.style.display === "none" || body.style.display === "" ? "flex" : "none";
}


function sendMessage() {
    const input = document.getElementById("user-input");
    const message = input.value.trim();
    if (message === "") return;

    const chatMessages = document.getElementById("chat-messages");

    // Display user's message
    const userMsg = document.createElement("div");
    userMsg.className = "message user-message";
    userMsg.innerHTML = `<span class="bold">You:</span> ${message}`;
    chatMessages.appendChild(userMsg);
    input.value = "";

    chatMessages.scrollTop = chatMessages.scrollHeight;

    // Create typing indicator element outside setTimeout so it's accessible later
    const typing = document.createElement("div");
    typing.className = "message bot-message typing";
    typing.innerHTML = `<span class="bold">Bot:</span> <span class='points'><span>.</span><span>.</span><span>.</span></span>`;

    // Add typing indicator after short delay
    setTimeout(() => {
        chatMessages.appendChild(typing);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }, 100);

    // Fetch response from Flask after 1.5 seconds
    setTimeout(() => {
        fetch("http://localhost:5000/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: message })
        })
            .then(response => response.json())
            .then(data => {
                chatMessages.removeChild(typing);

                const botMsg = document.createElement("div");
                botMsg.className = "message bot-message";
                botMsg.innerHTML = `<span class="bold">Bot:</span> ${data.response}`;
                chatMessages.appendChild(botMsg);
                chatMessages.scrollTop = chatMessages.scrollHeight;
            })
            .catch(error => {
                chatMessages.removeChild(typing);

                const errorMsg = document.createElement("div");
                errorMsg.className = "message bot-message";
                errorMsg.innerHTML = `<span class="bold">Bot:</span> Oops! Couldn't reach the chatbot.`;
                chatMessages.appendChild(errorMsg);
                chatMessages.scrollTop = chatMessages.scrollHeight;
                console.error("Chat error:", error);
            });
    }, 1500);
}




// Listen for Enter key when chatbot is open
document.addEventListener("keydown", function (event) {
    const isChatbotOpen = document.getElementById("chatbot-body").style.display === "flex";
    const input = document.getElementById("user-input");

    if (isChatbotOpen && document.activeElement === input && event.key === "Enter") {
        event.preventDefault(); // Prevents form submission if in a form
        sendMessage();
    }
});


function resetChat() {
    if (confirm("Are you sure you want to clear the chat?")) {
        // Clear frontend
        document.getElementById("chat-messages").innerHTML = "";

        // Send reset request to Flask backend
        fetch("http://localhost:5000/reset", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ action: "reset" })
        })
            .then(response => {
                if (!response.ok) throw new Error("Failed to reset conversation.");
                return response.json();
            })
            .then(data => {
                console.log("Chat reset:", data.message);
            })
            .catch(error => {
                console.error("Reset error:", error);
            });
    }
}
// Hide by default on load
window.onload = () => {
    document.getElementById("chatbot-body").style.display = "none";
};


