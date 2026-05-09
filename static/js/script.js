// Sample text setter
function setSample(text) {
    document.getElementById('newsText').value = text;
    document.getElementById('newsText').focus();
}

// Demo Form Handler
document.getElementById('demoForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const text = document.getElementById('newsText').value.trim();
    const btn = document.getElementById('classifyBtn');
    const resultBox = document.getElementById('resultBox');
    
    if (!text) {
        alert('Please enter some text to classify!');
        return;
    }
    
    // Show loading state
    btn.disabled = true;
    btn.classList.add('loading');
    resultBox.style.display = 'none';
    
    // Call real API instead of simulation
    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: text }),
    })
    .then(response => response.json())
    .then(data => {
        // Display result
        document.getElementById('predictedLabel').textContent = data.category;
        document.getElementById('confidence').textContent = 'Calculated by ML Model';
        resultBox.style.display = 'block';
        
        // Reset button
        btn.disabled = false;
        btn.classList.remove('loading');
        
        // Scroll to result
        resultBox.scrollIntoView({ behavior: 'smooth', block: 'center' });
    })
    .catch((error) => {
        console.error('Error:', error);
        alert('An error occurred while classifying the text.');
        btn.disabled = false;
        btn.classList.remove('loading');
    });
});

// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Add scroll animation
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('fade-in-up');
        }
    });
}, { threshold: 0.1 });

document.querySelectorAll('.custom-card, .model-card, .result-image').forEach(el => {
    observer.observe(el);
});
