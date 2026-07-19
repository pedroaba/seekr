from pathlib import Path

from seekr.application.ports.path_services import ExistingPathValidator
from seekr.domain.exceptions import PathDoesNotExistError


class FileSystemPathValidator(ExistingPathValidator):
    def validate(self, path: Path) -> Path:
        if not path.exists():
            raise PathDoesNotExistError(path)
        return path.resolve()
