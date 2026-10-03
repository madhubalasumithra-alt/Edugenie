const taskEl = document.getElementById("task");
const levelWrap = document.getElementById("levelWrap");
const levelEl = document.getElementById("level");
const inputEl = document.getElementById("userInput");
const submitBtn = document.getElementById("submitBtn");
const resultEl = document.getElementById("result");
const statusEl = document.getElementById("status");
const charCount = document.getElementById("charCount");

const placeholders = {
  qa: "Example: Which is the largest ocean?",
  explain: "Example: Explain the Pythagoras theorem in simple words",
  quiz: "Paste a topic or passage from which EduGenie should generate 3 MCQs",
  summarize: "Paste a longer educational passage to summarize",
  learn: "Example: SQL, Python, computer networks, machine learning"
};

taskEl.addEventListener("change", () => {
  inputEl.placeholder = placeholders[taskEl.value];
  levelWrap.classList.toggle("hidden", taskEl.value !== "learn");
});

inputEl.addEventListener("input", () => {
  charCount.textContent = `${inputEl.value.length} / 20000`;
});

function setStatus(message, isError = false) {
  statusEl.textContent = message;
  statusEl.classList.remove("hidden", "error");
  if (isError) statusEl.classList.add("error");
}

function escapeHtml(value) {
  return value.replace(/[&<>'"]/g, (char) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;"
  }[char]));
}

function renderText(data) {
  resultEl.innerHTML = `
    <h2>Result</h2>
    <div class="text-result">${escapeHtml(data.result)}</div>
    <div class="meta">Provider: ${escapeHtml(data.provider)}${data.model ? ` · Model: ${escapeHtml(data.model)}` : ""}</div>
  `;
}

function renderQuiz(data) {
  const questions = data.questions.map((q, i) => {
    const options = q.options.map((option) => {
      const safe = escapeHtml(option);
      return `<label class="option"><input type="radio" name="q${i}" value="${safe}"><span>${safe}</span></label>`;
    }).join("");

    return `
      <article class="quiz-card" data-answer="${escapeHtml(q.correct_answer)}" data-explanation="${escapeHtml(q.explanation)}">
        <h3>${i + 1}. ${escapeHtml(q.question)}</h3>
        ${options}
        <button class="check-btn" type="button">Check answer</button>
        <div class="feedback hidden"></div>
      </article>
    `;
  }).join("");

  resultEl.innerHTML = `<h2>Your Quiz</h2>${questions}<div class="meta">Provider: ${escapeHtml(data.provider)}${data.model ? ` · Model: ${escapeHtml(data.model)}` : ""}</div>`;

  resultEl.querySelectorAll(".check-btn").forEach((button) => {
    button.addEventListener("click", () => {
      const card = button.closest(".quiz-card");
      const selected = card.querySelector("input[type=radio]:checked");
      const feedback = card.querySelector(".feedback");
      if (!selected) {
        feedback.textContent = "Choose an option first.";
      } else if (selected.value === card.dataset.answer) {
        feedback.textContent = `Correct. ${card.dataset.explanation}`;
      } else {
        feedback.textContent = `Not quite. Correct answer: ${card.dataset.answer}. ${card.dataset.explanation}`;
      }
      feedback.classList.remove("hidden");
    });
  });
}

submitBtn.addEventListener("click", async () => {
  const text = inputEl.value.trim();
  if (!text) {
    setStatus("Please enter a question, topic, or passage first.", true);
    return;
  }

  submitBtn.disabled = true;
  resultEl.classList.add("hidden");
  setStatus("EduGenie is generating your result…");

  try {
    const response = await fetch("/api/run", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ task: taskEl.value, text, level: levelEl.value })
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "Request failed.");

    statusEl.classList.add("hidden");
    if (taskEl.value === "quiz") renderQuiz(data); else renderText(data);
    resultEl.classList.remove("hidden");
  } catch (error) {
    setStatus(error.message || "Something went wrong.", true);
  } finally {
    submitBtn.disabled = false;
  }
});
