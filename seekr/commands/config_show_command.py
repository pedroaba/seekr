import json
from dataclasses import dataclass
from pathlib import Path

from rich import print_json

from seekr.config import SeekrConfig
from seekr.security.redact import RedactPath


@dataclass(frozen=True, slots=True)
class ConfigShowCommandParams:
    pass


class ConfigShowCommand:
    def __init__(self, params: ConfigShowCommandParams) -> None:
        self.params = params

    def execute(self) -> None:
        config_on_memory = SeekrConfig.get_instance().get()
        ignores = []

        for ignore_path in config_on_memory["ignores"]:
            if ignore_path["is_nickname"]:
                ignores.append(ignore_path)
                continue

            ignores.append(
                {
                    **ignore_path,
                    "resource": RedactPath.execute(Path(ignore_path["resource"])),
                }
            )

        config_on_memory["ignores"] = ignores
        print_json(json.dumps(config_on_memory, indent=4))
