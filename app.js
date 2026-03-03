const questionBank = [
  {
    topic: "Python",
    difficulty: 1,
    prompt: "What does a Python list comprehension do? Give a tiny example.",
    answerKeywords: ["list", "for", "expression"],
    hint: "Think concise syntax for transforming/creating a list.",
    solution:
      "A list comprehension builds a list from an expression and loop, e.g. [x*x for x in range(5)] creates squares.",
  },
  {
    topic: "Linear Algebra",
    difficulty: 1,
    prompt: "What is the geometric meaning of a vector dot product?",
    answerKeywords: ["angle", "projection", "magnitude"],
    hint: "It relates vector lengths and cosine of the angle between them.",
    solution:
      "Dot product measures alignment: a·b = |a||b|cos(theta). It can be seen as projected length times magnitude.",
  },
  {
    topic: "Probability",
    difficulty: 1,
    prompt: "If events A and B are independent, how do you compute P(A and B)?",
    answerKeywords: ["p(a)", "p(b)", "multiply"],
    hint: "Independent joint probability has a simple product form.",
    solution: "For independent events, P(A ∩ B) = P(A) × P(B).",
  },
  {
    topic: "Software Engineering Basics",
    difficulty: 1,
    prompt: "Why are unit tests useful?",
    answerKeywords: ["regression", "confidence", "small"],
    hint: "Think reliability and safe refactoring.",
    solution:
      "Unit tests validate small components in isolation, catch regressions early, and improve confidence when changing code.",
  },
  {
    topic: "MLOps",
    difficulty: 2,
    prompt: "What is the role of model versioning in MLOps?",
    answerKeywords: ["reproduc", "tracking", "rollback"],
    hint: "Think experiments, deployment traceability, and recovering from bad releases.",
    solution:
      "Model versioning tracks artifacts, data, and configs so results are reproducible, comparable, and reversible via rollback.",
  },
  {
    topic: "Transformers",
    difficulty: 2,
    prompt: "What does self-attention help a transformer model capture?",
    answerKeywords: ["relationships", "tokens", "context"],
    hint: "The mechanism lets each token 'look at' others.",
    solution:
      "Self-attention captures contextual relationships between tokens, letting each token weigh the relevance of others.",
  },
  {
    topic: "Deployment Basics",
    difficulty: 1,
    prompt: "What is one advantage of containerizing an app before deployment?",
    answerKeywords: ["consistent", "environment", "dependency"],
    hint: "Think 'works on my machine' issues.",
    solution:
      "Containers package code and dependencies so the app runs consistently across environments.",
  },
  {
    topic: "Python",
    difficulty: 2,
    prompt: "When would you use a generator instead of a list?",
    answerKeywords: ["memory", "lazy", "iterate"],
    hint: "Focus on large/streaming data.",
    solution:
      "Use generators for lazy iteration over large or infinite sequences to reduce memory usage.",
  },
  {
    topic: "Linear Algebra",
    difficulty: 2,
    prompt: "What does an eigenvector represent (intuitively)?",
    answerKeywords: ["direction", "scal", "matrix"],
    hint: "A matrix transformation keeps something unchanged except scale.",
    solution:
      "An eigenvector is a direction that remains unchanged by a matrix transform, only scaled by an eigenvalue.",
  },
  {
    topic: "Probability",
    difficulty: 2,
    prompt: "What is the difference between a PMF and a PDF?",
    answerKeywords: ["discrete", "continuous", "density"],
    hint: "One is exact mass at points, the other is density over intervals.",
    solution:
      "PMF applies to discrete variables and assigns exact probabilities to values; PDF applies to continuous variables where interval integrals give probabilities.",
  },
];

const topics = [...new Set(questionBank.map((q) => q.topic))];

const defaultState = {
  xp: 0,
  streak: 0,
  attempts: 0,
  correct: 0,
  topicStats: Object.fromEntries(topics.map((t) => [t, { asked: 0, correct: 0, skipped: 0 }])),
};

const state = loadState();
let currentQuestion = null;
let answeredCurrent = false;

const topicBadge = document.getElementById("topicBadge");
const difficultyBadge = document.getElementById("difficultyBadge");
const questionText = document.getElementById("questionText");
const hintText = document.getElementById("hintText");
const answerInput = document.getElementById("answerInput");
const solutionText = document.getElementById("solutionText");
const feedback = document.getElementById("feedback");
const checkBtn = document.getElementById("checkBtn");
const skipBtn = document.getElementById("skipBtn");
const nextBtn = document.getElementById("nextBtn");
const resetProgressBtn = document.getElementById("resetProgressBtn");

const xpValue = document.getElementById("xpValue");
const streakValue = document.getElementById("streakValue");
const accuracyValue = document.getElementById("accuracyValue");
const masteryList = document.getElementById("masteryList");

