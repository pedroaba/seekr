from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class IgnoreRule:
    resource: str
    is_nickname: bool = False
    is_system_path: bool = False

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> IgnoreRule:
        return cls(
            resource=str(value["resource"]),
            is_nickname=bool(value.get("is_nickname", False)),
            is_system_path=bool(value.get("is_system_path", False)),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
