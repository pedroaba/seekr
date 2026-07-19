from pathlib import Path


class PathDoesNotExistError(OSError):
    def __init__(self, path: Path | str) -> None:
        super().__init__(f"File or folder does not exist: {Path(path).resolve()}")
