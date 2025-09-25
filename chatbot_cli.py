# frontend/chatbot_ui.py
import requests

API_URL = "http://127.0.0.1:8000/chat"

while True:
    query = input("You: ")
    if query.lower() in ["exit", "quit"]:
        break
    payload = {"user_id": "U001", "query": query}
    response = requests.post(API_URL, json=payload).json()
    print("Bot:", response.get("response"))
