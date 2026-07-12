from argparse import ArgumentParser, Namespace, RawDescriptionHelpFormatter

from seekr.commands.config_command import ConfigCommand
from seekr.commands.config_get_command import ConfigGetCommand
from seekr.commands.config_init_command import ConfigInitCommand
from seekr.commands.config_set_command import ConfigSetCommand
from seekr.commands.config_set_ignores_command import ConfigSetIgnoresCommand
from seekr.commands.config_show_command import ConfigShowCommand
from seekr.commands.init_command import InitCommand


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

        self.__build()
        self._arguments = Namespace()

    def parse(self):
        self._arguments = self._parser.parse_args()

    def exec(self):
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

        config_init_command = ConfigInitCommand(command=config_command)
        config_init_command.build()

        config_show_command = ConfigShowCommand(command=config_command)
        config_show_command.build()

        config_get_command = ConfigGetCommand(command=config_command)
        config_get_command.build()

        config_set_command = ConfigSetCommand(command=config_command)
        config_set_command.build()

        config_set_ignores_command = ConfigSetIgnoresCommand(command=config_set_command)
        config_set_ignores_command.build()

        init_command = InitCommand(parser=self._parser)
        init_command.build()
