from copy import deepcopy
from pathlib import Path
from typing import Any

from seekr.domain.entities.indexed_path import IndexedPath
from seekr.domain.entities.scan import ScanResult, ScanRoot


class InMemoryPathRepository:
    def __init__(self, paths: list[IndexedPath] | None = None) -> None:
        self.paths = list(paths or [])
        self.replace_calls: list[list[IndexedPath]] = []

    def count(self) -> int:
        return len(self.paths)

    def replace_all(self, paths: list[IndexedPath]) -> None:
        self.paths = list(paths)
        self.replace_calls.append(list(paths))

    def list_all(self) -> list[IndexedPath]:
        return list(self.paths)


class StubPathScanner:
    def __init__(self, result: ScanResult) -> None:
        self.result = result
        self.calls: list[list[ScanRoot]] = []

    def scan(self, roots: list[ScanRoot]) -> ScanResult:
        self.calls.append(list(roots))
        return self.result


class StubScanRootsProvider:
    def __init__(self, roots: list[ScanRoot]) -> None:
        self.roots = roots
        self.call_count = 0

    def get(self) -> list[ScanRoot]:
        self.call_count += 1
        return list(self.roots)


class StubSearchEngine:
    def __init__(self, indexes: list[int]) -> None:
        self.indexes = indexes
        self.calls: list[tuple[str, list[str], int, int]] = []

    def search(
        self,
        query: str,
        choices: list[str],
        limit: int,
        precision: int,
    ) -> list[int]:
        self.calls.append((query, choices, limit, precision))
        return list(self.indexes)


class InMemoryConfigRepository:
    def __init__(self, data: dict[str, Any] | None = None) -> None:
        self.data = deepcopy(data or {})
        self.initialize_calls: list[bool] = []
        self.commit_count = 0

    def initialize(self, reset: bool = False) -> None:
        self.initialize_calls.append(reset)

    def read(self) -> dict[str, Any]:
        return deepcopy(self.data)

    def replace(self, data: dict[str, Any]) -> None:
        self.data = deepcopy(data)

    def commit(self) -> None:
        self.commit_count += 1


class StubPathValidator:
    def __init__(self) -> None:
        self.calls: list[Path] = []

    def validate(self, path: Path) -> Path:
        self.calls.append(path)
        return Path("/validated") / path


class StubPathRedactor:
    def __init__(self) -> None:
        self.calls: list[Path] = []

    def redact(self, path: Path) -> str:
        self.calls.append(path)
        return f"redacted:{path.name}"
