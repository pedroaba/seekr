from dataclasses import dataclass, field

from seekr.application.ports.path_repository import PathRepository
from seekr.application.ports.search_engine import SearchEngine
from seekr.domain.entities.indexed_path import IndexedPath


@dataclass(frozen=True, slots=True)
class SearchPathsInput:
    query: list[str]
    limit: int = 10
    precision: int = 80


@dataclass(frozen=True, slots=True)
class SearchPathsOutput:
    paths: list[IndexedPath] = field(default_factory=list)


class SearchPaths:
    def __init__(self, repository: PathRepository, search_engine: SearchEngine) -> None:
        self._repository = repository
        self._search_engine = search_engine

    def execute(self, request: SearchPathsInput) -> SearchPathsOutput:
        paths = self._repository.list_all()
        if not paths:
            return SearchPathsOutput()
        indexes = self._search_engine.search(
            query=" ".join(request.query),
            choices=[path.normalized_filepath for path in paths],
            limit=request.limit,
            precision=request.precision,
        )
        return SearchPathsOutput(paths=[paths[index] for index in indexes])
