from argparse import ArgumentParser, Namespace

from seekr.commands.abstract import AbstractCommand
from seekr.commands.config import SeekrConfigCommand
from seekr.config import SeekrConfig
from seekr.texts import TextDisplayer, TextDisplayerClassKeys


class SeekrCli:
    def __init__(self):
        self._parser = ArgumentParser(description="A simple command-line tool.")
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

        for sub_command in self._sub_commands:
            if sub_command.identifier == self._arguments.command:
                sub_command.handle(self._arguments)

    def __build(self):
        self._parser.add_argument(
            "-i",
            "--init",
            help="Initialize system configuration, creates a default config file.",
            action="store_true",
        )

        config_command = SeekrConfigCommand(self._parser)
        config_command.build()

        self._sub_commands.append(config_command)
