from argparse import ArgumentParser, Namespace

from seekr.config import SeekrConfig
from seekr.texts import TextDisplayer, TextDisplayerClassKeys


class SeekrCli:
    def __init__(self):
        self._parser = ArgumentParser(description="A simple command-line tool.")
        self.__config = SeekrConfig()

        self.__build()

        self._arguments = Namespace()

    def parse(self):
        self._arguments = self._parser.parse_args()

    def exec(self):
        if self._arguments.init:
            TextDisplayer.display(TextDisplayerClassKeys.WELLCOME_INIT_COMMAND)
            # Add logic to initialize system configuration here

    def __build(self):
        self._parser.add_argument(
            "-i",
            "--init",
            help="Initialize system configuration, creates a default config file.",
            action="store_true",
        )
