import json
from fastapi import APIRouter, Request, Depends, HTTPException
from typing import List,Dict,Any
from app.api.dependencies import get_semantic_router,get_llm,get_rag,get_reflection
from app.schema.schema import ChatRequest,ChatHistory,ChatResponse
from llms.llms import LLMs
from rag.core import RAG
from reflection import Reflection
from semantic_router import SemanticRouter

router_chat = APIRouter(
    prefix="/chat",
    tags=["Userchat"]
)
PRODUCT_ROUTE_NAME = "product"
CHITCHAT_ROUTE_NAME = "chitchat"
SOURCE_CACHE = {}
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
    history_dicts: List[Dict[str,str]] = [item.dict() for item in request.history]

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
        history_dicts.append(
            {
                "role": "user",
                "content": combined_information,
            }
        )
        response = llm.generate_content(history_dicts)
    elif router_name == CHITCHAT_ROUTE_NAME:
        query_chitchat = [
            {
                "role": "user",
                "content": query,
            }
        ]
        response = llm.generate_content(query_chitchat)
    return ChatResponse(
        response=response,
        router_name=router_name,
        reflected_query=reflected_query,
        history=history_dicts,
    )