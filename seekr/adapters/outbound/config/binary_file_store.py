from pathlib import Path


class BinaryFileStore:
    def __init__(self, path: Path) -> None:
        self._path = path

    @property
    def exists(self) -> bool:
        return self._path.is_file()

    def read(self) -> bytes:
        return self._path.read_bytes()

    def write(self, content: bytes) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._path.write_bytes(content)
