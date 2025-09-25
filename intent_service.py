import sys
import mysql.connector
import os
import joblib

# ------------------------------
# 1. Load ML model
# ------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # current file directory
MODEL_PATH = os.path.join(BASE_DIR, "models", "intent_classifier.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "models", "tfidf_vectorizer.pkl")

if not os.path.exists(MODEL_PATH) or not os.path.exists(VECTORIZER_PATH):
    raise FileNotFoundError(
        f"Model or vectorizer not found.\nChecked paths:\n{MODEL_PATH}\n{VECTORIZER_PATH}\n"
        "Make sure your 'models' folder is in the project root."
    )

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)

# ------------------------------
# 2. Predict intent
# ------------------------------
def predict_intent(user_query: str) -> str:
    query_vec = vectorizer.transform([user_query])
    intent = model.predict(query_vec)[0]
    return intent

# ------------------------------
# 3. MySQL connection
# ------------------------------
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Hrushi@20",
            database="ai_chatbot"
        )
        return conn
    except mysql.connector.Error as err:
        print("Database connection error:", err)
        sys.exit(1)

# ------------------------------
# 4. Handlers
# ------------------------------
def handle_portfolio(user_query, user_id="U001"):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT asset_type, quantity FROM portfolio WHERE user_id=%s", (user_id,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    if not result:
        return "No portfolio data found."
    response = "Your portfolio:\n" + "\n".join([f"{r['asset_type']}: {r['quantity']}" for r in result])
    return response

def handle_market(user_query):
    if "buy" in user_query.lower():
        return "Market advice: Consider holding for now. Prices are volatile."
    elif "sell" in user_query.lower():
        return "Market advice: It might be a good time to sell a portion."
    else:
        return "Market trend: Overall stable, watch major indices."

def handle_loan(user_query, user_id="U001"):
    eligible_users = ["U001", "U002", "U003"]
    if user_id in eligible_users:
        return "You are eligible for a loan up to $10,000."
    else:
        return "You are currently not eligible for a loan."

def handle_faq(user_query):
    """
    Fetches FAQ answer from MySQL based on user query.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Simple search using LIKE (you can make it more sophisticated with NLP later)
    query = """
        SELECT answer 
        FROM faq
        WHERE question LIKE %s
        LIMIT 1
    """
    cursor.execute(query, (f"%{user_query}%",))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result:
        return result["answer"]
    else:
        return "Sorry, I could not find an answer to your question."


# ------------------------------
# 5. Main chatbot function
# ------------------------------
def chatbot_response(user_query, user_id="U001"):
    intent = predict_intent(user_query)  # only pass user_query
    if intent == "portfolio":
        return handle_portfolio(user_query, user_id)
    elif intent == "market":
        return handle_market(user_query)
    elif intent == "loan":
        return handle_loan(user_query, user_id)
    elif intent == "faq":
        return handle_faq(user_query)
    else:
        return "Sorry, I did not understand your query."
