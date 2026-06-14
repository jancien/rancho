import os

if "HF_HUB_DISABLE_SYMLINKS_WARNING" not in os.environ:
    os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
if "HF_TOKEN" not in os.environ:
    os.environ["HF_TOKEN"] = "0"

from sentence_transformers import SentenceTransformer

_model: SentenceTransformer | None = None


def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def embed_text(text: str) -> list[float]:
    return get_model().encode(text).tolist()


def embed_texts(texts: list[str]) -> list[list[float]]:
    return get_model().encode(texts).tolist()
