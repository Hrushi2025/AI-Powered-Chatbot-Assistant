from fastapi import FastAPI
from pydantic import BaseModel
from intent_service import chatbot_response  # your intent service module

app = FastAPI(title="AI-Powered Chatbot Assistant")

class QueryRequest(BaseModel):
    user_id: str
    query: str

@app.post("/chat")
def chat(request: QueryRequest):
    response = chatbot_response(request.query, request.user_id)
    return {"query": request.query, "response": response}

@app.get("/")
def root():
    return {"message": "AI-Powered Chatbot Assistant is running."}
