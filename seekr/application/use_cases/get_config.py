from dataclasses import dataclass
from typing import Any

from seekr.application.ports.config_repository import ConfigRepository
from seekr.application.ports.path_services import PathRedactor
from seekr.application.services.config_sanitizer import ConfigSanitizer


@dataclass(frozen=True, slots=True)
class GetConfigInput:
    key_names: list[str]


@dataclass(frozen=True, slots=True)
class GetConfigOutput:
    values: dict[str, Any]


class GetConfig:
    def __init__(self, repository: ConfigRepository, redactor: PathRedactor) -> None:
        self._repository = repository
        self._sanitizer = ConfigSanitizer(redactor)

    def execute(self, request: GetConfigInput) -> GetConfigOutput:
        config = self._sanitizer.sanitize(self._repository.read())
        return GetConfigOutput(
            values={key: config.get(key) for key in request.key_names}
        )
