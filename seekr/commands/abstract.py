from abc import ABC, abstractmethod
from argparse import ArgumentParser, Namespace, RawDescriptionHelpFormatter
from typing import Any


def show_help(parser: ArgumentParser):
    def show_empty_message_internal_fn(_namespace: Namespace | None = None) -> None:
        parser.print_help()

    return show_empty_message_internal_fn


INTERNAL_REFERENCE_COMMAND_NAME = "__internal_reference_command_name"
INTERNAL_REFERENCE_SUBCOMMAND_NAME = "__internal_reference_subcommand_name"
INTERNAL_EMPTY_HANDLER = "__internal_empty_handler"

INTERNAL_EMPTY_COMMAND_NAME = "__internal_empty_command_name"
INTERNAL_EMPTY_SUBCOMMAND_NAME = "__internal_empty_subcommand_name"


class AbstractCommand(ABC):
    identifier: str = None
    destination_command: str = None
    destination_description: str = None
    help_text: str = None
    description: str = None
    epilog: str = None

    # parent parser to set subcommands
    __parser: ArgumentParser
    __internal_parser: ArgumentParser

    __has_execute_an_action = True

    def __init__(
        self,
        parser: ArgumentParser | None = None,
        command: AbstractCommand | None = None,
    ):
        if command is None and parser is None:
            raise ValueError()

        if command is None and parser is not None:
            self.__parser = parser
            self.__subparsers = self._recover_or_create_subparsers(self.__parser)
        elif command is not None:
            self.__parser = command.parser
            self.__subparsers = command.get_or_create_internal_subparsers()

        self.__internal_parser = self.__subparsers.add_parser(
            self.identifier,
            help=self.help_text,
            description=self.description,
            epilog=self.epilog,
            formatter_class=RawDescriptionHelpFormatter,
        )

        self.__parent_command = command
        self.__internal_parser.set_defaults(handler=self.handle)

    @abstractmethod
    def build(self): ...

    def handle(self, namespace: Namespace):
        # _empty_handler = getattr(namespace, INTERNAL_EMPTY_HANDLER, None)
        # if _empty_handler is None:
        #     return
        #
        # ref_name = getattr(namespace,
        #                    INTERNAL_REFERENCE_COMMAND_NAME,
        #                    INTERNAL_EMPTY_COMMAND_NAME)
        # ref_subcommand = getattr(namespace,
        #                          INTERNAL_REFERENCE_SUBCOMMAND_NAME,
        #                          INTERNAL_EMPTY_SUBCOMMAND_NAME)
        #
        # name = getattr(namespace, ref_name, None)
        # subcommand = getattr(namespace, ref_subcommand, None)
        #
        # if name is not None and subcommand is None:
        #     Executor.execute(_empty_handler)
        self.__has_execute_an_action = False
        self.__internal_parser.print_help()

    def _recover_or_create_subparsers(self, parser: ArgumentParser) -> Any:
        if parser._subparsers is not None:
            return parser._subparsers._group_actions[0]

        return parser.add_subparsers(
            dest=self.destination_command,
            description=self.destination_description,
        )

    def get_or_create_internal_subparsers(self) -> Any:
        if self.__internal_parser._subparsers is not None:
            return self.__internal_parser._subparsers._group_actions[0]

        return self.__internal_parser.add_subparsers(
            dest=self.destination_command,
            description=self.destination_description,
        )

    @staticmethod
    def _set_help_text_when_is_empty(
        parser: ArgumentParser, reference_command_name: str, reference_subcommand: str
    ):
        parser.set_defaults(
            **{
                INTERNAL_EMPTY_HANDLER: show_help(parser),
                INTERNAL_REFERENCE_COMMAND_NAME: reference_command_name,
                INTERNAL_REFERENCE_SUBCOMMAND_NAME: reference_subcommand,
            }
        )

    @property
    def has_execute_an_action(self) -> bool:
        return self.__has_execute_an_action

    @property
    def subparsers(self):
        return self.__subparsers

    @property
    def parser(self) -> ArgumentParser:
        return self.__internal_parser

    @property
    def parent(self) -> ArgumentParser:
        return self.__parser

    @property
    def command(self) -> str:
        """Return the full command path for the current command.

        The command path is composed by joining the command hierarchy with ":".

        Example:
            config:set:ignores

        Where:
            config  -> root command
            set     -> parent/subcommand
            ignores -> current command

        Returns:
            The full command path as a string.
        """
        if self.__parent_command is None:
            return self.identifier
        return f"{self.__parent_command.command}:{self.identifier}"
