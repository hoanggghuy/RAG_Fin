from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class ChatHistory(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    query: str
    session_id: Optional[str] = None
class ChatResponse(BaseModel):
    response: str
    router_name: str
    reflected_query: Optional[str] =None
    history: Optional[List[Dict[str,str]]] =[]
    session_id: str