from typing import Protocol


class TextCommandProtocol(Protocol):
    @staticmethod
    def display() -> None:
        ...