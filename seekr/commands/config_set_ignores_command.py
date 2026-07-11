from argparse import Namespace
from pathlib import Path

from seekr.commands.abstract import AbstractCommand
from seekr.config import SeekrConfig
from seekr.decorators.finish_command import finish_command_execution
from seekr.models.path import PathModel
from seekr.utils.validators.nickname import NicknameValidator
from seekr.utils.validators.path import PathValidator


class ConfigSetIgnoresCommand(AbstractCommand):
    identifier = "ignores"
    help_text = "Configure ignored paths and path nicknames"
    description = (
        "Add ignored filesystem paths or nickname patterns to the Seekr configuration."
    )
    epilog = (
        "Examples:\n"
        "  seekr config set ignores --path .venv build\n"
        "  seekr config set ignores --path-nickname __pycache__ .pytest_cache\n"
        "  seekr config set ignores --override --path dist"
    )

    @finish_command_execution
    def handle(self, namespace: Namespace):
        paths = namespace.paths
        nicknames = namespace.nicknames

        if len(paths) == 0 and len(nicknames) == 0:
            super().handle(namespace)
            return

        ignores_patterns: list[PathModel] = []

        for path in paths:
            path_str = str(PathValidator(path).validate())
            model = PathModel(path_str, is_system_path=True)
            ignores_patterns.append(model)

        for nickname in nicknames:
            validated_nickname = NicknameValidator(nickname).validate()
            model = PathModel(validated_nickname, is_nickname=True)
            ignores_patterns.append(model)

        config = SeekrConfig.get_instance()

        if namespace.override:
            config.set_property("ignores", ignores_patterns)
        else:
            ignores_patterns_saved: list[PathModel] = (
                config.get_property("ignores", defaults=[])
                .map(lambda _, value, __: PathModel.from_json(value))
                .get()
            )

            for path_to_add in ignores_patterns:
                if path_to_add not in ignores_patterns_saved:
                    ignores_patterns_saved.append(path_to_add)

            config.set_property("ignores", ignores_patterns_saved)

    def build(self):
        self.parser.add_argument(
            "-p",
            "--path",
            action="extend",
            type=Path,
            dest="paths",
            nargs="+",
            default=[],
            help=(
                "Filesystem path to ignore. Accepts one or more existing files "
                "or folders."
            ),
        )

        self.parser.add_argument(
            "-pn",
            "--path-nickname",
            action="extend",
            dest="nicknames",
            nargs="+",
            default=[],
            help=(
                "Path nickname or pattern to ignore by name. Matching folders "
                "and their contents are ignored."
            ),
        )

        self.parser.add_argument(
            "-o",
            "--override",
            action="store_true",
            default=False,
            help="Replace the current ignore list instead of appending to it.",
        )

        self.parser.add_argument(
            "--no-commit",
            action="store_true",
            help="Apply the change in memory without saving it to disk.",
            default=False,
            dest="no_commit",
        )
