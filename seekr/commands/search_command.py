from rapidfuzz import process
from sqlalchemy import select

from seekr.commands.abstract import AbstractCommand
from seekr.database.connection import SqlAlchemyConnection
from seekr.database.models import PathModel
from seekr.texts.search_results import SearchResultsText


class SearchCommand(AbstractCommand):
    identifier = "search"

    def handle(self, namespace):
        query = " ".join(namespace.query or [])

        conn = SqlAlchemyConnection.get_instance()

        paths = []
        path_objects: list[PathModel] = []
        with conn.build_session() as session:
            statement = select(PathModel)
            rows = session.execute(statement).fetchall()

            for [row] in rows:
                paths.append(row.normalized_filepath)
                path_objects.append(row)

        results = process.extract(
            query,
            paths,
            limit=5,
            score_cutoff=80.0,
        )

        results_to_show = []
        for _string, _score, list_index in results:
            results_to_show.append(
                path_objects[list_index]
            )

        SearchResultsText(results_to_show).display()

    def build(self):
        self.parser.add_argument(
            "query",
            nargs="+",
            help="Terms used to search files and directories.",
        )
