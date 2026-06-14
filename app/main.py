from fasthtml.common import fast_app, serve
from dotenv import load_dotenv
from app.routes import ui, chat, scrape
from app.services.vector_store import store
from app.services.embeddings import get_model
from app.services.load_docs import load_docs_from_folder


load_dotenv()


async def lifespan(app):
    try:
        get_model()
    except Exception:
        print("Ostrzezenie: Nie udalo sie zaladowac modelu embedddingow.")
    try:
        if store.load():
            print("Zaladowano istniejacy indeks.")
        else:
            print("Budowanie indeksu z docs/ranczo/ ...")
            result = load_docs_from_folder()
            print(result["message"])
    except Exception as e:
        print(f"Ostrzezenie: Nie udalo sie zaladowac dokumentow: {e}")
    yield


app, rt = fast_app(lifespan=lifespan, pico=False)

ui.register(app, rt)
chat.register(app, rt)
scrape.register(app, rt)


if __name__ == "__main__":
    serve(appname="app.main")
