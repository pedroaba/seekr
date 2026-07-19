from typing import Protocol

from seekr.domain.entities.indexed_path import IndexedPath


class PathRepository(Protocol):
    def count(self) -> int: ...

    def replace_all(self, paths: list[IndexedPath]) -> None: ...

    def list_all(self) -> list[IndexedPath]: ...
