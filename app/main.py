import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uvicorn
from rag.core import RAG
from embedding import SentenceTransformerEmbeddings, ConfigEmbeddings
from reflection import Reflection
from semantic_router import SemanticRouter, Route
from semantic_router.samples import chitchatSample, productsSample
from llms.llms import LLMs
load_dotenv()
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

class ChatItem(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    query: str
    history: List[ChatItem] = []

class ChatResponse(BaseModel):
    response: str
    router_name: str
    reflected_query: Optional[str] = None
    history: List[ChatItem]

MODE = os.getenv("MODE", "online")
MODEL_NAME = os.getenv("MODEL_NAME", "openai")
MODEL_ENGINE = os.getenv("MODEL_ENGINE", "openai")
MODEL_VERSION = os.getenv("MODEL_VERSION", "gpt-5-nano") # Tên này có vẻ là placeholder, bạn hãy chắc chắn nó đúng
DB_TYPE = os.getenv("DB_TYPE", "qdrant")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "Qwen/Qwen3-Embedding-0.6B")

print("Initializing Semantic Router...")
product_route_name = "product"
chitchat_route_name = "chitchat"
embedding = SentenceTransformerEmbeddings(ConfigEmbeddings(name=EMBEDDING_MODEL))
product_route = Route(name=product_route_name, sample=productsSample)
chitchat_route = Route(name=chitchat_route_name, sample=chitchatSample)
router = SemanticRouter(embedding=embedding, routes=[chitchat_route, product_route])
print("Semantic Router initialized.")

print("Initializing LLM...")
MODEL_API_KEY = None
MODEL_BASE_URL = None

if MODE == "online" and MODEL_ENGINE == "gemini":
    MODEL_API_KEY = os.getenv("GEMINI_API_KEY")
    if not MODEL_API_KEY:
        print("GEMINI_API_KEY environment variable is not set")
elif MODE == "online" and MODEL_ENGINE == "openai":
    MODEL_API_KEY = os.getenv("OPENAI_API_KEY")
    if not MODEL_API_KEY:
        print("OPENAI_API_KEY environment variable is not set")
elif MODE == "offline" and MODEL_ENGINE == "ollama":
    MODEL_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    MODEL_API_KEY = "ollama" # Thường không cần key, nhưng class của bạn có thể cần
else:
    raise ValueError(f"Unsupported model engine: {MODEL_ENGINE}")

llm = LLMs(type=MODE, model_name=MODEL_NAME, model_version=MODEL_VERSION, engine=MODEL_ENGINE, base_url=MODEL_BASE_URL, api_key=MODEL_API_KEY)
print(f"LLM initialized (Mode: {MODE}, Engine: {MODEL_ENGINE}, Name: {MODEL_NAME}).")

# Init reflection
print("Initializing Reflection...")
reflection = Reflection(llm=llm)
print("Reflection initialized.")

print("Initializing RAG...")
if DB_TYPE == 'qdrant':
    QDRANT_API = os.getenv("QDRANT_API")
    QDRANT_URL = os.getenv("QDRANT_URL")
    if not QDRANT_API:
        print("QDRANT_API environment variable is not set")
    if not QDRANT_URL:
        print("QDRANT_URL environment variable is not set")

    rag = RAG(
        type='qdrant',
        qdrant_api=QDRANT_API,
        qdrant_url=QDRANT_URL,
        embedding_model=EMBEDDING_MODEL,
        llm=llm,
    )
    print("RAG (Qdrant) initialized.")
else:
    print(f"Unsupported DB type: {DB_TYPE}. Only Qdrant is supported.")
    # Có thể raise Exception ở đây nếu muốn
    rag = None

app = FastAPI(
    title="RAG Chatbot API",
    description="API cho chatbot RAG với Semantic Router và Reflection"
)
print("FastAPI app created. Server is starting...")


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Endpoint chính để xử lý chat.
    Nhận vào câu query và lịch sử chat, trả về câu trả lời và lịch sử mới.
    """
    if not rag:
        return {"error": "RAG system is not initialized."}  # Xử lý lỗi nếu RAG init fail

    query = request.query
    # Chuyển đổi Pydantic models (history) về dạng list[dict] mà code của bạn đang dùng
    history_dicts: List[Dict[str, Any]] = [item.dict() for item in request.history]

    response_content = ""
    reflected_query_str = None

    # 1. Phân loại query
    score, router_name = router.guide(query)

    if router_name == product_route_name:
        # 2. Reflection (nếu là product)
        # Hàm reflection của bạn (theo trí nhớ của tôi) sẽ dùng history và query mới
        reflected_query_str = reflection(history_dicts, query=query)

        # 3. Vector Search
        docs = rag.vector_search(query=reflected_query_str, top_k=2)
        source_information = ""
        for doc in docs:
            source_information += doc["text"] + "\n"  # Thêm newline cho dễ đọc

        # 4. Tạo prompt và thêm vào history
        combined_information = f"Hãy trở thành chuyên gia tư vấn bán hàng cho một cửa hàng điện thoại. Câu hỏi của khách hàng: {reflected_query_str}\nTrả lời câu hỏi dựa vào các thông tin sản phẩm dưới đây: {source_information}."

        history_dicts.append({
            "role": "user",
            "content": combined_information
        })

        # 5. Gọi LLM
        response_content = llm.generate_content(history_dicts)

    elif router_name == chitchat_route_name:
        # Xử lý chitchat, nhưng vẫn nên đưa history vào để duy trì ngữ cảnh
        history_dicts.append({
            "role": "user",
            "content": query
        })
        response_content = llm.generate_content(history_dicts)

    # 6. Thêm câu trả lời của AI vào lịch sử
    history_dicts.append({
        "role": "assistant",
        "content": response_content
    })

    # 7. Chuyển đổi list[dict] trở lại list[ChatItem] để validate response
    final_history = [ChatItem(**item) for item in history_dicts]

    return ChatResponse(
        response=response_content,
        router_name=router_name,
        reflected_query=reflected_query_str,
        history=final_history
    )


# --- 6. CHẠY SERVER ---
if __name__ == "__main__":
    print("Starting Uvicorn server on http://0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)