# chatbot_service.py

import mysql.connector
from intent_service import predict_intent, get_db_connection
from llm_intent_service import chatbot_response as llm_chatbot_response

# ------------------------------
# Chatbot handlers
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
    return "\n".join([f"{r['asset_type']}: {r['quantity']}" for r in result])


def handle_market(user_query):
    if "buy" in user_query.lower():
        return "Market advice: Consider holding for now. Prices are volatile."
    elif "sell" in user_query.lower():
        return "Market advice: It might be a good time to sell a portion."
    else:
        return "Market trend: Overall stable, watch major indices."


def handle_loan(user_query, user_id="U001"):
    eligible_users = ["U001", "U002", "U003"]
    return "You are eligible for a loan up to $10,000." if user_id in eligible_users else "Not eligible for a loan."


def handle_faq(user_query):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT question, answer FROM faq")
    faqs = cursor.fetchall()
    cursor.close()
    conn.close()

    for faq in faqs:
        if faq['question'].lower() in user_query.lower():
            return faq['answer']
    return "Sorry, I could not find an answer to your question."


# ------------------------------
# Main chatbot response
# ------------------------------
def chatbot_response(user_query, user_id="U001"):
    intent = predict_intent(user_query)
    if intent == "portfolio":
        return handle_portfolio(user_query, user_id)
    elif intent == "market":
        return handle_market(user_query)
    elif intent == "loan":
        return handle_loan(user_query, user_id)
    elif intent == "faq":
        return handle_faq(user_query)
    else:
        # If intent not recognized, send to LLM for generative response
        return llm_chatbot_response(user_query, user_id)


# ------------------------------
# 4. Test block
# ------------------------------
if __name__ == "__main__":
    test_queries = [
        "How much bitcoin do I have?",
        "Should I invest in gold now?",
        "Am I eligible for a loan?",
        "How can I change my password?",
        "Tell me a joke",
        "Explain market trends for next week"
    ]
    for q in test_queries:
        print(f"Query: '{q}'\nResponse: {chatbot_response(q)}\n")
