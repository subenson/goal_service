import logging
from contextlib import contextmanager

from sqlalchemy import Table, create_engine, MetaData, Column, String, \
    DateTime, Boolean
from sqlalchemy.orm import scoped_session, sessionmaker, mapper
from sqlalchemy_utils.functions import create_database

from domain.model.goal import Goal


log = logging.getLogger(__name__)


class SqlAlchemy:

    def __init__(self, uri):
        self.engine = create_engine(uri)
        self.session_factory = scoped_session(sessionmaker(self.engine), )
        self.metadata = None

    def create_schema(self):
        create_database(self.engine.url)
        self.metadata.create_all()

    def configure_mappings(self):
        self.metadata = MetaData(self.engine)

        goal_table = Table('goal', self.metadata,
            Column('id', String(36), primary_key=True),
            Column('name', String),
            Column('description', String),
            Column('due_date', DateTime(timezone=True)),
            Column('completed', Boolean),
            Column('discarded', Boolean))

        mapper(Goal, goal_table, properties={
            '_id': goal_table.c.id,
            '_name': goal_table.c.name,
            '_description': goal_table.c.description,
            '_due_date': goal_table.c.due_date,
            '_completed': goal_table.c.completed,
            '_discarded': goal_table.c.discarded})

    def session(self):
        return self.session_factory()

    @contextmanager
    def unit_of_work(self):
        session = self.session_factory()
        try:
            yield session
            session.commit()
        except Exception as ex:
            log.debug(ex)
            session.rollback()
            session.close()


database = SqlAlchemy('sqlite:////Users/svendenotter/Code/Python/goal_app'
                      '/adapter/test.db')
database.configure_mappings()
# database.create_schema()
