const chatWindow = document.getElementById("chat-window");
const userInput = document.getElementById("user-input");
const sendButton = document.getElementById("send-button");

let currentQuestion = null;

// Display messages in the chat window
function addMessage(content, sender) {
    const message = document.createElement("div");
    message.classList.add("message", sender);
    message.textContent = content;
    chatWindow.appendChild(message);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

// Start the chatbot
async function startChat() {
    try {
        const response = await fetch("/start");
        const data = await response.json();
        currentQuestion = data.question;
        addMessage(currentQuestion, "bot");
    } catch (error) {
        addMessage("Error: Unable to connect to the server.", "bot");
        sendButton.disabled = true;
    }
}

// Handle user input
async function handleUserInput() {
    const userResponse = userInput.value.trim();
    if (!userResponse) return;

    addMessage(userResponse, "user");
    userInput.value = "";

    try {
        const response = await fetch("/next", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ response: userResponse })
        });

        const data = await response.json();

        if (data.prediction) {
            addMessage(`Prediction: ${data.prediction}`, "bot");
            sendButton.disabled = true;
        } else if (data.question) {
            currentQuestion = data.question;
            addMessage(currentQuestion, "bot");
        } else if (data.error) {
            addMessage(data.error, "bot");
        }
    } catch (error) {
        addMessage("Error: Unable to process your input.", "bot");
    }
}

sendButton.addEventListener("click", handleUserInput);
userInput.addEventListener("keypress", (event) => {
    if (event.key === "Enter") {
        handleUserInput();
    }
});

// Start the chat
startChat();
