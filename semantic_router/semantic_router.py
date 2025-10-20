import numpy as np

class Route:
    def __init__(self,name:str, sample:list):
        self.name = name
        self.sample = sample

class SemanticRouter:
    def __init__(self,embedding, routes):
        self.embedding = embedding
        self.routes = routes
        self.route_embedding = {}

        for route in self.routes:
            embedding = self.embedding.encode(route.sample)
            norm = np.linalg.norm(embedding,axis=1,keepdims=True)
            self.route_embedding[route.name] = embedding/norm
            """
            embedding is a matrix of shape (n_sample, dimension)
            norm is a vector of shape (n_sample, 1) with 1 is length of a vector
            embedding = [
            [3, 4, 0],  # Vector 1
            [5, 12, 0]  # Vector 2
            ]
            norm = [
             [5],
            [13]
            ]
            embedding/norm = [
            [0.6,   0.8,   0],   
            [0.38,  0.92,  0]     
            ]
            axit = 1: chuan hoa theo hang
            """
    def get_routes(self):
        return self.routes
    def guide(self, query):
        queryEmbedding = self.embedding.encode([query])
        queryEmbedding = queryEmbedding / np.linalg.norm(queryEmbedding)
        scores = []

        # Calculate the cosine similarity of the query embedding with the sample embeddings of the router.

        for route in self.routes:
            routesEmbedding = self.routesEmbedding[route.name]
            score = np.mean(np.dot(routesEmbedding, queryEmbedding.T).flatten())
            scores.append((score, route.name))

        scores.sort(reverse=True)
        return scores[0]