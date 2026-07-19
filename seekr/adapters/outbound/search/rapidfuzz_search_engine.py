from rapidfuzz import process

from seekr.application.ports.search_engine import SearchEngine


class RapidFuzzSearchEngine(SearchEngine):
    def search(
        self,
        query: str,
        choices: list[str],
        limit: int,
        precision: int,
    ) -> list[int]:
        matches = process.extract(
            query,
            choices,
            limit=limit,
            score_cutoff=precision,
        )
        return [index for _, _, index in matches]