function loadState() {
  const saved = localStorage.getItem("skillsprint-state");
  if (!saved) return structuredClone(defaultState);
  try {
    const parsed = JSON.parse(saved);
    return {
      ...structuredClone(defaultState),
      ...parsed,
      topicStats: { ...structuredClone(defaultState).topicStats, ...(parsed.topicStats || {}) },
    };
  } catch {
    return structuredClone(defaultState);
  }
}

function saveState() {
  localStorage.setItem("skillsprint-state", JSON.stringify(state));
}

function topicMastery(topic) {
  const stats = state.topicStats[topic];
  if (!stats || stats.asked === 0) return 0.35;
  return stats.correct / stats.asked;
}

function chooseQuestion() {
  const weighted = questionBank.map((q) => {
    const mastery = topicMastery(q.topic);
    const weaknessWeight = 1.2 - mastery;
    const difficultyWeight = 1 + q.difficulty * 0.15;
    return { q, weight: Math.max(0.2, weaknessWeight * difficultyWeight) };
  });

  const total = weighted.reduce((sum, item) => sum + item.weight, 0);
  let threshold = Math.random() * total;

  for (const item of weighted) {
    threshold -= item.weight;
    if (threshold <= 0) return item.q;
  }

  return questionBank[Math.floor(Math.random() * questionBank.length)];
}

function setFeedback(message, type) {
  feedback.textContent = message;
  feedback.className = `feedback ${type}`;
}

function renderStats() {
  xpValue.textContent = String(state.xp);
  streakValue.textContent = `${state.streak} 🔥`;
  const accuracy = state.attempts ? Math.round((state.correct / state.attempts) * 100) : 0;
  accuracyValue.textContent = `${accuracy}%`;

  masteryList.innerHTML = "";
  topics
    .slice()
    .sort((a, b) => topicMastery(a) - topicMastery(b))
    .forEach((topic) => {
      const mastery = Math.round(topicMastery(topic) * 100);
      const row = document.createElement("div");
      row.className = "mastery-row";
      row.innerHTML = `
        <div><strong>${topic}</strong> — ${mastery}% mastery</div>
        <div class="progress-track">
          <div class="progress-fill" style="width: ${mastery}%;"></div>
        </div>
      `;
      masteryList.append(row);
    });
}

function loadQuestion() {
  currentQuestion = chooseQuestion();
  answeredCurrent = false;

  topicBadge.textContent = currentQuestion.topic;
  difficultyBadge.textContent = `Level ${currentQuestion.difficulty}`;
  questionText.textContent = currentQuestion.prompt;
  hintText.textContent = `Hint: ${currentQuestion.hint}`;
  solutionText.textContent = currentQuestion.solution;

  answerInput.value = "";
  nextBtn.disabled = true;
  checkBtn.disabled = false;
  skipBtn.disabled = false;
  setFeedback("", "");
}

function evaluateAnswer(answer, q) {
  if (!answer.trim()) return false;
  const lower = answer.toLowerCase();
  const hits = q.answerKeywords.filter((keyword) => lower.includes(keyword.toLowerCase())).length;
  return hits >= Math.max(1, Math.ceil(q.answerKeywords.length / 2));
}

checkBtn.addEventListener("click", () => {
  if (!currentQuestion || answeredCurrent) return;

  const correct = evaluateAnswer(answerInput.value, currentQuestion);
  const topicStats = state.topicStats[currentQuestion.topic];

  state.attempts += 1;
  topicStats.asked += 1;

  if (correct) {
    answeredCurrent = true;
    state.correct += 1;
    state.streak += 1;
    state.xp += 10 + currentQuestion.difficulty * 2;
    topicStats.correct += 1;
    setFeedback("✅ Nice! You got it. +XP earned.", "correct");
  } else {
    answeredCurrent = true;
    state.streak = 0;
    setFeedback("❌ Not quite yet. Review the solution and try the next one.", "incorrect");
  }

  checkBtn.disabled = true;
  skipBtn.disabled = true;
  nextBtn.disabled = false;

  saveState();
  renderStats();
});

skipBtn.addEventListener("click", () => {
  if (!currentQuestion || answeredCurrent) return;
  answeredCurrent = true;

  const topicStats = state.topicStats[currentQuestion.topic];
  topicStats.asked += 1;
  topicStats.skipped += 1;
  state.streak = 0;

  setFeedback("⏭️ Skipped. No XP change, but we'll revisit this topic.", "skipped");

  checkBtn.disabled = true;
  skipBtn.disabled = true;
  nextBtn.disabled = false;

  saveState();
  renderStats();
});

nextBtn.addEventListener("click", loadQuestion);

resetProgressBtn.addEventListener("click", () => {
  Object.assign(state, structuredClone(defaultState));
  saveState();
  renderStats();
  loadQuestion();
});

renderStats();
loadQuestion();
