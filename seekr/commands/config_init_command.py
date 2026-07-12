from argparse import Namespace

from seekr.commands.abstract import AbstractCommand
from seekr.config import SeekrConfig
from seekr.decorators.finish_command import finish_command_execution
from seekr.texts.config_initialized import ConfigInitializedText
from seekr.texts.config_reset import ConfigResetText


class ConfigInitCommand(AbstractCommand):
    identifier = "init"
    destination_command = "config_key"
    destination_description = "Initialize configuration values"
    help_text = "Initialize the local configuration"
    description = (
        "Create or load the local Seekr configuration. Existing values are preserved "
        "unless --reset is provided."
    )
    epilog = "Examples:\n  seekr config init\n  seekr config init --reset"

    def build(self):
        self.parser.add_argument(
            "-r",
            "--reset",
            dest="reset",
            action="store_true",
            default=False,
            help="Replace existing configuration values with Seekr's defaults.",
        )

    @finish_command_execution
    def handle(self, namespace: Namespace):
        conf = SeekrConfig.get_instance()
        conf.build(reset=namespace.reset)

        if namespace.reset:
            ConfigResetText.display()
            return

        ConfigInitializedText.display()
