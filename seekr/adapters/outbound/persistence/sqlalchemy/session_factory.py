from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session


class SqlAlchemySessionFactory:
    def __init__(self, database_url: str) -> None:
        self._engine: Engine = create_engine(database_url)

    @property
    def engine(self) -> Engine:
        return self._engine

    def create(self) -> Session:
        return Session(bind=self._engine)
