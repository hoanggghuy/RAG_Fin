from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    #Setting LLMs
    MODE: str = "online"
    MODEL_API_KEY: Optional[str] = None
    MODEL_BASE_URL: Optional[str] = None
    MODEL_NAME: str = "openai"
    MODEL_ENGINE: str = "openai"
    MODEL_VERSION: str = "gpt-5-mini"
    GEMINI_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    OLLAMA_BASE_URL: str = "https://localhost:11434"

    #Setting RAG&EMBEDDING
    DB_TYPE: str = "qdrant"
    EMBEDDING_MODEL: str = "Qwen/Qwen3-Embedding-0.6B"
    QDRANT_API_KEY: Optional[str] = None
    QDRANT_URL: Optional[str] = None

    TF_ENABLE_ONEDNN_OPTS: str = "0"

    class Config:
        env_file = ".env"
settings = Settings()
import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = settings.TF_ENABLE_ONEDNN_OPTS