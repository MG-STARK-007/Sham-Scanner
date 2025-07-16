from flask import Flask, render_template, request, jsonify
import joblib
import os

app = Flask(__name__)

# Updated paths to load model and vectorizer from the "model" directory
MODEL_PATH = os.path.join("model", "naive_bayes_fake_review_model.pkl")
VECTORIZER_PATH = os.path.join("model", "tfidf_vectorizer.pkl")

try:
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
except Exception as e:
    raise RuntimeError(f"Error loading model or vectorizer: {e}")

def count_exclamations(text):
    return text.count("!")

def count_hyperbole(text):
    absurd_words = [
        "miracle", "life-changing", "unbelievable", "magic", "instantly","miraculous", "universe",
        "transformed", "cured", "revolutionary", "breathtaking", "perfect", "flawless","magical"
    ]
    return sum(word in text.lower() for word in absurd_words)

def has_reasoning(text):
    """Check for reasoning cues within the review."""
    reasoning_keywords = [
        " but ", " however ", " although ", " yet ", " because ",
        " due to ", " since ", " nonetheless ", " even though ", " though ",
        " while ", " despite "
    ]
    return any(keyword in text.lower() for keyword in reasoning_keywords)

def classify_review(review_text):
    """Predict review authenticity using the local model and format the output clearly."""
    try:
        X = vectorizer.transform([review_text])
        prediction = model.predict(X)[0]
        proba = model.predict_proba(X)[0]
        confidence = max(proba)
    except Exception as e:
        return f"❌ Model error: {e}"
    
    word_count = len(review_text.split())
    reasoning = has_reasoning(review_text)
    exclamations = count_exclamations(review_text)
    hyperbole_score = count_hyperbole(review_text)
    threshold = 0.77 
    exaggeration_risk = (exclamations >= 2 or hyperbole_score >= 2)
    fake_probability = round(confidence * 100 if prediction == 1 else (1 - confidence) * 100, 2)

    if (prediction == 1 and not reasoning and confidence > threshold) or exaggeration_risk :
        verdict = "⚠ Potentially Fake Review"
    elif prediction == 1:
        verdict = "⚠ Review May Be Fake"
    else:
        verdict = "✅ Review Appears Genuine"

    if exaggeration_risk:
        return (
            f"<strong>{verdict}</strong><br>"
            f"📌 <b>Prediction:</b> {1} ({'Fake'})<br>"
            f"🧠 <b>Reasoning Detected:</b> {reasoning}<br>"
            f"📈 <b>Confidence:</b> {confidence:.2f}<br>"
        )
    else:
        return (
        f"<strong>{verdict}</strong><br>"
        f"📌 <b>Prediction:</b> {prediction} ({'Fake' if prediction else 'Genuine'})<br>"
        f"🧠 <b>Reasoning Detected:</b> {reasoning}<br>"
        f"📈 <b>Confidence:</b> {confidence:.2f}<br>"
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/classify', methods=['POST'])
def classify():
    data = request.get_json()
    review_text = data.get('review_text')
    if not review_text:
        return jsonify({"error": "❌ No review text provided."})
    result = classify_review(review_text)
    return jsonify({"classification": result})

if __name__ == '__main__':
    app.run(debug=True)
