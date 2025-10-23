from embedding import SentenceTransformerEmbeddings,ConfigEmbeddings
from qdrant_client import QdrantClient,models
from qdrant_client.http.models import Distance,VectorParams
import pymongo
class RAG:
    def __init__(self,
                 llm,
                 type:str,
                 qdrant_url:str=None,
                 qdrant_api:str=None,
                 db_name:str=None,
                 db_collection:str=None,
                 embedding_model:str=None,
                 mongo_url:str=None,
    ):
        self.type = type
        if self.type == 'qdrant':
            self.qdrant_url = qdrant_url
            self.qdrant_api = qdrant_api
            self.qdrant_collection = "datachatbot3"
            self.client = QdrantClient(self.qdrant_url,self.qdrant_api)
        elif self.type == 'mongodb':
            self.client = pymongo.MongoClient(mongo_url)
            self.db = self.client[db_name]
            self.collection = self.db[db_collection]
        self.embedding_model = SentenceTransformerEmbeddings(ConfigEmbeddings(name=embedding_model))
        self.llm = llm
    def check_collection_exist(self):
        if self.type =="qdrant":
            try:
                collections = self.client.get_collections().collections
                collection_name = [col.name for col in collections]
                return self.qdrant_collection in collection_name
            except Exception as e:
                return False
    def get_embedding(self,text):
        if not text.strip():
            return []
        embedding = self.embedding_model.encode(text)
        return embedding
    def vector_search(self,query:str,top_k = 3):
        query_embedding = self.get_embedding(query)
        if query_embedding is None:
            return "Invalid query or embedding failed"
        if self.type == 'qdrant':
            if self.check_collection_exist():
                hits = self.client.query_points(
                    collection_name=self.qdrant_collection,
                    query=query_embedding,
                    limit=top_k,
                )
                results = []
                for hit in hits.points:
                    results.append({
                        "score": hit.score,
                        "text": hit.payload.get("page_content") if "page_content" in hit.payload else None,
                    }
                    )
                return results
            else:
                print(f"Collection {self.qdrant_collection} does not exist")
    def generate_content(self,prompt):
        return self.llm.generate_content(prompt)


