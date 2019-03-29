from sqlalchemy import Table, Column, String, DateTime, Boolean
from . import database


GOAL_TABLE = Table('goal', database.metadata,
    Column('id', String(36), primary_key=True),
    Column('name', String), Column('description', String),
    Column('due_date', DateTime(timezone=True)),
    Column('completed', Boolean), Column('discarded', Boolean))
