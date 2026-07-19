from typing import Protocol


class SearchEngine(Protocol):
    def search(
        self,
        query: str,
        choices: list[str],
        limit: int,
        precision: int,
    ) -> list[int]: ...
