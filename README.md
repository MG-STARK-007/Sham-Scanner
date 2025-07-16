# 🕵️ Sham Scanner – Fake Review Detection System

**Sham Scanner** is an AI-powered web application that detects exaggerated or fake product reviews using a combination of machine learning and heuristic analysis. It features a custom canvas-based CAPTCHA, fast classification, and human-like reasoning cues to improve trust and clarity.

---

## 🚀 Features

- 🧠 **Multinomial Naive Bayes Model** trained on real labeled reviews
- ✨ **TF-IDF Text Vectorization** with up to 5000 informative features
- 🗣️ **Hyperbole & Reasoning Detection** (e.g. exclamation marks, cue words)
- 🤖 **Canvas-based eCAPTCHA** to block bots
- 🌐 **Web Frontend** using HTML/CSS/JavaScript
- 📊 **Verdict Explanation** with confidence score & interpretation

---

## 📦 Project Structure

├── model.py # ML pipeline: training + evaluation ├── app.py # Flask API backend ├── templates/ │ └── index.html # Multi-step user interface ├── static/ │ ├── style.css # Frontend styling │ └── script.js # Page transitions + CAPTCHA logic ├── model/ │ ├── naive_bayes_fake_review_model.pkl │ └── tfidf_vectorizer.pkl └── fake_reviews_dataset.csv

---

## 📊 ML Model Summary

- **Algorithm:** Multinomial Naive Bayes (probabilistic text classifier)
- **Vectorizer:** TF-IDF (with stopword removal and max 5000 features)
- **Metrics:**
  - Accuracy: ~84.5%
  - Precision (Fake): 0.828
  - Recall (Fake): 0.869
  - F1 Score (Fake): 0.848

| Label         | Precision | Recall | F1-Score | Support |
|---------------|-----------|--------|----------|---------|
| Genuine (0)   | 0.864     | 0.822  | 0.843    | 4071    |
| Fake (1)      | 0.828     | 0.869  | 0.848    | 4016    |
| **Accuracy**  |           |        | 0.845    | 8087    |

---

## 🧪 How the System Works

1. 🖥️ Users start at a welcome page and solve a canvas-based CAPTCHA.
2. ✍️ They submit a product review.
3. 🧠 Backend processes:
   - Cleans + vectorizes the text
   - Classifies using Naive Bayes model
   - Checks for exaggeration and reasoning markers
4. ✅ Verdict returned with:
   - Confidence score
   - Reasoning detected
   - Visual indicator (Genuine or Fake)

---

## 🔒 Canvas eCAPTCHA

- Renders randomized text with distortion inside an HTML5 `<canvas>`
- Prevents automated bots from submitting fake reviews
- Integrated seamlessly with the review flow

---
