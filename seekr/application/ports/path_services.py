from pathlib import Path
from typing import Protocol


class ExistingPathValidator(Protocol):
    def validate(self, path: Path) -> Path: ...


class PathRedactor(Protocol):
    def redact(self, path: Path) -> str: ...
