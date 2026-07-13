from argparse import ArgumentParser, Namespace

from sqlalchemy import select, func, delete

from seekr.commands.abstract import AbstractCommand
from seekr.constants.paths import DefaultToScan
from seekr.database.connection import SqlAlchemyConnection
from seekr.database.initializer import initialize_database
from seekr.database.models import PathModel
from seekr.decorators.finish_command import finish_command_execution
from seekr.texts import TextDisplayer, TextDisplayerClassKeys
from seekr.texts.found_paths import FoundPathsText, Metadata
from seekr.utils.normalize_path import normalize_path
from seekr.utils.walker import Walker


class InitCommand(AbstractCommand):
    identifier = "init"
    help_text = "Scan the default user folders"
    description = (
        "Scan Seekr's default folders for files and directories. The default "
        "locations are Downloads, Documents, Desktop, Pictures, Videos, and Music."
    )
    epilog = "Examples:\n  seekr init\n  seekr init --show"

    def __init__(
        self,
        parser: ArgumentParser | None = None,
        command: AbstractCommand | None = None,
    ):
        super().__init__(parser, command)
        self._conn = None

    def build(self):
        self.parser.add_argument(
            "-s",
            "--show",
            dest="show_mapped_paths",
            action="store_true",
            default=False,
            help="Display the files and directories found during the scan.",
        )

        self.parser.add_argument(
            "-n",
            "--number-of-paths-showing",
            dest="number_of_paths_showing",
            type=int,
            default=10,
            help="Number of paths to show. If pass -1 show all paths.",
        )
        
        self.parser.add_argument(
            "--force",
            dest="force",
            action="store_true",
            default=False,
        )

    @finish_command_execution
    def handle(self, namespace: Namespace):
        initialize_database()

        self._conn: SqlAlchemyConnection = SqlAlchemyConnection.get_instance()

        if not namespace.force:
            total_of_paths = 0
            with self._conn.build_session() as session:
                statement = select(
                    func.count(PathModel.id)
                )
    
                total_of_paths = session.scalar(statement) or 0
    
            if total_of_paths > 0:
                TextDisplayer.display(
                    TextDisplayerClassKeys.INIT_ALREADY_COMPLETED
                )
    
                return
            
        with self._conn.build_session() as session:
            statement = delete(PathModel)
            session.execute(statement)
            session.commit()

        TextDisplayer.display(TextDisplayerClassKeys.WELLCOME_INIT_COMMAND)

        default_paths = DefaultToScan()
        paths_to_map = default_paths.get()

        walker = Walker(paths_to_map)
        response = walker.walk()

        total = len(response.results)

        with self._conn.build_session() as session:
            for path in response.results:
                model = PathModel(
                    filepath=str(path.relative_path.resolve().absolute()),
                    parent_path=str(path.location.resource),
                    is_folder=path.is_dir,
                    is_file=path.is_file,
                    normalized_filepath=normalize_path(
                        path.relative_path,
                    ),
                    version=1
                )

                session.add(model)
            session.commit()

        if namespace.show_mapped_paths:
            position_to_slice_results = (
                namespace.number_of_paths_showing
                if namespace.number_of_paths_showing > 0
                else total
            )
            results = response.results[:position_to_slice_results]

            FoundPathsText(results).display(
                metadata=Metadata(
                    number_of_paths_showing=len(results),
                    total_files=response.total_files,
                    total_dirs=response.total_dirs,
                    total=total,
                )
            )
