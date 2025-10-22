from insert_data.chunk_service import chunk_data
input = r"C:\Users\ADMIN\Desktop\RAG\data\data_raw\rag_documents_grouped.json"
output = r"C:\Users\ADMIN\Desktop\RAG\data\data_chunked\data_chunked.json"

a = chunk_data(input,output,chunk_size=800,chunk_overlap=50)
