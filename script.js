const newsText = document.getElementById('newsText');
const classifyBtn = document.getElementById('classifyBtn');
const clearBtn = document.getElementById('clearBtn');
const statusText = document.getElementById('statusText');

const rules = [
  { category: 'Sports', words: ['stadium', 'team', 'goal', 'league', 'coach', 'player', 'tournament'] },
  { category: 'Business', words: ['market', 'stock', 'economy', 'revenue', 'investment', 'profit', 'trade'] },
  { category: 'Technology', words: ['software', 'technology', 'ai', 'device', 'internet', 'application', 'algorithm'] },
  { category: 'Politics', words: ['government', 'election', 'minister', 'policy', 'parliament', 'vote', 'law'] }
];

function escapeRegExp(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function classifyText(text) {
  let bestCategory = 'General';
  let bestScore = 0;

  for (const rule of rules) {
    let score = 0;
    for (const word of rule.words) {
      const wordPattern = new RegExp(`\\b${escapeRegExp(word)}\\b`, 'i');
      if (wordPattern.test(text)) {
        score += 1;
      }
    }
    if (score > bestScore) {
      bestScore = score;
      bestCategory = rule.category;
    }
  }

  return { category: bestCategory, score: bestScore };
}

classifyBtn.addEventListener('click', () => {
  const text = newsText.value.trim();

  if (!text) {
    statusText.textContent = 'Please enter news text before classifying.';
    return;
  }

  const result = classifyText(text);

  if (result.score === 0) {
    statusText.textContent = 'Category: General (no clear keyword match).';
    return;
  }

  statusText.textContent = `Category: ${result.category} (matched ${result.score} keyword${result.score > 1 ? 's' : ''}).`;
});

clearBtn.addEventListener('click', () => {
  newsText.value = '';
  statusText.textContent = 'No classification yet.';
  newsText.focus();
});
