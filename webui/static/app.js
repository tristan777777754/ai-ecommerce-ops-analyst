const messagesEl = document.querySelector("#messages");
const form = document.querySelector("#chatForm");
const input = document.querySelector("#messageInput");
const sendButton = document.querySelector("#sendButton");
const clearButton = document.querySelector("#clearChat");
const statusDot = document.querySelector("#statusDot");
const modelName = document.querySelector("#modelName");

let history = [];

function addMessage(role, content) {
  const article = document.createElement("article");
  article.className = `message ${role}`;

  const avatar = document.createElement("div");
  avatar.className = "avatar";
  avatar.textContent = role === "user" ? "YOU" : "AI";

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.innerHTML = renderText(content);

  article.append(avatar, bubble);
  messagesEl.append(article);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

function escapeHtml(text) {
  return text
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function renderText(text) {
  const escaped = escapeHtml(text);
  return escaped
    .replace(/^### (.*)$/gm, "<h3>$1</h3>")
    .replace(/^## (.*)$/gm, "<h2>$1</h2>")
    .replace(/^# (.*)$/gm, "<h2>$1</h2>")
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
    .replace(/\n/g, "<br>");
}

async function refreshStatus() {
  try {
    const response = await fetch("/api/status");
    const data = await response.json();
    statusDot.className = `status-dot ${data.has_api_key ? "ok" : "warn"}`;
    modelName.textContent = `Model: ${data.model}${data.has_api_key ? "" : " (missing API key)"}`;
  } catch {
    statusDot.className = "status-dot warn";
    modelName.textContent = "Model: status unavailable";
  }
}

async function sendMessage(message) {
  addMessage("user", message);
  history.push({ role: "user", content: message });
  sendButton.disabled = true;
  sendButton.textContent = "Wait";

  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message, history }),
    });
    const data = await response.json();
    if (!data.ok) {
      throw new Error(data.error || "Unknown error");
    }
    addMessage("assistant", data.answer);
    history.push({ role: "assistant", content: data.answer });
  } catch (error) {
    addMessage("assistant", `Error: ${error.message}`);
  } finally {
    sendButton.disabled = false;
    sendButton.textContent = "Send";
    input.focus();
  }
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const message = input.value.trim();
  if (!message) return;
  input.value = "";
  sendMessage(message);
});

input.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && (event.metaKey || event.ctrlKey)) {
    form.requestSubmit();
  }
});

document.querySelectorAll(".prompt").forEach((button) => {
  button.addEventListener("click", () => {
    input.value = button.textContent.trim();
    form.requestSubmit();
  });
});

clearButton.addEventListener("click", () => {
  history = [];
  messagesEl.innerHTML = "";
  addMessage(
    "assistant",
    "Ask me what the marketplace manager should do this week. I will answer from the ontology and the proposed BusinessRecommendation records."
  );
});

refreshStatus();
