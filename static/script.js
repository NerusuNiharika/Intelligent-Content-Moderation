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

    // Check empty input
    if (text === '') {
        alert('Please enter text for analysis.');
        return;
    }

    // Reset previous result
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


        // Handle server errors
        if (!response.ok) {
            throw new Error(data.error || 'Server Error');
        }


        // Hide loader
        loading.classList.add('hidden');

        // Show result
        resultCard.classList.remove('hidden');


        // =================================================
        // Prediction
        // =================================================

        predictionText.textContent = data.prediction;


        // =================================================
        // Cleaned Text
        // =================================================

        cleanedOutput.textContent = data.cleaned_text;


        // =================================================
        // Prediction Score
        // =================================================

        if (data.prediction_score !== null &&
            data.prediction_score !== undefined) {

            confidenceValue.textContent =
                `Model Decision Score: ${data.prediction_score}`;

            /*
             * LinearSVC decision score is NOT a percentage.
             * Therefore, we don't represent it as a percentage
             * using the width of the bar.
             */

            confidenceBar.style.width = '100%';

        }
        else {

            confidenceValue.textContent =
                'Model Decision Score: Not available';

            confidenceBar.style.width = '0%';
        }


        // =================================================
        // Reset Prediction Box Styling
        // =================================================

        predictionBox.className = 'prediction-box';


        // =================================================
        // Classification Explanation
        // =================================================

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