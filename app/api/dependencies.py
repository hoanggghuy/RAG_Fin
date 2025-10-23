from fastapi import HTTPException

from app.config.config import settings
from llms.llms import LLMs
from rag.core import RAG
from embedding import SentenceTransformerEmbeddings,ConfigEmbeddings
from reflection import Reflection
from semantic_router import SemanticRouter,Route
from semantic_router.samples import chitchatSample,productsSample

print("Initializing Dependencies")

#Set up LLM
MODEL_API_KEY = None
MODEL_BASE_URL = None
if settings.MODE == "online" and settings.MODEL_ENGINE == "gemini":
    MODEL_API_KEY = settings.GEMINI_API_KEY
elif settings.MODE == "online" and settings.MODEL_ENGINE == "openai":
    MODEL_API_KEY = settings.OPENAI_API_KEY
elif settings.MODE == "offline" and settings.MODEL_ENGINE == "ollama":
    MODEL_BASE_URL = settings.OLLAMA_BASE_URL
else:
    raise ValueError(f"Unsupported Model: {settings.MODEL_ENGINE}")
llm = LLMs(
    type=settings.MODE,
    model_name=settings.MODEL_NAME,
    api_key=MODEL_API_KEY,
    model_version=settings.MODEL_VERSION,
    base_url=MODEL_BASE_URL,
    engine=settings.MODEL_ENGINE,
)

print(f"LLM initialized: {settings.MODEL_ENGINE}")

#Setup EmbeddingModel
embedding = SentenceTransformerEmbeddings(ConfigEmbeddings(name=settings.EMBEDDING_MODEL))
print("Embeddings initialized")

#Setup SemanticRouter
product_route_name = "product"
chitchat_route_name = "chitchat"
product_route = Route(name=product_route_name, sample=productsSample)
chitchat_route = Route(name=chitchat_route_name, sample=chitchatSample)

router = SemanticRouter(embedding=embedding, routes=[product_route, chitchat_route])
print("Semantic Router initialized")

#Setup RAG
if settings.DB_TYPE == "qdrant":
    rag = RAG(
        llm=llm,
        type="qdrant",
        qdrant_url=settings.QDRANT_URL,
        embedding_model=settings.EMBEDDING_MODEL
    )
    print("RAG initialized")
else:
    print("Sorry, I only support the qdrant model")
#Set up Reflection
reflection = Reflection(llm=llm)
print("Reflection initialized")
async def get_llm() -> LLMs:
    return llm
async def get_rag() -> RAG:
    if rag is None:
        raise HTTPException(status_code=404, detail="RAG not initialized")
    return rag
async def get_semantic_router() -> SemanticRouter:
    return router
async def get_reflection() -> Reflection:
    return reflection
