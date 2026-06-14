from app.services.embeddings import embed_text
from app.services.vector_store import store
from app.services.llm import get_chat_response
from app.prompts.system import build_prompt
from app.config import settings


def ask_question(user_message: str, system_prompt: str, temperature: float, max_tokens: int, top_p: float) -> dict:
    query_embedding = embed_text(user_message)
    results = store.search(query_embedding, top_k=settings.top_k)

    if not results:
        return {
            "answer": "Nie mam tej informacji w dostepnych materialach. Indeks dokumentow jest pusty.",
            "sources": [],
        }

    context_parts = []
    sources = []
    for r in results:
        context_parts.append(f"[Source: {r['source']}]\n{r['chunk']}")
        sources.append(r["source"])

    context = "\n\n---\n\n".join(context_parts)
    messages = build_prompt(system_prompt, context, user_message)
    answer = get_chat_response(messages, temperature, max_tokens, top_p)

    return {"answer": answer, "sources": list(set(sources))}
