# Intelligent Content Moderation using NLP and Machine Learning

## Overview

Intelligent Content Moderation is an AI-powered Natural Language Processing (NLP) system designed to automatically classify user-generated text into:

* Hate Speech
* Offensive Language
* Neither

The project uses a complete machine learning pipeline including text preprocessing, TF-IDF vectorization, model comparison, evaluation, and deployment using Flask.

---

## Problem Statement

Social media platforms generate large amounts of user content every day. Manual moderation is difficult and time-consuming. This project aims to automate the detection of harmful content and assist moderation systems using machine learning.

---

## Features

* Hate Speech Detection
* Offensive Language Detection
* Neutral Content Detection
* Advanced Text Preprocessing Pipeline
* TF-IDF Feature Engineering
* N-Gram Analysis
* Multiple Machine Learning Models
* Flask-Based Web Application
* Interactive User Interface
* Real-Time Text Classification

---

## Dataset

The dataset contains labeled social media posts categorized into:

| Label | Category           |
| ----- | ------------------ |
| 0     | Hate Speech        |
| 1     | Offensive Language |
| 2     | Neither            |

The dataset was obtained from Kaggle and includes thousands of social media text samples.

---

## NLP Pipeline

Raw Text

↓

Text Cleaning

↓

Tokenization

↓

Stopword Removal

↓

Lemmatization

↓

TF-IDF Vectorization

↓

Model Training

↓

Prediction

---

## Machine Learning Models Evaluated

### Logistic Regression

Used as a baseline classifier for multiclass text classification.

### Multinomial Naive Bayes

A probabilistic text classification algorithm commonly used in NLP tasks.

### LinearSVC

Selected as the final model due to its superior performance on sparse high-dimensional TF-IDF features.

---

## Model Performance

| Model                   | Accuracy |
| ----------------------- | -------- |
| Logistic Regression     | 85.1%    |
| Multinomial Naive Bayes | 83.6%    |
| LinearSVC               | 87.6%    |

Final Model: LinearSVC

---

## Technologies Used

### Programming Language

* Python

### Machine Learning

* Scikit-Learn
* NLTK
* NumPy
* Pandas

### Web Development

* Flask
* HTML
* CSS
* JavaScript
* Jinja2

---

## Project Structure

```text
Intelligent-Content-Moderation/
│
├── app.py
├── final_model.pkl
├── tfidf_vectorizer.pkl
├── requirements.txt
├── README.md
│
├── templates/
├── static/
├── notebook/
└── screenshots/
```

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/Intelligent-Content-Moderation.git
```

Navigate to the project folder:

```bash
cd Intelligent-Content-Moderation
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000/
```

---

## Key Learnings

* Natural Language Processing
* Feature Engineering
* TF-IDF Vectorization
* Sparse Matrix Representation
* Model Evaluation
* Precision, Recall and F1 Score
* Class Imbalance Handling
* Machine Learning Deployment
* Flask Application Development

---

## Challenges Faced

* Class imbalance in the dataset
* Distinguishing hate speech from offensive language
* Misclassification of semantically similar text
* Balancing model performance across classes

---

## Future Improvements

* BERT Integration
* Transformer-Based Classification
* Explainable AI Features
* Confidence Scoring
* Real-Time Moderation Dashboard
* API Deployment
* Cloud Hosting

---

## Author
N Sai Niharika

Developed as an NLP and Machine Learning project focused on automated content moderation and hate speech detection.
