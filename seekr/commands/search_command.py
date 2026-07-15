from dataclasses import dataclass

from rapidfuzz import process
from sqlalchemy import select

from seekr.database.connection import SqlAlchemyConnection
from seekr.database.models import PathModel
from seekr.texts.search_results import SearchResultsText


@dataclass(frozen=True, slots=True)
class SearchCommandParams:
    query: list[str]
    limit: int = 10
    precision: int = 80


class SearchCommand:
    def __init__(self, params: SearchCommandParams) -> None:
        self.params = params

    def execute(self) -> None:
        connection = SqlAlchemyConnection.get_instance()

        paths = []
        path_objects: list[PathModel] = []
        with connection.build_session() as session:
            rows = session.execute(select(PathModel)).fetchall()

            for [row] in rows:
                paths.append(row.normalized_filepath)
                path_objects.append(row)

        results = process.extract(
            " ".join(self.params.query),
            paths,
            limit=self.params.limit,
            score_cutoff=self.params.precision,
        )
        results_to_show = [path_objects[list_index] for _, _, list_index in results]

        SearchResultsText(results_to_show).display()
