import os

from platformdirs import user_data_path


class DatabaseConfig:
    ENVIRONMENT_VARIABLE = "SEEKR_DATABASE_URL"

    def get_url(self) -> str:
        configured_url = os.getenv(self.ENVIRONMENT_VARIABLE)
        if configured_url:
            return configured_url
        data_directory = user_data_path("seekr")
        data_directory.mkdir(parents=True, exist_ok=True)
        return f"sqlite:///{(data_directory / 'seekr.db').as_posix()}"
