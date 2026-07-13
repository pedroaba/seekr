import os

DATABASE_URL_ENV_VAR = "SEEKR_DATABASE_URL"
DEFAULT_DATABASE_URL = "sqlite:///seekr.db"


def get_database_url() -> str:
    return os.getenv(DATABASE_URL_ENV_VAR, DEFAULT_DATABASE_URL)
