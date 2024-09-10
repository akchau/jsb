import os
from pathlib import Path
from pydantic import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    DEBUG: bool
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    BOT_TOKEN: str
    API_BASE_URL: str
    API_KEY: str
    BASE_STATION_CODE: str

    class Config:
        env_file = os.path.join(BASE_DIR, '.env')


settings = Settings()
