from dataclasses import dataclass
from typing import Any

from seekr.application.ports.config_repository import ConfigRepository
from seekr.application.ports.path_services import PathRedactor
from seekr.application.services.config_sanitizer import ConfigSanitizer


@dataclass(frozen=True, slots=True)
class ShowConfigOutput:
    config: dict[str, Any]


class ShowConfig:
    def __init__(self, repository: ConfigRepository, redactor: PathRedactor) -> None:
        self._repository = repository
        self._sanitizer = ConfigSanitizer(redactor)

    def execute(self) -> ShowConfigOutput:
        config = self._sanitizer.sanitize(self._repository.read())
        return ShowConfigOutput(config=config)
