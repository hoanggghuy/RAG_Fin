import json

from embedding import SentenceTransformerEmbeddings,ConfigEmbeddings

name_model = "Qwen/Qwen3-Embedding-0.6B"
model = SentenceTransformerEmbeddings(ConfigEmbeddings(name=name_model))
def embedding(input_path:str,model_name:str=None):
        with open(input_path,"r",encoding="utf-8") as f:
            texts = json.load(f)
        for text in texts:
            content = text.get("page_content")
            text["embedding"] = model.encode(content)
        with open(input_path,"w",encoding="utf-8") as f:
            json.dump(texts,f,ensure_ascii=False,indent=4)

if __name__ == "__main__":
    i = r"C:\Users\ADMIN\Desktop\RAG\data\data_to_db\data_chunked.json"
    embedding(i)
