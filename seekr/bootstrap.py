from seekr.adapters.outbound.config.encrypted_config_repository import (
    EncryptedConfigRepository,
)
from seekr.adapters.outbound.filesystem.path_redactor import HomePathRedactor
from seekr.adapters.outbound.filesystem.path_scanner import FileSystemPathScanner
from seekr.adapters.outbound.filesystem.path_validator import FileSystemPathValidator
from seekr.adapters.outbound.filesystem.scan_roots_provider import (
    PlatformScanRootsProvider,
)
from seekr.adapters.outbound.persistence.sqlalchemy.database_config import (
    DatabaseConfig,
)
from seekr.adapters.outbound.persistence.sqlalchemy.migrator import (
    AlembicDatabaseMigrator,
)
from seekr.adapters.outbound.persistence.sqlalchemy.repository import (
    SqlAlchemyPathRepository,
)
from seekr.adapters.outbound.persistence.sqlalchemy.session_factory import (
    SqlAlchemySessionFactory,
)
from seekr.adapters.outbound.search.rapidfuzz_search_engine import RapidFuzzSearchEngine
from seekr.application.ports.config_repository import ConfigRepository
from seekr.application.ports.path_repository import PathRepository
from seekr.application.ports.path_services import PathRedactor
from seekr.application.services.contains_words_search_engine import (
    ContainsWordsSearchEngine,
)
from seekr.application.services.fallback_search_engine import FallbackSearchEngine
from seekr.application.use_cases.build_index import BuildIndex
from seekr.application.use_cases.get_config import GetConfig
from seekr.application.use_cases.initialize_config import InitializeConfig
from seekr.application.use_cases.search_paths import SearchPaths
from seekr.application.use_cases.set_ignores import SetIgnores
from seekr.application.use_cases.show_config import ShowConfig


class ApplicationContainer:
    def __init__(self) -> None:
        self._path_repository: PathRepository | None = None
        self._config_repository: ConfigRepository | None = None
        self._redactor = HomePathRedactor()

    def build_index(self) -> BuildIndex:
        return BuildIndex(
            repository=self._get_path_repository(),
            scanner=FileSystemPathScanner(),
            roots_provider=PlatformScanRootsProvider(),
        )

    def search_paths(self) -> SearchPaths:
        return SearchPaths(
            repository=self._get_path_repository(),
            search_engine=FallbackSearchEngine(
                primary=RapidFuzzSearchEngine(),
                fallback=ContainsWordsSearchEngine(),
            ),
        )

    def initialize_config(self) -> InitializeConfig:
        return InitializeConfig(self._get_config_repository())

    def show_config(self) -> ShowConfig:
        return ShowConfig(self._get_config_repository(), self._redactor)

    def get_config(self) -> GetConfig:
        return GetConfig(self._get_config_repository(), self._redactor)

    def set_ignores(self) -> SetIgnores:
        return SetIgnores(
            self._get_config_repository(),
            FileSystemPathValidator(),
        )

    def path_redactor(self) -> PathRedactor:
        return self._redactor

    def _get_path_repository(self) -> PathRepository:
        if self._path_repository is None:
            database_url = DatabaseConfig().get_url()
            AlembicDatabaseMigrator(database_url).upgrade()
            sessions = SqlAlchemySessionFactory(database_url)
            self._path_repository = SqlAlchemyPathRepository(sessions)

        return self._path_repository

    def _get_config_repository(self) -> ConfigRepository:
        if self._config_repository is None:
            repository = EncryptedConfigRepository()
            repository.initialize()
            self._config_repository = repository
        return self._config_repository
