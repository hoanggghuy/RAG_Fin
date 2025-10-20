from sentence_transformers import SentenceTransformer
from embedding import BaseEmbeddings,ConfigEmbeddings
class SentenceTransformerEmbeddings(BaseEmbeddings):
    def __init__(self,config = ConfigEmbeddings()):
        super().__init__(config.name)
        self.config = config
        self.embedding_model = SentenceTransformer(config.name,trust_remote_code=True)
    def encode(self,text:str):
        return self.embedding_model.encode(text)