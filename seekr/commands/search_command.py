from rapidfuzz import process
from sqlalchemy import select

from seekr.commands.abstract import AbstractCommand
from seekr.database.connection import SqlAlchemyConnection
from seekr.database.models import PathModel
from seekr.texts.search_results import SearchResultsText


class SearchCommand(AbstractCommand):
    identifier = "search"
    help_text = "Search indexed files and directories"
    description = (
        "Find indexed files and directories using a fuzzy match. Type the search "
        "terms directly after seekr; the search command is selected automatically."
    )
    epilog = (
        "Examples:\n"
        "  seekr report final\n"
        "  seekr faculdade engenharia"
    )

    def handle(self, namespace):
        query = " ".join(namespace.query or [])
        limit_of_results = namespace.limit or 10
        precision_cutoff = namespace.precision or 80.0

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
            limit=limit_of_results,
            score_cutoff=precision_cutoff,
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
            metavar="QUERY",
            help="One or more terms to match against indexed paths.",
        )

        self.parser.add_argument(
            "-l",
            "--limit",
            dest="limit",
            type=int,
            default=10,
            metavar="COUNT",
            help=(
                "Maximum number of matching paths to display "
                "(default: %(default)s)."
            ),
        )

        self.parser.add_argument(
            "--precision",
            dest="precision",
            type=int,
            default=80,
            metavar="SCORE",
            help=(
                "Minimum fuzzy-match score required, from 0 to 100 "
                "(default: %(default)s)."
            ),
        )
