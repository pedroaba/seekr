from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session

from seekr.database.config import get_database_url


class SqlAlchemyConnection:
    __instance = None

    def __init__(self, database_uri: str | None = None):
        self.__database_uri = database_uri or get_database_url()
        self.__engine: Engine | None = None

        self.__sessions: list[Session] = []

    def connect(self) -> None:
        if self.__engine is None:
            self.__engine = create_engine(self.__database_uri)

    def build_session(self) -> Session:
        if self.__engine is None:
            self.connect()

        session = Session(bind=self.__engine)
        self.__sessions.append(session)

        return session

    def close_all_sessions(self) -> None:
        for session in self.__sessions:
            session.close()

    @staticmethod
    def get_instance(database_uri: str | None = None) -> SqlAlchemyConnection:
        if SqlAlchemyConnection.__instance is None:
            SqlAlchemyConnection.__instance = SqlAlchemyConnection(
                database_uri=database_uri)

        return SqlAlchemyConnection.__instance
