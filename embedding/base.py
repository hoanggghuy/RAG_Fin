from pydantic import BaseModel, Field, validators


class ConfigEmbeddings(BaseModel):
    name: str = Field(..., description="The name of the SentenceTransformer model")
    @validators("name")
    def check_name(cls, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("SentenceTransformer name cannot be empty")
        return value

class BaseEmbeddings():
    def __init__(self,name:str):
        super().__init__()
        self.name = name
    def encode(self,text:str):
        raise NotImplementedError("The encode method must be implemented by subclasses")