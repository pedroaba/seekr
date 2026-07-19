from seekr.application.ports.search_engine import SearchEngine


class FallbackSearchEngine(SearchEngine):
    def __init__(self, primary: SearchEngine, fallback: SearchEngine) -> None:
        self._primary = primary
        self._fallback = fallback

    def search(
        self,
        query: str,
        choices: list[str],
        limit: int,
        precision: int,
    ) -> list[int]:
        results = self._primary.search(query, choices, limit, precision)
        if results:
            return results
        return self._fallback.search(query, choices, limit, precision)
