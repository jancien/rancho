# Ranczo Dziki Sad - Chatbot z RAG

Chatbot oparty na RAG (Retrieval-Augmented Generation) dla strony [ranczo-dziki-sad.pl](https://ranczo-dziki-sad.pl/). Odpowiada na pytania uzytkownikow wylacznie na podstawie tresci strony internetowej.

## Architektura

- **Frontend**: FastHTML (HTML-first, brak frameworkow JS)
- **Backend**: FastAPI (przez FastHTML)
- **Embeddings**: Groq API (`nomic-embed-text`)
- **LLM**: Groq API (`llama-3.1-8b-instant` lub `llama-3.1-70b-versatile`)
- **Vector store**: FAISS (in-memory)
- **Scraping**: httpx + BeautifulSoup
- **Hosting**: Render.com (free tier)

## Struktura projektu

```
Rancho/
├── app/
│   ├── main.py              # Wejscie FastHTML + FastAPI
│   ├── config.py             # Konfiguracja (env vars)
│   ├── models.py             # Schematy Pydantic
│   ├── routes/
│   │   ├── chat.py           # POST /api/chat
│   │   ├── scrape.py         # POST /api/scrape
│   │   └── ui.py             # GET / (frontend)
│   ├── services/
│   │   ├── scraper.py        # Scrapowanie strony
│   │   ├── document_loader.py# Czyszczenie HTML, chunking
│   │   ├── vector_store.py   # Indeks FAISS
│   │   ├── embeddings.py     # Embeddingi przez Groq
│   │   ├── llm.py            # Chat completions przez Groq
│   │   └── rag.py            # Orchestracja RAG
│   └── prompts/
│       └── system.py         # Domylny system prompt
├── data/
│   └── faiss_index/          # Zapisany indeks FAISS
├── .env.example
├── requirements.txt
├── render.yaml
├── Procfile
└── README.md
```

## Instalacja lokalna

1. Skopiuj `.env.example` do `.env` i wpisz swoj klucz API:
   ```bash
   cp .env.example .env
   ```

2. Utworz virtual environment i zainstaluj zaleznosci:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/macOS
   venv\Scripts\activate      # Windows
   pip install -r requirements.txt
   ```

3. Uruchom aplikacje:
   ```bash
   python -m app.main
   ```

4. Otworz `http://localhost:8000` w przegladarce.

## Pierwsze uruchomienie

Po uruchomieniu kliknij przycisk **"Scrapuj strone"** aby pobrac tresc z ranczo-dziki-sad.pl i zbudowac indeks. Bez tego chatbot nie bedzie mial zadnych danych do odpowiedzi.

## Konfiguracja

Wszystkie parametry sa konfigurowalne w pliku `.env` lub przez interfejs UI:

| Parametr | Opis | Domyślnie |
|----------|------|-----------|
| `GROQ_API_KEY` | Klucz API Groq | (wymagany) |
| `GROQ_MODEL` | Model LLM | `llama-3.1-8b-instant` |
| `GROQ_TEMPERATURE` | Temperatura generowania | `0.3` |
| `GROQ_MAX_TOKENS` | Maksymalna liczba tokenow odpowiedzi | `1024` |
| `GROQ_TOP_P` | Top-p sampling | `0.9` |
| `SCRAPE_BASE_URL` | URL strony do scrapowania | `https://ranczo-dziki-sad.pl` |
| `SCRAPE_SUBPAGES` | Lista podstron do scrapowania | `/o-nas,/oferta,...` |
| `CHUNK_SIZE` | Rozmiar fragmentu tekstu | `500` |
| `CHUNK_OVERLAP` | Nakladanie sie fragmentow | `50` |
| `TOP_K` | Liczba pobieranych fragmentow | `3` |

## Deployment na Render.com

1. Pushuj kod do repozytorium GitHub.
2. Na [Render.com](https://render.com) utworz nowy **Web Service**.
3. Polacz z repozytorium GitHub.
4. Render automatycznie wykryje `render.yaml` i skonfiguruje usluge.
5. Dodaj zmienna srodowiskowa `GROQ_API_KEY` w panelu Render.
6. Deploy.

## Darmowe zasoby

| Serwis | Cel | Koszt |
|--------|-----|-------|
| Render.com | Hosting aplikacji Python | Free (512MB, uspienie po 15min) |
| Groq API | Embeddingi + LLM | Free tier |
| GitHub | Kod + trigger deployu | Free |

## Rozszerzenia

Architektura jest modularna i latwo rozszerzalna:

- **Historia konwersacji**: Dodaj pole `conversation_history: list[Message]` w `ChatRequest` i przekazuj je w promptach.
- **Autoryzacja**: Dodaj middleware FastAPI z JWT.
- **Trwaly vector store**: Zmien FAISS na Pinecone (free tier) lub ChromaDB.
- **Wiecej formatow dokumentow**: Dodaj obsluge DOCX, CSV w `document_loader.py`.
- **Wiecej stron do scrapowania**: Dodaj URL-e w `SCRAPE_SUBPAGES`.
