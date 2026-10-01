from flask import Flask, render_template, request, jsonify
import joblib
import re
import nltk

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


app = Flask(__name__)


# =========================================================
# Download required NLTK resources
# =========================================================

nltk.download("stopwords")
nltk.download("wordnet")


# =========================================================
# Load trained model and TF-IDF vectorizer
# =========================================================

model = joblib.load("final_model.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")


# =========================================================
# NLP setup
# =========================================================

lemmatizer = WordNetLemmatizer()

stop_words = set(stopwords.words("english"))

# Keep important negation words
negation_words = {"no", "not", "nor"}
stop_words = stop_words - negation_words


# =========================================================
# Text preprocessing
# =========================================================

def clean_text(text):

    text = str(text)

    # Convert to lowercase
    text = text.lower()

    # Remove URLs
    text = re.sub(r"http\S+|www\S+", "", text)

    # Remove mentions and hashtags
    text = re.sub(r"@\w+|#\w+", "", text)

    # Remove HTML artifacts
    text = re.sub(r"&amp;|&lt;|&gt;", "", text)

    # Remove retweet marker
    text = re.sub(r"\brt\b", "", text)

    # Remove numbers
    text = re.sub(r"\d+", "", text)

    # Normalize repeated characters
    # Example: "soooo" -> "soo"
    text = re.sub(r"(.)\1{2,}", r"\1\1", text)

    # Remove punctuation and special characters
    text = re.sub(r"[^a-zA-Z\s]", "", text)

    # Tokenization
    tokens = text.split()

    # Remove stopwords
    tokens = [
        word for word in tokens
        if word not in stop_words
    ]

    # Lemmatization
    tokens = [
        lemmatizer.lemmatize(word)
        for word in tokens
    ]

    # Remove very short tokens
    tokens = [
        word for word in tokens
        if len(word) > 2
    ]

    return " ".join(tokens)


# =========================================================
# Label mapping
# =========================================================

label_map = {
    0: "Hate Speech",
    1: "Offensive Language",
    2: "Neither"
}


# =========================================================
# Home page
# =========================================================

@app.route("/")
def home():
    return render_template("index.html")


# =========================================================
# Prediction API
# =========================================================

@app.route("/predict", methods=["POST"])
def predict():

    try:

        # Get JSON data from frontend
        data = request.get_json()

        if not data:
            return jsonify({
                "error": "No JSON data received"
            }), 400

        # Get user text
        user_text = data.get("text", "")

        # Check empty input
        if not user_text or not str(user_text).strip():
            return jsonify({
                "error": "Please enter some text"
            }), 400

        # Clean input text
        cleaned_text = clean_text(user_text)

        # Check if text became empty after preprocessing
        if not cleaned_text.strip():
            return jsonify({
                "error": "Text contains no meaningful words after preprocessing"
            }), 400

        # Convert text into TF-IDF features
        vectorized_text = vectorizer.transform([cleaned_text])

        # Predict class
        prediction = model.predict(vectorized_text)[0]

        # Convert numeric prediction into category
        predicted_label = label_map.get(
            int(prediction),
            str(prediction)
        )

        # -------------------------------------------------
        # LinearSVC decision score
        # -------------------------------------------------
        # LinearSVC does not provide probabilities by default.
        # Therefore, this is a model decision score, NOT a
        # true probability/confidence percentage.

        prediction_score = None

        try:

            decision_scores = model.decision_function(
                vectorized_text
            )

            if hasattr(decision_scores, "max"):

                prediction_score = round(
                    float(abs(decision_scores.max())),
                    4
                )

        except Exception:
            prediction_score = None

        # Return result to frontend
        return jsonify({
            "prediction": predicted_label,
            "cleaned_text": cleaned_text,
            "prediction_score": prediction_score
        })

    except Exception as e:

        print("\n========== ERROR ==========")
        print(type(e).__name__)
        print(str(e))
        print("===========================\n")

        return jsonify({
            "error": str(e)
        }), 500


# =========================================================
# Run Flask application
# =========================================================

if __name__ == "__main__":
    app.run(debug=True)