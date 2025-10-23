from pydantic import BaseModel
from typing import List,Dict,Any

class ChatHistory(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    query: str
    history: List[ChatHistory]=[]
