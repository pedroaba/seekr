import sys
from argparse import ArgumentParser, Namespace, RawDescriptionHelpFormatter

from seekr.commands.config_command import ConfigCommand
from seekr.commands.config_get_command import ConfigGetCommand
from seekr.commands.config_init_command import ConfigInitCommand
from seekr.commands.config_set_command import ConfigSetCommand
from seekr.commands.config_set_ignores_command import ConfigSetIgnoresCommand
from seekr.commands.config_show_command import ConfigShowCommand
from seekr.commands.init_command import InitCommand
from seekr.commands.search_command import SearchCommand


class SeekrCli:
    _explicite_commands = set()

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

    def parse(self, args: list[str] | None = None):
        arguments = list(sys.argv[1:] if args is None else args)

        if arguments and self._is_implicit_search(arguments[0]):
            arguments.insert(0, SearchCommand.identifier)

        self._arguments = self._parser.parse_args(arguments)

    def _is_implicit_search(self, first_argument: str) -> bool:
        return (
            first_argument not in self._explicite_commands
            and not first_argument.startswith("-")
        )

    def exec(self):
        has_handler_for_command = hasattr(self._arguments, "handler")
        if not has_handler_for_command:
            self._parser.print_help()
            return

        command_handler = getattr(self._arguments, "handler", None)
        if callable(command_handler):
            command_handler(self._arguments)

    def __build(self):
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

        search_command = SearchCommand(parser=self._parser)
        search_command.build()

        # explicite commands
        SeekrCli._explicite_commands.add(config_command.command)
        SeekrCli._explicite_commands.add(config_init_command.command)
        SeekrCli._explicite_commands.add(config_show_command.command)
        SeekrCli._explicite_commands.add(config_get_command.command)
        SeekrCli._explicite_commands.add(config_set_command.command)
        SeekrCli._explicite_commands.add(config_set_ignores_command.command)
        SeekrCli._explicite_commands.add(init_command.command)
