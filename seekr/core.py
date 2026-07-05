from argparse import ArgumentParser, Namespace, RawDescriptionHelpFormatter

from seekr.commands.abstract import AbstractCommand
from seekr.commands.config_command import ConfigCommand
from seekr.commands.config_set_command import ConfigSetCommand
from seekr.commands.config_set_ignores_command import ConfigSetIgnoresCommand
from seekr.commands.config_show_command import ConfigShowCommand
from seekr.config import SeekrConfig
from seekr.texts import TextDisplayer, TextDisplayerClassKeys


class SeekrCli:
    def __init__(self):
        self._parser = ArgumentParser(
            description="Search and configure ignored paths for Seekr.",
            epilog=(
                "Examples:\n"
                "  seekr --init\n"
                "  seekr config show\n"
                "  seekr config set ignores --path .venv build"
            ),
            formatter_class=RawDescriptionHelpFormatter,
        )
        self.__config = SeekrConfig()

        self._sub_commands: list[AbstractCommand] = []

        self.__build()

        self._arguments = Namespace()

    def parse(self):
        self._arguments = self._parser.parse_args()

    def exec(self):
        if self._arguments.init:
            TextDisplayer.display(TextDisplayerClassKeys.WELLCOME_INIT_COMMAND)
            return

        has_handler_for_command = hasattr(self._arguments, "handler")
        if not has_handler_for_command:
            self._parser.print_help()
            return

        command_handler = getattr(self._arguments, "handler", None)
        if callable(command_handler):
            command_handler(self._arguments)

    def __build(self):
        self._parser.add_argument(
            "-i",
            "--init",
            help="Create the default Seekr configuration file.",
            action="store_true",
        )

        config_command = ConfigCommand(parser=self._parser)
        config_command.build()

        config_show_command = ConfigShowCommand(command=config_command)
        config_show_command.build()

        config_set_command = ConfigSetCommand(command=config_command)
        config_set_command.build()

        config_set_ignores_command = ConfigSetIgnoresCommand(command=config_set_command)
        config_set_ignores_command.build()

        self._sub_commands.append(config_command)
        self._sub_commands.append(config_show_command)
        self._sub_commands.append(config_set_command)
