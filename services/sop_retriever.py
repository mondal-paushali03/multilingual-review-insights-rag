import numpy as np

class SOPRetriever:
    def __init__(self, embedding_store):
        self.store = embedding_store

    def retrieve(self, query, top_k=3):
        return self.store.query(query, top_k)
