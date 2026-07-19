from pathlib import Path

from alembic import command
from alembic.config import Config


class AlembicDatabaseMigrator:
    def __init__(self, database_url: str) -> None:
        self._database_url = database_url

    def upgrade(self) -> None:
        migrations = Path(__file__).parent / "migrations"
        config = Config()
        config.set_main_option("script_location", str(migrations))
        config.set_main_option("sqlalchemy.url", self._database_url)
        command.upgrade(config, "head")
