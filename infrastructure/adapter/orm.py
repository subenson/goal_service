from sqlalchemy import Table, create_engine, MetaData, Column, String, \
    DateTime, Boolean
from sqlalchemy.orm import scoped_session, sessionmaker, mapper
from sqlalchemy_utils.functions import create_database

from domain.model.goal import Goal


class SqlAlchemy:

    def __init__(self, uri):
        self.engine = create_engine(uri)
        self._session_maker = scoped_session(sessionmaker(self.engine), )
        self.metadata = None

    def create_schema(self):
        create_database(self.engine.url)
        self.metadata.create_all()

    def get_session(self):
        return self._session_maker()

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
