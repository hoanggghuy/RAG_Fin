from pydantic import BaseModel, Field, field_validator,PositiveInt

class BaseConfigDB(BaseModel):
    name: str = Field(..., description="The name of the VectorDatabase")
    db_collection: str = Field(..., description="The name of the collection")
    db_url: str = Field(..., description="The URL of the database")
    vector_size: PositiveInt = Field(..., description="Dimension of the embedding vectors")
    embedding_path: str = Field(..., description="The path of the embedding")
    @field_validator('name', 'db_collection', 'db_url','embedding_path')
    def check(cls, value:str):
        if not value.strip():
            raise ValueError("Field cannot be empty or just whitespace")
        return value
class OnlineConfigDB(BaseConfigDB):
    db_api_key: str = Field(..., description="The API key for the Online Database")
    @field_validator('db_api_key')
    def check_api(cls, value:str):
        if not value.strip():
            raise ValueError("Field cannot be empty or just whitespace")
        return value

