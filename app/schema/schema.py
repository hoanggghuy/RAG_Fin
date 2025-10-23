from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class ChatHistory(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    query: str
    history: List[ChatHistory]
class ChatResponse(BaseModel):
    response: str
    router_name: str
    reflected_query: Optional[str] =None
    history: List[Dict[str, str]]
