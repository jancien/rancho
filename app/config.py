from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    groq_api_key: str = ""
    groq_model: str = "llama-3.1-8b-instant"
    groq_temperature: float = 0.3
    groq_max_tokens: int = 1024
    groq_top_p: float = 0.9

    scrape_base_url: str = "https://ranczo-dziki-sad.pl"
    scrape_subpages: str = "/o-nas,/oferta,/atrakcje-w-okolicy,/kontakt"

    chunk_size: int = 500
    chunk_overlap: int = 50
    top_k: int = 3

    data_dir: Path = Path(__file__).parent.parent.parent / "data" / "faiss_index"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
