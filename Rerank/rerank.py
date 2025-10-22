from sentence_transformers import CrossEncoder
import numpy as np


class Reranker:
    def __init__(self,model_name: str):
        self.reranker = CrossEncoder(model_name,trust_remote_code=True)
    def __call__(self, query: str, passage: list[str]) -> tuple[list[float], list[str]]:
        query_passage_pairs = [[query, passage] for passage in passage]
        scores = self.reranker.predict(query_passage_pairs)

        ranked_passages = [passage for passage, score in sorted(zip(passage, scores), key=lambda x:x[1], reverse=True)]
        ranked_scores = sorted(scores,reverse=True)
        ranked_scores = [float(score) for score in ranked_scores]
        return ranked_scores, ranked_passages
