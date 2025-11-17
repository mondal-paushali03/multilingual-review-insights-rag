import json
import numpy as np
import os
import faiss
from sentence_transformers import SentenceTransformer

class EmbeddingStore:
    def __init__(self, sop_json_path="data/sop_knowledge_base.json",
                 embed_model="all-MiniLM-L6-v2",
                 embed_cache="data/sop_embeddings.npy",
                 faiss_index_path="data/faiss.index"):

        self.sop_json_path = sop_json_path
        self.embed_model = embed_model
        self.embed_cache = embed_cache
        self.faiss_index_path = faiss_index_path

        self.embedder = SentenceTransformer(self.embed_model)

        with open(self.sop_json_path, "r") as f:
            self.sops = json.load(f)

        self.sop_texts = [
            f"{s['department']} — {s['sop_guideline']} — {s['action_summary']}"
            for s in self.sops
        ]

        self.embeddings = self._load_embeddings()
        self.index = self._load_or_build_faiss()

    def _load_embeddings(self):
        if os.path.exists(self.embed_cache):
            return np.load(self.embed_cache)

        emb = self.embedder.encode(self.sop_texts, convert_to_numpy=True)
        emb = emb.astype("float32")
        np.save(self.embed_cache, emb)
        return emb

    def _normalize(self, x):
        return x / np.linalg.norm(x, axis=1, keepdims=True)

    def _load_or_build_faiss(self):
        d = self.embeddings.shape[1]

        if os.path.exists(self.faiss_index_path):
            index = faiss.read_index(self.faiss_index_path)
            return index

        emb_norm = self._normalize(self.embeddings.copy())
        index = faiss.IndexFlatIP(d)
        index.add(emb_norm)

        faiss.write_index(index, self.faiss_index_path)
        return index

    def query(self, text, top_k=3):
        q = self.embedder.encode([text], convert_to_numpy=True).astype("float32")
        q_norm = q / np.linalg.norm(q, axis=1, keepdims=True)

        scores, idx = self.index.search(q_norm, top_k)

        results = []
        for score, i in zip(scores[0], idx[0]):
            s = self.sops[i]
            results.append({
                "department": s["department"],
                "sop_guideline": s["sop_guideline"],
                "action_summary": s["action_summary"],
                "score": float(score)
            })

        return results
