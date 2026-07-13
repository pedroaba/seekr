import os

from platformdirs import user_data_path

DATABASE_URL_ENV_VAR = "SEEKR_DATABASE_URL"


def get_database_url() -> str:
    configured_url = os.getenv(DATABASE_URL_ENV_VAR)
    if configured_url:
        return configured_url

    data_directory = user_data_path("seekr")
    data_directory.mkdir(parents=True, exist_ok=True)

    database_path = data_directory / "seekr.db"
    return f"sqlite:///{database_path.as_posix()}"
