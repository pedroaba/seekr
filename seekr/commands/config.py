import json
from argparse import ArgumentParser, Namespace
from pathlib import Path

from rich import print_json

from seekr.commands.abstract import AbstractCommand
from seekr.config import SeekrConfig
from seekr.decorators.finish_command import finish_command_execution
from seekr.exceptions.file import FileOrFolderDoesNotExist
from seekr.models.path import PathModel


class SeekrConfigCommand(AbstractCommand):
    identifier = "config"

    def __init__(self, parent_parser: ArgumentParser):
        self._parent_parser = parent_parser

        # subcommands parsers
        self._config_parser = None
        self._set_parser = None
        self._show_parser = None

        self._config = SeekrConfig.get_instance()

    @finish_command_execution
    def handle(self, namespace: Namespace):
        super().handle(namespace)

        if namespace.config_command == "set" and namespace.config_key:
            paths = namespace.paths
            nicknames = namespace.nicknames

            ignores_patterns: list[PathModel] = []

            for path in paths:
                path_to_add = Path(path)
                if not path_to_add.exists():
                    raise FileOrFolderDoesNotExist(path_to_add)

                path_str = str(path_to_add.absolute())
                model = PathModel(path_str, is_system_path=True)
                ignores_patterns.append(model)

            for nickname in nicknames:
                model = PathModel(nickname, is_nickname=True)
                ignores_patterns.append(model)

            if namespace.override:
                self._config.set_property("ignores", ignores_patterns)
            else:
                ignores_patterns_saved: list[PathModel] = self._config.get_property(
                    "ignores", defaults=[]).map(
                    lambda _, value, __: PathModel.from_json(value)
                ).get()

                for path_to_add in ignores_patterns:
                    if path_to_add not in ignores_patterns_saved:
                        ignores_patterns_saved.append(path_to_add)

                self._config.set_property("ignores", ignores_patterns_saved)
        elif namespace.config_command == "show":
            config_on_memory = self._config.get()
            print_json(json.dumps(config_on_memory, indent=4))

    def build(self):
        subparsers = self._parent_parser.add_subparsers(dest="command",
                                                 description="sub-commands")

        # seekr config
        config_parser = subparsers.add_parser("config", help="Manage configuration")
        config_subparsers = config_parser.add_subparsers(
            dest="config_command",
        )

        # seekr config show
        show_parser = config_subparsers.add_parser("show", help="Show configuration")

        # seekr config set
        set_parser = config_subparsers.add_parser("set", help="Set config values")
        set_subparsers = set_parser.add_subparsers(
            dest="config_key",
        )

        # seekr config set ignores
        ignores_parser = set_subparsers.add_parser(
            "ignores",
            help="Set ignored paths",
        )

        ignores_parser.add_argument(
            "-p",
            "--path",
            action="extend",
            type=Path,
            dest="paths",
            nargs="+",
            default=[],
            help="Path to ignore. Can receive one or more paths.",
        )

        ignores_parser.add_argument(
            "-pn",
            "--path-nickname",
            action="extend",
            dest="nicknames",
            nargs="+",
            default=[],
            help=(
                "Nickname pattern used to ignore paths by regex. "
                "Any folder matching this nickname, including all its contents, "
                "will be ignored."
            ),
        )

        ignores_parser.add_argument(
            "-o",
            "--override",
            action="store_true",
            help="Replace current ignored paths instead of appending.",
        )

        ignores_parser.add_argument(
            "--no-commit",
            action="store_true",
            help="Commit configuration to save on your machine.",
            default=False,
            dest="no_commit",
        )

        self._config_parser = config_parser
        self._set_parser = set_parser
        self._show_parser = show_parser

        self._set_help_text_when_is_empty(config_parser, "command", "config_command")
        self._set_help_text_when_is_empty(set_parser, "config_command", "config_key")
        