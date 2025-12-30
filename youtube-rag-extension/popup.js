const chatDiv = document.getElementById("chat");
const questionInput = document.getElementById("question");
const sendBtn = document.getElementById("send");

const conversationId = crypto.randomUUID();

function addMessage(text, sender, isLoading = false) {
  const div = document.createElement("div");
  div.classList.add("message", sender);
  if (isLoading) div.classList.add("loading");
  div.textContent = text;
  chatDiv.appendChild(div);
  chatDiv.scrollTop = chatDiv.scrollHeight;
  return div;
}

async function sendMessage() {
  const question = questionInput.value.trim();
  if (!question) return;

  questionInput.value = "";
  addMessage(question, "user");

  const loadingMsg = addMessage("Thinking...", "bot", true);

  chrome.tabs.query({ active: true, currentWindow: true }, ([tab]) => {
    chrome.tabs.sendMessage(tab.id, { type: "GET_VIDEO_ID" }, async (response) => {

      if (!response || !response.videoId) {
        loadingMsg.textContent = "Not a YouTube video page.";
        loadingMsg.classList.remove("loading");
        return;
      }

      const payload = {
        video_id: response.videoId,
        question: question,
        conversation_id: conversationId
      };

      try {
        const res = await fetch("http://127.0.0.1:8000/chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        });

        const data = await res.json();
        loadingMsg.textContent = data.answer;
        loadingMsg.classList.remove("loading");

      } catch (err) {
        loadingMsg.textContent = "Backend not reachable.";
        loadingMsg.classList.remove("loading");
      }
    });
  });
}

sendBtn.addEventListener("click", sendMessage);

questionInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    sendMessage();
  }
});

