const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("userInput");

async function sendMessage() {
  const prompt = userInput.value.trim();
  if (!prompt) return;

  // Show user message
  appendMessage("You", prompt);
  userInput.value = "";

  try {
    const response = await fetch("https://98ufjyie04.execute-api.us-east-1.amazonaws.com/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ prompt })
    });

    const data = await response.json();
    appendMessage("Bot", data.response || "No response");
  } catch (error) {
    appendMessage("Bot", "⚠️ Something went wrong.");
    console.error(error);
  }
}

function appendMessage(sender, message) {
  const bubble = document.createElement("div");
  bubble.classList.add("message");
  bubble.innerHTML = `<strong>${sender}:</strong> ${message}`;
  chatBox.appendChild(bubble);
  chatBox.scrollTop = chatBox.scrollHeight;
}

// Enable pressing "Enter" to send message
document.getElementById("user-input").addEventListener("keydown", function(event) {
  if (event.key === "Enter") {
    event.preventDefault();  // Prevent new line
    send();                  // Call your send() function
  }
});

// Temp change to trigger Git commit
