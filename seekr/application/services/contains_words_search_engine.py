import unicodedata

from seekr.application.ports.search_engine import SearchEngine


class ContainsWordsSearchEngine(SearchEngine):
    def search(
        self,
        query: str,
        choices: list[str],
        limit: int,
        precision: int,
    ) -> list[int]:
        words = self._normalize(query).split()
        if not words or limit <= 0:
            return []

        results: list[int] = []
        for index, choice in enumerate(choices):
            normalized_choice = self._normalize(choice)
            if all(word in normalized_choice for word in words):
                results.append(index)
            if len(results) >= limit:
                break
        return results

    @staticmethod
    def _normalize(value: str) -> str:
        decomposed = unicodedata.normalize("NFKD", value.casefold())
        return "".join(
            character
            for character in decomposed
            if not unicodedata.combining(character)
        )
