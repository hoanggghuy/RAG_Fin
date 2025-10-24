import json
from fastapi import APIRouter, Request, Depends, HTTPException
from typing import List,Dict,Any
from app.api.dependencies import get_semantic_router,get_llm,get_rag,get_reflection
from app.schema.schema import ChatRequest,ChatHistory,ChatResponse
from llms.llms import LLMs
from rag.core import RAG
from reflection import Reflection
from semantic_router import SemanticRouter
import uuid

router_chat = APIRouter(
    prefix="/chat",
    tags=["Userchat"]
)
PRODUCT_ROUTE_NAME = "product"
CHITCHAT_ROUTE_NAME = "chitchat"
SOURCE_CACHE = {}
CHAT_SESSIONS: Dict[str, List[Dict[str, str]]] = {}
@router_chat.post("/")
async def chat(
        request: ChatRequest,
        client_request: Request,
        llm: LLMs = Depends(get_llm),
        rag: RAG = Depends(get_rag),
        router_name: SemanticRouter = Depends(get_semantic_router),
        reflection: Reflection = Depends(get_reflection),
):
    query = request.query
    session_id = request.session_id
    if not session_id or session_id not in CHAT_SESSIONS:
        session_id = str(uuid.uuid4())
        history_dicts: List[Dict[str, str]] = []
        CHAT_SESSIONS[session_id] = history_dicts
    else:
        history_dicts = CHAT_SESSIONS[session_id]
    score, router_name = router_name.guide(query)
    reflected_query = None

    if router_name == PRODUCT_ROUTE_NAME:
        reflected_query = reflection(history_dicts,query)
        if reflected_query in SOURCE_CACHE:
            source_information = SOURCE_CACHE[reflected_query]
        else:
            docs = rag.vector_search(query=reflected_query,top_k=2)
            source_information = "\n".join([doc["text"] for doc in docs])
            SOURCE_CACHE[reflected_query] = source_information
        combined_information = f"Hãy trở thành chuyên gia tư vấn bán hàng cho một cửa hàng điện thoại. Câu hỏi của khách hàng: {reflected_query}\nTrả lời câu hỏi dựa vào các thông tin sản phẩm dưới đây: {source_information}."
        llm_input_history = list(history_dicts)
        llm_input_history.append(
            {
                "role": "user",
                "content": combined_information,
            }
        )
        response = llm.generate_content(llm_input_history)
        history_dicts.append({"role": "user", "content": query})
        history_dicts.append({"role": "assistant", "content": response})
    elif router_name == CHITCHAT_ROUTE_NAME:
        query_chitchat = [
            {
                "role": "user",
                "content": query,
            }
        ]
        response = llm.generate_content(query_chitchat)
    CHAT_SESSIONS[session_id] = history_dicts
    return ChatResponse(
        response=response,
        router_name=router_name,
        reflected_query=reflected_query,
        history=history_dicts,
        session_id=session_id,
    )