from fastapi import FastAPI
from routes import router

app = FastAPI(title="AI-Powered Chatbot Assistant")
app.include_router(router)
