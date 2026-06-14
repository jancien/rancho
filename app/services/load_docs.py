from pathlib import Path
from app.config import settings
from app.services.document_loader import split_text
from app.services.embeddings import embed_texts
from app.services.vector_store import store


DOCS_DIR = Path(__file__).parent.parent.parent / "docs" / "ranczo"


def load_docs_from_folder() -> dict:
    if not DOCS_DIR.exists():
        return {"status": "error", "pages_scraped": 0, "chunks_created": 0, "message": "Brak folderu docs/ranczo/"}

    all_chunks = []
    all_sources = []
    pages_loaded = 0

    for fpath in sorted(DOCS_DIR.iterdir()):
        if fpath.suffix != ".txt":
            continue
        text = fpath.read_text(encoding="utf-8")
        source = fpath.stem
        chunks = split_text(text)
        all_chunks.extend(chunks)
        all_sources.extend([source] * len(chunks))
        pages_loaded += 1

    if not all_chunks:
        return {"status": "error", "pages_scraped": 0, "chunks_created": 0, "message": "Brak zawartosci w plikach"}

    embeddings = embed_texts(all_chunks)
    store.build(embeddings, all_chunks, all_sources)
    store.save()

    return {
        "status": "success",
        "pages_scraped": pages_loaded,
        "chunks_created": len(all_chunks),
        "message": f"Zaladowano {pages_loaded} stron, utworzono {len(all_chunks)} fragmentow",
    }
