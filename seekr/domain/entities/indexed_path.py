from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any, Self


@dataclass(frozen=True, slots=True)
class IndexedPath:
    filepath: str
    parent_path: str
    normalized_filepath: str
    is_folder: bool
    is_file: bool
    source_alias: str | None = None
    modified_path_at: datetime = field(default_factory=datetime.now)
    modified_content_at: datetime = field(default_factory=datetime.now)
    is_able_to_watch: bool = True
    version: int = 1

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> Self:
        return cls(
            filepath=str(value["filepath"]),
            parent_path=str(value["parent_path"]),
            normalized_filepath=str(value["normalized_filepath"]),
            is_folder=bool(value["is_folder"]),
            is_file=bool(value["is_file"]),
            source_alias=value.get("source_alias"),
            modified_path_at=value.get("modified_path_at", datetime.now()),
            modified_content_at=value.get("modified_content_at", datetime.now()),
            is_able_to_watch=bool(value.get("is_able_to_watch", True)),
            version=int(value.get("version", 1)),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
