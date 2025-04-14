
function toggleChatbot() {
    const body = document.getElementById("chatbot-body");
    body.style.display = body.style.display === "none" || body.style.display === "" ? "flex" : "none";
}

function sendMessage() {
    const input = document.getElementById("user-input");
    const message = input.value.trim();
    if (message === "") return;

    const chatMessages = document.getElementById("chat-messages");
    chatMessages.innerHTML += `<div><strong>You:</strong> ${message}</div>`;
    input.value = "";

    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;

    // TODO: Send to backend via fetch/AJAX if needed
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
        document.getElementById("chat-messages").innerHTML = "";
    }
}
// Hide by default on load
window.onload = () => {
    document.getElementById("chatbot-body").style.display = "none";
};


