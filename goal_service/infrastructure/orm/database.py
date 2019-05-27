from contextlib import contextmanager

from sqlalchemy import create_engine, MetaData
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import scoped_session, sessionmaker


class SqlAlchemy:

    def __init__(self, uri):
        self.engine = create_engine(uri)
        self.session_factory = scoped_session(sessionmaker(self.engine), )
        self.metadata = MetaData(self.engine)

    def session(self):
        return self.session_factory()

    @contextmanager
    def unit_of_work(self):
        session = self.session_factory()
        try:
            yield session
            session.commit()
        except SQLAlchemyError:
            session.rollback()
            session.close()


database = SqlAlchemy('postgres://goal_service:goal123@localhost:5432'
                      '/goal_service')
