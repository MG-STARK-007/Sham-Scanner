import pandas as pd
import string
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, accuracy_score

# --- 1. Load dataset ---
df = pd.read_csv("fake_reviews_dataset.csv")  # Update filename if needed

# --- 2. Drop rows with missing or empty reviews ---
df = df.dropna(subset=["text_", "label"])
df = df[df["text_"].str.strip().astype(bool)]

# --- 3. Label Encoding: 1 = CG (fake), 0 = OR (genuine) ---
df["label_bin"] = df["label"].apply(lambda x: 1 if x.strip().upper() == "CG" else 0)

# --- 4. Text Preprocessing Function (optional but helpful) ---
def clean_text(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

df["clean_text"] = df["text_"].apply(clean_text)

# --- 5. Train/Test Split ---
X = df["clean_text"]
y = df["label_bin"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- 6. TF-IDF Vectorization ---
vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# --- 7. Train Naive Bayes Model ---
model = MultinomialNB()
model.fit(X_train_vec, y_train)

# --- 8. Evaluation ---
y_pred = model.predict(X_test_vec)
print("✅ Accuracy:", accuracy_score(y_test, y_pred))
print("\n📊 Classification Report:\n", classification_report(y_test, y_pred, digits=3))

# --- 9. Save Model and Vectorizer ---
os.makedirs("model", exist_ok=True)
joblib.dump(model, "model/naive_bayes_fake_review_model.pkl")
joblib.dump(vectorizer, "model/tfidf_vectorizer.pkl")

print("🎉 Model and vectorizer saved to the 'model/' directory.")
