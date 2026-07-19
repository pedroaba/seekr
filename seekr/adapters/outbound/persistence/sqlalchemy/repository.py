from sqlalchemy import delete, func, select

from seekr.adapters.outbound.persistence.sqlalchemy.models import PathRecord
from seekr.adapters.outbound.persistence.sqlalchemy.path_record_mapper import (
    PathRecordMapper,
)
from seekr.adapters.outbound.persistence.sqlalchemy.session_factory import (
    SqlAlchemySessionFactory,
)
from seekr.application.ports.path_repository import PathRepository
from seekr.domain.entities.indexed_path import IndexedPath


class SqlAlchemyPathRepository(PathRepository):
    def __init__(
        self,
        sessions: SqlAlchemySessionFactory,
        mapper: PathRecordMapper | None = None,
    ) -> None:
        self._sessions = sessions
        self._mapper = mapper or PathRecordMapper()

    def count(self) -> int:
        with self._sessions.create() as session:
            return session.scalar(select(func.count(PathRecord.id))) or 0

    def replace_all(self, paths: list[IndexedPath]) -> None:
        with self._sessions.create() as session:
            session.execute(delete(PathRecord))
            session.add_all([self._mapper.from_indexed_path(path) for path in paths])
            session.commit()

    def list_all(self) -> list[IndexedPath]:
        with self._sessions.create() as session:
            records = session.scalars(select(PathRecord)).all()
            return [self._mapper.to_indexed_path(record) for record in records]
