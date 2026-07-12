from dataclasses import dataclass
from pathlib import Path
from typing import TypedDict

from seekr.models.path import PathModel, PathModelInJson


class WalkResultJson(TypedDict):
    location: PathModelInJson
    relative_path: str

    is_file: bool
    is_dir: bool


@dataclass(frozen=True)
class WalkResult:
    location: PathModel
    relative_path: Path

    is_file: bool = False
    is_dir: bool = False

    def to_json(self) -> WalkResultJson:
        return {
            "location": self.location.to_json(),
            "relative_path": str(self.relative_path.resolve()),
            "is_file": self.is_file,
            "is_dir": self.is_dir,
        }


class Walker:
    def __init__(self, paths: list[PathModel] | None = None):
        self.__default_paths = paths or []

    def walk(self) -> list[WalkResult]:
        results = []

        for model in self.__default_paths:
            path = Path(model.resource)

            if path.is_file():
                results.append(
                    WalkResult(location=model, relative_path=path, is_file=True)
                )

                continue

            for current_dir, _, files in path.walk():
                results.append(
                    WalkResult(
                        location=model,
                        relative_path=current_dir.resolve(),
                        is_dir=True,
                    )
                )

                for file in files:
                    mounted_path = self._mount_scanned_path(current_dir, file)

                    results.append(
                        WalkResult(
                            location=PathModel(
                                resource=str(current_dir.resolve()),
                                is_system_path=True,
                            ),
                            relative_path=mounted_path,
                            is_file=True,
                        )
                    )
        return results

    @staticmethod
    def _mount_scanned_path(current_dir: Path, filename: str) -> Path:
        return (current_dir / filename).resolve()
