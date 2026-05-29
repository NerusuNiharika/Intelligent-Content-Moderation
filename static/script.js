const analyzeBtn = document.getElementById('analyze-btn');
const userInput = document.getElementById('user-input');

const resultCard = document.getElementById('result-card');
const predictionText = document.getElementById('prediction-text');
const cleanedOutput = document.getElementById('cleaned-output');
const confidenceBar = document.getElementById('confidence-bar');
const confidenceValue = document.getElementById('confidence-value');
const predictionBox = document.getElementById('prediction-box');
const explanationOutput = document.getElementById('prediction-explanation');
const loading = document.getElementById('loading');

loading.classList.add('hidden');

analyzeBtn.addEventListener('click', async () => {

    const text = userInput.value.trim();

    if (text === '') {
        alert('Please enter text for analysis.');
        return;
    }

    resultCard.classList.add('hidden');
    loading.classList.remove('hidden');

    try {

        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                text: text
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Server Error');
        }

        loading.classList.add('hidden');
        resultCard.classList.remove('hidden');

        // Prediction
        predictionText.textContent = data.prediction;

        // Cleaned Text
        cleanedOutput.textContent = data.cleaned_text;

        // Confidence
        confidenceBar.style.width = `${data.confidence}%`;
        confidenceValue.textContent =
            `${data.confidence}% Confidence`;

        // Reset prediction box styling
        predictionBox.className = 'prediction-box';

        // Explanation + Color
        if (data.prediction === 'Hate Speech') {

            predictionBox.classList.add('hate');

            explanationOutput.textContent =
                'The text contains language that targets, attacks, or promotes hostility toward an individual or group.';

        }
        else if (data.prediction === 'Offensive Language') {

            predictionBox.classList.add('offensive');

            explanationOutput.textContent =
                'The text contains insulting, abusive, or offensive language but may not directly qualify as hate speech.';

        }
        else {

            predictionBox.classList.add('neither');

            explanationOutput.textContent =
                'The text does not contain hate speech or offensive language and is classified as normal content.';

        }

    }
    catch (error) {

        loading.classList.add('hidden');

        console.error('Prediction Error:', error);

        alert(`Error: ${error.message}`);

    }

});