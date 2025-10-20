from insert_data import QdrantLocal,BaseConfigDB,BaseVectorDB

def main():
    my_config = BaseConfigDB(
        name="QdrantLocal",
        db_collection="test_collection",
        db_url="localhost:6333",
        vector_size=1024,
        embedding_path="./data"
    )
    db = QdrantLocal(config=my_config)
    db.init_db_collection()
    data = db.load_embedding()
    db.insert_vector_embedding(embedding_to_db=data)


if __name__ == "__main__":
    main()