from dataclasses import dataclass

from sqlalchemy import delete, func, select

from seekr.constants.paths import DefaultToScan
from seekr.database.connection import SqlAlchemyConnection
from seekr.database.initializer import initialize_database
from seekr.database.models import PathModel
from seekr.texts import TextDisplayer, TextDisplayerClassKeys
from seekr.texts.found_paths import FoundPathsText, Metadata
from seekr.utils.normalize_path import normalize_path
from seekr.utils.walker import Walker


@dataclass(frozen=True, slots=True)
class InitCommandParams:
    show_mapped_paths: bool = False
    number_of_paths_showing: int = 10
    force: bool = False


class InitCommand:
    def __init__(self, params: InitCommandParams) -> None:
        self.params = params

    def execute(self) -> None:
        initialize_database()

        connection = SqlAlchemyConnection.get_instance()

        if not self.params.force:
            with connection.build_session() as session:
                total_of_paths = session.scalar(select(func.count(PathModel.id))) or 0

            if total_of_paths > 0:
                TextDisplayer.display(TextDisplayerClassKeys.INIT_ALREADY_COMPLETED)
                return

        with connection.build_session() as session:
            session.execute(delete(PathModel))
            session.commit()

        TextDisplayer.display(TextDisplayerClassKeys.WELLCOME_INIT_COMMAND)

        response = Walker(DefaultToScan().get()).walk()
        total = len(response.results)

        with connection.build_session() as session:
            for path in response.results:
                model = PathModel(
                    filepath=str(path.relative_path.resolve().absolute()),
                    parent_path=str(path.location.resource),
                    is_folder=path.is_dir,
                    is_file=path.is_file,
                    normalized_filepath=normalize_path(path.relative_path),
                    version=1,
                )
                session.add(model)
            session.commit()

        if self.params.show_mapped_paths:
            position_to_slice_results = (
                self.params.number_of_paths_showing
                if self.params.number_of_paths_showing > 0
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
