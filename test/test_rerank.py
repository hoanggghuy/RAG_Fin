from Rerank import Reranker

a = Reranker(model_name="Alibaba-NLP/gte-multilingual-base")
documents = [
    "Năng lượng mặt trời là nguồn năng lượng tái tạo giúp giảm khí thải CO2.",
    "Điện than tạo ra lượng lớn khí nhà kính và gây ô nhiễm không khí.",
    "Công nghệ pin mặt trời ngày càng rẻ và hiệu quả hơn.",
    "Lợi ích của việc tập thể dục thường xuyên đối với sức khỏe tim mạch.",
    "Năng lượng mặt trời có thể được sử dụng để cung cấp điện cho các hộ gia đình."
]
output = a(query = "Lợi ích của việc sử dụng năng lượng mặt trời",passage=documents)
print(output)
