from argparse import ArgumentParser, Namespace
from pathlib import Path

from seekr.commands.abstract import AbstractCommand
from seekr.config import SeekrConfig


class SeekrConfigCommand(AbstractCommand):
    identifier = "config"

    def __init__(self, parent_parser: ArgumentParser):
        self._parent_parser = parent_parser
        self._config_parser = None
        self._set_parser = None

        self._config = SeekrConfig.get_instance()

    def handle(self, namespace: Namespace):
        super().handle(namespace)

        if namespace.config_command == "set" and namespace.config_key:
            pass

    def build(self):
        subparsers = self._parent_parser.add_subparsers(dest="command",
                                                 description="sub-commands")

        # seekr config
        config_parser = subparsers.add_parser("config", help="Manage configuration")
        config_subparsers = config_parser.add_subparsers(
            dest="config_command",
        )

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
            dest="path_nicknames",
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

        self._config_parser = config_parser
        self._set_parser = set_parser

        self._set_help_text_when_is_empty(config_parser, "command", "config_command")
        self._set_help_text_when_is_empty(set_parser, "config_command", "config_key")
        