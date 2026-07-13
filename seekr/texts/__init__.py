from enum import StrEnum

from seekr.texts.init_already_completed import InitAlreadyCompletedText
from seekr.texts.wellcome_init_command import WellcomeInitCommand

_TEXT_DICTS = {
    InitAlreadyCompletedText.__name__: InitAlreadyCompletedText,
    WellcomeInitCommand.__name__: WellcomeInitCommand,
}


class TextDisplayerClassKeys(StrEnum):
    INIT_ALREADY_COMPLETED = InitAlreadyCompletedText.__name__
    WELLCOME_INIT_COMMAND = WellcomeInitCommand.__name__


class TextDisplayer:
    @staticmethod
    def display(class_key: TextDisplayerClassKeys) -> None:
        _TEXT_DICTS[class_key.value].display()
