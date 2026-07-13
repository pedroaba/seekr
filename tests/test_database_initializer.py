from pathlib import Path

from sqlalchemy import create_engine, inspect

from seekr.database.config import DATABASE_URL_ENV_VAR, get_database_url
from seekr.database.initializer import initialize_database


def test_database_url_uses_configured_environment_variable(monkeypatch):
    database_url = "sqlite:////tmp/custom-seekr.db"
    monkeypatch.setenv(DATABASE_URL_ENV_VAR, database_url)

    assert get_database_url() == database_url


def test_database_url_uses_seekr_user_data_directory(monkeypatch, tmp_path):
    monkeypatch.delenv(DATABASE_URL_ENV_VAR, raising=False)
    monkeypatch.setattr(
        "seekr.database.config.user_data_path",
        lambda _application_name: tmp_path / "application-data",
    )

    database_url = get_database_url()

    assert database_url == f"sqlite:///{tmp_path / 'application-data/seekr.db'}"
    assert (tmp_path / "application-data").is_dir()


def test_initialize_database_applies_all_migrations(monkeypatch, tmp_path):
    database_path = tmp_path / "seekr.db"
    database_url = f"sqlite:///{database_path}"
    monkeypatch.setenv(DATABASE_URL_ENV_VAR, database_url)

    initialize_database()

    assert database_path.is_file()

    inspector = inspect(create_engine(database_url))
    assert set(inspector.get_table_names()) == {"alembic_version", "paths"}


def test_initialize_database_can_run_more_than_once(monkeypatch, tmp_path):
    database_path = Path(tmp_path) / "seekr.db"
    monkeypatch.setenv(DATABASE_URL_ENV_VAR, f"sqlite:///{database_path}")

    initialize_database()
    initialize_database()

    assert database_path.is_file()
