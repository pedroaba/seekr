from dataclasses import dataclass, field

from seekr.domain.entities.indexed_path import IndexedPath


@dataclass(frozen=True, slots=True)
class ScanRoot:
    resource: str
    alias: str


@dataclass(frozen=True, slots=True)
class ScanResult:
    paths: list[IndexedPath] = field(default_factory=list)
    total_files: int = 0
    total_dirs: int = 0
