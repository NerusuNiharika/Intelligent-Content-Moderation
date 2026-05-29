from flask import Flask, render_template, request, jsonify
import joblib
import re
import nltk

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

app = Flask(__name__)

# Download required NLTK resources
nltk.download('stopwords')
nltk.download('wordnet')

# Load model and vectorizer
model = joblib.load('final_model.pkl')
vectorizer = joblib.load('tfidf_vectorizer.pkl')

# NLP setup
lemmatizer = WordNetLemmatizer()

stop_words = set(stopwords.words('english'))

# Keep negation words
negation_words = {'no', 'not', 'nor'}
stop_words = stop_words - negation_words


def clean_text(text):

    text = str(text)

    # lowercase
    text = text.lower()

    # remove URLs
    text = re.sub(r'http\S+|www\S+', '', text)

    # remove mentions and hashtags
    text = re.sub(r'@\w+|#\w+', '', text)

    # remove html artifacts
    text = re.sub(r'&amp;|&lt;|&gt;', '', text)

    # remove RT
    text = re.sub(r'\brt\b', '', text)

    # remove numbers
    text = re.sub(r'\d+', '', text)

    # normalize repeated characters
    text = re.sub(r'(.)\1{2,}', r'\1\1', text)

    # remove punctuation and special chars
    text = re.sub(r'[^a-zA-Z\s]', '', text)

    # tokenize
    tokens = text.split()

    # remove stopwords
    tokens = [word for word in tokens if word not in stop_words]

    # lemmatization
    tokens = [lemmatizer.lemmatize(word) for word in tokens]

    # remove short tokens
    tokens = [word for word in tokens if len(word) > 2]

    return " ".join(tokens)


label_map = {
    0: "Hate Speech",
    1: "Offensive Language",
    2: "Neither"
}


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "error": "No JSON data received"
            }), 400

        user_text = data.get("text", "")

        cleaned_text = clean_text(user_text)

        vectorized_text = vectorizer.transform([cleaned_text])

        prediction = model.predict(vectorized_text)[0]

        confidence = 95.0

        try:
            decision_scores = model.decision_function(vectorized_text)

            if hasattr(decision_scores, "max"):
                confidence = round(
                    float(abs(decision_scores.max()) * 10),
                    2
                )

                confidence = min(confidence, 99.0)

        except Exception:
            pass

        return jsonify({
            "prediction": label_map.get(int(prediction), str(prediction)),
            "cleaned_text": cleaned_text,
            "confidence": confidence
        })

    except Exception as e:

        print("\n========== ERROR ==========")
        print(type(e).__name__)
        print(str(e))
        print("===========================\n")

        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)