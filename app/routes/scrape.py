from app.models import ScrapeStatus
from app.services.load_docs import load_docs_from_folder


def register(app, rt):
    @rt("/api/scrape")
    def post():
        try:
            result = load_docs_from_folder()
            return ScrapeStatus(**result)
        except Exception as e:
            return ScrapeStatus(status="error", message=str(e))
