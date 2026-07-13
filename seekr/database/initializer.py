from pathlib import Path

from alembic import command
from alembic.config import Config

from seekr.database.config import get_database_url


def initialize_database() -> None:
    migrations_directory = Path(__file__).parent / "migrations"

    config = Config()
    config.set_main_option("script_location", str(migrations_directory))
    config.set_main_option("sqlalchemy.url", get_database_url())

    command.upgrade(config, "head")
