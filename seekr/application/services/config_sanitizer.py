from copy import deepcopy
from pathlib import Path
from typing import Any

from seekr.application.ports.path_services import PathRedactor


class ConfigSanitizer:
    def __init__(self, redactor: PathRedactor) -> None:
        self._redactor = redactor

    def sanitize(self, config: dict[str, Any]) -> dict[str, Any]:
        sanitized = deepcopy(config)
        sanitized["ignores"] = self._sanitize_ignores(sanitized.get("ignores", []))
        return sanitized

    def _sanitize_ignores(self, ignores: list[dict[str, Any]]) -> list[dict[str, Any]]:
        sanitized: list[dict[str, Any]] = []
        for rule in ignores:
            if rule.get("is_nickname", False):
                sanitized.append(rule)
                continue
            sanitized.append(
                {
                    **rule,
                    "resource": self._redactor.redact(Path(rule["resource"])),
                }
            )
        return sanitized
