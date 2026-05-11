// Initialize the page (verifies login + builds navbar)
function initPage(requireAuth) {
  if (localStorage.getItem('theme') === 'light') document.body.classList.add('light-mode');
  buildNavbar();
  if (requireAuth && !requireLogin()) return false;
  loadExplainableResult();
  return true;
}

// Load result data from localStorage (from previous analysis)
function loadExplainableResult() {
  const resultData = JSON.parse(localStorage.getItem('latestResult'));
  const summaryContainer = document.getElementById('summary');
  const explainContainer = document.getElementById('explanation');
  const recList = document.getElementById('recommendationsList');

  if (!resultData) {
    summaryContainer.innerHTML = `<p>No results found. Please analyze a URL, email, or SMS first.</p>`;
    return;
  }

  // Display summary
  summaryContainer.innerHTML = `
    <div class="result-card ${resultData.isPhishing ? 'phishing' : 'safe'}">
      <h2>${resultData.type.toUpperCase()} Analysis Result</h2>
      <p>Status: <strong>${resultData.isPhishing ? '⚠️ Phishing Detected' : '✅ Safe'}</strong></p>
      <p>Confidence: <strong>${resultData.confidence}%</strong></p>
      <p>Analyzed On: ${new Date(resultData.timestamp).toLocaleString()}</p>
    </div>
  `;

  // Explain why (or why not) phishing was detected
  explainContainer.innerHTML = `<h2>Explanation</h2>`;
  const list = document.createElement('ul');

  resultData.features.forEach(f => {
    const li = document.createElement('li');
    li.innerHTML = `
      <strong>${f.name}</strong>: ${f.description}
      <span class="feature-impact ${f.risk > 70 ? 'high' : f.risk > 40 ? 'medium' : 'low'}">
        Risk: ${f.risk}%
      </span>`;
    list.appendChild(li);
  });

  explainContainer.appendChild(list);

  // Visualize feature importance
  drawFeatureChart(resultData.features);

  // Recommendations
  const suggestions = getSafetyRecommendations(resultData);
  suggestions.forEach(s => {
    const li = document.createElement('li');
    li.textContent = s;
    recList.appendChild(li);
  });
}

// Chart for explainability
function drawFeatureChart(features) {
  const ctx = document.getElementById('featureChart').getContext('2d');
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: features.map(f => f.name),
      datasets: [{
        label: 'Risk Contribution (%)',
        data: features.map(f => f.risk),
        backgroundColor: features.map(f => 
          f.risk > 70 ? 'rgba(255, 80, 80, 0.7)' : 
          f.risk > 40 ? 'rgba(255, 180, 50, 0.7)' : 
          'rgba(80, 200, 120, 0.7)'
        ),
      }]
    },
    options: {
      plugins: {
        legend: { display: false },
        title: { display: true, text: 'Feature Risk Contributions' }
      },
      scales: {
        y: { beginAtZero: true, max: 100 }
      }
    }
  });
}

// Dynamic safety recommendations
function getSafetyRecommendations(result) {
  const recs = [];
  if (result.isPhishing) {
    recs.push("Do not click or share this link.");
    recs.push("Avoid entering personal information.");
    recs.push("Verify sender authenticity manually.");
    recs.push("Report this message to your IT/security team.");
  } else {
    recs.push("Continue to monitor links for suspicious updates.");
    recs.push("Stay cautious with unknown email senders.");
  }
  return recs;
}
