import json
import os
from qdrant_client import QdrantClient
from qdrant_client.http import models


from insert_data import BaseConfigDB, OnlineConfigDB
class BaseVectorDB():
    def __init__(self, config: BaseConfigDB):
        self.config = config
    def init_db_collection(self):
        raise NotImplementedError("DB must be implemented by subclass")
    def insert_vector_embedding(self, embedding: list[list[float]]) :
        raise NotImplementedError("DB must be implemented by subclass")

class QdrantLocal(BaseVectorDB):
    def __init__(self, config: BaseConfigDB):
        super().__init__(config)
        self.config: BaseConfigDB = config
    def init_db_collection(self):
        self.client = QdrantClient(self.config.db_url)
        self.client.create_collection(
            collection_name=self.config.db_collection,
            vectors_config=models.VectorParams(size=self.config.vector_size,distance=models.Distance.COSINE),
        )
    def load_embedding(self):
        embedding =[]
        for filename in os.listdir(self.config.embedding_path):
            if filename.endswith(".json"):
                with open(os.path.join(self.config.embedding_path, filename), "r",encoding="UTF-8") as f:
                    embedding.extend(json.load(f))
        return embedding
    def insert_vector_embedding(self, embedding_to_db: list) :
        self.client = QdrantClient(self.config.db_url)
        points = []
        for idx, item in enumerate(embedding_to_db):
            points.append(
                models.PointStruct(
                    id=item.get("id",idx),
                    vector=list(item["embedding"]),
                    payload={
                        "product_name": item["metadata"]["product_name"],
                        "source_url": item["metadata"]["source_url"],
                        "category": item["metadata"]["category"],
                        "page_content": item.get("page_content"),
                    }
                )
            )
        self.client.upsert(
            collection_name=self.config.db_collection,
            wait=True,
            points=points,
        )



