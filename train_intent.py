import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import joblib

# ------------------------------
# 1. Define paths
# ------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # project root
MODELS_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(MODELS_DIR, exist_ok=True)

MODEL_PATH = os.path.join(MODELS_DIR, "intent_classifier.pkl")
VECTORIZER_PATH = os.path.join(MODELS_DIR, "tfidf_vectorizer.pkl")

# ------------------------------
# 2. Generate dummy dataset
# ------------------------------
data = [
    ("How much gold do I have?", "portfolio"),
    ("Show me my bitcoin balance", "portfolio"),
    ("Should I buy stocks now?", "market"),
    ("What is the market trend today?", "market"),
    ("Am I eligible for a loan?", "loan"),
    ("Explain my last deposit transaction", "loan"),
    ("How do I reset my password?", "faq"),
    ("Where can I download account statement?", "faq"),
]

queries = []
for i in range(15):  # repeat to get ~120 samples
    for q, intent in data:
        queries.append((q, intent))

df = pd.DataFrame(queries, columns=["query", "intent"])
df = df.sample(frac=1, random_state=42).reset_index(drop=True)  # shuffle

print(f"Dummy dataset created with {len(df)} samples.")

# ------------------------------
# 3. Split dataset
# ------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    df["query"], df["intent"], test_size=0.2, random_state=42
)

# ------------------------------
# 4. TF-IDF Vectorization
# ------------------------------
vectorizer = TfidfVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# ------------------------------
# 5. Train Logistic Regression
# ------------------------------
model = LogisticRegression(max_iter=200)
model.fit(X_train_vec, y_train)

# ------------------------------
# 6. Evaluate Model
# ------------------------------
y_pred = model.predict(X_test_vec)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

# ------------------------------
# 7. Save Model & Vectorizer
# ------------------------------
joblib.dump(model, MODEL_PATH)
joblib.dump(vectorizer, VECTORIZER_PATH)
print(f"Model and vectorizer saved in: {MODELS_DIR}")
