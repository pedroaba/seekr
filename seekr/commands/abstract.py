from abc import ABC, abstractmethod
from argparse import ArgumentParser, Namespace

from seekr.config import SeekrConfig
from seekr.texts.commit_disable_warning import CommitDisabledWarningText
from seekr.utils.executor import Executor


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

    @abstractmethod
    def build(self): ...

    def handle(self, namespace: Namespace):
        _empty_handler = getattr(namespace, INTERNAL_EMPTY_HANDLER, None)
        if _empty_handler is None:
            return

        ref_name = getattr(namespace,
                           INTERNAL_REFERENCE_COMMAND_NAME,
                           INTERNAL_EMPTY_COMMAND_NAME)
        ref_subcommand = getattr(namespace,
                                 INTERNAL_REFERENCE_SUBCOMMAND_NAME,
                                 INTERNAL_EMPTY_SUBCOMMAND_NAME)

        name = getattr(namespace, ref_name, None)
        subcommand = getattr(namespace, ref_subcommand, None)

        if name is not None and subcommand is None:
            Executor.execute(_empty_handler)
    
    @staticmethod
    def _set_help_text_when_is_empty(parser: ArgumentParser,
                                     reference_command_name: str,
                                     reference_subcommand: str):
        parser.set_defaults(
            **{
                INTERNAL_EMPTY_HANDLER: show_help(parser),
                INTERNAL_REFERENCE_COMMAND_NAME: reference_command_name,
                INTERNAL_REFERENCE_SUBCOMMAND_NAME: reference_subcommand
            }
        )
