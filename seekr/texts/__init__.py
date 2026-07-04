from enum import StrEnum

from seekr.texts.wellcome_init_command import WellcomeInitCommand

_TEXT_DICTS = {
    WellcomeInitCommand.__name__: WellcomeInitCommand,
}


class TextDisplayerClassKeys(StrEnum):
    WELLCOME_INIT_COMMAND = WellcomeInitCommand.__name__

class TextDisplayer:
    @staticmethod
    def display(class_key: TextDisplayerClassKeys) -> None:
        _TEXT_DICTS[class_key.value].display()
