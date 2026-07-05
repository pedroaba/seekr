from dataclasses import dataclass
from pathlib import Path
from typing import Optional, TypedDict


class PathModelInJson(TypedDict):
    resource: str
    is_nickname: bool | None
    is_system_path: bool | None


@dataclass(frozen=True)
class PathModel:
    resource: str

    is_nickname: bool = False
    is_system_path: bool = False

    def to_system_path(self) -> Path:
        return Path(self.resource).absolute()

    def to_json(self) -> PathModelInJson:
        return {
            "resource": self.resource,
            "is_nickname": self.is_nickname,
            "is_system_path": self.is_system_path,
        }

    def compare(self, other: PathModel) -> bool:
        return (self.resource == other.resource
                and self.is_nickname == other.is_nickname
                and self.is_system_path == other.is_system_path)

    def __eq__(self, other):
        if not isinstance(other, PathModel):
            return False

        return self.compare(other)

    @staticmethod
    def from_json(json: PathModelInJson) -> PathModel:
        return PathModel(
            resource=json["resource"],
            is_nickname=json["is_nickname"] or False,
            is_system_path=json["is_system_path"] or False,
        )
