from fastapi import FastAPI
from app.api.router import chat

app = FastAPI(
    title="RAG Chatbot",
    description="RAG Chatbot with SemanticRouter and Reflection"
)

@app.get("/")
async def read_root():
    return {"message": "Welcome to RAG Chatbot API! Go to /docs to test."}

app.include_router(chat.router)