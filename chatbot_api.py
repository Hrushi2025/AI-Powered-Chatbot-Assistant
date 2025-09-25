from fastapi import FastAPI
from pydantic import BaseModel
from intent_service import chatbot_response  # same folder import

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

# ------------------------------
# 5. Run server with info output
# ------------------------------
if __name__ == "__main__":
    import uvicorn

    host = "127.0.0.1"
    port = 8000

    print(f"Server is starting...")
    print(f"Root endpoint → http://{host}:{port}/")
    print(f"Swagger UI → http://{host}:{port}/docs")
    print(f"ReDoc → http://{host}:{port}/redoc")

    uvicorn.run("chatbot_api:app", host=host, port=port, reload=True)
