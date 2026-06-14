import asyncio
import httpx
from app.config import settings
from app.services.document_loader import clean_html, split_text
from app.services.embeddings import embed_texts
from app.services.vector_store import store


async def _fetch(client: httpx.AsyncClient, url: str, base_url: str) -> tuple[str, list[str]] | None:
    try:
        resp = await client.get(url)
        resp.raise_for_status()
        text = clean_html(resp.text)
        if not text.strip():
            return None
        chunks = split_text(text)
        source_name = url.replace(base_url, "").rstrip("/") or "/"
        return source_name, chunks
    except Exception:
        return None


async def scrape_website() -> dict:
    base_url = settings.scrape_base_url
    subpages = [s.strip() for s in settings.scrape_subpages.split(",") if s.strip()]
    urls = [base_url] + [f"{base_url}{s}" if not s.startswith("http") else s for s in subpages]

    async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
        tasks = [_fetch(client, url, base_url) for url in urls]
        results = await asyncio.gather(*tasks)

    all_chunks = []
    all_sources = []
    pages_scraped = 0

    for r in results:
        if r is not None:
            source_name, chunks = r
            all_chunks.extend(chunks)
            all_sources.extend([source_name] * len(chunks))
            pages_scraped += 1

    if not all_chunks:
        return {"status": "error", "pages_scraped": 0, "chunks_created": 0, "message": "No content found"}

    embeddings = embed_texts(all_chunks)
    store.build(embeddings, all_chunks, all_sources)
    store.save()

    return {
        "status": "success",
        "pages_scraped": pages_scraped,
        "chunks_created": len(all_chunks),
        "message": f"Scraped {pages_scraped} pages, indexed {len(all_chunks)} chunks",
    }
