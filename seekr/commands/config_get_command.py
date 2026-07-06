import json
from argparse import Namespace

from rich import print_json

from seekr.commands.abstract import AbstractCommand
from seekr.config import SeekrConfig
from seekr.decorators.finish_command import finish_command_execution
from seekr.texts.config_show_specific_property import ConfigShowSpecificProperty


class ConfigGetCommand(AbstractCommand):
    identifier = "get"
    destination_command = "config_key"

    @finish_command_execution
    def handle(self, namespace: Namespace):
        if namespace.key_names is None or len(namespace.key_names) == 0:
            super().handle(namespace)
            return

        config = SeekrConfig.get_instance()
        properties_names = namespace.key_names

        config_show_specific_property = ConfigShowSpecificProperty()
        for property_name in properties_names:
            property_value = config.get_property(property_name, None)

            config_show_specific_property.add_row(property_name, property_value.get())
        config_show_specific_property.display(namespace.format_output)

    def build(self):
        self.parser.add_argument(
            "key_names",
            default=None,
            nargs="*",
        )

        self.parser.add_argument(
            "-f", "--format",
            action="store_true",
            dest="format_output",
            default=False,
        )
