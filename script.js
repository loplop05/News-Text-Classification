const newsText = document.getElementById('newsText');
const classifyBtn = document.getElementById('classifyBtn');
const clearBtn = document.getElementById('clearBtn');
const statusText = document.getElementById('statusText');

async function classifyText(text) {
  const response = await fetch('/predict', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ text })
  });

  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error || 'Classification failed.');
  }
  return data;
}

classifyBtn.addEventListener('click', async () => {
  const text = newsText.value.trim();

  if (!text) {
    statusText.textContent = 'Please enter news text before classifying.';
    return;
  }

  statusText.textContent = 'Classifying...';

  try {
    const result = await classifyText(text);
    if (typeof result.confidence === 'number') {
      const confidencePercent = result.confidence <= 1 ? result.confidence * 100 : result.confidence;
      statusText.textContent = `Category: ${result.category} (confidence: ${confidencePercent.toFixed(1)}%).`;
    } else {
      statusText.textContent = `Category: ${result.category}.`;
    }
  } catch (error) {
    statusText.textContent = error.message || 'Unable to classify text.';
  }
});

clearBtn.addEventListener('click', () => {
  newsText.value = '';
  statusText.textContent = 'No classification yet.';
  newsText.focus();
});
