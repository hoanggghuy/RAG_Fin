from dotenv import load_dotenv
import os
from rag.core import RAG
from embedding import SentenceTransformerEmbeddings,ConfigEmbeddings
from reflection import Reflection
from semantic_router import SemanticRouter,Route
from semantic_router.samples import chitchatSample,productsSample
import openai
from llms.llms import LLMs
import argparse

load_dotenv()
os.environ["TF_ENABLE_ONEDNN_OPTS"]="0"

def main(args):
    product_route_name = "product"
    chitchat_route_name = "chitchat"
    # Setup SemanticRouter
    embedding = SentenceTransformerEmbeddings(ConfigEmbeddings(name=args.embedding_model))
    product_route = Route(name=product_route_name,sample=productsSample)
    chitchat_route = Route(name=chitchat_route_name,sample=chitchatSample)
    router = SemanticRouter(embedding=embedding,routes=[chitchat_route,product_route])

    # Setup LLMs
    if args.mode == "online" and args.model_engine == "gemini":
        MODEL_API_KEY = os.getenv("GEMINI_API_KEY")
        MODEL_BASE_URL = None
        if not MODEL_API_KEY:
            print("GEMINI_API_KEY environment variable is not set")
    elif args.mode == "online" and args.model_engine == "openai":
        MODEL_API_KEY = os.getenv("OPENAI_API_KEY")
        MODEL_BASE_URL = None
        if not MODEL_API_KEY:
            print("OPENAI_API_KEY environment variable is not set")
    elif args.mode == "offline" and args.model_engine == "ollama":
        MODEL_BASE_URL = os.getenv("OLLAMA_BASE_URL",None)
        MODEL_API_KEY = None
    else:
        raise ValueError(f"Unsupported model engine: {args.model_engine}")

    llm = LLMs(type=args.mode,model_name=args.model_name,model_version=args.model_version,engine=args.model_engine,base_url=MODEL_BASE_URL,api_key=MODEL_API_KEY)

    # Init reflection
    reflection = Reflection(llm=llm)

    #Init RAG
    if args.db == 'qdrant':
        QDRANT_API = os.getenv("QDRANT_API",None)
        QDRANT_URL = os.getenv("QDRANT_URL",None)
        if not QDRANT_API:
            print("QDRANT_API environment variable is not set")
        if not QDRANT_URL:
            print("QDRANT_URL environment variable is not set")

        rag = RAG(
            type = 'qdrant',
            qdrant_api=QDRANT_API,
            qdrant_url=QDRANT_URL,
            embedding_model=args.embedding_model,
            llm=llm,
        )
    else:
        print("Only supported Qdrant mode ....")

    query = input("Please enter a query: ")
    score, router_name =router.guide(query)
    if router_name == product_route_name:
        reflected_query = reflection(data,query=query)
        docs = rag.vector_search(query=reflected_query,top_k=2)
        source_information = ""
        for doc in docs:
            source_information += doc["text"]
        combined_information = f"Hãy trở thành chuyên gia tư vấn bán hàng cho một cửa hàng điện thoại. Câu hỏi của khách hàng: {reflected_query}\nTrả lời câu hỏi dựa vào các thông tin sản phẩm dưới đây: {source_information}."
        data.append({
            "role": "user",
            "content": combined_information
        }
        )
        response = llm.generate_content(data)
        print(reflected_query)
        print("-----------------------------")
    elif router_name == chitchat_route_name:
        query_chitchat = [{
            "role": "user",
            "content": query
        }]
        response = llm.generate_content(query_chitchat)
    print(response)
    print("-----------------------------")
    print(data)
    print("-----------------------------")
    print(router_name)



if __name__ == "__main__":
    data = []
    parser = argparse.ArgumentParser()
    model_group = parser.add_argument_group("Model Option")
    model_group.add_argument('-m','--mode', type=str, choices=['online', 'offline'], default='online', help='Choose either online or offline mode system')
    model_group.add_argument('-n','--model_name', type=str, default='openai', help='Define name of LLM model to use')
    model_group.add_argument('-e','--model_engine', type=str, default='openai', help='Define model engine of LLM model (Optional)')
    model_group.add_argument('-v','--model_version', type=str,default='gpt-5-nano' , help='')

    feature_group = parser.add_argument_group("Feature Option")
    feature_group.add_argument('--db', type=str, choices=['qdrant', 'mongodb', 'chromadb'], default='qdrant', help='Choose type of vector store database')
    feature_group.add_argument('--embedding_model', type=str, default='Qwen/Qwen3-Embedding-0.6B', help='Declare what embedding model to use for RAG')

    args = parser.parse_args()
    while True:
        main(args)

