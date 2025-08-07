import { marked } from "https://cdn.jsdelivr.net/npm/marked/lib/marked.esm.js";

const chat = document.getElementById("chat");
const input = document.getElementById("message");
const sendButton = document.getElementById("send");

function displayGenerating() {
  const loadingMsg = document.createElement("div");
  loadingMsg.className = "js-loading-msg message bot";
  const loadingStates = ["🤖 generating..", "🤖 generating...", "🤖 generating."]
  let index = 0;
  loadingMsg.innerHTML = "🤖 generating.";
  const loadingInterval = setInterval(() => {
        index = (index + 1) % loadingStates.length;
        loadingMsg.innerHTML = loadingStates[index];
      }, 500);
  chat.appendChild(loadingMsg);
  return loadingInterval;
}


function addUserMessage(text, className) {
    const msg = document.createElement("div");
    msg.className = "message " + className;
    msg.innerHTML = text.replace(/\n/g, "<br>");
    chat.appendChild(msg);
    chat.scrollTop = chat.scrollHeight;
}

function addBotMessage(text, className) {
    const msg = document.createElement("div");
    msg.className = "message " + className;
    msg.innerHTML = marked.parse(text);
    //msg.innerHTML = formatMarkdownText(text)
    chat.appendChild(msg);
    chat.scrollTop = chat.scrollHeight;
}

function formatMarkdownText(markdownText){
  const lines = markdownText.trim().split(/\r?\n/);
  const htmlLines = [];
  let inList = false;

  for (let line of lines) {
    let stripped = line.trim();

    // Bold formatting (**text** to <b>text</b>)
    stripped = stripped.replace(/\*\*(.*?)\*\*/g, '<b>$1</b>');

    // List item
    if (stripped.startsWith('* ')) {
      if (!inList) {
        htmlLines.push('<ul>');
        inList = true;
      }
      const item = stripped.substring(2).trim();
      htmlLines.push(`<li>${item}</li>`);
    } else {
      if (inList) {
        htmlLines.push('</ul>');
        inList = false;
      }
      if (stripped) {
        htmlLines.push(`<p>${stripped}</p>`);
      }
    }
  }

  if (inList) {
    htmlLines.push('</ul>');
  }

  return htmlLines.join('\n');
}

sendButton.onclick = async function () {
    const userText = input.value.trim();
    if (userText === "") return;
    addUserMessage(userText, "user");
    const loadingInterval = displayGenerating()
    input.value = "";
    const response = await fetch("/send", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({message: userText})
    });
    
    const data = await response.json();
    clearInterval(loadingInterval);
    document.querySelector(".js-loading-msg").remove();
    addBotMessage(data.response, "bot");
}



/*
input.addEventListener("keypress", function(e) {
    if (e.key === "Enter") sendButton.click();
});
*/