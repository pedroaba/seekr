from typing import Protocol

from seekr.domain.entities.scan import ScanResult, ScanRoot


class PathScanner(Protocol):
    def scan(self, roots: list[ScanRoot]) -> ScanResult: ...


class ScanRootsProvider(Protocol):
    def get(self) -> list[ScanRoot]: ...
