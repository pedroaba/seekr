from pathlib import Path

from seekr.exceptions.file import FileOrFolderDoesNotExist


class PathValidator:
    def __init__(self, path: Path):
        self._value = path

    def validate(self) -> Path:
        if not self._value.exists():
            raise FileOrFolderDoesNotExist(self._value)

        self._value = self._value.resolve()
        return self._value
