from pathlib import Path


class FileOrFolderDoesNotExist(OSError):
    def __init__(self, path: Path | str):
        super().__init__(f"File or folder does not exist: {Path(path).resolve()}")


class FileDoesNotExist(FileNotFoundError):
    def __init__(self, path: Path | str):
        super().__init__(f"File does not exist: {Path(path).resolve()}")


class FolderDoesNotExist(NotADirectoryError):
    def __init__(self, path: Path | str):
        super().__init__(f"Folder does not exist: {Path(path).resolve()}")
