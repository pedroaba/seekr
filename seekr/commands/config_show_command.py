import json
from argparse import Namespace
from pathlib import Path

from rich import print_json

from seekr.commands.abstract import AbstractCommand
from seekr.config import SeekrConfig
from seekr.decorators.finish_command import finish_command_execution
from seekr.security.redact import RedactPath


class ConfigShowCommand(AbstractCommand):
    identifier = "show"
    destination_command = "config_command"
    destination_description = "Configuration output options"
    help_text = "Show the current configuration"
    description = "Print the current Seekr configuration as formatted JSON."

    @finish_command_execution
    def handle(self, namespace: Namespace):
        config = SeekrConfig.get_instance()

        config_on_memory = config.get()
        ignores = []

        for ignore_path in config_on_memory["ignores"]:
            if ignore_path["is_nickname"]:
                ignores.append(ignore_path)
                continue

            ignore_path = {
                **ignore_path,
                "resource": RedactPath.execute(Path(ignore_path["resource"])),
            }

            ignores.append(ignore_path)

        config_on_memory["ignores"] = ignores
        print_json(json.dumps(config_on_memory, indent=4))

    def build(self):
        pass
