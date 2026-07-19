from dataclasses import dataclass, field
from enum import StrEnum

from seekr.application.ports.path_repository import PathRepository
from seekr.application.ports.path_scanner import PathScanner, ScanRootsProvider
from seekr.domain.entities.indexed_path import IndexedPath


class BuildIndexStatus(StrEnum):
    CREATED = "created"
    ALREADY_EXISTS = "already_exists"


@dataclass(frozen=True, slots=True)
class BuildIndexInput:
    force: bool = False


@dataclass(frozen=True, slots=True)
class BuildIndexOutput:
    status: BuildIndexStatus
    paths: list[IndexedPath] = field(default_factory=list)
    total_files: int = 0
    total_dirs: int = 0


class BuildIndex:
    def __init__(
        self,
        repository: PathRepository,
        scanner: PathScanner,
        roots_provider: ScanRootsProvider,
    ) -> None:
        self._repository = repository
        self._scanner = scanner
        self._roots_provider = roots_provider

    def execute(self, request: BuildIndexInput) -> BuildIndexOutput:
        if not request.force and self._repository.count() > 0:
            return BuildIndexOutput(status=BuildIndexStatus.ALREADY_EXISTS)

        scan = self._scanner.scan(self._roots_provider.get())
        self._repository.replace_all(scan.paths)
        return BuildIndexOutput(
            status=BuildIndexStatus.CREATED,
            paths=scan.paths,
            total_files=scan.total_files,
            total_dirs=scan.total_dirs,
        )
