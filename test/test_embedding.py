from embedding import SentenceTransformerEmbeddings,ConfigEmbeddings

name_model = "sentence-transformers/all-MiniLM-L6-v2"
model = SentenceTransformerEmbeddings(ConfigEmbeddings(name=name_model))
text = "Hello world"
print(model.encode(text))