import faiss
import numpy as np
import json
from pathlib import Path
from app.config import settings


class VectorStore:
    def __init__(self, dimension: int = 384):
        self.dimension = dimension
        self.index: faiss.IndexFlatIP | None = None
        self.chunks: list[str] = []
        self.sources: list[str] = []

    def build(self, embeddings: list[list[float]], chunks: list[str], sources: list[str]):
        arr = np.array(embeddings, dtype=np.float32)
        faiss.normalize_L2(arr)
        self.index = faiss.IndexFlatIP(self.dimension)
        self.index.add(arr)
        self.chunks = chunks
        self.sources = sources

    def save(self, path: Path | None = None):
        path = path or settings.data_dir / "index.faiss"
        path.parent.mkdir(parents=True, exist_ok=True)
        if self.index is not None:
            faiss.write_index(self.index, str(path))
        with open(path.with_suffix(".json"), "w", encoding="utf-8") as f:
            json.dump({"chunks": self.chunks, "sources": self.sources}, f, ensure_ascii=False)

    def load(self, path: Path | None = None) -> bool:
        path = path or settings.data_dir / "index.faiss"
        if not path.exists():
            return False
        self.index = faiss.read_index(str(path))
        with open(path.with_suffix(".json"), "r", encoding="utf-8") as f:
            data = json.load(f)
        self.chunks = data["chunks"]
        self.sources = data["sources"]
        return True

    def search(self, query_embedding: list[float], top_k: int = None) -> list[dict]:
        top_k = top_k or settings.top_k
        if self.index is None:
            return []
        q = np.array([query_embedding], dtype=np.float32)
        faiss.normalize_L2(q)
        scores, indices = self.index.search(q, top_k)
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < len(self.chunks):
                results.append({
                    "chunk": self.chunks[idx],
                    "source": self.sources[idx],
                    "score": float(score),
                })
        return results


store = VectorStore()
