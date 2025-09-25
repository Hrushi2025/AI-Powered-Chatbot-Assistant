# AI-Powered-Chatbot-Assistant
The AI-Powered Chatbot Assistant is a fully functional chatbot system designed to provide financial insights, explain transactions, guide loan eligibility, and answer FAQs. It integrates:

Intent classification engine – Determines user intent from queries.

FAQ and document retriever – Retrieves answers from a knowledge base (MySQL).

Local LLaMA/Alpaca LLM – Generates human-like, multilingual responses for complex queries.

Web GUI (Tkinter) – Simple interface for user interaction.

FastAPI backend – Handles requests from GUI and processes chatbot responses.

This project demonstrates an end-to-end conversational AI system with a self-contained local LLM, without relying on paid OpenAI API access.

Features

Intent Classification: Classifies queries into categories like portfolio, market, loan, faq, or sends to LLM if unknown.

FAQ/Document Retrieval: Queries the internal MySQL knowledge base for exact matches to user questions.

Local LLM Integration: Uses lightweight LLaMA/Alpaca/Vicuna models to generate natural, multilingual, and human-like responses.

Portfolio & Market Insights: Provides portfolio summaries and simple market advice.

Loan Eligibility Checks: Returns user eligibility based on predefined rules.

End-to-End GUI: Tkinter GUI for chatting with the bot, including multi-turn conversations.

FastAPI Backend: API layer connects GUI and chatbot engine, allowing scalable deployment.

Optional Enhancements:

Frontend switch to Streamlit or React.

GPU acceleration for LLM inference.

Conversation history storage in MySQL.

Multilingual translation before sending prompts to LLM.

Project Structure

<img width="999" height="815" alt="image" src="https://github.com/user-attachments/assets/4c5d4021-2a99-45ae-9d0b-b35b509474d5" />


File Descriptions
1. frontend/chatbot_ui.py

Tkinter-based GUI for chatting with the bot.

Starts FastAPI server in a background thread.

Sends user queries to FastAPI backend (/chat) and displays responses.

Features:

Scrollable chat area

Entry box for user input

Send button and Enter-key binding

2. backend/chatbot_service.py

Handles all intent-based query responses:

handle_portfolio() – fetches portfolio data from MySQL

handle_market() – simple buy/sell/hold advice

handle_loan() – checks user eligibility

handle_faq() – searches FAQ table in MySQL

Main entry: chatbot_response(user_query) – predicts intent and routes query.

3. backend/llm_intent_service.py

Routes queries to the local LLM if intent is unknown.

Uses generate_llm_response() from llm_service.py.

Supports multilingual responses and human-like generative answers.

4. backend/llm_service.py

Integrates local LLaMA/Alpaca/Vicuna models via HuggingFace Transformers.

Uses CPU or GPU (optional) for inference.

Example:

from transformers import LlamaForCausalLM, LlamaTokenizer
import torch

MODEL_NAME = "TheBloke/vicuna-7B-1.1-HF"
tokenizer = LlamaTokenizer.from_pretrained(MODEL_NAME)
model = LlamaForCausalLM.from_pretrained(MODEL_NAME, device_map="auto")

def generate_llm_response(prompt, user_id="U001", language="en"):
    inputs = tokenizer(prompt, return_tensors="pt")
    output = model.generate(**inputs, max_new_tokens=150)
    return tokenizer.decode(output[0])


Handles all queries that the intent engine cannot classify.

5. backend/intent_service.py

Predicts user intent.

Can use:

Pre-trained ML model (intent_model.pkl) + vectorizer

Or a simple rule-based classifier

Example intents: portfolio, market, loan, faq.

6. backend/routes.py

FastAPI API endpoint:

from fastapi import FastAPI
from backend.llm_intent_service import chatbot_response

app = FastAPI()

@app.post("/chat")
async def chat_api(payload: dict):
    user_query = payload.get("query", "")
    user_id = payload.get("user_id", "U001")
    response = chatbot_response(user_query, user_id)
    return {"response": response}


GUI or other clients send POST requests here.

7. models/ folder

Store ML models or vectorizers.

Optional if using rule-based intent classification.

8. data/ folder

Contains dummy MySQL tables for:

portfolio – sample user assets (≥100 rows recommended)

faq – question-answer pairs

9. requirements.txt

Include:

fastapi
uvicorn
tk
requests
transformers
torch
huggingface_hub
mysql-connector-python
scikit-learn
joblib

Setup Instructions

Clone Project

git clone <repo_url>
cd AI-Powered-Chatbot-Assistant


Create Virtual Environment & Install Dependencies

python -m venv .venv
.venv\Scripts\activate  # Windows
pip install --upgrade pip
pip install -r requirements.txt


Set Up MySQL Database

CREATE DATABASE chatbot_db;
USE chatbot_db;

-- Example portfolio table
CREATE TABLE portfolio(user_id VARCHAR(10), asset_type VARCHAR(50), quantity INT);
INSERT INTO portfolio VALUES ('U001', 'gold', 10), ('U001', 'bitcoin', 5);

-- Example FAQ table
CREATE TABLE faq(question VARCHAR(255), answer TEXT);
INSERT INTO faq VALUES ('How to reset password?', 'Go to settings -> reset password.');


Run Backend API

uvicorn backend.routes:app --reload


Run Frontend GUI

python frontend/chatbot_ui.py


Chat With Bot

Enter queries like:

"How much gold do I have?"

"Should I sell bitcoin?"

"Am I eligible for a loan?"

"How do I reset my password?"

Notes

No paid API required – Uses local LLaMA/Alpaca models.

Supports multilingual and generative responses.

Conversation can be extended to save chat history in MySQL or other databases.

Future enhancements:

Streamlit or React frontend

GPU acceleration

Advanced multilingual translation

Author

Hrushikesh Kanhaiya Pardeshi

Data Engineer / AI Enthusiast

Built end-to-end AI-powered financial chatbot using local LLM models
