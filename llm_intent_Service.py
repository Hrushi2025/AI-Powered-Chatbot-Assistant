# llm_intent_service.py
from llm_service import generate_llm_response

def predict_intent(user_query: str):
    # For now, all unrecognized queries go to LLM
    return "llm"

def chatbot_response(user_query: str, user_id: str = "U001", language: str = "en"):
    return generate_llm_response(user_query, user_id, language)

# Testing mode
if __name__ == "__main__":
    print("Local LLM Chatbot Test Mode (type 'exit' to quit)")
    while True:
        query = input("You: ")
        if query.lower() in ["exit", "quit"]:
            break
        answer = chatbot_response(query)
        print("Bot:", answer)
